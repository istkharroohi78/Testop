import random
from typing import Union
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import ButtonStyle
from AviaxMusic import app


# Random color (style) generate karne ka function
def get_random_style():
    styles = [
        ButtonStyle.PRIMARY,
        ButtonStyle.SECONDARY,
        ButtonStyle.POSITIVE,
        ButtonStyle.NEGATIVE
    ]
    return random.choice(styles)


def help_pannel(_, START: Union[bool, int] = None):
    # Close button hamesha red (NEGATIVE) rakha hai better look ke liye
    first = [InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data=f"close", style=ButtonStyle.NEGATIVE)]
    second = [
        InlineKeyboardButton(
            text=_["BACK_BUTTON"],
            callback_data=f"settingsback_helper",
            style=get_random_style(),
        ),
    ]
    mark = second if START else first
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["H_B_1"],
                    callback_data="help_callback hb1",
                    style=get_random_style(),
                ),
                InlineKeyboardButton(
                    text=_["H_B_2"],
                    callback_data="help_callback hb2",
                    style=get_random_style(),
                ),
                InlineKeyboardButton(
                    text=_["H_B_3"],
                    callback_data="help_callback hb3",
                    style=get_random_style(),
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_["H_B_4"],
                    callback_data="help_callback hb4",
                    style=get_random_style(),
                ),
                InlineKeyboardButton(
                    text=_["H_B_5"],
                    callback_data="help_callback hb5",
                    style=get_random_style(),
                ),
                InlineKeyboardButton(
                    text=_["H_B_6"],
                    callback_data="help_callback hb6",
                    style=get_random_style(),
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_["H_B_7"],
                    callback_data="help_callback hb7",
                    style=get_random_style(),
                ),
                InlineKeyboardButton(
                    text=_["H_B_8"],
                    callback_data="help_callback hb8",
                    style=get_random_style(),
                ),
                InlineKeyboardButton(
                    text=_["H_B_9"],
                    callback_data="help_callback hb9",
                    style=get_random_style(),
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_["H_B_10"],
                    callback_data="help_callback hb10",
                    style=get_random_style(),
                ),
                InlineKeyboardButton(
                    text=_["H_B_11"],
                    callback_data="help_callback hb11",
                    style=get_random_style(),
                ),
                InlineKeyboardButton(
                    text=_["H_B_12"],
                    callback_data="help_callback hb12",
                    style=get_random_style(),
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_["H_B_13"],
                    callback_data="help_callback hb13",
                    style=get_random_style(),
                ),
                InlineKeyboardButton(
                    text=_["H_B_14"],
                    callback_data="help_callback hb14",
                    style=get_random_style(),
                ),
                InlineKeyboardButton(
                    text=_["H_B_15"],
                    callback_data="help_callback hb15",
                    style=get_random_style(),
                ),
            ],
            mark,
        ]
    )
    return upl


def help_back_markup(_):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["BACK_BUTTON"],
                    callback_data=f"settings_back_helper",
                    style=get_random_style(),
                ),
            ]
        ]
    )
    return upl


def private_help_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_4"],
                url=f"https://t.me/{app.username}?start=help",
                style=get_random_style(),
            ),
        ],
    ]
    return buttons
