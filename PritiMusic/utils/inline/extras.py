import random
from pyrogram import enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import SUPPORT_CHAT

STYLES = [
    enums.ButtonStyle.PRIMARY,
    enums.ButtonStyle.SUCCESS,
    enums.ButtonStyle.DANGER
]

def botplaylist_markup(_):
    alone_style = random.choice(STYLES)
    group_style = random.choice([s for s in STYLES if s != alone_style])

    buttons = [
        [
            InlineKeyboardButton(text=_["S_B_9"], url=SUPPORT_CHAT, style=group_style),
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close", style=group_style),
        ],
    ]
    return buttons


def close_markup(_):
    alone_style = random.choice(STYLES)

    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["CLOSE_BUTTON"],
                    callback_data="close",
                    style=alone_style
                ),
            ]
        ]
    )
    return upl


def supp_markup(_):
    alone_style = random.choice(STYLES)
    
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["S_B_9"],
                    url=SUPPORT_CHAT,
                    style=alone_style
                ),
            ]
        ]
    )
    return upl
