# scireadability
[![PyPI Downloads](https://static.pepy.tech/badge/scireadability)](https://pepy.tech/projects/scireadability)  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**`scireadability` is a user-friendly Python library designed to calculate text statistics for English texts. It's helpful for assessing readability, complexity, and grade level of texts. While specifically enhanced for scientific documents, it works well with any type of text. Punctuation is removed by default, with the exception of apostrophes in contractions.**

> You can try it out on the scireadability demo site [here](https://scireadability-rwroth5.pythonanywhere.com/).

This library is built upon the foundation of the [`textstat`](https://github.com/shivam5992/textstat) Python library, originally created by Shivam Bansal and Chaitanya Aggarwal.

## Why scireadability?

While building upon the excellent `textstat` library, `scireadability` is specifically designed to address the unique challenges of analyzing scientific and technical texts. 
It offers improved accuracy for syllable counting, especially for scientific vocabulary and names. If you need readability statistics for academic papers, web pages, or any text containing specialized terms, `scireadability` provides enhanced accuracy.

>`scireadability` currently only offers support for English texts. For non-English texts, `textstat` offers broad coverage.

### Key features

- Enhanced syllable counting accuracy, particularly for complex and scientific vocabulary.
- Customizable syllable dictionary to handle exceptions and domain-specific terms, enhancing accuracy for specialized texts. Includes a built-in custom dictionary for common edge-cases.
- Verbose mode identifies the most complex sentences and provides specific suggestions for improving readability.

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
>>> scireadability.add_word_to_dictionary("pterodactyl", 4) # Adding a word with its syllable count
>>> scireadability.syllable_count("pterodactyl") # Now it will be counted correctly

>>> # Using verbose mode to get detailed analysis:
>>> analysis = scireadability.flesch_kincaid_grade(text, verbose=True)
>>> print(f"Overall grade level: {analysis['score']}")
>>> print(f"Most complex sentence: {analysis['complex_sentences'][0]['text']}")
>>> print(f"Improvement suggestions: {analysis['complex_sentences'][0]['suggestions']}")

>>> # Configure verbose analysis:
>>> verbose_config = {
...     "top_n": 5,                  # Return top 5 most complex sentences
...     "include_word_analysis": True,      # Include difficult word analysis
...     "include_suggestions": True         # Include improvement suggestions
... }
>>> detailed = scireadability.gunning_fog(text, verbose=True, verbose_config=verbose_config)
```

For all functions, the input argument (`text`) remains the same: the text you want to analyze for readability statistics.

## Language Support

This library is designed exclusively for English text analysis. The English-focused approach allows for more accurate syllable counting and readability assessments specifically tailored to English language texts. For syllable counting, `scireadability` uses a multi-tiered approach:

- **CMUdict**: The Carnegie Mellon Pronouncing Dictionary (CMUdict) is used for accurate syllable counts.
- **Custom Dictionary**: A user-customizable dictionary for handling specialized terminology.
- **Regex**: If a word is not found in CMUdict or the custom dictionary, syllables are counted through a refined version of the base regex by [hauntsaninja](https://datascience.stackexchange.com/a/89312). It accounts for common suffixes in species names that often lead to undercounting.

## Custom syllable dictionary

`scireadability` allows you to customize syllable counts for words that the default algorithm might miscount or to include words not found in the standard dictionaries. This feature is particularly useful for:

- **Handling exceptions**: Correcting syllable counts for words that don't follow typical pronunciation rules.
- **Adding specialized vocabulary**: Including syllable counts for terms specific to certain fields that are not in general dictionaries.
- **Improving accuracy**: Fine-tuning syllable counts to enhance the precision of readability scores and other text statistics.

**Managing Your Custom Dictionary**

`scireadability` includes a pre-built custom dictionary (`resources/en/custom_dict.json`) that contains words often miscounted by standard syllable counters. The library also provides tools to manage your custom syllable dictionary. These dictionaries are stored as JSON files in your user configuration directory. The exact location depends on your operating system but is usually within your user profile in a directory named `.scireadability` or similar.

You can use the following functions to interact with the custom dictionary:

- `load_custom_syllable_dict()`: Loads the active custom dictionary. If no user-defined dictionary exists, it loads the default dictionary.
- `overwrite_dictionary(file_path)`: Replaces your entire custom dictionary with the contents of a JSON file you provide.
- `add_word_to_dictionary(word, syllable_count)`: Adds a new word and its syllable count to the custom dictionary, or updates the count if the word already exists.
- `add_words_from_file_to_dictionary(file_path)`: Adds multiple words and their syllable counts from a JSON file. This file should contain a key `"CUSTOM_SYLLABLE_DICT"` which maps words to their integer syllable counts.
- `revert_dictionary_to_default()`: Resets your custom dictionary back to the original default dictionary.
- `print_dictionary()`: Prints the contents of your currently loaded custom dictionary in a readable JSON format.

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

Choose the apostrophe handling mode that best suits your analysis needs. For most general readability assessments, the default behavior (`rm_apostrophe=False`) is recommended.

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

Returns the Flesch Reading Ease score. A higher score indicates greater text readability. Scores can range up to a maximum of approximately 121, with negative scores possible for extremely complex texts. The formula is based on average sentence length and average syllables per word.

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
scireadability.text_standard(text, as_string=True)
```

Provides an estimated school grade level based on a consensus of all the readability tests included in this library. It aggregates the grade level outputs from Flesch-Kincaid Grade Level, Flesch Reading Ease, SMOG Index, Coleman-Liau Index, Automated Readability Index, Dale-Chall Readability Score, Linsear Write Formula, and Gunning Fog Index to provide a consolidated readability grade. Setting `as_string=False` will return a numerical average grade level instead of an integer-based level.

**FORCAST**
```python
scireadability.forcast(text)
```

Returns the FORCAST readability estimate, expressed as a U.S. grade level. FORCAST is calculated based on how many single-syllable words appear in a 150-word consecutive sample (by default, taken from the beginning of the text). The resulting score indicates the education level needed to comprehend the text.

Notes:
- The original research validates FORCAST only for English texts and specifically for 150-word samples from U.S. Army technical manuals. Using FORCAST for narrative is not advised.
- If your text is shorter than 150 words, a warning is issued because the formula may be less reliable.

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

### Aggregates and averages

**Syllable count**

```python
scireadability.syllable_count(text)
```

Returns the total number of syllables in the input text. It first checks against custom dictionaries, then uses cmudict, and finally falls back to a regex-based syllable counting method if CMUdict fails. This function is affected by the `set_rm_apostrophe()` setting, as punctuation is removed before counting.

**Word count (lexicon Count)**

```python
scireadability.lexicon_count(text, removepunct=True)
```

Calculates the number of words in the text. By default, punctuation is removed before counting (`removepunct=True`). You can control apostrophe handling using `set_rm_apostrophe()`. Hyphenated words and contractions are generally counted as single words.

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

## Verbose analysis

```python
scireadability.any_readability_metric(text, verbose=True, verbose_config=None)
```

All readability metrics in `scireadability` support verbose analysis mode, which provides detailed information about text complexity and specific suggestions for improvement. When `verbose=True`, instead of returning a simple score, the function returns a structured dictionary containing:

- The overall readability score
- A list of the most complex sentences with detailed metrics for each
- Specific suggestions for improving each sentence
- An overall improvement summary

**Example output structure:**

```python
{
    "score": 14.2,                      # The overall readability score
    "metric": "flesch_kincaid_grade",   # The metric used
    "complex_sentences": [              # List of most complex sentences
        {
            "text": "The intricate molecular mechanisms...",  # The sentence
            "length": 32,               # Word count
            "avg_syllables": 2.1,       # Average syllables per word
            "difficult_words": 12,      # Count of difficult words
            "polysyllabic_words": 8,    # Words with 3+ syllables
            "difficult_word_list": ["intricate", "molecular", ...],
            "suggestions": [            # Improvement suggestions
                "Consider breaking this into shorter sentences",
                "Replace complex words: intricate, molecular, mechanisms"
            ]
        },
        # More sentences...
    ],
    "improvement_summary": {            # Overall summary
        "total_complex_sentences": 10,
        "long_sentences": 7,
        "high_syllable_sentences": 8,
        "common_difficult_words": {"molecular": 5, "mechanisms": 3, ...},
        "general_advice": [
            "Break up long sentences",
            "Use simpler vocabulary with fewer syllables"
        ]
    }
}
```

**Customizing the analysis:**

You can configure the verbose output by providing a `verbose_config` dictionary:

```python
verbose_config = {
    "top_n": 10,                  # Number of complex sentences to return (default: 10)
    "include_word_analysis": True, # Include analysis of difficult words (default: True)
    "include_suggestions": True    # Include improvement suggestions (default: True)
}

analysis = scireadability.flesch_kincaid_grade(text, verbose=True, verbose_config=verbose_config)
```

This feature is particularly useful for:

- **Writing assistance**: Identify exactly which sentences are most challenging for readers
- **Document improvement**: Get actionable suggestions for enhancing readability
- **Educational purposes**: Teach writers how to create more accessible content
- **Content analysis**: Perform detailed analysis of document complexity

The `text_standard()` function with `verbose=True` provides an especially comprehensive analysis by combining results from multiple readability metrics to identify sentences that are consistently flagged as complex across different formulas.

## Limitations

Please be aware of the following limitations:

- **SMOG Index sentence requirement**: The SMOG Index formula is most reliable for texts with at least 30 sentences. `scireadability` will return 0.0 if the text has fewer than 3 sentences when calculating the SMOG index.
- **Short texts**: Readability formulas are generally designed for paragraphs or longer texts. Applying them to very short texts (e.g., single sentences or phrases) may yield less meaningful or less stable results.
- **Highly-specialized jargon**: While `scireadability` is enhanced for scientific texts, extremely dense or novel jargon not present in CMUdict or custom dictionaries might still affect syllable counting accuracy and, consequently, readability scores. For highly domain-specific texts, careful review and custom dictionary adjustments may be beneficial.
- **Syllable, sentence, and word counting**: Counting these accurately is inherently difficult. While `scireadability` makes every attempt to
accurately count, its approach is heuristic-based for efficiency and ease-of-use. The regex-based syllable
count for English fallback (a refined version of hauntsaninja's base regex [here](https://datascience.stackexchange.com/a/89312)) agrees with CMUdict ~91% of the time.
- **non-English texts**: `scireadability` does not support non-English texts or non-English readability measures. Please use another package such as `textstat` for non-English texts.

## Contributing

If you encounter any issues, please open an
[issue](https://github.com/robert-roth/scireadability/issues) to report it or provide feedback on the
[Try it page]([TRY_IT_PAGE_URL]).

If you are able to fix a bug or implement a new feature, we welcome you to submit a
[pull request](https://github.com/robert-roth/scireadability/pulls).

1. Fork this repository on GitHub to begin making your changes on the master branch (or create a new branch from it).
2. Write a test to demonstrate that the bug is fixed or that the new feature functions as expected.
3. Submit a pull request with your changes!
