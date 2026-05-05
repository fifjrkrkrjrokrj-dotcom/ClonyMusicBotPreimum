import random
from pyrogram import enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

STYLES = [
    enums.ButtonStyle.PRIMARY,
    enums.ButtonStyle.SUCCESS,
    enums.ButtonStyle.DANGER
]

def stats_buttons(_, status):
    alone_style = random.choice(STYLES)
    group_style = random.choice([s for s in STYLES if s != alone_style])

    not_sudo = [
        InlineKeyboardButton(
            text=_["SA_B_1"],
            callback_data="TopOverall",
            style=alone_style
        )
    ]
    sudo = [
        InlineKeyboardButton(
            text=_["SA_B_2"],
            callback_data="bot_stats_sudo",
            style=group_style
        ),
        InlineKeyboardButton(
            text=_["SA_B_3"],
            callback_data="TopOverall",
            style=group_style
        ),
    ]
    upl = InlineKeyboardMarkup(
        [
            sudo if status else not_sudo,
            [
                InlineKeyboardButton(
                    text=_["CLOSE_BUTTON"],
                    callback_data="close",
                    style=alone_style
                ),
            ],
        ]
    )
    return upl


def back_stats_buttons(_):
    alone_style = random.choice(STYLES)
    group_style = random.choice([s for s in STYLES if s != alone_style])

    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["BACK_BUTTON"],
                    callback_data="stats_back",
                    style=group_style
                ),
                InlineKeyboardButton(
                    text=_["CLOSE_BUTTON"],
                    callback_data="close",
                    style=group_style
                ),
            ],
        ]
    )
    return upl
