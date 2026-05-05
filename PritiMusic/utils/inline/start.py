import random 
from pyrogram import enums
from pyrogram.types import InlineKeyboardButton
import config
from PritiMusic import app

STYLES = [
    enums.ButtonStyle.PRIMARY,
    enums.ButtonStyle.SUCCESS,
    enums.ButtonStyle.DANGER
]

def start_panel(_):
    alone_style = random.choice(STYLES)
    group_style = random.choice([s for s in STYLES if s != alone_style])

    buttons = [
        [
            InlineKeyboardButton(
                text=_["SO_B_1"], 
                url=f"https://t.me/{app.username}?startgroup=true",
                style=group_style,
                icon_custom_emoji_id=6291913431196902384
            ),
            InlineKeyboardButton(
                text=_["S_B_2"], 
                url=config.SUPPORT_CHAT,
                style=group_style,
                icon_custom_emoji_id=6291601230024154367
            ),
        ],
    ]
    return buttons

def private_panel(_):
    alone_style = random.choice(STYLES)
    group_style = random.choice([s for s in STYLES if s != alone_style])

    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_3"],
                url=f"https://t.me/{app.username}?startgroup=true",
                style=alone_style,
                icon_custom_emoji_id=6294190043036655313
            )
        ],
        [
            InlineKeyboardButton(
                text=_["S_B_5"], 
                user_id=config.OWNER_ID, 
                style=group_style,
                icon_custom_emoji_id=6291642736588103714
            ),
            InlineKeyboardButton(
                text="ᴄʟᴏɴᴇ", 
                callback_data="clone_page", 
                style=group_style,
                icon_custom_emoji_id=6294117690017585518
            )
        ],
        [
            InlineKeyboardButton(
                text="sᴜᴘᴘᴏʀᴛ", 
                callback_data="support_page", 
                style=group_style,
                icon_custom_emoji_id=6293983407865076087
            ),
            InlineKeyboardButton(
                text="sᴏᴜʀᴄᴇ", 
                callback_data="gib_source", 
                style=group_style,
                icon_custom_emoji_id=6293858106489183038
            )
        ],
        [
            InlineKeyboardButton(
                text=_["S_B_4"], 
                callback_data="settings_back_helper", 
                style=alone_style,
                icon_custom_emoji_id=6291902122548010396
            )
        ],
    ]
    return buttons

def support_panel(_):
    alone_style = random.choice(STYLES)
    group_style = random.choice([s for s in STYLES if s != alone_style])

    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_2"], 
                url=config.SUPPORT_CHAT, 
                style=group_style,
                icon_custom_emoji_id=6293903693272062962
            ),
            InlineKeyboardButton(
                text=_["S_B_6"], 
                url=config.SUPPORT_CHANNEL, 
                style=group_style,
                icon_custom_emoji_id=6291865795714620955
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["BACK_BUTTON"], 
                callback_data="settingsback_helper", 
                style=alone_style,
                icon_custom_emoji_id=6294262490545002769
            )
        ]
    ]
    return buttons

def about_panel(_):
    alone_style = random.choice(STYLES)
    group_style = random.choice([s for s in STYLES if s != alone_style])

    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_5"], 
                user_id=config.OWNER_ID, 
                style=group_style,
                icon_custom_emoji_id=6292065301240487582
            ),
            InlineKeyboardButton(
                text=_["S_B_11"], 
                url=config.GITHUB, 
                style=group_style,
                icon_custom_emoji_id=6291995469367221404
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["S_B_6"], 
                url=config.SUPPORT_CHANNEL, 
                style=group_style,
                icon_custom_emoji_id=6294250464636574181
            ),
            InlineKeyboardButton(
                text=_["S_B_2"], 
                url=config.SUPPORT_CHAT, 
                style=group_style,
                icon_custom_emoji_id=6293865863200118994
            )
        ],
        [
            InlineKeyboardButton(
                text=_["BACK_BUTTON"], 
                callback_data="settingsback_helper", 
                style=alone_style,
                icon_custom_emoji_id=6291942074333797664
            )
        ]
    ]
    return buttons
