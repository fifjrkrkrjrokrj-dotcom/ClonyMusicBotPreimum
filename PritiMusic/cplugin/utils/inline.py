import random
from pyrogram import enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

STYLES = [
    enums.ButtonStyle.PRIMARY,
    enums.ButtonStyle.SUCCESS,
    enums.ButtonStyle.DANGER
]

# --- OPTION 1: Static (Jo aapne bheja) ---
# Note: Ye tabhi use karein agar aapke paas 'resume_cb' ka alag handler ho.
_alone_style_static = random.choice(STYLES)
_group_style_static = random.choice([s for s in STYLES if s != _alone_style_static])

buttons = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="▷", callback_data="resume_cb", style=_group_style_static),
            InlineKeyboardButton(text="II", callback_data="pause_cb", style=_group_style_static),
            InlineKeyboardButton(text="‣‣I", callback_data="skip_cb", style=_group_style_static),
            InlineKeyboardButton(text="▢", callback_data="end_cb", style=_group_style_static),
        ]
    ]
)

close_key = InlineKeyboardMarkup(
    [[InlineKeyboardButton(text="✯ ᴄʟᴏsᴇ ✯", callback_data="close", style=_alone_style_static)]]
)


# --- OPTION 2: Dynamic (RECOMMENDED) ---
# Ye function use karein taaki 'resume.py' aur 'pause.py' ke logic ke sath match kare.
# Isme hum 'chat_id' pass karte hain taaki bot confuse na ho.

def stream_markup(chat_id):
    alone_style = random.choice(STYLES)
    group_style = random.choice([s for s in STYLES if s != alone_style])

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="▷", callback_data=f"ADMIN Resume|{chat_id}", style=group_style),
                InlineKeyboardButton(text="II", callback_data=f"ADMIN Pause|{chat_id}", style=group_style),
                InlineKeyboardButton(text="‣‣I", callback_data=f"ADMIN Skip|{chat_id}", style=group_style),
                InlineKeyboardButton(text="▢", callback_data=f"ADMIN Stop|{chat_id}", style=group_style),
            ],
            [
                InlineKeyboardButton(text="✯ ᴄʟᴏsᴇ ✯", callback_data="close", style=alone_style)
            ]
        ]
    )
