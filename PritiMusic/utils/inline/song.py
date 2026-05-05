import random
from pyrogram import enums
from pyrogram.types import InlineKeyboardButton

STYLES = [
    enums.ButtonStyle.PRIMARY,
    enums.ButtonStyle.SUCCESS,
    enums.ButtonStyle.DANGER
]

def song_markup(_, vidid):
    alone_style = random.choice(STYLES)
    group_style = random.choice([s for s in STYLES if s != alone_style])

    buttons = [
        [
            InlineKeyboardButton(
                text=_["SG_B_2"],
                callback_data=f"song_helper audio|{vidid}",
                style=group_style
            ),
            InlineKeyboardButton(
                text=_["SG_B_3"],
                callback_data=f"song_helper video|{vidid}",
                style=group_style
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"], callback_data="close", style=alone_style
            ),
        ],
    ]
    return buttons
