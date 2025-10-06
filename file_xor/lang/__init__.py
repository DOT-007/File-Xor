from . import en, hi, ko, ar, ml ,js
from config import BotInfoConfig

LANGUAGES = {
    "en": en.msgs,
    "ml": ml.msgs,
    "hi": hi.msgs,
    "ko": ko.msgs,
    "js": js.msgs,
    "ar": ar.msgs,
}


def msg_translate(lang: str | None, key: str) -> str:
    """Return the localized text for `key`.

    Behavior:
    - If `lang` is None or empty, fall back to English ("en").
    - Normalize the language code (lowercase, strip whitespace).
    - Accept the synonym "mal" and map it to the configured key "ml".
    - If the language or key is missing, return the English string if available,
      otherwise return an empty string.
    """
    # Default to configured language (from config.BotInfoConfig.LANG) when lang is falsy
    if not lang:
        lang_code = (getattr(BotInfoConfig, "LANG", "en") or "en").lower().strip()
    else:
        lang_code = str(lang).lower().strip()

    # accept both 'mal' and 'ml' for Malayalam
    if lang_code == "mal":
        lang_code = "ml"

    texts = LANGUAGES.get(lang_code, LANGUAGES.get("en", {}))
    # final fallback to English key
    return texts.get(key, LANGUAGES.get("en", {}).get(key, ""))


lang = BotInfoConfig.LANG