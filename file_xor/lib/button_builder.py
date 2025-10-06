from typing import List, Tuple, Optional
from pyrogram.types import InlineKeyboardButton
from .url_utils import is_valid_http_url


def build_button_row(label_url_pairs: List[Tuple[str, Optional[str]]]):
    """Build a list of InlineKeyboardButton objects from (label, url_or_callback) pairs.

    - If the second item looks like a valid http(s) URL, builds a URL button.
    - If it's a non-empty string but not a URL, uses it as callback_data.
    - If it's None or empty, builds a disabled-looking button by using callback_data="noop".
    Returns a list of InlineKeyboardButton.
    """
    buttons = []
    for label, target in label_url_pairs:
        if target and is_valid_http_url(target):
            buttons.append(InlineKeyboardButton(label, url=target))
        elif isinstance(target, str) and target:
            buttons.append(InlineKeyboardButton(label, callback_data=target))
        else:
            # fallback: create a harmless callback to avoid invalid URL
            buttons.append(InlineKeyboardButton(label, callback_data="noop"))
    return buttons
