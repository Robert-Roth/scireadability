# textstatsci
### Textual statistics for science communication

>`textstatsci` is a fork of the [textstat](https://github.com/shivam5992/textstat) Python library, originally created by Shivam Bansal and Chaitanya Aggarwal.  It builds upon textstat to provide improved text statistics for scientific and academic texts, particularly in handling specialized vocabulary like species names.

> Modifications include a built-in custom dictionary (and the ability to use your own) and improved handling for specialized vocabulary.

**textstatsci is an easy-to-use library to calculate statistics from text. It helps determine readability, complexity, and grade level. It is specialized for scientific texts, but can be applied to non-scientific texts as well. However, it is possible that the enhancements made with scientific texts in mind could impact accuracy of non-scientific texts.**

## Usage

```python
>>> import textstatsci

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

>>> textstatsci.flesch_reading_ease(test_data)
>>> textstatsci.flesch_kincaid_grade(test_data)
>>> textstatsci.smog_index(test_data)
>>> textstatsci.coleman_liau_index(test_data)
>>> textstatsci.automated_readability_index(test_data)
>>> textstatsci.dale_chall_readability_score(test_data)
>>> textstatsci.difficult_words(test_data)
>>> textstatsci.linsear_write_formula(test_data)
>>> textstatsci.gunning_fog(test_data)
>>> textstatsci.text_standard(test_data)
>>> textstatsci.fernandez_huerta(test_data)
>>> textstatsci.szigriszt_pazos(test_data)
>>> textstatsci.gutierrez_polini(test_data)
>>> textstatsci.crawford(test_data)
>>> textstatsci.gulpease_index(test_data)
>>> textstatsci.osman(test_data)
```

The argument (text) for all the defined functions remains the same —
i.e the text for which statistics need to be calculated.

## Install

You can install textstatsci either via the Python Package Index (PyPI) or from source.

### Install using pip

```shell
pip install textstatsci
```

### Install latest version from GitHub

```shell
git clone https://github.com/robert-roth/textstatsci.git
cd textstatsci
pip install .
```

### Install from PyPI

Download the latest version of textstatsci from http://pypi.python.org/pypi/textstatsci/

You can install it by doing the following:

```shell
tar xfz textstatsci-*.tar.gz
cd textstatsci-*/
python setup.py build
python setup.py install # as root
```

## Language support
By default functions implement algorithms for English language. 
>Note that accuracy may suffer for non-English scientific texts. The custom dictionary and 
> syllable counter fallbacks are based on pronunciations in American English.

To change language, use:

```python
textstatsci.set_lang(lang)
``` 

The language will be used for syllable calculation and to choose 
variant of the formula. 

### Language variants
All functions implement `en_US` language. Some of them has also variants 
for other languages listed below. 

|  Function                   | en | de | es | fr | it | nl | pl | ru |
|-----------------------------|----|----|----|----|----|----|----|----|
| flesch_reading_ease         | ✔  | ✔  | ✔  | ✔  | ✔  | ✔  |    | ✔  |
| gunning_fog                 | ✔  |    |    |    |    |    | ✔  |    |

#### Spanish-specific tests
The following functions are specifically designed for Spanish language.
They can be used on non-Spanish texts, even though that use case is not recommended.

```python
>>> textstatsci.fernandez_huerta(test_data)
>>> textstatsci.szigriszt_pazos(test_data)
>>> textstatsci.gutierrez_polini(test_data)
>>> textstatsci.crawford(test_data)
```

Additional information on the formula they implement can be found in their respective docstrings.

### Custom Syllable Dictionary

Textstatsci allows you to customize the syllable counts for words that might be miscounted by the default algorithm or to add counts for words not present in the base dictionaries. This is particularly useful for:

*   **Handling exceptions:** Correcting syllable counts for words that are exceptions to general syllabification rules (e.g., proper nouns, different pronunciations).
*   **Adding specialized vocabulary:** Including syllable counts for terms specific to your domain or field that might not be in standard dictionaries, such as species names and drug names.
*   **Improving accuracy:** Fine-tuning syllable counts to enhance the precision of readability scores and other text statistics.

**Managing Your Custom Dictionary**

Textstatsci comes prebundled with a custom dictionary (`resources/en/custom_dict.json`) that is loaded with some words that are poorly handled by syllable counters. Textstatsci also provides utilities to manage your custom syllable dictionary. These dictionaries are stored as JSON files in your user configuration directory (the location of which depends on your operating system, but is typically within your user profile under a directory named `.textstatsci` or similar).

The dictionary uses the following functions to interact with the custom dictionary:

*   **`load_custom_syllable_dict(lang="en")`**:  Loads the currently active custom syllable dictionary for the specified language (default is English - "en"). This function prioritizes a user-defined dictionary if it exists, falling back to the default dictionary provided with the package if no user dictionary is found. The loaded dictionary is case-insensitive for word lookups.

*   **`overwrite_custom_dict(file_path, lang="en")`**: Replaces your entire custom dictionary for the given language with the contents of a JSON file you provide at `file_path`. The JSON file must be formatted correctly (see "Dictionary file format" below).

*   **`add_term_to_custom_dict(word, syllable_count, lang="en")`**: Adds a single `word` with a specified `syllable_count` to your custom dictionary. If the `word` already exists, its syllable count will be updated to the new value.

*   **`add_terms_from_file(file_path, lang="en")`**:  Allows you to add multiple terms to your custom dictionary from a JSON file at `file_path`. The JSON file should contain a dictionary of words and their syllable counts under the `"CUSTOM_SYLLABLE_DICT"` key (see "Dictionary file format" below).

*   **`revert_custom_dict_to_default(lang="en")`**: Resets your custom dictionary for the specified language back to the original default dictionary that comes with textstatsci. This effectively removes all your custom word additions and overrides.

*   **`print_custom_dict(lang="en")`**: Prints the contents of your currently loaded custom dictionary to the console in a readable JSON format. Useful for inspecting the dictionary's contents.

**Dictionary file format**

Custom dictionary files (used with `overwrite_custom_dict` and `add_terms_from_file`) must be valid JSON files with the following structure:

```json
{
  "CUSTOM_SYLLABLE_DICT": {
    "word1": syllable_count1,
    "word2": syllable_count2,
    "anotherword": 4,
    "...": "..."
  }
}
```
#### Schema:

- The top-level JSON object must contain a key named "CUSTOM_SYLLABLE_DICT".
- The value associated with "CUSTOM_SYLLABLE_DICT" must be a JSON object (dictionary).
- Within this dictionary, keys are words (strings), and values are their corresponding syllable counts (integers).
## List of Functions

### Formulas

#### The Flesch Reading Ease formula

```python
textstatsci.flesch_reading_ease(text)
```

Returns the Flesch Reading Ease Score.

The following table can be helpful to assess the ease of
readability in a document.

The table is an _example_ of values. While the
maximum score is 121.22, there is no limit on how low
the score can be. A negative score is valid.

| Score |    Difficulty     |
|-------|-------------------|
|90-100 | Very Easy         |
| 80-89 | Easy              |
| 70-79 | Fairly Easy       |
| 60-69 | Standard          |
| 50-59 | Fairly Difficult  |
| 30-49 | Difficult         |
| 0-29  | Very Confusing    |

> Further reading on
[Wikipedia](https://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_tests#Flesch_reading_ease)

#### The Flesch-Kincaid Grade Level

```python
textstatsci.flesch_kincaid_grade(text)
```

Returns the Flesch-Kincaid Grade of the given text. This is a grade
formula in that a score of 9.3 means that a ninth grader would be able to
read the document.

> Further reading on
[Wikipedia](https://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_tests#Flesch%E2%80%93Kincaid_grade_level)

#### The Fog Scale (Gunning FOG Formula)

```python
textstatsci.gunning_fog(text)
```

Returns the FOG index of the given text. This is a grade formula in that
a score of 9.3 means that a ninth grader would be able to read the document.

> Further reading on
[Wikipedia](https://en.wikipedia.org/wiki/Gunning_fog_index)

#### The SMOG Index

```python
textstatsci.smog_index(text)
```

Returns the SMOG index of the given text. This is a grade formula in that
a score of 9.3 means that a ninth grader would be able to read the document.

Texts of fewer than 30 sentences are statistically invalid, because
the SMOG formula was normed on 30-sentence samples. textstatsci requires at
least 3 sentences for a result.

> Further reading on
[Wikipedia](https://en.wikipedia.org/wiki/SMOG)

#### Automated Readability Index

```python
textstatsci.automated_readability_index(text)
```

Returns the ARI (Automated Readability Index) which outputs
a number that approximates the grade level needed to
comprehend the text.

For example if the ARI is 6.5, then the grade level to comprehend
the text is 6th to 7th grade.

> Further reading on
[Wikipedia](https://en.wikipedia.org/wiki/Automated_readability_index)

#### The Coleman-Liau Index

```python
textstatsci.coleman_liau_index(text)
```

Returns the grade level of the text using the Coleman-Liau Formula. This is
a grade formula in that a score of 9.3 means that a ninth grader would be
able to read the document.

> Further reading on
[Wikipedia](https://en.wikipedia.org/wiki/Coleman%E2%80%93Liau_index)

#### Linsear Write Formula

```python
textstatsci.linsear_write_formula(text)
```

Returns the grade level using the Linsear Write Formula. This is
a grade formula in that a score of 9.3 means that a ninth grader would be
able to read the document.

> Further reading on
[Wikipedia](https://en.wikipedia.org/wiki/Linsear_Write)

#### Dale-Chall Readability Score

```python
textstatsci.dale_chall_readability_score(text)
```

Different from other tests, since it uses a lookup table
of the most commonly used 3000 English words. Thus it returns
the grade level using the New Dale-Chall Formula.

| Score       |  Understood by                                |
|-------------|-----------------------------------------------|
|4.9 or lower | average 4th-grade student or lower            |
|  5.0–5.9    | average 5th or 6th-grade student              |
|  6.0–6.9    | average 7th or 8th-grade student              |
|  7.0–7.9    | average 9th or 10th-grade student             |
|  8.0–8.9    | average 11th or 12th-grade student            |
|  9.0–9.9    | average 13th to 15th-grade (college) student  |

> Further reading on
[Wikipedia](https://en.wikipedia.org/wiki/Dale%E2%80%93Chall_readability_formula)

#### Readability Consensus based upon all the above tests

```python
textstatsci.text_standard(text, float_output=False)
```

Based upon all the above tests, returns the estimated school
grade level required to understand the text.

Optional `float_output` allows the score to be returned as a
`float`. Defaults to `False`.

#### Spache Readability Formula

```python
textstatsci.spache_readability(text)
```

Returns grade level of english text.

Intended for text written for children up to grade four.

> Further reading on
[Wikipedia](https://en.wikipedia.org/wiki/Spache_readability_formula)

#### McAlpine EFLAW Readability Score

```python
textstatsci.mcalpine_eflaw(text)
```

Returns a score for the readability of an english text for a foreign learner or
English, focusing on the number of miniwords and length of sentences.

It is recommended to aim for a score equal to or lower than 25. 

> Further reading on
[This blog post](https://strainindex.wordpress.com/2009/04/30/mcalpine-eflaw-readability-score/)

#### Reading Time

```python
textstatsci.reading_time(text, ms_per_char=14.69)
```

Returns the reading time of the given text.

Assumes 14.69ms per character.

> Further reading in
[This academic paper](https://homepages.inf.ed.ac.uk/keller/papers/cognition08a.pdf)

### Language Specific Formulas 
#### Índice de lecturabilidad Fernandez-Huerta (Spanish)  

```python
textstatsci.fernandez_huerta(text)
```

Reformulation of the Flesch Reading Ease Formula specifically for spanish.
The results can be interpreted similarly

> Further reading on
[This blog post](https://legible.es/blog/lecturabilidad-fernandez-huerta/)

#### Índice de perspicuidad de Szigriszt-Pazos (Spanish)  

```python
textstatsci.szigriszt_pazos(text)
```
Adaptation of Flesch Reading Ease formula for spanish-based texts.

Attempts to quantify how understandable a text is.

> Further reading on
[This blog post](https://legible.es/blog/perspicuidad-szigriszt-pazos/)

#### Fórmula de comprensibilidad de Gutiérrez de Polini (Spanish)  

```python
textstatsci.gutierrez_polini(text)
```

Returns the Guttiérrez de Polini understandability index.

Specifically designed for the texts in spanish, not an adaptation.
Conceived for grade-school level texts.

Scores for more complex text are not reliable.

> Further reading on
[This blog post](https://legible.es/blog/comprensibilidad-gutierrez-de-polini/)

#### Fórmula de Crawford (Spanish)  

```python
textstatsci.crawford(text)
```

Returns the Crawford score for the text.

Returns an estimate of the years of schooling required to understand the text.

The text is only valid for elementary school level texts.

> Further reading on
[This blog post](https://legible.es/blog/formula-de-crawford/)

#### Osman (Arabic)

```python
textstatsci.osman(text)
```

Returns OSMAN score for text.

Designed for Arabic, an adaption of Flesch and Fog Formula.
Introduces a new factor called "Faseeh".

> Further reading in
[This academic paper](https://www.aclweb.org/anthology/L16-1038.pdf)

#### Gulpease Index (Italian)

```python
textstatsci.gulpease_index(text)
```

Returns the Gulpease index of Italian text, which translates to 
level of education completed.

Lower scores require higher level of education to read with ease.

> Further reading on
[Wikipedia](https://it.wikipedia.org/wiki/Indice_Gulpease)

#### Wiener Sachtextformel (German)

```python
textstatsci.wiener_sachtextformel(text, variant)
```

Returns a grade level score for the given text.

A value of 4 means very easy text, whereas 15 means very difficult text.

> Further reading on
[Wikipedia](https://de.wikipedia.org/wiki/Lesbarkeitsindex#Wiener_Sachtextformel)

### Aggregates and Averages

#### Syllable Count

```python
textstatsci.syllable_count(text)
```

Returns the number of syllables present in the given text.
All syllable counts first check the custom dictionary, then, in English, uses [cmudit](https://github.com/prosegrinder/python-cmudict).
For words not in cmudict, a regex-based counter (which agrees with cmudict ~91% of the time)
is used. The regex is a refined version of hauntsaninja's answer [here](https://datascience.stackexchange.com/a/89312) that
adds new rules for common miscounts and adjusts based on common species-name endings.

Uses the Python module [Pyphen](https://github.com/Kozea/Pyphen)
for syllable calculation in most other languages.

#### Lexicon Count

```python
textstatsci.lexicon_count(text, removepunct=True)
```

Calculates the number of words present in the text.
Optional `removepunct` specifies whether we need to take
punctuation symbols into account while counting lexicons.
Default value is `True`, which removes the punctuation
before counting lexicon items.

#### Sentence Count

```python
textstatsci.sentence_count(text)
```

Returns the number of sentences present in the given text.

#### Character Count

```python
textstatsci.char_count(text, ignore_spaces=True)
```

Returns the number of characters present in the given text.

#### Letter Count

```python
textstatsci.letter_count(text, ignore_spaces=True)
```

Returns the number of characters present in the given text without punctuation.

#### Polysyllable Count

```python
textstatsci.polysyllabcount(text)
```

Returns the number of words with a syllable count greater than or equal to 3.

#### Monosyllable Count

```python
textstatsci.monosyllabcount(text)
```

Returns the number of words with a syllable count equal to one.

## Contributing

If you find any problems, you should open an
[issue](https://github.com/robert-roth/textstatsci/issues).

If you can fix an issue you've found, or another issue, you should open
a [pull request](https://github.com/robert-roth/textstatsci/pulls).

1. Fork this repository on GitHub to start making your changes to the master
branch (or branch off of it).
2. Write a test which shows that the bug was fixed or that the feature works as expected.
3. Send a pull request!

### Development setup

> It is recommended you use a [virtual environment](
https://docs.python.org/3/tutorial/venv.html), or [Pipenv](
https://docs.pipenv.org/) to keep your development work isolated from your
systems Python installation.

```bash
$ git clone https://github.com/<yourname>/textstatsci.git  # Clone the repo from your fork
$ cd textstatsci
$ pip install -r requirements.txt  # Install all dependencies

$ # Make changes

$ python -m pytest test.py  # Run tests
```

