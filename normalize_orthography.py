"""
Normalize Kapampangan orthography from 1730s Spanish-influenced spelling to modern form.

Ported from learn-kulitan-app-v2/lib/utils/utils.dart (TextUtils.convertOrthography).

Usage as module:
    from normalize_orthography import convert_orthography
    result = convert_orthography("QUINANG")  # -> "KINANG"
"""

from __future__ import annotations

import re


EXCEPTIONS = {
    "CAI": "KAYI",
    "AIA": "AYA",
    "VATAUAT": "WATAWAT",
    "VALI": "WALI",
    "PASIBAIO": "PASIBAYO",
    "MAIUTPUT": "MAYUTPUT",
    "OGNAY": "UGNE",
    "BABAY": "BABAYI",
    "IUAD": "IWAD",
    "DALIUAUAT": "DALYAWAT",
    "GUIUA": "GIWA",
    "SAGUESAI": "SAGESE",
    "MAUI": "MAWI",
    "QUECAI": "KEKE",
    "CABAYIAN": "KABAYIAN",
    # Manual edge case
    "PAYNG": "PAING",
}

# Phase 1: Spanish orthography normalization
REPLACEMENTS_1 = [
    ("QUI", "KI"),
    ("QUE", "KE"),
    (re.compile(r"(?<!SI)C"), "K"),
    ("Ñ", "N"),
    ("LL", "L"),
    ("LLA", "LA"),
    ("LL", "L"),
    ("ÑY", "NY"),
    ("NN", "N"),
    (re.compile(r"^V"), "W"),
]

# Phase 2: Vowel cluster and diphthong normalization
# Note: Dart supports variable-width lookbehinds but Python doesn't.
# Patterns like (?<=..+) ("preceded by 2+ chars") are rewritten as
# equivalent fixed-width or capturing-group approaches.
REPLACEMENTS_2 = [
    (re.compile(r"^O(?!U)"), "U"),           # O -> U (word-initial, not before U)
    (re.compile(r"(?<=..)AO$"), "O"),        # AO -> O (not at start, 2+ chars before)
    (re.compile(r"(?<=.)AI$"), "E"),         # AI -> E (not at start, 1+ char before)
    (re.compile(r"(?<=.)AY$"), "E"),         # AY -> E (not at start)
    (re.compile(r"AU$"), "AW"),              # AU -> AW (word-final)
    (re.compile(r"(?<!L)UA$"), "WA"),        # UA -> WA (not after L)
    (re.compile(r"(?<!B)UO"), "WO"),         # UO -> WO (not after B)
    (re.compile(r"(?<=..)IA"), "YA"),        # IA -> YA (2+ chars before)
    (re.compile(r"IU(?=A)"), "IW"),          # IU -> IW (before A)
    (re.compile(r"IU(?=E)"), "IW"),          # IU -> IW (before E)
    (re.compile(r"(?<=.)IU(?!A)"), "YU"),    # IU -> YU (1+ char before, not before A)
    (re.compile(r"(?<=..)UI$"), "I"),        # UI -> I (2+ chars before, word-final)
    (re.compile(r"(?<=..)IO$"), "YO"),       # IO -> YO (2+ chars before, word-final)
    (re.compile(r"(?<=..z)IY$"), "I"),       # IY -> I (after 2+ chars ending in z, word-final)
    (re.compile(r"IE$"), "YE"),              # IE -> YE (word-final)
    ("AUA", "AWA"),
    ("AUI", "AWI"),
    ("EUA", "EWA"),
    ("UE", "WE"),
    ("KK", "K"),
]


def _apply_replacements(replacements: list, word: str) -> str:
    for pattern, repl in replacements:
        if isinstance(pattern, str):
            word = word.replace(pattern, repl)
        else:
            word = pattern.sub(repl, word)
    return word


def _convert_orthography(word: str) -> str:
    new_word = _apply_replacements(REPLACEMENTS_1, word)
    # Remove gemination across hyphens: K-K -> K
    new_word = re.sub(r"(\w)-\1", r"\1", new_word)
    return _apply_replacements(REPLACEMENTS_2, new_word)


def convert_orthography(word: str) -> str | None:
    """Convert a word from 1730s orthography to modern form.

    Returns the normalized form, or None if no conversion is needed
    (i.e., the word is already in modern orthography).
    """
    upper = word.upper()

    if upper in EXCEPTIONS:
        return EXCEPTIONS[upper]

    converted = _convert_orthography(upper)
    if converted == upper:
        return None

    # Second pass
    converted2 = _convert_orthography(converted)
    if converted2 == upper:
        return None

    return converted2


if __name__ == "__main__":
    # Quick test
    test_cases = [
        ("QUINANG", "KINANG"),
        ("CAI", "KAYI"),
        ("VATAUAT", "WATAWAT"),
        ("PAYNG", "PAING"),
        ("QUECAI", "KEKE"),
    ]
    for original, expected in test_cases:
        result = convert_orthography(original)
        status = "OK" if result == expected else f"FAIL (got {result})"
        print(f"  {original} -> {result}  {status}")
