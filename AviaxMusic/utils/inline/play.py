import math
import random
from pyrogram.types import InlineKeyboardButton
from pyrogram.enums import ButtonStyle
from AviaxMusic import app
from AviaxMusic.utils.formatters import time_to_seconds

# Random color (style) generate karne ka function
def get_random_style():
    styles = [
        ButtonStyle.PRIMARY,
        ButtonStyle.SECONDARY,
        ButtonStyle.POSITIVE,
        ButtonStyle.NEGATIVE
    ]
    return random.choice(styles)


def track_markup(_, videoid, user_id, channel, fplay):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
                style=get_random_style()
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
                style=get_random_style()
            ),
        ],
        [
            InlineKeyboardButton(
                text="🎁 Get Rewards", url=f"https://t.me/{app.username}?startgroup=true",
            ),
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}",
                style=ButtonStyle.NEGATIVE
            ),
        ],
    ]
    return buttons


def stream_markup_timer(_, chat_id, played, dur):
    played_sec = time_to_seconds(played)
    duration_sec = time_to_seconds(dur)
    
    # Avoid division by zero if duration is 0
    if duration_sec == 0:
        percentage = 0
    else:
        percentage = (played_sec / duration_sec) * 100
        
    umm = math.floor(percentage)

    # Define bar states based on percentage
    bar_states = [
        "⚚‎—————————", "—⚚‎————————", "——⚚‎———————", "———⚚‎——————",
        "————⚚‎—————", "—————⚚‎————", "——————⚚‎———", "———————⚚‎——",
        "————————⚚‎—", "—————————⚚‎"
    ]
    bar = bar_states[min(umm // 10, len(bar_states) - 1)]  # Ensure we pick a valid index

    buttons = [
        [
            InlineKeyboardButton(text="❤️‍🔥", callback_data=f"ADMIN Resume|{chat_id}", style=get_random_style()),
            InlineKeyboardButton(text="🪼", callback_data=f"ADMIN Pause|{chat_id}", style=get_random_style()),
            InlineKeyboardButton(text="🪫", callback_data=f"ADMIN Replay|{chat_id}", style=get_random_style()),
            InlineKeyboardButton(text="👻", callback_data=f"ADMIN Skip|{chat_id}", style=get_random_style()),
            InlineKeyboardButton(text="♦️", callback_data=f"ADMIN Stop|{chat_id}", style=get_random_style()),
        ],
        [
            InlineKeyboardButton(
                text=f"{played} {bar} {dur}",
                callback_data="GetTimer",
                style=get_random_style()
            ),
        ],
        [
            InlineKeyboardButton(
                text="🎁 Get Rewards", url=f"https://t.me/{app.username}?startgroup=true",
            ),
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close", style=ButtonStyle.NEGATIVE)
        ],
    ]
    return buttons


def stream_markup(_, chat_id):
    buttons = [
        [
            InlineKeyboardButton(text="❤️‍🔥", callback_data=f"ADMIN Resume|{chat_id}", style=get_random_style()),
            InlineKeyboardButton(text="🪼", callback_data=f"ADMIN Pause|{chat_id}", style=get_random_style()),
            InlineKeyboardButton(text="🪫", callback_data=f"ADMIN Replay|{chat_id}", style=get_random_style()),
            InlineKeyboardButton(text="👻", callback_data=f"ADMIN Skip|{chat_id}", style=get_random_style()),
            InlineKeyboardButton(text="♦️", callback_data=f"ADMIN Stop|{chat_id}", style=get_random_style())
        ],
        [
            InlineKeyboardButton(
                text="🎁 Get Rewards", url=f"https://t.me/{app.username}?startgroup=true",
            ),
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close", style=ButtonStyle.NEGATIVE)
        ],
    ]
    return buttons


def playlist_markup(_, videoid, user_id, ptype, channel, fplay):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"AyushPlaylists {videoid}|{user_id}|{ptype}|a|{channel}|{fplay}",
                style=get_random_style()
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"AyushPlaylists {videoid}|{user_id}|{ptype}|v|{channel}|{fplay}",
                style=get_random_style()
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}",
                style=ButtonStyle.NEGATIVE
            ),
        ],
    ]
    return buttons


def livestream_markup(_, videoid, user_id, mode, channel, fplay):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["P_B_3"],
                callback_data=f"LiveStream {videoid}|{user_id}|{mode}|{channel}|{fplay}",
                style=get_random_style()
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}",
                style=ButtonStyle.NEGATIVE
            ),
        ],
    ]
    return buttons


def slider_markup(_, videoid, user_id, query, query_type, channel, fplay):
    query = f"{query[:20]}"  # Ensure query is truncated to 20 characters
    buttons = [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
                style=get_random_style()
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
                style=get_random_style()
            ),
        ],
        [
            InlineKeyboardButton(
                text="◁",
                callback_data=f"slider B|{query_type}|{query}|{user_id}|{channel}|{fplay}",
                style=get_random_style()
            ),
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {query}|{user_id}",
                style=ButtonStyle.NEGATIVE
            ),
            InlineKeyboardButton(
                text="▷",
                callback_data=f"slider F|{query_type}|{query}|{user_id}|{channel}|{fplay}",
                style=get_random_style()
            ),
        ],
    ]
    return buttons
