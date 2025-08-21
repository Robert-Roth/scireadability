import math
import re
import warnings
from collections import Counter
from functools import lru_cache, wraps
from typing import Union, Dict, List, Set, Optional

import pkg_resources

from .dictionary_utils import (
    add_term_to_custom_dict,
    add_terms_from_file,
    load_custom_syllable_dict,
    overwrite_custom_dict,
    print_custom_dict,
    revert_custom_dict_to_default,
)

# --- module level state ---
_round_outputs = False
_round_points = None
_rm_apostrophe = False
text_encoding = "utf-8"


# --- helper functions and decorators ---
def _handle_zero_division(func):
    """A decorator to handle ZeroDivisionError and return 0.0."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ZeroDivisionError:
            return 0.0

    return wrapper


def _apply_rounding(
    number: float,
    rounding: Optional[bool] = None,
    points: Optional[int] = None,
    default_points: int = 2,
) -> float:
    """Applies rounding based on per-call or global settings."""
    round_this_call = rounding if rounding is not None else _round_outputs
    round_points = points if points is not None else _round_points

    if round_this_call:
        num_points = round_points if round_points is not None else default_points
        p = 10**num_points
        return float(math.floor((number * p) + math.copysign(0.5, number))) / p
    return number


def get_grade_suffix(grade: int) -> str:
    """Selects the correct ordinal suffix for a given grade."""
    ordinal_map = {1: "st", 2: "nd", 3: "rd"}
    teens_map = {11: "th", 12: "th", 13: "th"}
    return teens_map.get(grade % 100, ordinal_map.get(grade % 10, "th"))


@lru_cache(maxsize=1)
def _load_cmu_dict() -> Dict[str, List[List[str]]]:
    """Loads the CMU dictionary from package resources."""
    cmu_dict_path = "resources/en/cmudict.dict"
    pronouncing_dict: Dict[str, List[List[str]]] = {}
    cmu_text = pkg_resources.resource_string("scireadability", cmu_dict_path).decode(
        "utf-8"
    )
    for line in cmu_text.splitlines():
        if not line.startswith(";;;"):
            parts = line.split()
            if len(parts) > 1:
                word = re.sub(r"\(\d+\)$", "", parts[0]).lower()
                pronunciation = parts[1:]
                if word not in pronouncing_dict:
                    pronouncing_dict[word] = []
                pronouncing_dict[word].append(pronunciation)
    return pronouncing_dict


# --- initializations ---
custom_dict = load_custom_syllable_dict()
cmu_pronouncing_dict = _load_cmu_dict()

# --- readability constants ---
FRE_BASE = 206.835
FRE_SENTENCE_LENGTH = 1.015
FRE_SYLL_PER_WORD = 84.6
SYLLABLE_THRESHOLD = 3

# --- regular expressions ---
VOWEL_RUNS = re.compile("[aeiouy]+", flags=re.I)
EXCEPTIONS = re.compile("[^aeiou]e[sd]?$|[^e]ely$", flags=re.I)
ADDITIONAL = re.compile(
    r"[^aeioulr][lr]e[sd]?$|[csgz]es$|[td]ed$|"
    r".y[aeiou]|ia(?!n$)|eo|ism$|[^aeiou]ire$|[^gq]ua|"
    r"[^aeiouy][bcdfgjklmnpqrstvwxyz]le$|"
    r"ian$|^bio",
    flags=re.I,
)

# --- species name adjustments ---
SPECIES_NAME_ADJUSTMENTS = {
    "ii": 1,
    "odes": 1,
    "eae": 1,
    "oides": 1,
    "mallei": 1,
}


# --- public API for configuration ---
def set_rounding(rounding: bool, points: Optional[int] = None) -> None:
    """Sets the module-level rounding for all readability scores."""
    global _round_outputs, _round_points
    _round_outputs = rounding
    _round_points = points


def set_rm_apostrophe(rm_apostrophe: bool) -> None:
    """Sets the module-level apostrophe handling."""
    global _rm_apostrophe
    _rm_apostrophe = rm_apostrophe
    _cache_clear()


def _cache_clear() -> None:
    """Clears all cached results from LRU caches."""
    caching_funcs = [
        _load_cmu_dict,
        _get_easy_words,
        char_count,
        letter_count,
        lexicon_count,
        miniword_count,
        syllable_count,
        sentence_count,
        avg_sentence_length,
        avg_syllables_per_word,
        avg_character_per_word,
        avg_letter_per_word,
        avg_sentence_per_word,
        words_per_sentence,
    ]
    for func in caching_funcs:
        if hasattr(func, "cache_clear"):
            func.cache_clear()


# --- dictionary management ---
def add_word_to_dictionary(word: str, syll_count: int):
    """Adds a single word to the custom dictionary."""
    global custom_dict
    add_term_to_custom_dict(word, syll_count)
    custom_dict = load_custom_syllable_dict()
    _cache_clear()


def add_words_from_file_to_dictionary(file_path: str):
    """Adds words from a file to the custom dictionary."""
    global custom_dict
    add_terms_from_file(file_path)
    custom_dict = load_custom_syllable_dict()
    _cache_clear()


def overwrite_dictionary(file_path: str):
    """Overwrites the custom dictionary with a new one from a file."""
    global custom_dict
    overwrite_custom_dict(file_path)
    custom_dict = load_custom_syllable_dict()
    _cache_clear()


def revert_dictionary_to_default():
    """Reverts the custom dictionary to the default."""
    global custom_dict
    revert_custom_dict_to_default()
    custom_dict = load_custom_syllable_dict()
    _cache_clear()


def print_dictionary():
    """Prints the current custom dictionary."""
    print_custom_dict()


# --- core text statistics ---
@lru_cache(maxsize=128)
def char_count(text: str, ignore_spaces: bool = True) -> int:
    """Counts the number of characters in a text."""
    if ignore_spaces:
        text = re.sub(r"\s", "", text)
    return len(text)


@lru_cache(maxsize=128)
def letter_count(text: str, ignore_spaces: bool = True) -> int:
    """Counts the letters (A–Z) in a text."""
    if ignore_spaces:
        text = re.sub(r"\s", "", text)
    return sum(1 for ch in text if ch.isalpha())


def remove_punctuation(text: str) -> str:
    """Removes punctuation from a text."""
    if _rm_apostrophe:
        punctuation_regex = r"[^\w\s]"
    else:
        text = re.sub(r"\'(?![tsd]\b|ve\b|ll\b|re\b)", '"', text)
        punctuation_regex = r"[^\w\s\']"
    return re.sub(punctuation_regex, "", text)


@lru_cache(maxsize=128)
def lexicon_count(text: str, removepunct: bool = True) -> int:
    """Counts words in a text."""
    if removepunct:
        text = remove_punctuation(text)
    return len(text.split())


@lru_cache(maxsize=128)
def miniword_count(text: str, max_size: int = 3) -> int:
    """Counts common words with `max_size` letters or less."""
    return len(
        [word for word in remove_punctuation(text).split() if len(word) <= max_size]
    )


@lru_cache(maxsize=128)
def syllable_count(text: str) -> int:
    """Calculates syllables in words using a multi-tiered approach."""
    if isinstance(text, bytes):
        text = text.decode(text_encoding)

    text = text.lower()
    text = remove_punctuation(text)

    if not text:
        return 0

    total_syllables = 0
    for word in text.split():
        if word in custom_dict:
            total_syllables += custom_dict[word]
            continue

        if word in cmu_pronouncing_dict:
            try:
                phones_list = cmu_pronouncing_dict[word]
                syls = min(
                    sum(1 for p in phones if p[-1].isdigit()) for phones in phones_list
                )
                total_syllables += syls
                continue
            except (TypeError, IndexError, ValueError):
                pass

        count = regex_syllable_count(word)
        for ending, adjust in SPECIES_NAME_ADJUSTMENTS.items():
            if word.endswith(ending):
                count += adjust
                break
        total_syllables += count
    return total_syllables


def regex_syllable_count(word: str) -> int:
    """An improved regex syllable counter. Based on hauntsaninja's implementation:
    https://datascience.stackexchange.com/a/89312"""
    vowel_runs = len(VOWEL_RUNS.findall(word))
    exceptions = len(EXCEPTIONS.findall(word))
    additional = len(ADDITIONAL.findall(word))
    return max(1, vowel_runs - exceptions + additional)


@lru_cache(maxsize=128)
def sentence_count(text: str) -> int:
    """Counts the sentences in a text."""
    sentences = re.findall(r"\b[^.!?]+[.!?]*", text, re.UNICODE)
    ignore_count = sum(1 for s in sentences if lexicon_count(s) <= 2)
    return max(1, len(sentences) - ignore_count)


# --- averaged text statistics ---
@lru_cache(maxsize=128)
@_handle_zero_division
def avg_sentence_length(text: str) -> float:
    """Calculates the average sentence length."""
    return float(lexicon_count(text) / sentence_count(text))


@lru_cache(maxsize=128)
@_handle_zero_division
def avg_syllables_per_word(text: str) -> float:
    """Gets the average number of syllables per word."""
    return float(syllable_count(text)) / float(lexicon_count(text))


@lru_cache(maxsize=128)
@_handle_zero_division
def avg_character_per_word(text: str) -> float:
    """Calculates the average word length in characters."""
    return float(char_count(text)) / float(lexicon_count(text))


@lru_cache(maxsize=128)
@_handle_zero_division
def avg_letter_per_word(text: str) -> float:
    """Calculates the average word length in letters."""
    return float(letter_count(text)) / float(lexicon_count(text))


@lru_cache(maxsize=128)
@_handle_zero_division
def avg_sentence_per_word(text: str) -> float:
    """Gets the number of sentences per word."""
    return float(sentence_count(text)) / float(lexicon_count(text))


@lru_cache(maxsize=128)
def words_per_sentence(text: str) -> float:
    """Calculates the average number of words per sentence."""
    s_count = sentence_count(text)
    return float(lexicon_count(text) / s_count) if s_count >= 1 else lexicon_count(text)


# --- readability formulas ---
def flesch_reading_ease(
    text: str, rounding: Optional[bool] = None, points: Optional[int] = None
) -> float:
    """Calculates the Flesch reading ease score."""
    if not text.strip() or lexicon_count(text) == 0:
        return 0.0

    asl = avg_sentence_length(text)
    asw = avg_syllables_per_word(text)

    score = FRE_BASE - (FRE_SENTENCE_LENGTH * asl) - (FRE_SYLL_PER_WORD * asw)
    return _apply_rounding(score, rounding, points, default_points=2)


def flesch_kincaid_grade(
    text: str, rounding: Optional[bool] = None, points: Optional[int] = None
) -> float:
    """Calculates the Flesch-Kincaid grade."""
    if not text.strip() or lexicon_count(text) == 0:
        return 0.0

    asl = avg_sentence_length(text)
    asw = avg_syllables_per_word(text)

    score = (0.39 * asl) + (11.8 * asw) - 15.59
    return _apply_rounding(score, rounding, points, default_points=1)


def smog_index(
    text: str, rounding: Optional[bool] = None, points: Optional[int] = None
) -> float:
    """Calculates the SMOG index."""
    if not text.strip() or lexicon_count(text) == 0:
        return 0.0
    sentences = sentence_count(text)
    if sentences < 3:
        return 0.0
    try:
        poly_syllab = polysyllabcount(text)
        smog = (1.043 * (30 * (poly_syllab / sentences)) ** 0.5) + 3.1291
        return _apply_rounding(smog, rounding, points, default_points=1)
    except ZeroDivisionError:
        return 0.0


def coleman_liau_index(
    text: str, rounding: Optional[bool] = None, points: Optional[int] = None
) -> float:
    """Calculates the Coleman-Liau index."""
    if not text.strip() or lexicon_count(text) == 0:
        return 0.0

    alw = avg_letter_per_word(text)
    asw = avg_sentence_per_word(text)

    letters = alw * 100
    sentences = asw * 100

    coleman = (0.0588 * letters) - (0.296 * sentences) - 15.8
    return _apply_rounding(coleman, rounding, points, default_points=2)


@_handle_zero_division
def automated_readability_index(
    text: str, rounding: Optional[bool] = None, points: Optional[int] = None
) -> float:
    """Calculates the automated readability index."""
    if not text.strip() or lexicon_count(text) == 0:
        return 0.0

    acw = avg_character_per_word(text)
    wps = words_per_sentence(text)

    readability = (4.71 * acw) + (0.5 * wps) - 21.43
    return _apply_rounding(readability, rounding, points, default_points=1)


def linsear_write_formula(
    text: str, rounding: Optional[bool] = None, points: Optional[int] = None
) -> float:
    """Calculates the Linsear Write formula."""
    if not text.strip():
        return -1.0

    text_list = text.split()[:100]
    easy_word = sum(1 for word in text_list if syllable_count(word) < 3)
    difficult_word = len(text_list) - easy_word
    text_sample = " ".join(text_list)

    try:
        number = float((easy_word + (difficult_word * 3)) / sentence_count(text_sample))
    except ZeroDivisionError:
        return -1.0

    result = number / 2
    if number <= 20:
        result -= 1

    return _apply_rounding(result, rounding, points, default_points=2)


def forcast(
    text: str, rounding: Optional[bool] = None, points: Optional[int] = None
) -> float:
    """Calculates the FORCAST readability score."""
    if not text.strip():
        return 0.0

    words = remove_punctuation(text).split()
    if len(words) < 150:
        warnings.warn(
            "FORCAST formula is validated on a 150-word sample. "
            "The text is shorter than 150 words, so the result may be less reliable."
        )

    sample = words[:150]
    single_syllable_count = sum(1 for w in sample if syllable_count(w) == 1)
    score = 20.0 - (single_syllable_count / 10.0)
    return _apply_rounding(score, rounding, points, default_points=1)


@_handle_zero_division
def dale_chall_readability_score(
    text: str, rounding: Optional[bool] = None, points: Optional[int] = None
) -> float:
    """Calculates the Dale-Chall readability score."""
    if not text.strip() or lexicon_count(text) == 0:
        return 0.0

    word_count = lexicon_count(text)
    pdw = (difficult_words(text, syllable_threshold=0) / word_count) * 100
    asl = avg_sentence_length(text)

    score = (0.1579 * pdw) + (0.0496 * asl)
    if pdw > 5:
        score += 3.6365

    return _apply_rounding(score, rounding, points, default_points=2)


@_handle_zero_division
def gunning_fog(
    text: str, rounding: Optional[bool] = None, points: Optional[int] = None
) -> float:
    """Calculates the Gunning Fog index."""
    if not text.strip() or lexicon_count(text) == 0:
        return 0.0

    asl = avg_sentence_length(text)
    per_complex_words = (polysyllabcount(text) / lexicon_count(text)) * 100

    grade = 0.4 * (asl + per_complex_words)
    return _apply_rounding(grade, rounding, points, default_points=2)


@_handle_zero_division
def lix(
    text: str, rounding: Optional[bool] = None, points: Optional[int] = None
) -> float:
    """Calculates the LIX score."""
    if not text.strip() or lexicon_count(text) == 0:
        return 0.0

    tokens = remove_punctuation(text).split()
    words_len = len(tokens)
    long_words = sum(1 for w in tokens if len(w) > 6)
    per_long_words = (float(long_words) * 100) / words_len
    asl = words_len / sentence_count(text)

    score = asl + per_long_words
    return _apply_rounding(score, rounding, points, default_points=2)


@_handle_zero_division
def rix(
    text: str, rounding: Optional[bool] = None, points: Optional[int] = None
) -> float:
    """Calculates the RIX score."""
    if not text.strip() or lexicon_count(text) == 0:
        return 0.0

    words = remove_punctuation(text).split()
    long_words_count = len([wrd for wrd in words if len(wrd) > 6])
    sentences_count = sentence_count(text)

    score = long_words_count / sentences_count
    return _apply_rounding(score, rounding, points, default_points=2)


@_handle_zero_division
def spache_readability(
    text: str,
    float_output: bool = True,
    rounding: Optional[bool] = None,
    points: Optional[int] = None,
) -> Union[float, int]:
    """Calculates SPACHE readability."""
    if not text.strip() or lexicon_count(text) == 0:
        return 0.0 if float_output else 0

    asl = avg_sentence_length(text)
    pdw = (difficult_words(text) / lexicon_count(text)) * 100

    spache = (0.141 * asl) + (0.086 * pdw) + 0.839

    if not float_output:
        return int(spache)
    else:
        return _apply_rounding(spache, rounding, points, default_points=2)


@_handle_zero_division
def mcalpine_eflaw(
    text: str, rounding: Optional[bool] = None, points: Optional[int] = None
) -> float:
    """Calculates the McAlpine EFLAW score."""
    if not text.strip() or lexicon_count(text) == 0:
        return 0.0

    score = (lexicon_count(text) + miniword_count(text)) / sentence_count(text)
    return _apply_rounding(score, rounding, points, default_points=1)


def text_standard(text: str, as_string: bool = True) -> Union[float, str]:
    """Calculates a consensus readability score."""
    if not text.strip():
        return "0th grade" if as_string else 0.0

    grade_levels = []

    fk_grade = flesch_kincaid_grade(text, rounding=False)
    grade_levels.extend([round(fk_grade), math.ceil(fk_grade)])

    score = flesch_reading_ease(text, rounding=False)
    if 100 > score >= 90:
        grade_levels.append(5)
    elif 90 > score >= 80:
        grade_levels.append(6)
    elif 80 > score >= 70:
        grade_levels.append(7)
    elif 70 > score >= 60:
        grade_levels.extend([8, 9])
    elif 60 > score >= 50:
        grade_levels.append(10)
    elif 50 > score >= 40:
        grade_levels.append(11)
    elif 40 > score >= 30:
        grade_levels.append(12)
    else:
        grade_levels.append(13)

    metrics = [
        smog_index,
        coleman_liau_index,
        automated_readability_index,
        dale_chall_readability_score,
        linsear_write_formula,
        gunning_fog,
    ]
    for metric in metrics:
        val = metric(text, rounding=False)
        if not isinstance(val, (int, float)) or val < 0:
            continue
        if metric is dale_chall_readability_score:
            grade_levels.append(_dc_score_to_grade(val))
        else:
            grade_levels.extend([round(val), math.ceil(val)])

    if not grade_levels:
        return "N/A" if as_string else 0.0

    consensus_grade = Counter(int(g) for g in grade_levels).most_common(1)[0][0]

    if not as_string:
        return float(consensus_grade)

    if consensus_grade <= 1:
        return "Kindergarten to 1st grade"

    lower_grade = consensus_grade - 1
    return (
        f"{lower_grade}{get_grade_suffix(lower_grade)} and "
        f"{consensus_grade}{get_grade_suffix(consensus_grade)} grade"
    )


# --- word and syllable counts ---
def polysyllabcount(text: str) -> int:
    """Counts words with three or more syllables."""
    return sum(
        1 for word in remove_punctuation(text).split() if syllable_count(word) >= 3
    )


def monosyllabcount(text: str) -> int:
    """Counts words with one syllable."""
    return sum(
        1 for word in remove_punctuation(text).split() if syllable_count(word) < 2
    )


def long_word_count(text: str) -> int:
    """Counts words with more than 6 characters."""
    return sum(1 for word in remove_punctuation(text).split() if len(word) > 6)


# --- difficult word analysis ---
def difficult_words(text: str, syllable_threshold: int = 2) -> int:
    """Counts the number of difficult words (token-based)."""
    return len(difficult_words_list(text, syllable_threshold))


def difficult_words_list(text: str, syllable_threshold: int = 2) -> List[str]:
    """Gets a list of difficult word tokens."""
    tokens = remove_punctuation(text).lower().split()
    return [word for word in tokens if is_difficult_word(word, syllable_threshold)]


def is_difficult_word(word: str, syllable_threshold: int = 2) -> bool:
    easy_word_set = _get_easy_words()
    w = word.lower()
    if w in easy_word_set:
        return False
    if syllable_threshold > 0 and syllable_count(w) < syllable_threshold:
        return False
    return True


def is_easy_word(word: str, syllable_threshold: int = 2) -> bool:
    """Returns true if a word is easy."""
    return not is_difficult_word(word, syllable_threshold)


@lru_cache(maxsize=1)
def _get_easy_words() -> Set[str]:
    """Loads the set of easy words from resources."""
    try:
        return {
            ln.decode("utf-8").strip()
            for ln in pkg_resources.resource_stream(
                "scireadability", "resources/en/easy_words.txt"
            )
        }
    except FileNotFoundError:
        warnings.warn("Could not find the easy words vocabulary file.", Warning)
        return set()


# --- other utilities ---
def _dc_score_to_grade(score: float) -> int:
    if score <= 4.9:
        return 4  # 4th grade and below
    elif score <= 5.9:
        return 6  # 5th–6th
    elif score <= 6.9:
        return 8  # 7th–8th
    elif score <= 7.9:
        return 10  # 9th–10th
    elif score <= 8.9:
        return 12  # 11th–12th
    else:
        return 13  # College


def reading_time(
    text: str,
    wpm: float = 200.0,
    rounding: Optional[bool] = None,
    points: Optional[int] = None,
) -> float:
    """Calculates reading time in seconds based on words per minute."""
    words = lexicon_count(text)
    if words == 0:
        return 0.0
    seconds = (words / wpm) * 60.0
    return _apply_rounding(seconds, rounding, points, default_points=2)
