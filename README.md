# scireadability
[![PyPI Downloads](https://static.pepy.tech/badge/scireadability)](https://pepy.tech/projects/scireadability)  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**`scireadability` is a user-friendly Python library designed to calculate text statistics for English texts. It's helpful for assessing readability, complexity, and grade level of texts. While specifically enhanced for scientific documents, it works well with any type of text. Punctuation is removed by default, with the exception of apostrophes in contractions.**

> You can try it out on the scireadability demo site [here](https://scireadability-rwroth5.pythonanywhere.com/).

This library is built upon the foundation of the [`textstat`](https://github.com/shivam5992/textstat) Python library, but behaves differently.

## Why scireadability?

While building upon the excellent `textstat` library, `scireadability` is enhanced to provide more accurate coverage of scientific and technical texts.

- CMUdict-driven syllables (with multiple pronunciations handled conservatively).
- Token-based difficult-word math for formulas that require it (e.g., Dale–Chall, SPACHE).
- Consistent tokenization and letter counting that plays nicely with Coleman–Liau.
- A custom dictionary for words that are inaccurately counted by other methods (often jargon, species names, and other specialized words)

> `scireadability` currently supports English. For non-English texts, `textstat` offers broad coverage.

### Key features

- **Accurate syllable counts** using a multi-tiered approach:
  1) **CMUdict** (takes the *minimum* syllable count across pronunciations),
  2) a **custom dictionary** you can edit/extend,
  3) a refined **regex** fallback with scientific-name adjustments.
- **Token-based difficult word rates** where the original formulas expect them.
- **Configurable apostrophe handling** and **rounding**.

## Quick start

### Install

```bash
pip install scireadability
````

### Usage

```python
>>> import scireadability

>>> test_data = (
...     "Within the heterogeneous canopy of the Amazonian rainforest, a fascinating interspecies interaction manifests "
...     "between Cephalotes atratus, a species of arboreal ant, and Epiphytes dendrobii, a genus of epiphytic orchids.  "
...     "Observations reveal that C. atratus colonies cultivate E. dendrobii within their carton nests, providing a "
...     "nitrogen-rich substrate derived from ant detritus.  In return, the orchids, exhibiting a CAM photosynthetic "
...     "pathway adapted to the shaded understory, contribute to nest structural integrity through their root systems and "
...     "potentially volatile organic compounds.  This interaction exemplifies a form of facultative mutualism, where both "
...     "species derive benefits, yet neither exhibits obligate dependence for survival in situ. Further investigation into "
...     "the biochemical signaling involved in this symbiosis promises to elucidate novel ecological strategies."
... )

>>> scireadability.flesch_reading_ease(test_data)
>>> scireadability.flesch_kincaid_grade(test_data)
>>> scireadability.smog_index(test_data)
>>> scireadability.coleman_liau_index(test_data)
>>> scireadability.automated_readability_index(test_data)
>>> scireadability.dale_chall_readability_score(test_data)
>>> scireadability.linsear_write_formula(test_data)
>>> scireadability.gunning_fog(test_data)

# Using the custom dictionary:
>>> scireadability.add_word_to_dictionary("pterodactyl", 4)
>>> scireadability.syllable_count("pterodactyl")
```

For all functions, the input argument (`text`) is the text you want to analyze.

## Language support

This library is English-only by design. Syllables are computed via:

* **CMUdict**: Carnegie Mellon Pronouncing Dictionary; when multiple pronunciations exist, the **minimum** syllable count is used.
* **Custom dictionary**: User-editable overrides for domain terms.
* **Regex fallback**: An improved counter that handles common scientific suffixes (e.g., species names), which typical counters undercount.

## Custom syllable dictionary

Tune syllables for edge cases or specialized vocabulary.

* `load_custom_syllable_dict()`
* `overwrite_dictionary(file_path)`
* `add_word_to_dictionary(word, syllable_count)`
* `add_words_from_file_to_dictionary(file_path)`
* `revert_dictionary_to_default()`
* `print_dictionary()`

**Dictionary file format**

```json
{
  "CUSTOM_SYLLABLE_DICT": {
    "word1": 3,
    "word2": 2,
    "anotherword": 4
  }
}
```

## Controlling apostrophe handling

```python
scireadability.set_rm_apostrophe(rm_apostrophe)
```

This is a global setting that changes the library's behavior for all subsequent calls.

By default, this is set to `false` (apostrophes in common contractions like don't or it's are preserved). If you set it to `true`, all apostrophes will be stripped along with other punctuation. Because this is a global change, it's recommended to set it once at the beginning of your script.

## Controlling output rounding

This library offers two ways to control rounding: a global setting and a flexible per-call override.

```python
scireadability.set_rounding(rounding, points=None)
```

Call this function once to change the default rounding behavior for all subsequent formula calls.

- By default, rounding is False.

- If you enable rounding without specifying points, each metric uses a sensible default precision (e.g., one decimal for grade levels, two for scores).

- Pass an explicit points value to force a specific number of decimals for all calls.

### Per-call override

For more explicit and predictable control, you can pass rounding arguments directly to any formula function. These arguments will always take precedence over the global setting for that specific call.
```python
# The global setting is off, but this specific call will be rounded
scireadability.flesch_kincaid_grade(text, rounding=True, points=1)

# Override the global setting to get an unrounded score for just this call
scireadability.set_rounding(True, points=2)
scireadability.flesch_reading_ease(text, rounding=False)
```
## List of functions

### Formulas

**Flesch Reading Ease**

```python
scireadability.flesch_reading_ease(text)
```

Higher = easier (approx. up to ~121; negatives possible for very hard text).

**Flesch–Kincaid Grade Level**

```python
scireadability.flesch_kincaid_grade(text)
```

Estimated U.S. grade level based on ASL and ASW.

**Gunning Fog Index**

```python
scireadability.gunning_fog(text)
```

Uses average sentence length and the **percentage of polysyllabic tokens** (≥3 syllables).

**SMOG Index**

```python
scireadability.smog_index(text)
```

Most reliable with ~30 sentences; returns 0.0 if fewer than 3 sentences.

**Automated Readability Index (ARI)**

```python
scireadability.automated_readability_index(text)
```

Grade level from characters/word and words/sentence.

**Coleman–Liau Index**

```python
scireadability.coleman_liau_index(text)
```

Grade level from **letters**/word and sentences/word (no syllables).

**Linsear Write Formula**

```python
scireadability.linsear_write_formula(text)
```

Uses the **first 100 words**; counts “easy” (1–2 syllables) and “difficult” (≥3).

**Dale–Chall Readability Score**

```python
scireadability.dale_chall_readability_score(text)
```

Computes the standard DC score from **token-based** difficult words and maps to grade bands in `text_standard`.

| Score        | Understood by                      |
| ------------ | ---------------------------------- |
| 4.9 or lower | Average 4th-grade student or below |
| 5.0–5.9      | Average 5th or 6th-grade student   |
| 6.0–6.9      | Average 7th or 8th-grade student   |
| 7.0–7.9      | Average 9th or 10th-grade student  |
| 8.0–8.9      | Average 11th or 12th-grade student |
| 9.0–9.9      | College (13th–15th grade)          |

**Readability Consensus (Text Standard)**

```python
scireadability.text_standard(text, as_string=True)
```

Consensus grade from multiple indices. Dale–Chall is first converted from **score → grade band** before voting.

**FORCAST**

```python
scireadability.forcast(text)
```

Grade estimate from single-syllable counts in a 150-word sample (warns if shorter).

**SPACHE**

```python
scireadability.spache_readability(text)
```

For young readers; uses sentence length and percentage of “hard words” (token-based).

**McAlpine EFLAW**

```python
scireadability.mcalpine_eflaw(text)
```

Useful for EFL materials; combines word count, mini-word count (≤3 letters), and sentence count.

**LIX**

A Swedish readability formula that measures the text's difficulty based on average sentence length and the percentage of long words (more than 6 characters).
The score is not mapped to a specific grade level.

```python
scireadability.lix(text)
```

| Score   | Readability    |
|---------|----------------|
| < 30    | Very easy      |
| 30–40   | Easy           |
| 40–50   | Standard       |
| 50–60   | Difficult      |
| > 60    | Very difficult |

**RIX**

A simple formula that calculates a grade-level score based on the ratio of long words (more than 6 characters) to the number of sentences.
It is closely related to LIX but presents the output as a grade level.


**Reading time**

```python
scireadability.reading_time(text, wpm=200.0)
```

Returns **seconds**, using a words-per-minute model (default 200 WPM).

### Aggregates and averages

**Syllable count**

```python
scireadability.syllable_count(text)
```

Total syllables; CMUdict → custom dict → regex fallback.

**Word count (lexicon)**

```python
scireadability.lexicon_count(text, removepunct=True)
```

Counts tokens; hyphens/punctuation removed by default. Apostrophes depend on `set_rm_apostrophe()`.

**Sentence count**

```python
scireadability.sentence_count(text)
```

Regex-based; very short “sentences” (≤2 words) are ignored.

**Character count**

```python
scireadability.char_count(text, ignore_spaces=True)
```

Counts all characters (optionally ignoring spaces).

**Letter count**

```python
scireadability.letter_count(text, ignore_spaces=True)
```

Counts **alphabetic** code points (letters only). Spaces aren’t letters, so the flag typically has no effect.

**Polysyllable / Monosyllable counts**

```python
scireadability.polysyllabcount(text)   # ≥3 syllables
scireadability.monosyllabcount(text)   # exactly 1 syllable
```

## Limitations

* **SMOG** is best with \~30 sentences; <3 returns 0.0.
* Short snippets make most readability scores unstable.
* Extremely novel jargon may still require custom dictionary entries.
* Counting syllables with heuristics is inherently approximate; the regex fallback agrees with CMUdict \~91% of the time.
* English only.

## Contributing

If you hit a bug or want to propose a tweak, please open an
[issue](https://github.com/robert-roth/scireadability/issues) or leave feedback on the
[Try it page](https://scireadability-rwroth5.pythonanywhere.com/).

If you’re able to fix a bug or add a feature, we welcome a
[pull request](https://github.com/robert-roth/scireadability/pulls).

1. Fork the repo and branch off `master` (or create a dedicated branch).
2. Add tests that demonstrate the fix/feature.
3. Open a PR.
