#!/usr/bin/python
# -*- coding:utf-8 -*-

"""Test suite for scireadability (English-Only Version)"""

import json
import os
import shutil
from scireadability import dictionary_utils
import scireadability
import pytest


# --- Fixture for setup and teardown ---
@pytest.fixture(scope="function")
def test_env():
    """Fixture to set up test environment (temp dirs, mocks) and teardown."""
    test_config_dir = os.path.join(os.getcwd(), "test_config_dir")
    test_resources_dir = os.path.join(os.getcwd(), "test_resources_dir")
    os.makedirs(test_config_dir, exist_ok=True)
    os.makedirs(test_resources_dir, exist_ok=True)

    # --- Create necessary directories for default dictionaries within test_resources_dir ---
    default_dict_en_dir = os.path.join(
        test_resources_dir, "resources", "en"
    )  # Path to en default dict dir
    os.makedirs(default_dict_en_dir, exist_ok=True)  # Create it

    original_user_config_dir = dictionary_utils.user_config_dir
    original_read_resource = dictionary_utils._read_package_resource
    dictionary_utils.user_config_dir = lambda package_name: test_config_dir
    dictionary_utils._read_package_resource = lambda resource_path: (
        _mock_resource_string(test_resources_dir, resource_path)
    )

    yield test_config_dir, test_resources_dir

    # --- Teardown ---
    dictionary_utils.user_config_dir = original_user_config_dir
    dictionary_utils._read_package_resource = original_read_resource
    if os.path.exists(test_config_dir):
        shutil.rmtree(test_config_dir)
    if os.path.exists(test_resources_dir):
        shutil.rmtree(test_resources_dir)


def _mock_resource_string(test_resources_dir, resource_path):
    """Mock for _read_package_resource to use test resources."""
    full_resource_path = os.path.join(test_resources_dir, resource_path)
    if not os.path.exists(full_resource_path):
        raise FileNotFoundError(f"Resource not found: {full_resource_path}")
    with open(full_resource_path, "r", encoding="utf-8") as f:
        return f.read().encode("utf-8")


# --- Test Text Samples ---
short_test = "Cool dogs wear da sunglasses."

punct_text = """
I said: 'This is a test sentence to test the remove_punctuation function.
It's short and not the work of a singer-songwriter. But it'll suffice.'
Your answer was: "I don't know. If I were you I'd write a test; just to make
sure, you're really just removing the characters you want to remove!" Didn't
"""

punct_text_result_w_apostr = """
I said This is a test sentence to test the remove_punctuation function
It's short and not the work of a singersongwriter But it'll suffice
Your answer was I don't know If I were you I'd write a test just to make
sure you're really just removing the characters you want to remove Didn't
"""

punct_text_result_wo_apostr = """
I said This is a test sentence to test the remove_punctuation function
Its short and not the work of a singersongwriter But itll suffice
Your answer was I dont know If I were you Id write a test just to make
sure youre really just removing the characters you want to remove Didnt
"""

long_test = (
    "Playing ... games has always been thought to be "
    "important to the development of well-balanced and "
    "creative children; however, what part, if any, "
    "they should play in the lives of adults has never "
    "been researched that deeply. I believe that "
    "playing games is every bit as important for adults "
    "as for children. Not only is taking time out to "
    "play games with our children and other adults "
    "valuable to building interpersonal relationships "
    "but is also a wonderful way to release built up "
    "tension.\n"
    "There's nothing my husband enjoys more after a "
    "hard day of work than to come home and play a game "
    "of Chess with someone. This enables him to unwind "
    "from the day's activities and to discuss the highs "
    "and lows of the day in a non-threatening, kick back "
    "environment. One of my most memorable wedding "
    "gifts, a Backgammon set, was received by a close "
    "friend. I asked him why in the world he had given "
    "us such a gift. He replied that he felt that an "
    "important aspect of marriage was for a couple to "
    "never quit playing games together. Over the years, "
    "as I have come to purchase and play, with other "
    "couples & coworkers, many games like: Monopoly, "
    "Chutes & Ladders, Mastermind, Dweebs, Geeks, & "
    "Weirdos, etc. I can reflect on the integral part "
    "they have played in our weekends and our "
    '"shut-off the T.V. and do something more '
    'stimulating" weeks. They have enriched my life and '
    "made it more interesting. Sadly, many adults "
    "forget that games even exist and have put them "
    "away in the cupboards, forgotten until the "
    "grandchildren come over.\n"
    "All too often, adults get so caught up in working "
    "to pay the bills and keeping up with the "
    '"Joneses\'" that they neglect to harness the fun '
    "in life; the fun that can be the reward of "
    "enjoying a relaxing game with another person. It "
    'has been said that "man is that he might have '
    'joy" but all too often we skate through life '
    "without much of it. Playing games allows us to: "
    "relax, learn something new and stimulating, "
    "interact with people on a different more "
    "comfortable level, and to enjoy non-threatening "
    "competition. For these reasons, adults should "
    "place a higher priority on playing games in their "
    "lives"
)

easy_text = (
    "Anna and her family love doing puzzles. Anna is best at "
    "little puzzles. Anna and her brother work on medium size "
    "puzzles together. Anna's Brother likes puzzles with cars "
    "in them. When the whole family does a puzzle, they do really "
    "big puzzles. It can take them a week to finish a really "
    "big puzzle. Last year they did a puzzle with 500 pieces! "
    "Anna tries to finish one small puzzle a day by her. "
    "Her puzzles have about 50 pieces. They all glue their "
    "favorite puzzles together and frame them. The puzzles look "
    "so nice on the wall."
)

difficult_word = "Regardless"
easy_word = "Dog"
empty_str = ""


def test_char_count():
    count = scireadability.char_count(long_test)
    count_spaces = scireadability.char_count(long_test, ignore_spaces=False)
    assert count == 1748
    assert count_spaces == 2123


def test_letter_count():
    count = scireadability.letter_count(long_test)
    assert count == 1686


def test_remove_punctuation_incl_apostrophe():
    scireadability.set_rm_apostrophe(True)
    text = scireadability.remove_punctuation(punct_text)
    scireadability.set_rm_apostrophe(False)  # Reset to default
    assert text == punct_text_result_wo_apostr


def test_remove_punctuation_excl_apostrophe():
    scireadability.set_rm_apostrophe(False)
    text = scireadability.remove_punctuation(punct_text)
    assert text == punct_text_result_w_apostr


def test_lexicon_count():
    count = scireadability.lexicon_count(long_test)
    count_punc = scireadability.lexicon_count(long_test, removepunct=False)
    assert count == 372
    assert count_punc == 376


@pytest.mark.parametrize(
    "text,n_syllables,margin",
    [
        (short_test, 7, 0),
        (punct_text, 74, 2),
        ("faeries", 2, 1),
        ("relived", 2, 0),
        ("couple", 2, 0),
        ("enriched", 2, 0),
        ("us", 1, 0),
        ("too", 1, 0),
        ("monopoly", 4, 0),
        ("him", 1, 0),
        ("he", 1, 0),
        ("without", 2, 0),
        ("creative", 3, 0),
        ("every", 2, 0),
        ("stimulating", 4, 0),
        ("life", 1, 0),
        ("cupboards", 2, 0),
        ("day's", 1, 0),
        ("forgotten", 3, 0),
        ("through", 1, 0),
        ("marriage", 2, 0),
        ("hello", 2, 0),
        ("the", 1, 0),
        ("sentences", 3, 0),
        ("songwriter", 3, 0),
        ("removing", 3, 0),
        ("interpersonal", 5, 0),
    ],
)
def test_syllable_count(text: str, n_syllables: int, margin: int):
    count = scireadability.syllable_count(text)
    diff = abs(count - n_syllables)
    assert diff <= margin


def test_sentence_count():
    count = scireadability.sentence_count(long_test)
    assert count == 17


def test_avg_sentence_length():
    # Test for the precise, unrounded value
    avg = scireadability.avg_sentence_length(long_test)
    assert avg == 21.88235294117647


def test_avg_syllables_per_word():
    scireadability.set_rounding(False)
    avg = scireadability.avg_syllables_per_word(long_test)
    assert avg == 1.4623655913978495
    scireadability.set_rounding(False)


def test_avg_letter_per_word():
    scireadability.set_rounding(False)
    avg = scireadability.avg_letter_per_word(long_test)
    assert avg == 4.532258064516129
    scireadability.set_rounding(False)


def test_avg_sentence_per_word():
    scireadability.set_rounding(False)
    avg = scireadability.avg_sentence_per_word(long_test)
    assert avg == 0.0456989247311828
    scireadability.set_rounding(False)


def test_flesch_reading_ease():
    scireadability.set_rounding(False)
    score = scireadability.flesch_reading_ease(long_test)
    assert score == 60.90828273244783
    scireadability.set_rounding(False)


def test_flesch_kincaid_grade():
    scireadability.set_rounding(False)
    score = scireadability.flesch_kincaid_grade(long_test)
    assert score == 10.20003162555345
    scireadability.set_rounding(False)


def test_polysyllabcount():
    count = scireadability.polysyllabcount(long_test)
    assert count == 36


def test_smog_index():
    scireadability.set_rounding(False)
    index = scireadability.smog_index(long_test)
    assert index == 11.442366930564873
    scireadability.set_rounding(False)


def test_coleman_liau_index():
    scireadability.set_rounding(False)
    index = scireadability.coleman_liau_index(long_test)
    assert index == 9.496989247311827
    scireadability.set_rounding(False)


def test_automated_readability_index():
    scireadability.set_rounding(False)
    index = scireadability.automated_readability_index(long_test)
    assert index == 11.643111954459208
    scireadability.set_rounding(False)


def test_linsear_write_formula():
    result = scireadability.linsear_write_formula(long_test)
    assert result == 15.0
    result = scireadability.linsear_write_formula(empty_str)
    assert result == -1.0


def test_difficult_words():
    result = scireadability.difficult_words(long_test)
    assert result == 67


def test_difficult_words_list():
    result = scireadability.difficult_words_list(short_test)
    assert result == ["sunglasses"]


def test_is_difficult_word():
    result = scireadability.is_difficult_word(difficult_word)
    assert result is True


def test_is_easy_word():
    result = scireadability.is_easy_word(easy_word)
    assert result is True


def test_dale_chall_readability_score():
    scireadability.set_rounding(False)
    score = scireadability.dale_chall_readability_score(long_test)
    assert score == 8.499579759645794
    score = scireadability.dale_chall_readability_score(empty_str)
    assert score == 0.0
    scireadability.set_rounding(False)


def test_gunning_fog():
    scireadability.set_rounding(False)
    score = scireadability.gunning_fog(long_test)
    assert score == 12.623908918406073
    scireadability.set_rounding(False)


def test_lix():
    scireadability.set_rounding(False)
    score = scireadability.lix(long_test)
    assert score == 42.85009487666034
    result = scireadability.lix(empty_str)
    assert result == 0.0
    scireadability.set_rounding(False)


def test_rix():
    scireadability.set_rounding(False)
    score = scireadability.rix(long_test)
    assert score == 4.588235294117647
    scireadability.set_rounding(False)


def test_text_standard():
    # Test with the long text sample
    standard_long = scireadability.text_standard(long_test)
    assert standard_long == "11th and 12th grade"

    # Test with the short text sample
    standard_short = scireadability.text_standard(short_test)
    assert standard_short == "2nd and 3rd grade"


def test_reading_time():
    scireadability.set_rounding(False)
    score = scireadability.reading_time(long_test)
    assert score == 111.60000000000001
    scireadability.set_rounding(False)


def test_lru_caching():
    # Clear any cache before starting
    scireadability.sentence_count.cache_clear()

    # Call the function for the first time (a "miss")
    scireadability.sentence_count(long_test)
    assert scireadability.sentence_count.cache_info().misses == 1
    assert scireadability.sentence_count.cache_info().hits == 0

    # Call it a second time (should be a "hit")
    scireadability.sentence_count(long_test)
    assert (
        scireadability.sentence_count.cache_info().misses == 1
    )  # Misses don't increase
    assert scireadability.sentence_count.cache_info().hits >= 1  # Hits increase


def test_cache_clearing():
    # Clear all caches initially
    scireadability._cache_clear()

    # 1. Populate the cache for a specific function
    scireadability.avg_sentence_length(short_test)
    info_before = scireadability.avg_sentence_length.cache_info()
    assert info_before.misses == 1

    # 2. Call again to confirm a cache hit
    scireadability.avg_sentence_length(short_test)
    info_hit = scireadability.avg_sentence_length.cache_info()
    assert info_hit.hits >= 1

    # 3. Use the global clear function
    scireadability._cache_clear()

    # 4. Verify the cache for that specific function is now empty
    info_after = scireadability.avg_sentence_length.cache_info()
    assert info_after.currsize == 0
    assert info_after.hits == 0
    assert info_after.misses == 0


def test_unicode_support():
    scireadability.text_standard(
        "\u3042\u308a\u304c\u3068\u3046\u3054\u3056\u3044\u307e\u3059"
    )
    scireadability.text_standard("ありがとうございます")


def test_spache_readability():
    spache = scireadability.spache_readability(easy_text, float_output=False)
    assert spache == 3
    score = scireadability.spache_readability(empty_str)
    assert score == 0.0


def test_mcalpine_eflaw():
    # 1. Test default unrounded behavior for accuracy
    scireadability.set_rounding(False)
    score = scireadability.mcalpine_eflaw(long_test)
    assert score == 30.764705882352942

    # 2. Test per-call rounding override
    score_rounded = scireadability.mcalpine_eflaw(long_test, rounding=True, points=1)
    assert score_rounded == 30.8


def test_miniword_count():
    count = scireadability.miniword_count(long_test)
    assert count == 151


def test_empty_string_handling():
    """Test that all metrics handle empty strings consistently."""
    metrics = [
        "flesch_reading_ease",
        "flesch_kincaid_grade",
        "gunning_fog",
        "coleman_liau_index",
        "dale_chall_readability_score",
        "automated_readability_index",
        "smog_index",
        "lix",
        "rix",
        "spache_readability",
        "mcalpine_eflaw",
    ]

    # Check each metric handles empty strings properly
    for metric_name in metrics:
        metric_func = getattr(scireadability, metric_name)
        result = metric_func(empty_str)
        assert result == 0.0, f"Metric {metric_name} failed on empty string"

    # Test special cases
    assert scireadability.linsear_write_formula(empty_str) == -1.0
    assert scireadability.text_standard(empty_str) == "0th grade"


# --- Dictionary Util Tests ---
def test_load_custom_syllable_dict_user_dict_exists_valid_json(test_env):
    test_config_dir, _ = test_env
    user_dict_content = {"CUSTOM_SYLLABLE_DICT": {"testword": 3}}
    user_dict_path = dictionary_utils._get_user_dict_path()
    os.makedirs(os.path.dirname(user_dict_path), exist_ok=True)
    with open(user_dict_path, "w", encoding="utf-8") as f:
        json.dump(user_dict_content, f)

    loaded_dict = dictionary_utils.load_custom_syllable_dict()
    assert loaded_dict == user_dict_content["CUSTOM_SYLLABLE_DICT"]


def test_load_custom_syllable_dict_user_dict_not_exists_default_exists_valid(test_env):
    _, test_resources_dir = test_env
    default_dict_content = {"CUSTOM_SYLLABLE_DICT": {"defaultword": 2}}
    default_dict_path = dictionary_utils._get_default_dict_path()
    with open(
        os.path.join(test_resources_dir, default_dict_path), "w", encoding="utf-8"
    ) as f:
        json.dump(default_dict_content, f)

    loaded_dict = dictionary_utils.load_custom_syllable_dict()
    assert loaded_dict == default_dict_content["CUSTOM_SYLLABLE_DICT"]


def test_load_custom_syllable_dict_user_dict_not_exists_default_not_exists(test_env):
    loaded_dict = dictionary_utils.load_custom_syllable_dict()
    assert loaded_dict == {}


def test_load_custom_syllable_dict_user_dict_not_exists_default_exists_invalid_json(
    test_env,
):
    _, test_resources_dir = test_env
    default_dict_path = dictionary_utils._get_default_dict_path()
    with open(
        os.path.join(test_resources_dir, default_dict_path), "w", encoding="utf-8"
    ) as f:
        f.write("invalid json")

    loaded_dict = dictionary_utils.load_custom_syllable_dict()
    assert loaded_dict == {}


def test_overwrite_custom_dict_valid_json_file(test_env):
    test_config_dir, _ = test_env
    new_dict_content = {"CUSTOM_SYLLABLE_DICT": {"newword": 4, "anotherword": 5}}
    test_json_file = os.path.join(test_config_dir, "test_dict.json")
    with open(test_json_file, "w", encoding="utf-8") as f:
        json.dump(new_dict_content, f)

    dictionary_utils.overwrite_custom_dict(test_json_file)
    loaded_dict = dictionary_utils.load_custom_syllable_dict()

    assert loaded_dict == new_dict_content["CUSTOM_SYLLABLE_DICT"]
