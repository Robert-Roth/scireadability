__version__ = "2.0.1"

from .scireadability import (
    # Configuration
    set_rounding,
    set_rm_apostrophe,
    # Dictionary management
    add_word_to_dictionary,
    add_words_from_file_to_dictionary,
    overwrite_dictionary,
    revert_dictionary_to_default,
    print_dictionary,
    # Core stats
    char_count,
    letter_count,
    lexicon_count,
    syllable_count,
    sentence_count,
    polysyllabcount,
    monosyllabcount,
    long_word_count,
    miniword_count,
    # Averaged stats
    avg_sentence_length,
    avg_syllables_per_word,
    avg_character_per_word,
    avg_letter_per_word,
    avg_sentence_per_word,
    # Readability formulas
    flesch_reading_ease,
    flesch_kincaid_grade,
    smog_index,
    coleman_liau_index,
    automated_readability_index,
    dale_chall_readability_score,
    linsear_write_formula,
    gunning_fog,
    forcast,
    spache_readability,
    mcalpine_eflaw,
    lix,
    rix,
    # Difficult words
    difficult_words,
    difficult_words_list,
    is_difficult_word,
    is_easy_word,
    # Other utilities
    text_standard,
    reading_time,
    remove_punctuation,
    _cache_clear,
)

__all__ = [
    # Configuration
    "set_rounding",
    "set_rm_apostrophe",
    # Dictionary management
    "add_word_to_dictionary",
    "add_words_from_file_to_dictionary",
    "overwrite_dictionary",
    "revert_dictionary_to_default",
    "print_dictionary",
    # Core stats
    "char_count",
    "letter_count",
    "lexicon_count",
    "syllable_count",
    "sentence_count",
    "polysyllabcount",
    "monosyllabcount",
    "long_word_count",
    "miniword_count",
    # Averaged stats
    "avg_sentence_length",
    "avg_syllables_per_word",
    "avg_character_per_word",
    "avg_letter_per_word",
    "avg_sentence_per_word",
    # Readability formulas
    "flesch_reading_ease",
    "flesch_kincaid_grade",
    "smog_index",
    "coleman_liau_index",
    "automated_readability_index",
    "dale_chall_readability_score",
    "linsear_write_formula",
    "gunning_fog",
    "forcast",
    "spache_readability",
    "mcalpine_eflaw",
    "lix",
    "rix",
    # Difficult words
    "difficult_words",
    "difficult_words_list",
    "is_difficult_word",
    "is_easy_word",
    # Other utilities
    "text_standard",
    "reading_time",
    "remove_punctuation",
    "_cache_clear",
]
