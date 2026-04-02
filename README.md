# normalize-kap-orthography

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

An **exceptions table** handles words that don't follow general patterns, and a **two-pass conversion** catches cascading transformations.

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

## Contributing

Contributions are welcome, especially:
- Expanding the exceptions table
- Adding test coverage against known word lists
- Adding diacritical mark support
- Supporting additional orthographic target systems

## License

MIT
