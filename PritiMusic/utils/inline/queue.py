import random
from typing import Union
from pyrogram import enums
from PritiMusic import app
from PritiMusic.utils.formatters import time_to_seconds
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

STYLES = [
    enums.ButtonStyle.PRIMARY,
    enums.ButtonStyle.SUCCESS,
    enums.ButtonStyle.DANGER
]

def queue_markup(
    _,
    DURATION,
    CPLAY,
    videoid,
    played: Union[bool, int] = None,
    dur: Union[bool, int] = None,
):
    alone_style = random.choice(STYLES)
    group_style = random.choice([s for s in STYLES if s != alone_style])

    not_dur = [
        [
            InlineKeyboardButton(
                text=_["QU_B_1"],
                callback_data=f"GetQueued {CPLAY}|{videoid}",
                style=group_style,
                icon_custom_emoji_id=6325625462726856746
            ),
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data="close",
                style=group_style,
                icon_custom_emoji_id=6325766887409979144
            ),
        ]
    ]
    dur = [
        [
            InlineKeyboardButton(
                text=_["QU_B_2"].format(played, dur),
                callback_data="GetTimer",
                style=alone_style,
                icon_custom_emoji_id=6327647687948636219
            )
        ],
        [
            InlineKeyboardButton(
                text=_["QU_B_1"],
                callback_data=f"GetQueued {CPLAY}|{videoid}",
                style=group_style,
                icon_custom_emoji_id=6325625462726856746
            ),
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data="close",
                style=group_style,
                icon_custom_emoji_id=6325766887409979144
            ),
        ],
    ]
    upl = InlineKeyboardMarkup(not_dur if DURATION == "Unknown" else dur)
    return upl


def queue_back_markup(_, CPLAY):
    alone_style = random.choice(STYLES)
    group_style = random.choice([s for s in STYLES if s != alone_style])

    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["BACK_BUTTON"],
                    callback_data=f"queue_back_timer {CPLAY}",
                    style=group_style,
                    icon_custom_emoji_id=6325766887409979144
                ),
                InlineKeyboardButton(
                    text=_["CLOSE_BUTTON"],
                    callback_data="close",
                    style=group_style,
                    icon_custom_emoji_id=6325766887409979144
                ),
            ]
        ]
    )
    return upl


def aq_markup(_, chat_id):
    alone_style = random.choice(STYLES)
    group_style = random.choice([s for s in STYLES if s != alone_style])

    buttons = [
        [
            InlineKeyboardButton(text=" ", callback_data=f"ADMIN Resume|{chat_id}", style=group_style, icon_custom_emoji_id=6327709071621230949),
            InlineKeyboardButton(text=" ", callback_data=f"ADMIN Pause|{chat_id}", style=group_style, icon_custom_emoji_id=6325497687449801252),
            InlineKeyboardButton(text=" ", callback_data=f"ADMIN Replay|{chat_id}", style=group_style, icon_custom_emoji_id=6327960378747655590),
            InlineKeyboardButton(text=" ", callback_data=f"ADMIN Skip|{chat_id}", style=group_style, icon_custom_emoji_id=6325829666946945052),
            InlineKeyboardButton(text=" ", callback_data=f"ADMIN Stop|{chat_id}", style=group_style, icon_custom_emoji_id=6325697098486386211),
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data="close",
                style=alone_style,
                icon_custom_emoji_id=6325766887409979144
            ),
        ],
    ]
    return buttons


def queuemarkup(_, vidid, chat_id):
    alone_style = random.choice(STYLES)
    group_style = random.choice([s for s in STYLES if s != alone_style])

    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_5"],
                url=f"https://t.me/{app.username}?startgroup=true",
                style=alone_style,
                icon_custom_emoji_id=6325669060939878745
            ),
        ],
        [
            InlineKeyboardButton(
                text="ᴘᴀᴜsᴇ",
                callback_data=f"ADMIN Pause|{chat_id}",
                style=group_style,
                icon_custom_emoji_id=6325497687449801252
            ),
            InlineKeyboardButton(text="sᴛᴏᴘ", callback_data=f"ADMIN Stop|{chat_id}", style=group_style, icon_custom_emoji_id=6325697098486386211),
            InlineKeyboardButton(text="sᴋɪᴘ", callback_data=f"ADMIN Skip|{chat_id}", style=group_style, icon_custom_emoji_id=6325829666946945052),
        ],
        [
            InlineKeyboardButton(
                text="ʀᴇsᴜᴍᴇ", callback_data=f"ADMIN Resume|{chat_id}", style=group_style, icon_custom_emoji_id=6327709071621230949
            ),
            InlineKeyboardButton(
                text="ʀᴇᴘʟᴀʏ", callback_data=f"ADMIN Replay|{chat_id}", style=group_style, icon_custom_emoji_id=6327960378747655590
            ),
        ],
        [
            InlineKeyboardButton(
                text="ᴍᴏʀᴇ",
                url="https://t.me/+DlgFzulC_JY5OWI1",
                style=alone_style,
                icon_custom_emoji_id=6325625462726856746
            ),
        ],
    ]

    return buttons
