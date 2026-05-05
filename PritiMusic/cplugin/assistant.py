import asyncio
from pyrogram import Client, filters, StopPropagation
from pyrogram.types import Message
from pyrogram.errors import (
    SessionPasswordNeeded, FloodWait,
    PhoneNumberInvalid, ApiIdInvalid,
    PhoneCodeInvalid, PhoneCodeExpired,
    UserDeactivated, AuthKeyUnregistered,
    PasswordHashInvalid
)
from PritiMusic.utils.database import clonebotdb
from config import API_ID, API_HASH, OWNER_ID

# ==========================================
# 🌟 BULLETPROOF ASK SYSTEM (GLOBAL LISTENER)
# ==========================================
ASK_DICT = {}

# This listener will always remain active in the background
@Client.on_message(filters.private & ~filters.me, group=-99)
async def catch_ask_messages(client: Client, message: Message):
    chat_id = message.chat.id
    if chat_id in ASK_DICT:
        future = ASK_DICT[chat_id]
        if not future.done() and message.text:
            future.set_result(message)
            raise StopPropagation # This prevents other commands from triggering

# Custom ask function that adds an entry to the dictionary
async def custom_ask(client: Client, chat_id: int, text: str, timeout: int = 300):
    await client.send_message(chat_id, text)
    loop = asyncio.get_event_loop()
    future = loop.create_future()
    
    ASK_DICT[chat_id] = future # Notify the listener to wait for a message
    
    try:
        return await asyncio.wait_for(future, timeout)
    finally:
        ASK_DICT.pop(chat_id, None) # Remove from dictionary after timeout or success


# ==========================================
# 1. CONNECT ASSISTANT (Phone + OTP)
# Command: /connect
# ==========================================
@Client.on_message(filters.command(["connect"]) & filters.private)
async def connect_assistant(client: Client, message: Message):
    bot_id = client.me.id
    user = message.from_user

    clone_data = await clonebotdb.find_one({"bot_id": bot_id})
    if not clone_data:
        return await message.reply_text("❌ **ᴇʀʀᴏʀ:** ʙᴏᴛ ᴅᴀᴛᴀ ɴᴏᴛ ғᴏᴜɴᴅ ɪɴ ᴛʜᴇ ᴅᴀᴛᴀʙᴀsᴇ.")

    if clone_data["user_id"] != user.id and user.id != OWNER_ID:
        return await message.reply_text("❌ **ᴀᴄᴄᴇss ᴅᴇɴɪᴇᴅ:** ᴏɴʟʏ ᴛʜᴇ ʙᴏᴛ ᴏᴡɴᴇʀ ᴄᴀɴ ᴘᴇʀғᴏʀᴍ ᴛʜɪs ᴀᴄᴛɪᴏɴ.")

    await message.reply_text(
        "⚡ **ᴄᴏɴɴᴇᴄᴛ ᴀssɪsᴛᴀɴᴛ**\n"
        "ɪ ᴡɪʟʟ ʜᴇʟᴘ ʏᴏᴜ ᴄᴏɴɴᴇᴄᴛ ʏᴏᴜʀ ᴀᴄᴄᴏᴜɴᴛ sᴀғᴇʟʏ.\n\n"
        "🛑 ᴛʏᴘᴇ `/cancel` ᴀɴʏᴛɪᴍᴇ ᴛᴏ sᴛᴏᴘ."
    )

    try:
        phone_msg = await custom_ask(
            client, 
            message.chat.id,
            "📲 **ᴘʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ ᴛᴇʟᴇɢʀᴀᴍ ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀ:**\n"
            "(ᴇxᴀᴍᴘʟᴇ: `+919876543210`)\n\n"
            "⚠️ **ᴅᴏɴ'ᴛ ғᴏʀɢᴇᴛ ᴛʜᴇ ᴄᴏᴜɴᴛʀʏ ᴄᴏᴅᴇ!**",
            timeout=300
        )
    except asyncio.TimeoutError:
        return await message.reply("❌ ᴛɪᴍᴇ ʟɪᴍɪᴛ ᴇxᴄᴇᴇᴅᴇᴅ. ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ.")

    if not phone_msg.text or phone_msg.text == "/cancel":
        return await message.reply("❌ ᴘʀᴏᴄᴇss ᴄᴀɴᴄᴇʟʟᴇᴅ.")

    # 🛠️ Phone Number Formatting Fix
    phone_number = phone_msg.text.strip().replace(" ", "").replace("-", "")
    if not phone_number.startswith("+"):
        phone_number = "+" + phone_number

    msg = await message.reply(f"🔄 **ᴄᴏɴɴᴇᴄᴛɪɴɢ ᴛᴏ sᴇʀᴠᴇʀ ᴡɪᴛʜ ɴᴜᴍʙᴇʀ {phone_number}...**")
    
    temp_client = Client(
        name=f"connect_{bot_id}",
        api_id=API_ID,
        api_hash=API_HASH,
        in_memory=True
    )
    
    try:
        await temp_client.connect()
    except Exception as e:
        await msg.edit(f"❌ **ᴄᴏɴɴᴇᴄᴛɪᴏɴ ғᴀɪʟᴇᴅ:** `{str(e)}`")
        return

    try:
        try:
            code = await temp_client.send_code(phone_number)
        except PhoneNumberInvalid:
            await msg.edit("❌ **ɪɴᴠᴀʟɪᴅ ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀ!** ᴘʟᴇᴀsᴇ sᴇɴᴅ ɪɴ ᴛʜᴇ ᴄᴏʀʀᴇᴄᴛ ғᴏʀᴍᴀᴛ (ᴇx: +919876543210).")
            return
        except ApiIdInvalid:
            await msg.edit("❌ **ᴀᴘɪ ɪᴅ & ʜᴀsʜ ɪɴᴠᴀʟɪᴅ:** ᴛᴇʟᴇɢʀᴀᴍ ʀᴇᴊᴇᴄᴛᴇᴅ ʏᴏᴜʀ ᴀᴘɪ ᴅᴇᴛᴀɪʟs. ᴘʟᴇᴀsᴇ ᴜsᴇ ᴀ ᴅɪғғᴇʀᴇɴᴛ ᴀᴘɪ ɪᴅ/ʜᴀsʜ.")
            return
        except FloodWait as e:
            await msg.edit(f"❌ **ғʟᴏᴏᴅᴡᴀɪᴛ:** ʏᴏᴜ ʜᴀᴠᴇ ᴛʀɪᴇᴅ ᴛᴏᴏ ᴍᴀɴʏ ᴛɪᴍᴇs. ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ғᴏʀ {e.value} sᴇᴄᴏɴᴅs ʙᴇғᴏʀᴇ ᴛʀʏɪɴɢ ᴀɢᴀɪɴ.")
            return
        except Exception as e:
            await msg.edit(f"❌ **ᴇʀʀᴏʀ sᴇɴᴅɪɴɢ ᴄᴏᴅᴇ:** `{e}`")
            return

        await msg.delete()

        try:
            otp_msg = await custom_ask(
                client,
                message.chat.id,
                "📩 **ᴏᴛᴘ sᴇɴᴛ sᴜᴄᴄᴇssғᴜʟʟʏ!**\n\n"
                "⚠️ **ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴏғғɪᴄɪᴀʟ ᴛᴇʟᴇɢʀᴀᴍ ᴀᴘᴘ** (ʏᴏᴜ sʜᴏᴜʟᴅ ʀᴇᴄᴇɪᴠᴇ ᴛʜᴇ ᴄᴏᴅᴇ ɪɴ ʏᴏᴜʀ ᴛᴇʟᴇɢʀᴀᴍ ᴄʜᴀᴛ, ɴᴏᴛ ᴠɪᴀ sᴍs).\n\n"
                "sᴇɴᴅ ᴛʜᴇ ᴏᴛᴘ ᴄᴏᴅᴇ ʟɪᴋᴇ ᴛʜɪs:\n"
                "ғᴏʀᴍᴀᴛ: `1 2 3 4 5` (sᴘᴀᴄᴇs ʙᴇᴛᴡᴇᴇɴ ᴇᴀᴄʜ ɴᴜᴍʙᴇʀ ᴀʀᴇ ᴍᴀɴᴅᴀᴛᴏʀʏ)",
                timeout=300
            )
        except asyncio.TimeoutError:
            return await message.reply("❌ ᴛɪᴍᴇ ʟɪᴍɪᴛ ᴇxᴄᴇᴇᴅᴇᴅ.")

        if not otp_msg.text or otp_msg.text == "/cancel":
            return await message.reply("❌ ᴘʀᴏᴄᴇss ᴄᴀɴᴄᴇʟʟᴇᴅ.")

        otp = otp_msg.text.replace(" ", "").strip()

        try:
            await temp_client.sign_in(phone_number, code.phone_code_hash, otp)
        except PhoneCodeInvalid:
            await message.reply("❌ **ᴡʀᴏɴɢ ᴏᴛᴘ!** ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ.")
            return
        except PhoneCodeExpired:
            await message.reply("❌ **ᴏᴛᴘ ᴇxᴘɪʀᴇᴅ.** ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ.")
            return
        except SessionPasswordNeeded:
            try:
                pwd_msg = await custom_ask(
                    client,
                    message.chat.id,
                    "🔐 **ᴛᴡᴏ-sᴛᴇᴘ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ:**\n\n"
                    "ʏᴏᴜʀ ᴀᴄᴄᴏᴜɴᴛ ɪs ᴘʀᴏᴛᴇᴄᴛᴇᴅ ᴡɪᴛʜ ᴀ ᴘᴀssᴡᴏʀᴅ. ᴘʟᴇᴀsᴇ ᴇɴᴛᴇʀ ɪᴛ ʙᴇʟᴏᴡ:",
                    timeout=300
                )
            except asyncio.TimeoutError:
                return await message.reply("❌ ᴛɪᴍᴇ ʟɪᴍɪᴛ ᴇxᴄᴇᴇᴅᴇᴅ.")
            
            if not pwd_msg.text or pwd_msg.text == "/cancel":
                return await message.reply("❌ ᴘʀᴏᴄᴇss ᴄᴀɴᴄᴇʟʟᴇᴅ.")
            
            try:
                await temp_client.check_password(password=pwd_msg.text)
            except PasswordHashInvalid:
                await message.reply("❌ **ᴡʀᴏɴɢ ᴘᴀssᴡᴏʀᴅ!** ᴄᴏɴɴᴇᴄᴛɪᴏɴ ғᴀɪʟᴇᴅ.")
                return
            except Exception as e:
                await message.reply(f"❌ **ᴇʀʀᴏʀ:** `{str(e)}`")
                return
        except Exception as e:
            await message.reply(f"❌ **ᴇʀʀᴏʀ:** `{str(e)}`")
            return

        await message.reply("🔄 **ᴄᴏɴɴᴇᴄᴛɪᴏɴ sᴜᴄᴄᴇssғᴜʟ! sᴀᴠɪɴɢ & sᴛᴀʀᴛɪɴɢ ᴀssɪsᴛᴀɴᴛ...**")
        
        try:
            if hasattr(client, "assistant") and client.assistant:
                try:
                    await client.assistant.stop()
                except:
                    pass
                try:
                    del client.assistant
                except:
                    pass

            string_session = await temp_client.export_session_string()
            
            await clonebotdb.update_one(
                {"bot_id": bot_id},
                {"$set": {"session_string": string_session}}
            )

            new_assistant = Client(
                f"Ass_{bot_id}",
                api_id=API_ID,
                api_hash=API_HASH,
                session_string=string_session,
                no_updates=True,
                in_memory=True
            )
            await new_assistant.start()
            ass_info = await new_assistant.get_me()
            client.assistant = new_assistant

            bot_username = client.me.username or client.me.first_name

            await message.reply_text(
                f"🎉 **ᴄᴏɴɴᴇᴄᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ!**\n\n"
                f"👤 **ᴀssɪsᴛᴀɴᴛ:** {ass_info.first_name}\n"
                f"🆔 **ɪᴅ:** `{ass_info.id}`\n"
                f"🤖 **ʙᴏᴛ:** @{bot_username}\n\n"
                "🎸 **ɴᴏᴡ ʏᴏᴜ ᴄᴀɴ ᴘʟᴀʏ ᴍᴜsɪᴄ ᴅɪʀᴇᴄᴛʟʏ!**"
            )

        except Exception as e:
            await message.reply(f"❌ **ᴇʀʀᴏʀ sᴀᴠɪɴɢ sᴇssɪᴏɴ:** `{str(e)}`")

    finally:
        if temp_client.is_connected:
            await temp_client.disconnect()


# ==========================================
# 2. MANUAL SET STRING (Paste String)
# ==========================================
@Client.on_message(filters.command(["setstring", "setmode"]) & filters.private)
async def set_clone_session(client: Client, message: Message):
    bot_id = client.me.id
    user = message.from_user

    clone_data = await clonebotdb.find_one({"bot_id": bot_id})
    if not clone_data:
        return await message.reply_text("❌ **ᴇʀʀᴏʀ:** ʙᴏᴛ ᴅᴀᴛᴀ ɴᴏᴛ ғᴏᴜɴᴅ ɪɴ ᴅᴀᴛᴀʙᴀsᴇ.")

    if clone_data["user_id"] != user.id and user.id != OWNER_ID:
        return await message.reply_text("❌ **ᴀᴄᴄᴇss ᴅᴇɴɪᴇᴅ:** ᴏɴʟʏ ᴛʜᴇ ᴏᴡɴᴇʀ ᴄᴀɴ sᴇᴛ ᴛʜᴇ sᴇssɪᴏɴ.")

    if len(message.command) < 2:
        return await message.reply_text(
            "⚠️ **ᴜsᴀɢᴇ:**\n`/setstring <session_string>`\n\n"
            "❗ **ɴᴏᴛᴇ:** ᴏɴʟʏ **ᴘʏʀᴏɢʀᴀᴍ ᴠ2 sᴛʀɪɴɢs** ᴀʀᴇ sᴜᴘᴘᴏʀᴛᴇᴅ."
        )

    string_session = message.text.split(None, 1)[1].strip()
    msg = await message.reply_text("🔄 **ᴘʀᴏᴄᴇssɪɴɢ sᴛʀɪɴɢ...**")

    try:
        if hasattr(client, "assistant") and client.assistant:
            try:
                await client.assistant.stop()
            except:
                pass
            try:
                del client.assistant
            except:
                pass

        new_assistant = Client(
            f"Ass_{bot_id}",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=string_session,
            no_updates=True,
            in_memory=True
        )
        
        await new_assistant.start()
        ass_info = await new_assistant.get_me()

        client.assistant = new_assistant

        await clonebotdb.update_one(
            {"bot_id": bot_id},
            {"$set": {"session_string": string_session}}
        )
        
        bot_username = client.me.username or client.me.first_name

        await msg.edit(
            f"✅ **ᴄᴏɴɴᴇᴄᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ!**\n\n"
            f"👤 **ᴀssɪsᴛᴀɴᴛ:** {ass_info.first_name}\n"
            f"🆔 **ɪᴅ:** `{ass_info.id}`\n"
            f"🤖 **ʙᴏᴛ:** @{bot_username}\n\n"
            "🎸 **ɴᴏᴡ ʏᴏᴜ ᴄᴀɴ ᴘʟᴀʏ ᴍᴜsɪᴄ!**"
        )

    except (UserDeactivated, AuthKeyUnregistered):
        await msg.edit("❌ **ɪɴᴠᴀʟɪᴅ sᴛʀɪɴɢ:** ᴛʜɪs sᴇssɪᴏɴ ʜᴀs ᴇxᴘɪʀᴇᴅ. ᴘʟᴇᴀsᴇ ᴄᴏɴɴᴇᴄᴛ ᴀɢᴀɪɴ.")
    except Exception as e:
        await msg.edit(f"❌ **ᴇʀʀᴏʀ:** `{str(e)}`")


# ==========================================
# 3. DISCONNECT / REMOVE SESSION
# ==========================================
@Client.on_message(filters.command(["disconnect", "delstring"]) & filters.private)
async def disconnect_assistant(client: Client, message: Message):
    bot_id = client.me.id
    user = message.from_user

    clone_data = await clonebotdb.find_one({"bot_id": bot_id})
    if not clone_data:
        return await message.reply_text("❌ **ᴇʀʀᴏʀ:** ʙᴏᴛ ᴅᴀᴛᴀ ɴᴏᴛ ғᴏᴜɴᴅ ɪɴ ᴅᴀᴛᴀʙᴀsᴇ.")

    if clone_data["user_id"] != user.id and user.id != OWNER_ID:
        return await message.reply_text("❌ **ᴀᴄᴄᴇss ᴅᴇɴɪᴇᴅ:** ᴏɴʟʏ ᴛʜᴇ ᴏᴡɴᴇʀ ᴄᴀɴ ᴅɪsᴄᴏɴɴᴇᴄᴛ.")

    msg = await message.reply_text("🔄 **ᴅɪsᴄᴏɴɴᴇᴄᴛɪɴɢ...**")

    try:
        if hasattr(client, "assistant") and client.assistant:
            try:
                await client.assistant.stop()
            except:
                pass 
            try:
                del client.assistant
            except:
                pass

        await clonebotdb.update_one(
            {"bot_id": bot_id},
            {"$unset": {"session_string": 1}}
        )
        
        await msg.edit(
            "✅ **ᴅɪsᴄᴏɴɴᴇᴄᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ!**\n\n"
            "ᴀssɪsᴛᴀɴᴛ ʜᴀs ʙᴇᴇɴ ʀᴇᴍᴏᴠᴇᴅ."
        )

    except Exception as e:
        await msg.edit(f"❌ **ᴇʀʀᴏʀ:** `{str(e)}`")
