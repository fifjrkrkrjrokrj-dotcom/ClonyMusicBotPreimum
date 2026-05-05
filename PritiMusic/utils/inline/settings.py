import random
from typing import Union
from pyrogram import enums
from pyrogram.types import InlineKeyboardButton

STYLES = [
    enums.ButtonStyle.PRIMARY,
    enums.ButtonStyle.SUCCESS,
    enums.ButtonStyle.DANGER
]

def setting_markup(_):
    alone_style = random.choice(STYLES)
    group_style = random.choice([s for s in STYLES if s != alone_style])

    buttons = [
        [
            InlineKeyboardButton(text=_["ST_B_1"], callback_data="AU", style=group_style, icon_custom_emoji_id=5465629669829128119),
            InlineKeyboardButton(text=_["ST_B_3"], callback_data="LG", style=group_style, icon_custom_emoji_id=5465629669829128119),
        ],
        [
            InlineKeyboardButton(text=_["ST_B_2"], callback_data="PM", style=alone_style, icon_custom_emoji_id=5465629669829128119),
        ],
        [
            InlineKeyboardButton(text=_["ST_B_4"], callback_data="VM", style=alone_style, icon_custom_emoji_id=5465629669829128119),
        ],
        [
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close", style=alone_style, icon_custom_emoji_id=5465629669829128119),
        ],
    ]
    return buttons


def vote_mode_markup(_, current, mode: Union[bool, str] = None):
    alone_style = random.choice(STYLES)
    group_style = random.choice([s for s in STYLES if s != alone_style])

    buttons = [
        [
            InlineKeyboardButton(text="Vᴏᴛɪɴɢ ᴍᴏᴅᴇ ➜", callback_data="VOTEANSWER", style=group_style, icon_custom_emoji_id=5465629669829128119),
            InlineKeyboardButton(
                text=_["ST_B_5"] if mode == True else _["ST_B_6"],
                callback_data="VOMODECHANGE",
                style=group_style,
                icon_custom_emoji_id=5465629669829128119
            ),
        ],
        [
            InlineKeyboardButton(text="-2", callback_data="FERRARIUDTI M", style=group_style, icon_custom_emoji_id=5465629669829128119),
            InlineKeyboardButton(
                text=f"ᴄᴜʀʀᴇɴᴛ : {current}",
                callback_data="ANSWERVOMODE",
                style=group_style,
                icon_custom_emoji_id=5465629669829128119
            ),
            InlineKeyboardButton(text="+2", callback_data="FERRARIUDTI A", style=group_style, icon_custom_emoji_id=5465629669829128119),
        ],
        [
            InlineKeyboardButton(
                text=_["BACK_BUTTON"],
                callback_data="settings_helper",
                style=group_style,
                icon_custom_emoji_id=5465629669829128119
            ),
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close", style=group_style, icon_custom_emoji_id=5465629669829128119),
        ],
    ]
    return buttons


def auth_users_markup(_, status: Union[bool, str] = None):
    alone_style = random.choice(STYLES)
    group_style = random.choice([s for s in STYLES if s != alone_style])

    buttons = [
        [
            InlineKeyboardButton(text=_["ST_B_7"], callback_data="AUTHANSWER", style=group_style, icon_custom_emoji_id=5465629669829128119),
            InlineKeyboardButton(
                text=_["ST_B_8"] if status == True else _["ST_B_9"],
                callback_data="AUTH",
                style=group_style,
                icon_custom_emoji_id=5465629669829128119
            ),
        ],
        [
            InlineKeyboardButton(text=_["ST_B_1"], callback_data="AUTHLIST", style=alone_style, icon_custom_emoji_id=5465629669829128119),
        ],
        [
            InlineKeyboardButton(
                text=_["BACK_BUTTON"],
                callback_data="settings_helper",
                style=group_style,
                icon_custom_emoji_id=5465629669829128119
            ),
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close", style=group_style, icon_custom_emoji_id=5465629669829128119),
        ],
    ]
    return buttons


def playmode_users_markup(
    _,
    Direct: Union[bool, str] = None,
    Group: Union[bool, str] = None,
    Playtype: Union[bool, str] = None,
):
    alone_style = random.choice(STYLES)
    group_style = random.choice([s for s in STYLES if s != alone_style])

    buttons = [
        [
            InlineKeyboardButton(text=_["ST_B_10"], callback_data="SEARCHANSWER", style=group_style, icon_custom_emoji_id=5465629669829128119),
            InlineKeyboardButton(
                text=_["ST_B_11"] if Direct == True else _["ST_B_12"],
                callback_data="MODECHANGE",
                style=group_style,
                icon_custom_emoji_id=5465629669829128119
            ),
        ],
        [
            InlineKeyboardButton(text=_["ST_B_13"], callback_data="AUTHANSWER", style=group_style, icon_custom_emoji_id=5465629669829128119),
            InlineKeyboardButton(
                text=_["ST_B_8"] if Group == True else _["ST_B_9"],
                callback_data="CHANNELMODECHANGE",
                style=group_style,
                icon_custom_emoji_id=5465629669829128119
            ),
        ],
        [
            InlineKeyboardButton(text=_["ST_B_14"], callback_data="PLAYTYPEANSWER", style=group_style, icon_custom_emoji_id=5465629669829128119),
            InlineKeyboardButton(
                text=_["ST_B_8"] if Playtype == True else _["ST_B_9"],
                callback_data="PLAYTYPECHANGE",
                style=group_style,
                icon_custom_emoji_id=5465629669829128119
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["BACK_BUTTON"],
                callback_data="settings_helper",
                style=group_style,
                icon_custom_emoji_id=5465629669829128119
            ),
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close", style=group_style, icon_custom_emoji_id=5465629669829128119),
        ],
    ]
    return buttons
