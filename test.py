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
    default_dict_en_dir = os.path.join(test_resources_dir, "resources", "en") # Path to en default dict dir
    os.makedirs(default_dict_en_dir, exist_ok=True) # Create it

    original_user_config_dir = dictionary_utils.user_config_dir
    original_resource_string = dictionary_utils.pkg_resources.resource_string
    dictionary_utils.user_config_dir = lambda package_name: test_config_dir
    dictionary_utils.pkg_resources.resource_string = lambda package_name, resource_path: _mock_resource_string(test_resources_dir, resource_path)

    yield test_config_dir, test_resources_dir

    # --- Teardown ---
    dictionary_utils.user_config_dir = original_user_config_dir
    dictionary_utils.pkg_resources.resource_string = original_resource_string
    if os.path.exists(test_config_dir):
        shutil.rmtree(test_config_dir)
    if os.path.exists(test_resources_dir):
        shutil.rmtree(test_resources_dir)


def _mock_resource_string(test_resources_dir, resource_path):
    """Mock for pkg_resources.resource_string to use test resources."""
    full_resource_path = os.path.join(test_resources_dir, resource_path)
    if not os.path.exists(full_resource_path):
        raise FileNotFoundError(f"Resource not found: {full_resource_path}")
    with open(full_resource_path, 'r', encoding='utf-8') as f:
        return f.read().encode('utf-8')


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
    "\"shut-off the T.V. and do something more "
    "stimulating\" weeks. They have enriched my life and "
    "made it more interesting. Sadly, many adults "
    "forget that games even exist and have put them "
    "away in the cupboards, forgotten until the "
    "grandchildren come over.\n"
    "All too often, adults get so caught up in working "
    "to pay the bills and keeping up with the "
    "\"Joneses'\" that they neglect to harness the fun "
    "in life; the fun that can be the reward of "
    "enjoying a relaxing game with another person. It "
    "has been said that \"man is that he might have "
    "joy\" but all too often we skate through life "
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
    count_spaces = scireadability.char_count(
        long_test, ignore_spaces=False
    )

    assert count == 1748
    assert count_spaces == 2123


def test_letter_count():
    count = scireadability.letter_count(long_test)
    count_spaces = scireadability.letter_count(
        long_test, ignore_spaces=False
    )

    assert count == 1686
    assert count_spaces == 2063


def test_remove_punctuation_incl_apostrophe():
    scireadability.set_rm_apostrophe(True)
    text = scireadability.remove_punctuation(punct_text)

    # set the __rm_apostrophe attribute back to the default
    scireadability.set_rm_apostrophe(False)

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
        ("every", 3, 0),
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
    ]
)
def test_syllable_count(text: str, n_syllables: int, margin: int):
    count = scireadability.syllable_count(text)
    diff = abs(count - n_syllables)

    assert diff <= margin


def test_sentence_count():
    count = scireadability.sentence_count(long_test)

    assert count == 17


def test_avg_sentence_length():
    avg = scireadability.avg_sentence_length(long_test)

    assert avg == 21.88235294117647


def test_avg_syllables_per_word():
    avg = scireadability.avg_syllables_per_word(long_test)

    assert avg == 1.4758064516129032


def test_avg_letter_per_word():
    avg = scireadability.avg_letter_per_word(long_test)

    assert avg == 4.532258064516129


def test_avg_sentence_per_word():
    avg = scireadability.avg_sentence_per_word(long_test)

    assert avg == 0.0456989247311828


def test_flesch_reading_ease():
    score = scireadability.flesch_reading_ease(long_test)

    assert score == 59.77118595825428


def test_flesch_kincaid_grade():
    score = scireadability.flesch_kincaid_grade(long_test)

    assert score == 10.358633776091082


def test_polysyllabcount():
    count = scireadability.polysyllabcount(long_test)

    assert count == 38


def test_smog_index():
    index = scireadability.smog_index(long_test)

    assert index == 11.670169846198839


def test_coleman_liau_index():
    index = scireadability.coleman_liau_index(long_test)

    assert index == 9.13440860215054


def test_automated_readability_index():
    index = scireadability.automated_readability_index(long_test)

    assert index == 11.643111954459208


def test_linsear_write_formula():
    result = scireadability.linsear_write_formula(long_test)

    assert result == 15.25

    result = scireadability.linsear_write_formula(empty_str)

    assert result == -1.0


def test_difficult_words():
    result = scireadability.difficult_words(long_test)

    assert result == 54


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
    score = scireadability.dale_chall_readability_score(long_test)

    assert score == 7.7779937381404185

    score = scireadability.dale_chall_readability_score(empty_str)

    assert score == 0.0


def test_gunning_fog():
    score = scireadability.gunning_fog(long_test)

    assert score == 11.118532574320051


def test_lix():
    score = scireadability.lix(long_test)

    assert score == 43.69086357947434

    result = scireadability.lix(empty_str)

    assert result == 0.0


def test_rix():
    score = scireadability.rix(long_test)

    assert score == 4.588235294117647


def test_text_standard():
    standard = scireadability.text_standard(long_test)

    assert standard == "10th and 11th grade"

    standard = scireadability.text_standard(short_test)

    assert standard == "1st and 2nd grade"


def test_reading_time():
    score = scireadability.reading_time(long_test)

    assert score == 25.67812


def test_lru_caching():
    # Clear any cache
    scireadability.sentence_count.cache_clear()
    scireadability.avg_sentence_length.cache_clear()

    # Make a call that uses `sentence_count`
    scireadability.avg_sentence_length(long_test)

    # Test that `sentence_count` was called
    assert scireadability.sentence_count.cache_info().misses == 1

    # Call `avg_sentence_length` again, but clear it's cache first
    scireadability.avg_sentence_length.cache_clear()
    scireadability.avg_sentence_length(long_test)

    # Test that `sentence_count` wasn't called again
    assert scireadability.sentence_count.cache_info().hits == 1


def test_cache_clearing():
    # Instead of calling _cache_clear directly, clear specific caches we need to test
    scireadability.flesch_reading_ease_core.cache_clear()

    # Make a call to populate cache
    scireadability.flesch_reading_ease(short_test)

    # Check the cache has only been missed once
    assert scireadability.flesch_reading_ease_core.cache_info().misses == 1

    # Verify cache is used on second call
    scireadability.flesch_reading_ease(short_test)
    assert scireadability.flesch_reading_ease_core.cache_info().hits >= 1


def test_unicode_support():
    scireadability.text_standard(
        "\u3042\u308a\u304c\u3068\u3046\u3054\u3056\u3044\u307e\u3059")

    scireadability.text_standard("ありがとうございます")


def test_spache_readability():
    spache = scireadability.spache_readability(easy_text, False)

    assert spache == 2

    score = scireadability.spache_readability(empty_str)

    assert score == 0.0


def test_dale_chall_readability_score_v2():
    score = scireadability.dale_chall_readability_score_v2(long_test)

    assert score == 7.013961480075902


def test_mcalpine_eflaw():
    score = scireadability.mcalpine_eflaw(long_test)

    assert score == 30.8


def test_miniword_count():
    count = scireadability.miniword_count(long_test)

    assert count == 151


# --- Tests for load_custom_syllable_dict ---
def test_load_custom_syllable_dict_user_dict_exists_valid_json(test_env):
    test_config_dir, _ = test_env
    user_dict_content = {"CUSTOM_SYLLABLE_DICT": {"testword": 3}}
    user_dict_path = dictionary_utils._get_user_dict_path()
    os.makedirs(os.path.dirname(user_dict_path), exist_ok=True)
    with open(user_dict_path, 'w', encoding='utf-8') as f:
        json.dump(user_dict_content, f)

    loaded_dict = dictionary_utils.load_custom_syllable_dict()
    assert loaded_dict == user_dict_content["CUSTOM_SYLLABLE_DICT"]


def test_load_custom_syllable_dict_user_dict_not_exists_default_exists_valid(test_env):
    _, test_resources_dir = test_env
    default_dict_content = {"CUSTOM_SYLLABLE_DICT": {"defaultword": 2}}
    default_dict_path = dictionary_utils._get_default_dict_path()
    with open(os.path.join(test_resources_dir, default_dict_path), 'w', encoding='utf-8') as f:
        json.dump(default_dict_content, f)

    loaded_dict = dictionary_utils.load_custom_syllable_dict()
    assert loaded_dict == default_dict_content["CUSTOM_SYLLABLE_DICT"]


def test_load_custom_syllable_dict_user_dict_not_exists_default_not_exists(test_env):
    loaded_dict = dictionary_utils.load_custom_syllable_dict()
    assert loaded_dict == {}


def test_load_custom_syllable_dict_user_dict_not_exists_default_exists_invalid_json(test_env):
    _, test_resources_dir = test_env
    default_dict_path = dictionary_utils._get_default_dict_path()
    # No need to create dirs here, fixture does it now
    with open(os.path.join(test_resources_dir, default_dict_path), 'w', encoding='utf-8') as f:
        f.write("invalid json")

    loaded_dict = dictionary_utils.load_custom_syllable_dict()
    assert loaded_dict == {}


# --- Tests for overwrite_custom_dict ---
def test_overwrite_custom_dict_valid_json_file(test_env):
    test_config_dir, _ = test_env
    new_dict_content = {"CUSTOM_SYLLABLE_DICT": {"newword": 4, "anotherword": 5}}
    test_json_file = os.path.join(test_config_dir, "test_dict.json")
    with open(test_json_file, 'w', encoding='utf-8') as f:
        json.dump(new_dict_content, f)

    dictionary_utils.overwrite_custom_dict(test_json_file)
    loaded_dict = dictionary_utils.load_custom_syllable_dict()

    assert loaded_dict == new_dict_content["CUSTOM_SYLLABLE_DICT"]


def test_overwrite_custom_dict_file_not_found(test_env):
    test_config_dir, _ = test_env
    non_existent_file = os.path.join(test_config_dir, "nonexistent.json")
    with pytest.raises(FileNotFoundError):
        dictionary_utils.overwrite_custom_dict(non_existent_file)


def test_overwrite_custom_dict_invalid_json_file(test_env):
    test_config_dir, _ = test_env
    invalid_json_file = os.path.join(test_config_dir, "invalid.json")
    with open(invalid_json_file, 'w', encoding='utf-8') as f:
        f.write("invalid json")

    with pytest.raises(json.JSONDecodeError):
        dictionary_utils.overwrite_custom_dict(invalid_json_file)


def test_overwrite_custom_dict_invalid_dict_format(test_env):
    test_config_dir, _ = test_env
    invalid_format_file = os.path.join(test_config_dir, "badformat.json")
    bad_format_content = {"WRONG_KEY": {"word": 1}}
    with open(invalid_format_file, 'w', encoding='utf-8') as f:
        json.dump(bad_format_content, f)

    with pytest.raises(ValueError):
        dictionary_utils.overwrite_custom_dict(invalid_format_file)


# --- Tests for add_term_to_custom_dict ---
def test_add_term_to_custom_dict_valid_term(test_env):
    test_config_dir, _ = test_env
    word_to_add = "testterm"
    syllable_count = 4

    dictionary_utils.add_term_to_custom_dict(word_to_add, syllable_count)
    loaded_dict = dictionary_utils.load_custom_syllable_dict()

    assert word_to_add in loaded_dict
    assert loaded_dict[word_to_add] == syllable_count


def test_add_term_to_custom_dict_invalid_syllable_count_zero(test_env):
    with pytest.raises(ValueError):
        dictionary_utils.add_term_to_custom_dict("word", 0)


def test_add_term_to_custom_dict_invalid_syllable_count_negative(test_env):
    with pytest.raises(ValueError):
        dictionary_utils.add_term_to_custom_dict("word", -1)


def test_add_term_to_custom_dict_invalid_syllable_count_not_int(test_env):
    with pytest.raises(ValueError):
        dictionary_utils.add_term_to_custom_dict("word", "not_an_int")


# --- Tests for add_terms_from_file ---
def test_add_terms_from_file_valid_json_file(test_env):
    test_config_dir, _ = test_env
    new_terms_content = {"CUSTOM_SYLLABLE_DICT": {"fileword1": 2, "fileword2": 3}}
    test_json_file = os.path.join(test_config_dir, "terms.json")
    with open(test_json_file, 'w', encoding='utf-8') as f:
        json.dump(new_terms_content, f)

    dictionary_utils.add_terms_from_file(test_json_file)
    loaded_dict = dictionary_utils.load_custom_syllable_dict()

    for word, count in new_terms_content["CUSTOM_SYLLABLE_DICT"].items():
        assert word in loaded_dict
        assert loaded_dict[word] == count


def test_add_terms_from_file_file_not_found(test_env):
    test_config_dir, _ = test_env
    non_existent_file = os.path.join(test_config_dir, "nonexistent_terms.json")
    with pytest.raises(FileNotFoundError):
        dictionary_utils.add_terms_from_file(non_existent_file)


def test_add_terms_from_file_invalid_json_file(test_env):
    test_config_dir, _ = test_env
    invalid_json_file = os.path.join(test_config_dir, "invalid_terms.json")
    with open(invalid_json_file, 'w', encoding='utf-8') as f:
        f.write("invalid json")

    with pytest.raises(json.JSONDecodeError):
        dictionary_utils.add_terms_from_file(invalid_json_file)


def test_add_terms_from_file_invalid_dict_format(test_env):
    test_config_dir, _ = test_env
    invalid_format_file = os.path.join(test_config_dir, "badformat_terms.json")
    bad_format_content = {"WRONG_KEY": {"word": 1}}
    with open(invalid_format_file, 'w', encoding='utf-8') as f:
        json.dump(bad_format_content, f)

    with pytest.raises(ValueError):
        dictionary_utils.add_terms_from_file(invalid_format_file)


# --- Tests for revert_custom_dict_to_default ---
def test_revert_custom_dict_to_default_user_dict_exists(test_env):
    test_config_dir, test_resources_dir = test_env
    user_dict_path = dictionary_utils._get_user_dict_path()
    os.makedirs(os.path.dirname(user_dict_path), exist_ok=True)
    with open(user_dict_path, 'w', encoding='utf-8') as f:
        json.dump({"CUSTOM_SYLLABLE_DICT": {"userword": 100}}, f)

    default_dict_content = {"CUSTOM_SYLLABLE_DICT": {"defaultword": 2}}
    default_dict_path = dictionary_utils._get_default_dict_path()
    # No need to create dirs here, fixture does it now
    with open(os.path.join(test_resources_dir, default_dict_path), 'w', encoding='utf-8') as f:
        json.dump(default_dict_content, f)

    dictionary_utils.revert_custom_dict_to_default()
    loaded_dict = dictionary_utils.load_custom_syllable_dict()

    assert loaded_dict == default_dict_content["CUSTOM_SYLLABLE_DICT"]


def test_revert_custom_dict_to_default_default_dict_not_found(test_env):
    _, test_resources_dir = test_env
    default_dict_path = dictionary_utils._get_default_dict_path()
    default_dict_file = os.path.join(test_resources_dir, default_dict_path)
    if os.path.exists(default_dict_file):
        os.remove(default_dict_file)
    os.makedirs(os.path.dirname(default_dict_file), exist_ok=True) # Ensure en dir exists

    with pytest.raises(FileNotFoundError):
        dictionary_utils.revert_custom_dict_to_default()


def test_revert_custom_dict_to_default_invalid_json_in_default(test_env):
    _, test_resources_dir = test_env
    default_dict_path = dictionary_utils._get_default_dict_path()
    # No need to create dirs here, fixture does it now
    with open(os.path.join(test_resources_dir, default_dict_path), 'w', encoding='utf-8') as f:
        f.write("invalid json")

    with pytest.raises(json.JSONDecodeError):
        dictionary_utils.revert_custom_dict_to_default()


def test_load_custom_syllable_dict_case_sensitivity(test_env):
    _, test_resources_dir = test_env
    default_dict_content = {"CUSTOM_SYLLABLE_DICT": {"TestWord": 2}} # Mixed case in default
    default_dict_path = dictionary_utils._get_default_dict_path()
    with open(os.path.join(test_resources_dir, default_dict_path), 'w', encoding='utf-8') as f:
        json.dump(default_dict_content, f)

    loaded_dict = dictionary_utils.load_custom_syllable_dict()
    assert "testword" in loaded_dict # Assert lowercase lookup works (case-insensitive loading is assumed)
    assert loaded_dict["testword"] == 2 # Check correct count


def test_load_custom_syllable_dict_empty_default_dict_file(test_env):
    _, test_resources_dir = test_env
    default_dict_path = dictionary_utils._get_default_dict_path()
    with open(os.path.join(test_resources_dir, default_dict_path), 'w', encoding='utf-8') as f:
        json.dump({}, f) # Empty JSON as default

    loaded_dict = dictionary_utils.load_custom_syllable_dict()
    assert loaded_dict == {} # Should load as empty dict


# --- Additional Tests for overwrite_custom_dict ---
def test_overwrite_custom_dict_large_json_file(test_env):
    test_config_dir, _ = test_env
    large_dict_content = {"CUSTOM_SYLLABLE_DICT": {f"word_{i}": i % 5 + 1 for i in range(1000)}}
    test_json_file = os.path.join(test_config_dir, "large_dict.json")
    with open(test_json_file, 'w', encoding='utf-8') as f:
        json.dump(large_dict_content, f)

    dictionary_utils.overwrite_custom_dict(test_json_file)
    loaded_dict = dictionary_utils.load_custom_syllable_dict()
    assert loaded_dict == large_dict_content["CUSTOM_SYLLABLE_DICT"] # Verify content


def test_overwrite_custom_dict_verify_file_content(test_env):
    test_config_dir, _ = test_env
    new_dict_content = {"CUSTOM_SYLLABLE_DICT": {"filecheckword": 3}}
    test_json_file = os.path.join(test_config_dir, "temp_dict.json")
    with open(test_json_file, 'w', encoding='utf-8') as f:
        json.dump(new_dict_content, f)

    dictionary_utils.overwrite_custom_dict(test_json_file)
    user_dict_path = dictionary_utils._get_user_dict_path()
    with open(user_dict_path, 'r', encoding='utf-8') as f:
        file_dict_content = json.load(f)
    assert file_dict_content == new_dict_content # Verify file content directly


# --- Additional Tests for add_term_to_custom_dict ---
def test_add_term_to_custom_dict_existing_term_same_count(test_env):
    test_config_dir, _ = test_env
    word_to_add = "existingword"
    syllable_count = 2
    user_dict_path = dictionary_utils._get_user_dict_path()
    os.makedirs(os.path.dirname(user_dict_path), exist_ok=True)
    with open(user_dict_path, 'w', encoding='utf-8') as f:
        json.dump({"CUSTOM_SYLLABLE_DICT": {word_to_add: syllable_count}}, f) # Dict exists with word

    dictionary_utils.add_term_to_custom_dict(word_to_add, syllable_count) # Add again with same count
    loaded_dict = dictionary_utils.load_custom_syllable_dict()
    assert loaded_dict[word_to_add] == syllable_count # Count should remain the same


def test_add_term_to_custom_dict_existing_term_different_count(test_env):
    test_config_dir, _ = test_env
    word_to_add = "existingword"
    initial_syllable_count = 2
    new_syllable_count = 3
    user_dict_path = dictionary_utils._get_user_dict_path()
    os.makedirs(os.path.dirname(user_dict_path), exist_ok=True)
    with open(user_dict_path, 'w', encoding='utf-8') as f:
        json.dump({"CUSTOM_SYLLABLE_DICT": {word_to_add: initial_syllable_count}}, f) # Dict exists with word

    dictionary_utils.add_term_to_custom_dict(word_to_add, new_syllable_count) # Add again with different count
    loaded_dict = dictionary_utils.load_custom_syllable_dict()
    assert loaded_dict[word_to_add] == new_syllable_count # Count should be updated/overwritten


# --- Additional Tests for add_terms_from_file ---
def test_add_terms_from_file_empty_custom_syllable_dict_key(test_env):
    test_config_dir, _ = test_env
    empty_dict_file_content = {"CUSTOM_SYLLABLE_DICT": {}} # Empty dict for the key
    test_json_file = os.path.join(test_config_dir, "empty_dict_terms.json")
    with open(test_json_file, 'w', encoding='utf-8') as f:
        json.dump(empty_dict_file_content, f)

    dictionary_utils.add_terms_from_file(test_json_file)
    loaded_dict = dictionary_utils.load_custom_syllable_dict()
    assert loaded_dict == {} # Should remain or become empty


def test_add_terms_from_file_non_dict_value_for_custom_syllable_dict(test_env):
    test_config_dir, _ = test_env
    non_dict_file_content = {"CUSTOM_SYLLABLE_DICT": ["not", "a", "dict"]} # List instead of dict
    test_json_file = os.path.join(test_config_dir, "non_dict_terms.json")
    with open(test_json_file, 'w', encoding='utf-8') as f:
        json.dump(non_dict_file_content, f)

    with pytest.raises(ValueError):
        dictionary_utils.add_terms_from_file(test_json_file)


# --- Additional Tests for revert_custom_dict_to_default ---
def test_revert_custom_dict_to_default_no_user_dict_exists(test_env):
    test_config_dir, test_resources_dir = test_env
    user_dict_path = dictionary_utils._get_user_dict_path()
    if os.path.exists(user_dict_path): # Ensure no user dict exists before test
        os.remove(user_dict_path)
    user_dict_dir = os.path.dirname(user_dict_path)
    if os.path.exists(user_dict_dir) and not os.listdir(user_dict_dir):
        os.rmdir(user_dict_dir) # Remove user dir if empty

    default_dict_content = {"CUSTOM_SYLLABLE_DICT": {"defaultword": 2}}
    default_dict_path = dictionary_utils._get_default_dict_path()
    with open(os.path.join(test_resources_dir, default_dict_path), 'w', encoding='utf-8') as f:
        json.dump(default_dict_content, f)

    dictionary_utils.revert_custom_dict_to_default()
    loaded_dict = dictionary_utils.load_custom_syllable_dict()
    assert loaded_dict == default_dict_content["CUSTOM_SYLLABLE_DICT"] # Should create user dict from default


def test_revert_custom_dict_to_default_empty_default_dict(test_env):
    _, test_resources_dir = test_env
    default_dict_path = dictionary_utils._get_default_dict_path()
    with open(os.path.join(test_resources_dir, default_dict_path), 'w', encoding='utf-8') as f:
        json.dump({}, f) # Empty default dictionary

    dictionary_utils.revert_custom_dict_to_default()
    loaded_dict = dictionary_utils.load_custom_syllable_dict()
    assert loaded_dict == {} # Should revert to empty dict


def test_verbose_output_structure():
    """Test that verbose output has the expected structure."""
    result = scireadability.flesch_kincaid_grade(long_test, verbose=True)

    # Check basic structure
    assert isinstance(result, dict)
    assert "score" in result
    assert "metric" in result
    assert "complex_sentences" in result
    assert "improvement_summary" in result

    # Check types
    assert isinstance(result["score"], float)
    assert isinstance(result["metric"], str)
    assert isinstance(result["complex_sentences"], list)
    assert isinstance(result["improvement_summary"], dict)

    # Check metric name matches
    assert result["metric"] == "flesch_kincaid_grade"

    # Check score matches non-verbose output
    non_verbose_score = scireadability.flesch_kincaid_grade(long_test)
    assert result["score"] == non_verbose_score


def test_verbose_empty_string():
    """Test that verbose mode handles empty strings correctly."""
    result = scireadability.flesch_kincaid_grade("", verbose=True)

    assert result["score"] == 0.0
    assert len(result["complex_sentences"]) == 0
    assert result["improvement_summary"]["total_complex_sentences"] == 0


def test_verbose_complex_sentences():
    """Test that complex sentences are identified and analyzed correctly."""
    result = scireadability.flesch_kincaid_grade(long_test, verbose=True)

    # Check complex sentences list
    assert len(result["complex_sentences"]) > 0

    # Check first complex sentence has expected data
    first_sentence = result["complex_sentences"][0]
    assert "text" in first_sentence
    assert "length" in first_sentence
    assert "avg_syllables" in first_sentence
    assert isinstance(first_sentence["text"], str)
    assert isinstance(first_sentence["length"], int)
    assert isinstance(first_sentence["avg_syllables"], float)

    # Verify text is actually from the original text
    assert first_sentence["text"] in long_test


def test_verbose_config():
    """Test that verbose_config parameters work correctly."""
    # Test with default config
    default_result = scireadability.flesch_kincaid_grade(long_test, verbose=True)

    # Test with custom top_n
    custom_config = {"top_n": 3}
    custom_result = scireadability.flesch_kincaid_grade(long_test, verbose=True,
                                                        verbose_config=custom_config)

    assert len(custom_result["complex_sentences"]) == 3
    assert len(default_result["complex_sentences"]) > 3

    # Test with word analysis disabled
    no_word_config = {"include_word_analysis": False}
    no_word_result = scireadability.flesch_kincaid_grade(long_test, verbose=True,
                                                         verbose_config=no_word_config)

    # "difficult_word_list" should be empty or very short
    if "difficult_word_list" in no_word_result["complex_sentences"][0]:
        assert len(no_word_result["complex_sentences"][0]["difficult_word_list"]) == 0


def test_verbose_suggestions():
    """Test that improvement suggestions are generated."""
    result = scireadability.flesch_kincaid_grade(long_test, verbose=True)

    # Check that at least some sentences have suggestions
    has_suggestions = False
    for sentence in result["complex_sentences"]:
        if "suggestions" in sentence and len(sentence["suggestions"]) > 0:
            has_suggestions = True
            break

    assert has_suggestions, "No improvement suggestions were generated"

    # Test with suggestions disabled
    no_suggestions = {"include_suggestions": False}
    no_sugg_result = scireadability.flesch_kincaid_grade(long_test, verbose=True,
                                                         verbose_config=no_suggestions)

    has_suggestions = False
    for sentence in no_sugg_result["complex_sentences"]:
        if "suggestions" in sentence and len(sentence["suggestions"]) > 0:
            has_suggestions = True
            break

    assert not has_suggestions, "Suggestions found even though they were disabled"


def test_various_metrics_verbose():
    """Test that verbose mode works with different readability metrics."""
    # Test a few different metrics with verbose mode
    metrics = [
        "flesch_reading_ease",
        "gunning_fog",
        "coleman_liau_index",
        "dale_chall_readability_score",
        "smog_index"
    ]

    for metric in metrics:
        method = getattr(scireadability, metric)
        result = method(long_test, verbose=True)

        assert isinstance(result, dict)
        assert result["metric"] == metric
        assert "complex_sentences" in result
        assert len(result["complex_sentences"]) > 0


def test_text_standard_verbose():
    """Test that text_standard verbose mode provides comprehensive analysis."""
    result = scireadability.text_standard(long_test, verbose=True)

    assert isinstance(result, dict)
    assert "consensus_score" in result
    assert "individual_scores" in result
    assert "complex_sentences" in result

    # Check individual scores include multiple metrics
    assert len(result["individual_scores"]) > 3

    # Check that flagged_by exists in complex sentences
    first_sentence = result["complex_sentences"][0]
    assert "flagged_by" in first_sentence
    assert isinstance(first_sentence["flagged_by"], list)
    assert len(first_sentence["flagged_by"]) > 0


def test_verbose_score_consistency():
    """
    Test that scores returned in verbose mode match exactly the scores
    returned in non-verbose mode across all metrics and various text samples.
    """
    # Test multiple readability metrics
    metrics = [
        "flesch_reading_ease",
        "flesch_kincaid_grade",
        "gunning_fog",
        "coleman_liau_index",
        "dale_chall_readability_score",
        "automated_readability_index",
        "smog_index",
        # Skip linsear_write_formula for empty strings as it has special behavior
    ]

    # Test with various text samples including edge cases
    test_texts = [
        long_test,  # Normal long text
        short_test,  # Short text
        #"",  # Empty string - skip this as it has special handling
        "Single.",  # Single word
        punct_text,  # Text with lots of punctuation
        easy_text,  # Simple text
        "Pneumonoultramicroscopicsilicovolcanoconiosis is a long word."  # Complex word
    ]

    # Test each metric with each text
    for metric in metrics:
        method = getattr(scireadability, metric)

        for text in test_texts:
            # Get scores in both modes
            regular_score = method(text)
            verbose_result = method(text, verbose=True)

            # Scores should match exactly
            assert verbose_result["score"] == regular_score, \
                f"Score mismatch for {metric} with text: {text[:30]}..."

            # Also check with different verbose_config values
            configs = [
                {"top_n": 3},
                {"include_word_analysis": False},
                {"include_suggestions": False},
                {"top_n": 5, "include_word_analysis": False, "include_suggestions": False}
            ]

            for config in configs:
                config_result = method(text, verbose=True, verbose_config=config)
                assert config_result["score"] == regular_score, \
                    f"Score mismatch with config {config} for {metric} with text: {text[:30]}..."


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
        "dale_chall_readability_score_v2",
        "mcalpine_eflaw"
    ]

    # Check each metric handles empty strings properly
    for metric_name in metrics:
        metric = getattr(scireadability, metric_name)
        result = metric(empty_str)
        assert result == 0.0, f"Metric {metric_name} didn't return 0.0 for empty string"

    # Test special cases
    assert scireadability.linsear_write_formula(empty_str) == -1.0
    assert scireadability.text_standard(empty_str) == "0th grade"
