# scireadability
[![PyPI Downloads](https://static.pepy.tech/badge/scireadability)](https://pepy.tech/projects/scireadability)  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**`scireadability` is a user-friendly Python library designed to calculate text statistics. It's helpful for assessing readability, complexity, and grade level of texts. While specifically enhanced for scientific documents, it works well with any type of text. Punctuation is removed by default, with the exception of apostrophes in contractions.**

> You can try it out on the scireadability demo site [here](https://scireadability-rwroth5.pythonanywhere.com/).

This library is built upon the foundation of the [`textstat`](https://github.com/shivam5992/textstat) Python library, originally created by Shivam Bansal and Chaitanya Aggarwal.

## Why scireadability?

While building upon the excellent `textstat` library, `scireadability` is specifically designed to address the unique challenges of analyzing scientific and technical texts. It offers improved accuracy for syllable counting, especially for scientific vocabulary and names. If you need readability statistics for academic papers, web pages, or any text containing specialized terms, `scireadability` provides enhanced accuracy.

### Key features

- Enhanced syllable counting accuracy, particularly for complex and scientific vocabulary.
- Customizable syllable dictionary to handle exceptions and domain-specific terms, enhancing accuracy for specialized texts. Includes a built-in custom dictionary for common edge-cases.

## Quick start

### Install using pip

```shell
pip install scireadability
```

### Usage

Here are a few examples to get you started:

```python
>>> import scireadability

>>> test_data = (
    "Within the heterogeneous canopy of the Amazonian rainforest, a fascinating interspecies interaction manifests "
    "between Cephalotes atratus, a species of arboreal ant, and Epiphytes dendrobii, a genus of epiphytic orchids.  "
    "Observations reveal that C. atratus colonies cultivate E. dendrobii within their carton nests, providing a "
    "nitrogen-rich substrate derived from ant detritus.  In return, the orchids, exhibiting a CAM photosynthetic "
    "pathway adapted to the shaded understory, contribute to nest structural integrity through their root systems and "
    "potentially volatile organic compounds.  This interaction exemplifies a form of facultative mutualism, where both "
    "species derive benefits, yet neither exhibits obligate dependence for survival in situ. Further investigation into "
    "the biochemical signaling involved in this symbiosis promises to elucidate novel ecological strategies."
)

>>> scireadability.flesch_reading_ease(test_data)
>>> scireadability.flesch_kincaid_grade(test_data)
>>> scireadability.smog_index(test_data)
>>> scireadability.coleman_liau_index(test_data)
>>> scireadability.automated_readability_index(test_data)
>>> scireadability.dale_chall_readability_score(test_data)
>>> scireadability.linsear_write_formula(test_data)
>>> scireadability.gunning_fog(test_data)

>>> # Using the custom dictionary:
>>> scireadability.add_term_to_custom_dict("pterodactyl", 4) # Adding a word with its syllable count
>>> scireadability.syllable_count("pterodactyl") # Now it will be counted correctly
```

For all functions, the input argument (`text`) remains the same: the text you want to analyze for readability statistics.

## Language support

By default, the functions are configured for English language algorithms. Please be aware that accuracy may be reduced when used with non-English texts. The built-in custom dictionary and syllable counting methods are based on pronunciations in American English.  For syllable counting, `scireadability` relies on:

- **CMUdict**: For English, the Carnegie Mellon Pronouncing Dictionary (CMUdict) is used for accurate syllable counts.
- **Pyphen**: For other languages, the Pyphen library is used if available. If the Pyphen dictionary for a specific language is not installed, a warning will be issued, and syllable counting may be less accurate. You can install Pyphen dictionaries using pip (e.g., `pip install pyphen`).

To change the language setting, use:

```python
scireadability.set_lang(lang)
```

The specified language will be used for syllable calculation, to load language-specific resources like CMUdict or Pyphen, and to select the appropriate formula variant where available.  The `set_lang()` function not only changes the language but also:

- Loads `cmudict` when set to English ("en") or sets it to `None` for other languages.
- Attempts to load `Pyphen` for non-English languages.
- Clears internal caches to ensure language changes are applied immediately.

For Spanish-specific readability tests (fernandez_huerta, szigriszt_pazos, gutierrez_polini, crawford), it is not recommended to use them on non-Spanish texts as they are specifically designed for the Spanish language.

## Custom syllable dictionary

`scireadability` allows you to customize syllable counts for words that the default algorithm might miscount or to include words not found in the standard dictionaries. Custom dictionaries are managed per language. When you load or modify a custom dictionary, it applies to the currently set language. This feature is particularly useful for:

- **Handling exceptions**: Correcting syllable counts for words that don't follow typical pronunciation rules.
- **Adding specialized vocabulary**: Including syllable counts for terms specific to certain fields that are not in general dictionaries.
- **Improving accuracy**: Fine-tuning syllable counts to enhance the precision of readability scores and other text statistics.

**Managing Your Custom Dictionary**

`scireadability` includes a pre-built custom dictionary (`resources/en/custom_dict.json`) that contains words often miscounted by standard syllable counters. The library also provides tools to manage your custom syllable dictionary. These dictionaries are stored as JSON files in your user configuration directory. The exact location depends on your operating system but is usually within your user profile in a directory named `.scireadability` or similar.

You can use the following functions to interact with the custom dictionary:

- `load_custom_syllable_dict(lang="en")`: Loads the active custom dictionary for the specified language. If no user-defined dictionary exists, it loads the default dictionary.
- `overwrite_custom_dict(file_path, lang="en")`: Replaces your entire custom dictionary for the given language with the contents of a JSON file you provide.
- `add_term_to_custom_dict(word, syllable_count, lang="en")`: Adds a new word and its syllable count to the custom dictionary, or updates the count if the word already exists.
- `add_terms_from_file(file_path, lang="en")`: Adds multiple words and their syllable counts from a JSON file. This file should contain a key `"CUSTOM_SYLLABLE_DICT"` which maps words to their integer syllable counts.
- `revert_custom_dict_to_default(lang="en")`: Resets your custom dictionary back to the original default dictionary.
- `print_custom_dict(lang="en")`: Prints the contents of your currently loaded custom dictionary in a readable JSON format.

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

The top-level JSON object must have a key named `"CUSTOM_SYLLABLE_DICT"`. Within this object, each key is a word (string), and its corresponding value is the word's syllable count (integer).

## Controlling apostrophe handling

```python
scireadability.set_rm_apostrophe(rm_apostrophe)
```

The `set_rm_apostrophe` function allows you to control how apostrophes in contractions are handled when counting words, syllables, and characters.

By default (`rm_apostrophe=False`), `scireadability` **retains apostrophes in common English contractions** (like "don't" or "can't") and treats these contractions as single words. This is because CMUdict accurately counts contractions. All other punctuation (periods, commas, question marks, exclamation points, hyphens, etc.) is removed.

If you call `scireadability.set_rm_apostrophe(True)`, **apostrophes in contractions will also be removed** along with all other punctuation. In this mode, contractions might be counted as multiple words depending on the context (though `scireadability` generally still treats contractions as single lexical units).

**Example:**

```python
>>> import scireadability
>>> text_example = "Let's analyze this sentence with contractions like aren't and it's."

>>> scireadability.set_rm_apostrophe(False) # Default behavior
>>> word_count_default = scireadability.lexicon_count(text_example)
>>> print(f"Word count with default apostrophe handling: {word_count_default}")

>>> scireadability.set_rm_apostrophe(True) # Remove apostrophes
>>> word_count_remove_apostrophe = scireadability.lexicon_count(text_example)
>>> print(f"Word count with apostrophes removed: {word_count_remove_apostrophe}")
```

Choose the apostrophe handling mode that best suits your analysis needs.  For most general readability assessments, the default behavior (`rm_apostrophe=False`) is recommended.

## Controlling output rounding

```python
scireadability.set_rounding(rounding, points=None)
```

The `set_rounding` function lets you control whether the numerical outputs of `scireadability` functions are rounded and to how many decimal places.

By default, output rounding is disabled (`rounding=False`), and you will receive scores with their full decimal precision.

To enable rounding, call `scireadability.set_rounding(True, points)`, where `points` is an integer specifying the number of decimal places to round to. If `points` is `None` (or not provided), it defaults to rounding to the nearest whole number (0 decimal places).

**Example:**

```python
>>> import scireadability
>>> text_example = "This is a text for demonstrating rounding."
>>> score_unrounded = scireadability.flesch_reading_ease(text_example)
>>> print(f"Unrounded Flesch Reading Ease: {score_unrounded}")

>>> scireadability.set_rounding(True, 2) # Enable rounding to 2 decimal places
>>> score_rounded_2_decimal = scireadability.flesch_reading_ease(text_example)
>>> print(f"Rounded to 2 decimal places: {score_rounded_2_decimal}")

>>> scireadability.set_rounding(True) # Enable rounding to whole number (0 decimals)
>>> score_rounded_whole = scireadability.flesch_reading_ease(text_example)
>>> print(f"Rounded to whole number: {score_rounded_whole}")
```

Use `set_rounding` to format the output scores according to your desired level of precision.


## List of functions

### Formulas

**Flesch Reading Ease**

```python
scireadability.flesch_reading_ease(text)
```

Returns the Flesch Reading Ease score. A higher score indicates greater text readability. Scores can range up to a maximum of approximately 121, with negative scores possible for extremely complex texts.  The formula is based on average sentence length and average syllables per word. The formula's parameters (base score, sentence length factor, syllable per word factor) are language-dependent and can be configured for different languages using the `set_lang()` function.

| Score   | Difficulty       |
|---------|------------------|
| 90-100  | Very Easy        |
| 80-89   | Easy             |
| 70-79   | Fairly Easy      |
| 60-69   | Standard         |
| 50-59   | Fairly Difficult |
| 30-49   | Difficult        |
| 0-29    | Very Confusing   |

**Flesch-Kincaid Grade Level**

```python
scireadability.flesch_kincaid_grade(text)
```

Returns the Flesch-Kincaid Grade Level. For example, a score of 9.3 suggests that the text is readable for a student in the 9th grade. This formula estimates the U.S. grade level equivalent to understand the text. It is calculated based on average sentence length and average syllables per word.

**Gunning Fog Index**

```python
scireadability.gunning_fog(text)
```

Returns the Gunning Fog Index. A score of 9.3 indicates that the text is likely understandable to a 9th-grade student. The Gunning Fog Index estimates the years of formal education required for a person to understand the text on the first reading. It uses average sentence length and the percentage of complex words (words with more than two syllables).

**SMOG Index**

```python
scireadability.smog_index(text)
```

Returns the SMOG Index. This formula is most reliable for texts containing at least 30 sentences. `scireadability` requires a minimum of 3 sentences to calculate this index. The SMOG Index (Simple Measure of Gobbledygook) is another grade-level readability test. It focuses on polysyllabic words (words with three or more syllables) and sentence count to estimate reading difficulty.

**Automated Readability Index (ARI)**

```python
scireadability.automated_readability_index(text)
```

Returns the Automated Readability Index (ARI). A score of 6.5 suggests the text is suitable for students in 6th to 7th grade. The ARI estimates the grade level needed to understand the text. It uses character count, word count, and sentence count in its calculation.

**Coleman-Liau Index**

```python
scireadability.coleman_liau_index(text)
```

Returns the Coleman-Liau Index grade level. For example, a score of 9.3 indicates that the text is likely readable for a 9th-grade student. The Coleman-Liau Index relies on character count per word and sentence count per word, rather than syllable count, to estimate the grade level.

**Linsear Write Formula**

```python
scireadability.linsear_write_formula(text)
```

Returns the estimated grade level of the text based on the Linsear Write Formula. This formula is unique in that it only uses the first 100 words of the text to calculate readability. It counts "easy words" (1-2 syllables) and "difficult words" (3+ syllables) in this sample.

**Dale-Chall Readability Score**

```python
scireadability.dale_chall_readability_score(text)
```

Calculates readability using a lookup table of the 3,000 most common English words. The resulting score corresponds to a grade level as follows:

| Score         | Understood by                                   |
|---------------|-------------------------------------------------|
| 4.9 or lower  | Average 4th-grade student or below              |
| 5.0–5.9       | Average 5th or 6th-grade student                |
| 6.0–6.9       | Average 7th or 8th-grade student                |
| 7.0–7.9       | Average 9th or 10th-grade student               |
| 8.0–8.9       | Average 11th or 12th-grade student              |
| 9.0–9.9       | Average 13th to 15th-grade (college) student    |

**Readability Consensus (Text Standard)**

```python
scireadability.text_standard(text, float_output=False)
```

Provides an estimated school grade level based on a consensus of all the readability tests included in this library. It aggregates the grade level outputs from Flesch-Kincaid Grade Level, Flesch Reading Ease, SMOG Index, Coleman-Liau Index, Automated Readability Index, Dale-Chall Readability Score, Linsear Write Formula, and Gunning Fog Index to provide a consolidated readability grade. Setting `float_output=True` will return a numerical average grade level instead of an integer-based level.

**Spache Readability Formula**

```python
scireadability.spache_readability(text)
```

Returns a grade level score for English text, primarily designed for texts aimed at or below the 4th-grade reading level. The Spache formula is specifically tailored for assessing the readability of texts for young children, focusing on sentence length and the proportion of "hard words" (words not on a list of common words).

**McAlpine EFLAW Readability Score**

```python
scireadability.mcalpine_eflaw(text)
```

Returns a readability score for English text intended for foreign language learners. A score of 25 or lower is generally recommended for learners. The McAlpine EFLAW score is designed to evaluate text readability for learners of English as a Foreign Language. It considers word count, "mini-word" count (words with 3 letters or less), and sentence count.

**Reading time estimation**

```python
scireadability.reading_time(text, ms_per_char=14.69)
```

Returns an estimated reading time for the text in milliseconds. It uses a default reading speed of 14.69 milliseconds per character, but you can adjust this using the `ms_per_char` parameter. This function provides a rough estimate of how long it might take to read the text, based on the number of characters and an assumed reading speed.

### Language-specific formulas

**Índice de Lecturabilidad Fernandez-Huerta (Spanish)**

```python
scireadability.fernandez_huerta(text)
```

A Spanish-language reformulation of the Flesch Reading Ease formula. This formula adapts the Flesch Reading Ease principles to better suit the characteristics of the Spanish language.

**Índice de Perspicuidad de Szigriszt-Pazos (Spanish)**

```python
scireadability.szigriszt_pazos(text)
```

An adaptation of the Flesch Reading Ease formula specifically tailored for Spanish texts.  Similar to Fernandez-Huerta, this is another Spanish adaptation of Flesch Reading Ease, with slightly different weighting of factors.

**Fórmula de Comprensibilidad de Gutiérrez de Polini (Spanish)**

```python
scireadability.gutierrez_polini(text)
```

Returns the Gutiérrez de Polini Understandability Index. This formula is designed for Spanish texts intended for grade-school levels. This index is specifically developed for assessing the comprehensibility of Spanish texts for elementary school children.

**Fórmula de Crawford (Spanish)**

```python
scireadability.crawford(text)
```

Returns an estimate of the years of schooling required to understand a Spanish text. This formula is intended for elementary-level Spanish texts. The Crawford formula estimates the years of education needed to understand Spanish text aimed at elementary school levels.

**Osman Score (Arabic)**

```python
scireadability.osman(text)
```

Returns the Osman score, which is an adaptation of the Flesch and Fog formulas for Arabic texts. The Osman index adapts principles from Flesch and Gunning Fog to create a readability score suitable for Arabic language texts.

**Gulpease Index (Italian)**

```python
scireadability.gulpease_index(text)
```

Returns the Gulpease index for Italian texts. Lower scores indicate more difficult text. The Gulpease Index is designed for Italian and, unlike many other indices, a *lower* score indicates *higher* reading difficulty.

**Wiener Sachtextformel (German)**

```python
scireadability.wiener_sachtextformel(text, variant)
```

Returns a grade-level style readability score for German text. The score ranges approximately from 4 (very easy) to 15 (very difficult).  The Wiener Sachtextformel has different variants; the `variant` parameter allows you to choose between these variations (1 to 4), each with slightly different weighting of factors like polysyllable count and sentence length.

### Aggregates and averages

**Syllable count**

```python
scireadability.syllable_count(text)
```

Returns the total number of syllables in the input text. It first checks against custom dictionaries, then uses cmudict (for English), and finally falls back to a regex-based syllable counting method for English if CMUdict fails. For non-English languages, if Pyphen is available, it's used; otherwise, no fallback is applied. This function is affected by the `set_rm_apostrophe()` setting, as punctuation is removed before counting.

**Word count (lexicon Count)**

```python
scireadability.lexicon_count(text, removepunct=True)
```

Calculates the number of words in the text. By default, punctuation is removed before counting (`removepunct=True`). You can control apostrophe handling using `set_rm_apostrophe()`.  Hyphenated words and contractions are generally counted as single words.

**Sentence count**

```python
scireadability.sentence_count(text)
```

Returns the number of sentences identified in the text. It uses regular expressions to detect sentence boundaries based on sentence-ending punctuation marks (., !, ?). Short "sentences" of 2 words or less are ignored to avoid miscounting headings or fragments.

**Character count**

```python
scireadability.char_count(text, ignore_spaces=True)
```

Returns the total number of characters in the text. Spaces are ignored by default (`ignore_spaces=True`). This function simply counts all characters, including letters, numbers, punctuation, and symbols (unless spaces are ignored).

**Letter count**

```python
scireadability.letter_count(text, ignore_spaces=True)
```

Returns the number of letters in the text, excluding punctuation and spaces. Spaces are ignored by default (`ignore_spaces=True`). This function counts only alphabetic characters (a-z, A-Z) after removing punctuation (based on the `set_rm_apostrophe()` setting).

**Polysyllable count**

```python
scireadability.polysyllabcount(text)
```

Returns the number of words in the text that have three or more syllables. It uses `syllable_count()` to determine the number of syllables for each word.

**Monosyllable count**

```python
scireadability.monosyllabcount(text)
```

Returns the number of words in the text that have exactly one syllable. It uses `syllable_count()` to determine the number of syllables for each word.

## Advanced usage and customization

`scireadability` incorporates several advanced features for customization and performance:

- **Caching**: For efficiency, `scireadability` extensively uses caching (via `@lru_cache`) to store the results of computationally intensive functions like syllable count and various text statistics. This significantly speeds up repeated analyses of the same or similar texts. Caches are automatically cleared when you change the language using `set_lang()`.
- **Extending Language Support**: While `scireadability` provides built-in support for several languages, you can potentially contribute to expanding language support. Language-specific parameters for formulas are defined in the internal `langs` dictionary. Contributions of new language configurations and easy word lists are welcome.

## Limitations

Please be aware of the following limitations:

- **SMOG Index sentence requirement**: The SMOG Index formula is most reliable for texts with at least 30 sentences. `scireadability` will return 0.0 if the text has fewer than 3 sentences when calculating the SMOG index.
- **Short texts**: Readability formulas are generally designed for paragraphs or longer texts. Applying them to very short texts (e.g., single sentences or phrases) may yield less meaningful or less stable results.
- **Highly-specialized jargon**: While `scireadability` is enhanced for scientific texts, extremely dense or novel jargon not present in CMUdict, Pyphen, or custom dictionaries might still affect syllable counting accuracy and, consequently, readability scores. For highly domain-specific texts, careful review and custom dictionary adjustments may be beneficial.
- **Syllable, sentence, and word counting**: Counting these accurately is inherently difficult. While `scireadability` makes every attempt to
accurately count, its approach is heuristic-based for efficiency and ease-of-use. For non-English tests, Pyphen is used as a fallback, which is not accurate for syllable counts. The regex-based syllable
count for English fallback (a refined version of hauntsaninja's base regex [here](https://datascience.stackexchange.com/a/89312)) agrees with CMUdict ~91% of the time.

## Contributing

If you encounter any issues, please open an
[issue](https://github.com/robert-roth/scireadability/issues) to report it or provide feedback on the
[Try it page]([TRY_IT_PAGE_URL]).

If you are able to fix a bug or implement a new feature, we welcome you to submit a
[pull request](https://github.com/robert-roth/scireadability/pulls).

1. Fork this repository on GitHub to begin making your changes on the master branch (or create a new branch from it).
2. Write a test to demonstrate that the bug is fixed or that the new feature functions as expected.
3. Submit a pull request with your changes!
