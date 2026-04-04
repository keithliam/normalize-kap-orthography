# normalize-kap-orthography

[![PyPI version](https://img.shields.io/pypi/v/normalize-kap-orthography)](https://pypi.org/project/normalize-kap-orthography/)
[![License](https://img.shields.io/pypi/l/normalize-kap-orthography)](https://github.com/keithmanaloto/normalize-kap-orthography/blob/main/LICENSE)
[![PyPI downloads](https://img.shields.io/pypi/dm/normalize-kap-orthography)](https://pypi.org/project/normalize-kap-orthography/)

A Python utility to normalize Kapampangan words from Spanish-era (1730s) orthography to modern K-based orthography.

Built to make historical Kapampangan texts — like Bergaño's 1732 *Vocabulario de la Lengua Pampanga* — more accessible to modern readers, researchers, and NLP pipelines.

## Background

Before the Spanish conquest, Kapampangans used their own indigenous writing system (Kulitan). Spanish missionaries romanized the language using Spanish orthographic conventions (C, Q, Ñ, LL, etc.). Over the past century, multiple competing romanized orthographies have emerged:

## Disclaimer

I am not a linguist — I'm a native Kapampangan speaker who happens to be a computer science graduate. The conversion rules in this tool were identified through patterns I recognized while cleaning historical dictionary data, not through formal linguistic analysis. The script was spot-checked against the dataset and appears accurate, but it has not been exhaustively verified. If you spot errors or have linguistic expertise to contribute, please open an issue or PR.

| System | Also known as | Key features |
|---|---|---|
| Spanish-era ("Q & C") | *Súlat Bacúlud*, Old Orthography | Uses QU, C, Ñ, LL — the system used in colonial-era texts |
| ABAKADA ("K") | *Súlat Wáwâ*, New Orthography | K-based, aligned with the Philippine national orthography |
| Samson Hybrid | *Ámung Samson* | Retains C before a/o/u, replaces QU→K, adds diacritical marks |
| Batiáuan Revised | *Súlat Wáwâ a alâng WA* | K-based without W, with diacritical marks |

This tool converts from the **Spanish-era system** to a **modern K-based form** (closest to ABAKADA). For more on the orthography dispute, see [Pangilinan (2006)](https://sil-philippines-languages.org/ical/papers/pangilinan-Dispute%20on%20Orthography.pdf).

## What it does

The converter applies two phases of transformation:

**Phase 1 — Spanish letter substitutions:**
- `QUI` → `KI`, `QUE` → `KE`
- `C` → `K` (except after `SI`)
- `Ñ` → `N`, `LL` → `L`
- Word-initial `V` → `W`

**Phase 2 — Vowel cluster and diphthong normalization:**
- `AO` → `O`, `AI`/`AY` → `E` (word-final, non-initial)
- `UA` → `WA`, `UO` → `WO`
- Various other diphthong simplifications

An **exceptions table** handles words that don't follow general patterns, and a **two-pass conversion** catches cascading transformations. For a detailed breakdown of every rule and why it exists, see [How it works](#how-it-works).

## Installation

```shell
pip install normalize-kap-orthography
```

Or just copy `normalize_orthography.py` into your project.

## Usage

```python
from normalize_orthography import convert_orthography

convert_orthography("QUINANG")   # → "KINANG"

convert_orthography("VATAUAT")   # → "WATAWAT"

convert_orthography("QUECAI")    # → "KEKE"

convert_orthography("KINANG")    # → None (already modern)
```

Returns the normalized form, or `None` if no conversion is needed.

### CLI

```shell
python normalize_orthography.py
```


Runs a small set of built-in test cases.

## Limitations

- **Not linguistically verified.** The rules were identified through pattern recognition by a native speaker, not through formal linguistic analysis. The script was spot-checked against dictionary data but not exhaustively validated.
- **No diacritical marks.** The script does not handle stress marking, which is important in Kapampangan — e.g., *masakit* (painful) vs. *masákit* (difficult) vs. *másakit* (ill) are three distinct words.
- **One-directional.** Currently only converts Spanish-era → modern. Reverse conversion is not supported.
- **Uppercase only.** Input is converted to uppercase internally; output is always uppercase.

## Origin

Originally written in Dart as part of the v2 of [Learn Kulitan](https://github.com/keithliam/learn-kulitan-app), then rewritten in Python with **Claude Code Opus 4.6**.

## Real-World Usage

This script was originally used to normalize ~5,000 words extracted from [*Vocabulario de la Lengua Pampanga*](https://archive.org/details/aqn8189.0001.001.umich.edu/page/1/mode/2up) by Fray Diego Bergaño, originally published in 1732 — one of the earliest known dictionaries of the Kapampángan language. About 40% of entries (1,989 out of 4,971) had their orthography normalized.

The raw, uncleaned entries and their cleaned, normalized versions are available as part of an open dataset on Hugging Face:

**[keithmanaloto/kapampangan-dictionary-embeddings](https://huggingface.co/datasets/keithmanaloto/kapampangan-dictionary-embeddings)**

The dataset also includes LLM-enriched metadata and pre-computed embeddings across multiple models — designed for semantic search, retrieval, and clustering over Kapampángan vocabulary. Both the original 1730s spelling and the normalized modern form are preserved in the dataset.

For the full story behind the dataset and what I learned building it, see the article:
[From a 300-Year-Old Dictionary to Hugging Face: I Built Kapampángan's First Embedding Dataset](https://keithmanaloto.medium.com/from-a-300-year-old-dictionary-to-hugging-face-i-built-kapampángans-first-embedding-dataset-dce2b877bd83)

## How it works

### Pipeline

```
convert_orthography(word)
  1. Check EXCEPTIONS table — return immediately if matched
  2. First pass:
       a. Phase 1 — Spanish consonant conventions
       b. Remove geminate consonants across hyphens (K-K → K)
       c. Phase 2 — vowel cluster and diphthong normalization
  3. If output == input, return None (already modern)
  4. Second pass — same as above, on first-pass output
  5. Return second-pass result
```

### Phase 1 — Spanish Consonant Orthography

Spanish missionaries had no `K`, `W`, or `Y` in their alphabet, so they wrote Kapampangan sounds using Spanish equivalents. Phase 1 undoes those conventions:

| Rule | Explanation |
|---|---|
| `QUI → KI`, `QUE → KE` | Spanish `QU` digraph before front vowels — the `U` is silent, not a vowel |
| `C → K` (not after `SI`) | Spanish "hard C" for /k/; the `(?<!SI)` guard protects sequences like `SCIENCIA` where `SC` represents /s/, not /sk/ |
| `Ñ → N`, `NN → N` | Spanish nasal conventions; Kapampangan has no distinct /ɲ/ phoneme |
| `LL → L` | Spanish lateral digraph /ʎ/ has no Kapampangan equivalent; written to represent plain /l/ |
| `^V → W` | Spanish had no `W` grapheme; word-initial /w/ was written as `V` |

Phase 1 must run before Phase 2. The `QU` digraph's `U` is not a real vowel — converting consonants first ensures Phase 2 only operates on genuine vowel sequences.

### Phase 2 — Vowel Clusters and Diphthongs

Spanish scribes wrote Kapampangan glides (/w/, /y/) as vowels (`U`, `I`), and many historical diphthongs have since monophthongized. Phase 2 maps these to modern forms:

**Glide insertion** — vowel sequences where `U` or `I` functions as a consonant glide:

| Rule | Explanation |
|---|---|
| `UA → WA` (not after `L`) | The `U` is a /w/ glide. Guard protects `LUA` = /lu.a/ (two syllables), not /lwa/ |
| `UO → WO` (not after `B`) | Same; `BUO` = /bu.o/ — the preceding bilabial /b/ means `U` stays a vowel |
| `IA → YA` (2+ chars before) | The `I` is a /y/ glide; lookbehind prevents misfiring on short prefix+root sequences |
| `IE → YE`, `IO → YO` | Same glide pattern at word boundaries |
| `IU → IW` (before A or E) | Here the `U` is the glide; `IU → YU` elsewhere (the `I` is the glide) |

**Diphthong simplification** — historical diphthongs that monophthongized in modern Kapampangan:

| Rule | Explanation |
|---|---|
| `AI → E`, `AY → E` (word-final) | /ai/ → /e/ — lookbehind prevents firing on bare monosyllabic roots |
| `AO → O` (word-final) | /ao/ → /o/ |
| `AU → AW` (word-final) | Not a simplification — rewrites the glide explicitly |
| `^O → U` (word-initial) | /o/ and /u/ were conflated; word-initially, modern standard prefers `U` |
| `UI → I`, `KK → K` | Degemination and cluster simplification |

### Two-Pass Conversion

Phase 1 can expose new vowel sequences that weren't visible in the original spelling. For example, removing a `QU` digraph may bring two vowels into adjacency for the first time. Running the full pipeline a second time catches these cascading transformations.

The function returns `None` if either pass produces no change, or if the second pass reverts to the original — indicating the word is already in modern orthography (or the rules don't apply).

### Exceptions Table

Some words produce incorrect output under the general rules due to irregular phonological history or overlapping patterns. These are handled by a hard-coded lookup table checked before any rules are applied. Examples:

| Original | Modern | Why an exception is needed |
|---|---|---|
| `DALIUAUAT` | `DALYAWAT` | Complex multi-glide word the sequential rules can't decompose correctly |
| `OGNAY` | `UGNE` | Irregular vowel shift not covered by any general rule |
| `QUECAI` | `KEKE` | Produces wrong output without intervention |

## Contributing

Contributions are welcome, especially:
- Expanding the exceptions table
- Adding test coverage against known word lists
- Adding diacritical mark support
- Supporting additional orthographic target systems

## License

MIT
