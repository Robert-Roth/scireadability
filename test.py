#!/usr/bin/python
# -*- coding:utf-8 -*-

"""Test suite for scireadability"""

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

long_spanish_text = (
    "Muchos años después, frente al pelotón de fusilamiento, "
    "el coronel Aureliano Buendía había de recordar aquella "
    "tarde remota en que su padre lo llevó a conocer el hielo. "
    "Macondo era entonces una aldea de veinte casas de barro y "
    "cañabrava construidas a la orilla de un río de aguas "
    "diáfanas que se precipitaban por un lecho de piedras pulidas, "
    "blancas y enormes como huevos prehistóricos. El mundo era tan "
    "reciente, que muchas cosas carecían de nombre, y para mencionarlas "
    "había que señalarlas con el dedo. Todos los años, por el mes de marzo, "
    "una familia de gitanos desarrapados plantaba su carpa cerca "
    "de la aldea, y con un grande alboroto de pitos y timbales daban a "
    "conocer los nuevos inventos. Primero llevaron el imán. "
    "Un gitano corpulento, de barba montaraz y manos de gorrión, que se "
    "presentó con el nombre de Melquíades, hizo una truculenta demostración "
    "pública de lo que él mismo llamaba la octava maravilla de "
    "los sabios alquimistas de Macedonia."
)

easy_spanish_text = "Hoy es un lindo día"

long_russian_text_guillemets = (
    "Игра ... игры всегда считались важными для развития "
    "уравновешенных и творческих детей; однако, какую роль "
    "они должны играть в жизни взрослых, если таковая имеется, "
    "никогда не исследовалась так глубоко. Я считаю, "
    "что игры для взрослых не менее важны, чем для детей. "
    "Выделение времени для игр с нашими детьми и другими "
    "взрослыми не только ценно для построения межличностных "
    "отношений, но также является прекрасным способом снять "
    "накопившееся напряжение.\n"
    "Ничто не доставляет такого же удовольствие для моего мужа "
    "после тяжелого рабочего дня, как прийти домой и поиграть "
    "с кем-нибудь в шахматы. Это позволяет ему расслабиться от "
    "повседневных дел и обсудить плюсы и минусы дня в спокойной "
    "обстановке. Один из самых запоминающихся свадебных "
    "подарков - набор нардов - получил близкий друг. Я спросила "
    "его, зачем он сделал нам такой подарок. Он ответил, что "
    "считает важным аспектом брака никогда не прекращать "
    "совместные игры. По прошествии лет, когда я "
    "начала покупать и проходить с другими парами и коллегами "
    "многие игры, такие как: Monopoly, Chutes & Ladders, "
    "Mastermind, Dweebs, Geeks, & Weirdos и т.д. Я сознаю их "
    "неотъемлемую роль, которую они сыграли в наши выходные и "
    "в наши недели аля «выключите телевизор и займитесь "
    "чем-нибудь более стимулирующим». Они обогатили мою "
    "жизнь и сделали ее интереснее. К сожалению, многие "
    "взрослые забывают, что игры вообще существуют, а "
    "прячут их в шкафы, о которых забывают, пока не придут "
    "внуки.\n"
    "Слишком часто взрослые настолько увлечены работой, чтобы "
    "платить по счетам и не отставать от «Джонсов», что "
    "пренебрегают радостью жизни; удовольствием, которое может "
    "быть наградой за расслабляющую игру с другим человеком. "
    "Было сказано, что «человек - это для того, чтобы иметь "
    "радость», но слишком часто мы идем по жизни без особой "
    "радости. Игры позволяют нам расслабиться, узнать что-то "
    "новое и интересное, взаимодействовать с людьми на другом, "
    "более комфортном уровне и наслаждаться безопасным "
    "соревнованием. По этим причинам взрослые должны уделять "
    "больше внимания играм в своей жизни"
)

italian_text = (
    "Roma è un comune italiano, capitale della Repubblica Italiana, "
    "nonché capoluogo dell'omonima città metropolitana e della regione Lazio."
)

difficult_word = "Regardless"
easy_word = "Dog"

empty_str = ""

easy_arabic_text = "ذهب هند وأحمد الى المدرسة. هند تحب الرسم والمطالعة"
hard_arabic_text = (
    "\u062a\u062a\u0631\u0643\u0632 \u0623\u0633\u0633 \
    \u0627\u0644\u0641\u064a\u0632\u064a\u0627\u0621 \
    \u0627\u0644\u0646\u0648\u0648\u064a\u0629 \u0628\u0634\u0643\u0644 \
    \u0639\u0627\u0645 \u0639\u0644\u064a \u0627\u0644\u0630\u0631\u0629 \
    \u0648\u0645\u0643\u0648\u0646\u0627\u062a\u0647\u0627 \
    \u0627\u0644\u062f\u0627\u062e\u0644\u064a\u0629 \
    \u0648\u0627\u0644\u062a\u0639\u0627\u0645\u0644 \
    \u0645\u0639 \u062a\u0644\u0643 \u0627\u0644\u0630\u0631\u0629 \
    \u0648\u0627\u0644\u0639\u0646\u0627\u0635\u0631 \
    \u0648\u062d\u064a\u062b \u0627\u0646 \u0647\u0630\u0627 \u0647\u0648 \
    \u0627\u0644\u0645\u0628\u062d\u062b \u0627\u0644\u0639\u0627\u0645 \
    \u0644\u0644\u0641\u064a\u0632\u064a\u0627\u0621 \
    \u0627\u0644\u0646\u0648\u0648\u064a\u0629 \u0641\u0627\u0646\u0647 \
    \u0627\u062d\u064a\u0627\u0646\u0627 \u0645\u0627 \
    \u064a\u0637\u0644\u0642 \u0639\u0644\u064a\u0647\u0627 \
    \u0627\u0644\u0641\u064a\u0632\u064a\u0627\u0621 \
    \u0627\u0644\u0630\u0631\u064a\u0629 \
    \u0627\u0644\u0627 \u0623\u0646 \u0645\u062c\u0627\u0644 \
    \u0627\u0644\u0641\u064a\u0632\u064a\u0627\u0621 \
    \u0627\u0644\u0646\u0648\u0648\u064a\u0629 \
    \u0623\u0639\u0645 \u0648\u0627\u0634\u0645\u0644 \u0645\u0646 \
    \u0627\u0644\u0641\u064a\u0632\u064a\u0627\u0621 \
    \u0627\u0644\u0630\u0631\u064a\u0629 \u0648\u0643\u0630\u0644\u0643 \
    \u0627\u0644\u0641\u064a\u0632\u064a\u0627\u0621 \
    \u0627\u0644\u0630\u0631\u064a\u0629 \u062a\u0647\u062a\u0645 \
    \u0628\u062f\u0627\u0631\u0633\u0629 \
    \u0627\u0644\u0630\u0631\u0629 \u0641\u0649 \
    \u062d\u0627\u0644\u0627\u062a\u0647\u0627 \
    \u0648\u062a\u0641\u0627\u0639\u0644\u0627\u062a\u0647\u0627 \
    \u0627\u0644\u0645\u062e\u062a\u0644\u0641\u0629"
)


def test_char_count():
    scireadability.set_lang("en")
    count = scireadability.char_count(long_test)
    count_spaces = scireadability.char_count(
        long_test, ignore_spaces=False
    )

    assert count == 1748
    assert count_spaces == 2123


def test_letter_count():
    scireadability.set_lang("en")
    count = scireadability.letter_count(long_test)
    count_spaces = scireadability.letter_count(
        long_test, ignore_spaces=False
    )

    assert count == 1686
    assert count_spaces == 2063


def test_remove_punctuation_incl_apostrophe():
    scireadability.set_lang('en')
    scireadability.set_rm_apostrophe(True)
    text = scireadability.remove_punctuation(punct_text)

    # set the __rm_apostrophe attribute back to the default
    scireadability.set_rm_apostrophe(False)

    assert text == punct_text_result_wo_apostr


def test_remove_punctuation_excl_apostrophe():
    scireadability.set_lang('en')
    scireadability.set_rm_apostrophe(False)
    text = scireadability.remove_punctuation(punct_text)

    assert text == punct_text_result_w_apostr


def test_lexicon_count():
    scireadability.set_lang("en")
    count = scireadability.lexicon_count(long_test)
    count_punc = scireadability.lexicon_count(long_test, removepunct=False)

    assert count == 372
    assert count_punc == 376


@pytest.mark.parametrize(
    "lang,text,n_syllables,margin",
    [
        ("en", short_test, 7, 0),
        ("en", punct_text, 74, 2),
        ("en", "faeries", 2, 1),
        ("en", "relived", 2, 0),
        ("en", "couple", 2, 0),
        ("en", "enriched", 2, 0),
        ("en", "us", 1, 0),
        ("en", "too", 1, 0),
        ("en", "monopoly", 4, 0),
        ("en", "him", 1, 0),
        ("en", "he", 1, 0),
        ("en", "without", 2, 0),
        ("en", "creative", 3, 0),
        ("en", "every", 3, 0),
        ("en", "stimulating", 4, 0),
        ("en", "life", 1, 0),
        ("en", "cupboards", 2, 0),
        ("en", "day's", 1, 0),
        ("en", "forgotten", 3, 0),
        ("en", "through", 1, 0),
        ("en", "marriage", 2, 0),
        ("en", "hello", 2, 0),
        ("en", "the", 1, 0),
        ("en", "sentences", 3, 0),
        ("en", "songwriter", 3, 0),
        ("en", "removing", 3, 0),
        ("en", "interpersonal", 5, 0),
    ]
)
def test_syllable_count(lang: str, text: str, n_syllables: int, margin: int):
    scireadability.set_lang(lang)
    count = scireadability.syllable_count(text)
    diff = abs(count - n_syllables)

    assert diff <= margin


def test_sentence_count():
    scireadability.set_lang("en")
    count = scireadability.sentence_count(long_test)

    assert count == 17


def test_sentence_count_russian():
    scireadability.set_lang('ru_RU')
    count = scireadability.sentence_count(long_russian_text_guillemets)

    assert count == 16


def test_avg_sentence_length():
    scireadability.set_lang("en")
    avg = scireadability.avg_sentence_length(long_test)

    assert avg == 21.88235294117647


def test_avg_syllables_per_word():
    scireadability.set_lang("en")
    avg = scireadability.avg_syllables_per_word(long_test)

    assert avg == 1.4758064516129032


def test_avg_letter_per_word():
    scireadability.set_lang("en")
    avg = scireadability.avg_letter_per_word(long_test)

    assert avg == 4.532258064516129


def test_avg_sentence_per_word():
    scireadability.set_lang("en")
    avg = scireadability.avg_sentence_per_word(long_test)

    assert avg == 0.0456989247311828


def test_flesch_reading_ease():
    scireadability.set_lang("en")
    score = scireadability.flesch_reading_ease(long_test)

    assert score == 59.77118595825428

    scireadability.set_lang("de_DE")
    score = scireadability.flesch_reading_ease(long_test)

    assert score == 66.27893738140419

    scireadability.set_lang("es_ES")
    score = scireadability.flesch_reading_ease(long_test)

    assert score == 86.77806451612905

    scireadability.set_lang("fr_FR")
    score = scireadability.flesch_reading_ease(long_test)

    assert score == 82.30339025932953

    scireadability.set_lang("it_IT")
    score = scireadability.flesch_reading_ease(long_test)

    assert score == 91.61745730550285

    scireadability.set_lang("nl_NL")
    score = scireadability.flesch_reading_ease(long_test)

    assert score == 66.01666982922202

    scireadability.set_lang("ru_RU")
    score = scireadability.flesch_reading_ease(long_test)

    assert score == 118.28794117647061


def test_flesch_kincaid_grade():
    scireadability.set_lang("en")
    score = scireadability.flesch_kincaid_grade(long_test)

    assert score == 10.358633776091082


def test_polysyllabcount():
    scireadability.set_lang("en")
    count = scireadability.polysyllabcount(long_test)

    assert count == 38


def test_smog_index():
    scireadability.set_lang("en")
    index = scireadability.smog_index(long_test)

    assert index == 11.670169846198839


def test_coleman_liau_index():
    scireadability.set_lang("en")
    index = scireadability.coleman_liau_index(long_test)

    assert index == 9.13440860215054


def test_automated_readability_index():
    scireadability.set_lang("en")
    index = scireadability.automated_readability_index(long_test)

    assert index == 11.643111954459208


def test_linsear_write_formula():
    scireadability.set_lang("en")
    result = scireadability.linsear_write_formula(long_test)

    assert result == 15.25

    result = scireadability.linsear_write_formula(empty_str)

    assert result == -1.0


def test_difficult_words():
    scireadability.set_lang("en")
    result = scireadability.difficult_words(long_test)

    assert result == 54


def test_difficult_words_list():
    scireadability.set_lang("en")
    result = scireadability.difficult_words_list(short_test)

    assert result == ["sunglasses"]


def test_is_difficult_word():
    scireadability.set_lang("en")
    result = scireadability.is_difficult_word(difficult_word)

    assert result is True


def test_is_easy_word():
    scireadability.set_lang("en")
    result = scireadability.is_easy_word(easy_word)

    assert result is True


def test_dale_chall_readability_score():
    scireadability.set_lang("en")
    score = scireadability.dale_chall_readability_score(long_test)

    assert score == 7.7779937381404185

    score = scireadability.dale_chall_readability_score(empty_str)

    assert score == 0.0


def test_gunning_fog():
    scireadability.set_lang("en")
    score = scireadability.gunning_fog(long_test)

    assert score == 11.118532574320051

    # FOG-PL
    scireadability.set_lang("pl_PL")
    score_pl = scireadability.gunning_fog(long_test)

    assert score_pl == 9.82820999367489


def test_lix():
    scireadability.set_lang("en")
    score = scireadability.lix(long_test)

    assert score == 43.69086357947434

    result = scireadability.lix(empty_str)

    assert result == 0.0


def test_rix():
    scireadability.set_lang("en")
    score = scireadability.rix(long_test)

    assert score == 4.588235294117647


def test_text_standard():
    scireadability.set_lang("en")
    standard = scireadability.text_standard(long_test)

    assert standard == "10th and 11th grade"

    standard = scireadability.text_standard(short_test)

    assert standard == "1st and 2nd grade"


def test_reading_time():
    scireadability.set_lang("en")
    score = scireadability.reading_time(long_test)

    assert score == 25.67812


def test_lru_caching():
    scireadability.set_lang("en")
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


def test_changing_lang_clears_cache():
    scireadability.set_lang("en")

    # Clear any cache and call reading ease
    scireadability.flesch_reading_ease.cache_clear()
    scireadability.flesch_reading_ease(short_test)

    # Check the cache has only been missed once
    assert scireadability.flesch_reading_ease.cache_info().misses == 1

    # Change the language and recall reading ease
    scireadability.set_lang("fr")
    scireadability.flesch_reading_ease(short_test)

    # Check the cache hasn't been hit again
    assert scireadability.flesch_reading_ease.cache_info().misses == 1


def test_unicode_support():
    scireadability.set_lang("en")
    scireadability.text_standard(
        "\u3042\u308a\u304c\u3068\u3046\u3054\u3056\u3044\u307e\u3059")

    scireadability.text_standard("ありがとうございます")


def test_spache_readability():
    scireadability.set_lang("en")
    spache = scireadability.spache_readability(easy_text, False)

    assert spache == 2

    score = scireadability.spache_readability(empty_str)

    assert score == 0.0


def test_dale_chall_readability_score_v2():
    scireadability.set_lang("en")
    score = scireadability.dale_chall_readability_score_v2(long_test)

    assert score == 7.013961480075902


def test_fernandez_huerta():
    scireadability.set_lang("es")
    score = scireadability.fernandez_huerta(long_spanish_text)

    assert score == 65.96666666666667

    score = scireadability.fernandez_huerta(empty_str)

    assert score == 206.84


def test_szigriszt_pazos():
    scireadability.set_lang("es")
    score = scireadability.szigriszt_pazos(long_spanish_text)

    assert score == 62.16222222222224

    score = scireadability.szigriszt_pazos(empty_str)

    assert score == 0.0


def test_gutierrez_polini():
    scireadability.set_lang("es")
    score = scireadability.gutierrez_polini(easy_spanish_text)

    assert score == 64.35000000000001

    score = scireadability.gutierrez_polini(empty_str)

    assert score == 0.0


def test_crawford():
    scireadability.set_lang("es")
    score = scireadability.crawford(long_spanish_text)

    assert score == 5.089296296296297

    score = scireadability.crawford(empty_str)

    assert score == 0.0


def test_wienersachtext_formula():
    scireadability.set_lang("de")
    sample_text = 'Alle meine Entchen schwimmen auf dem See, \
    Köpfchen unters Wasser, Schwänzchen in die Höh.'
    wstf = scireadability.wiener_sachtextformel(sample_text, variant=1)

    assert wstf == 3.8

    sample_text = 'Alle Parteien widmen dem Thema rein quantitativ \
    betrachtet nennenswerte Aufmerksamkeit, die Grünen wenig überraschend \
    am meisten.'
    wstf = scireadability.wiener_sachtextformel(sample_text, variant=1)

    assert wstf == 13.9


def test_gulpease_index():
    scireadability.set_lang("it")
    score = scireadability.gulpease_index(italian_text)

    assert score == 40.111111111111114


def test_default_lang_configs():
    # Config from default en should be used
    scireadability.set_lang("en_GB")
    score = scireadability.flesch_reading_ease(long_test)

    assert score == 70.23247628083493


def test_osman():
    easy_score = scireadability.osman(easy_arabic_text)
    hard_score = scireadability.osman(hard_arabic_text)

    assert easy_score == 102.18627777777778
    assert hard_score == 39.292019999999994


def test_disabling_rounding():
    scireadability.set_lang("en")
    scireadability.set_rounding(False)

    index = scireadability.spache_readability(long_test)

    scireadability.set_rounding(True)

    assert index == 5.172798861480075


def test_changing_rounding_points():
    scireadability.set_lang("en")
    scireadability.set_rounding(True, points=5)

    index = scireadability.spache_readability(long_test)

    scireadability.set_rounding(True)

    assert index == 5.1728


def test_instanced_textstat_rounding():
    scireadability.set_lang("en")

    from scireadability.scireadability import readability

    my_textstat = readability()
    my_textstat.set_rounding(False)

    my_not_rounded_index = my_textstat.spache_readability(long_test)

    assert my_not_rounded_index == 5.172798861480075

    default_rounded_index = scireadability.spache_readability(long_test)

    assert default_rounded_index == 5.17


def test_mcalpine_eflaw():
    scireadability.set_lang("en")
    score = scireadability.mcalpine_eflaw(long_test)

    assert score == 30.8


def test_miniword_count():
    scireadability.set_lang("en")
    count = scireadability.miniword_count(long_test)

    assert count == 151


# Hungarian tests

easy_hungarian_text = "A ló zabot eszik és én a csillagos ég alatt alszom ma."

easy_hungarian_text2 = """
    Mondok neked egy nyelvtani fejtöröt.Melyik több?
    Hat tucat tucat vagy fél tucat tucat?
    """

hard_hungarian_text = (
    """
    A mai fagylalt elődjének számító hideg édességet több ezer éve
    készítettek először. Egyes feljegyzések szerint az ó kori kínaiak a
    mézzel édesített gyümölcsleveket hóval, jéggel hűtötték, és ezen hideg
    édességeket szolgálták fel a kiváltságosoknak. Annyi bizonyos, hogy a
    római császárok kedvelt csemegéi voltak a hegyekből hozatott hóval
    kevert gyümölcs levek, melyek sűrűn folyó, hideg, fagylaltszerű
    italkülönlegességet eredményeztek.
    """
)

hard_academic_hungarian_text = (
    """
    Az Amerikai Egyesült Államokban már a múlt század közepétől
    alkalmazzák az angol nyelv matematikai elemzésére szolgáló olvashatósági
    formulákat. Ezek közül hármat a neveléstudomány is használ a tengerentúli
    oktatásban,a különböző rendeltetési célú szövegek elemzésére. A
    vizsgálatok célja az, hogy meghatározzák a tanítási folyamatban használt
    könyvek és tankönyvek érthető megfogalmazásának korcsoport vagy iskolai
    osztályok alapján besorolható szintjét. Figyelembe véve az elméleti
    hátteret, magyar szövegeken is teszteltük a formulákat, hogy
    megállapítsuk, érvényesek-e az angol nyelvű szövegek következtetései.
    Az olvashatósági tesztek eredeti célja meghatározni azt a fogalmazási
    szintet, amely a legtöbb embernek érthető, és elkerüli az
    olvasásértelmezést zavaró szakkifejezéseket, illetve bonyolult szavak
    alkalmazását. Az 1920-as évektől kezdődően Edward Thorndike a tankönyvek
    olvasásának nehézségi fokát vizsgálta, és különböző szószedeteket
    javasolt iskolai használatra, az életkornak és az iskolai évfolyamoknak
    megfelelően."""
)


def test_char_count_hungarian():
    # Arrange
    scireadability.set_lang("hu_HU")
    expected_easy_count = 43
    expected_easy_count_spaces = 54

    # Act
    actual_count = scireadability.char_count(easy_hungarian_text)
    actual_count_spaces = scireadability.char_count(
        easy_hungarian_text, ignore_spaces=False
    )

    # Assert
    assert actual_count == expected_easy_count
    assert actual_count_spaces == expected_easy_count_spaces


def test_letter_count_hungarian():
    # Arrange
    scireadability.set_lang("hu_HU")
    expected_easy_count = 42
    expected_easy_count_spaces = 53

    actual_count = scireadability.letter_count(easy_hungarian_text)
    actual_count_spaces = scireadability.letter_count(
        easy_hungarian_text, ignore_spaces=False
    )

    # Assert
    assert actual_count == expected_easy_count
    assert actual_count_spaces == expected_easy_count_spaces


def test_sentence_count_hungarian():
    # Arrange
    scireadability.set_lang('hu_HU')
    expected_hard = 3
    expected_hard_academic = 6

    # Act
    actual_hard = scireadability.sentence_count(hard_hungarian_text)
    actual_academic = scireadability.sentence_count(hard_academic_hungarian_text)

    # Assert
    assert actual_hard == expected_hard
    assert actual_academic == expected_hard_academic


def test_flesch_reading_ease_hungarian():
    # Arrange
    scireadability.set_lang("hu_HU")
    expected_easy = 89.09
    expected_hard = 53.0
    expected_hard_academic = 22.02

    # Act
    actual_easy = scireadability.flesch_reading_ease(easy_hungarian_text2)
    actual_hard = scireadability.flesch_reading_ease(hard_hungarian_text)
    actual_academic = scireadability.flesch_reading_ease(
        hard_academic_hungarian_text
    )

    # Assert
    assert actual_easy == expected_easy
    assert actual_hard == expected_hard
    assert actual_academic == expected_hard_academic


def test_smog_index_hungarian():
    # Arrange
    scireadability.set_lang("hu_HU")
    expected_easy = 0
    expected_hard = 17.9
    expected_hard_academic = 21.9

    # Act
    actual_easy = scireadability.smog_index(easy_hungarian_text)
    actual_hard = scireadability.smog_index(hard_hungarian_text)
    actual_academic = scireadability.smog_index(hard_academic_hungarian_text)

    # Assert
    assert actual_easy == expected_easy
    assert actual_hard == expected_hard
    assert actual_academic == expected_hard_academic


def test_gunning_fog_hungarian():
    # Arrange
    scireadability.set_lang("hu_HU")
    expected_easy = 2.6
    expected_hard = 9.71
    expected_hard_academic = 14.41

    # Act
    actual_easy = scireadability.gunning_fog(easy_hungarian_text2)
    actual_hard = scireadability.gunning_fog(hard_hungarian_text)
    actual_academic = scireadability.gunning_fog(hard_academic_hungarian_text)

    # Assert
    assert actual_easy == expected_easy
    assert actual_hard == expected_hard
    assert actual_academic == expected_hard_academic

# --- Tests for load_custom_syllable_dict ---
def test_load_custom_syllable_dict_user_dict_exists_valid_json(test_env):
    test_config_dir, _ = test_env
    lang = "en"
    user_dict_content = {"CUSTOM_SYLLABLE_DICT": {"testword": 3}}
    user_dict_path = dictionary_utils._get_user_dict_path(lang)
    os.makedirs(os.path.dirname(user_dict_path), exist_ok=True)
    with open(user_dict_path, 'w', encoding='utf-8') as f:
        json.dump(user_dict_content, f)

    loaded_dict = dictionary_utils.load_custom_syllable_dict(lang)
    assert loaded_dict == user_dict_content["CUSTOM_SYLLABLE_DICT"]


def test_load_custom_syllable_dict_user_dict_not_exists_default_exists_valid(test_env):
    _, test_resources_dir = test_env
    lang = "en"
    default_dict_content = {"CUSTOM_SYLLABLE_DICT": {"defaultword": 2}}
    default_dict_path = dictionary_utils._get_default_dict_path(lang)
    with open(os.path.join(test_resources_dir, default_dict_path), 'w', encoding='utf-8') as f:
        json.dump(default_dict_content, f)

    loaded_dict = dictionary_utils.load_custom_syllable_dict(lang)
    assert loaded_dict == default_dict_content["CUSTOM_SYLLABLE_DICT"]


def test_load_custom_syllable_dict_user_dict_not_exists_default_not_exists(test_env):
    lang = "en"
    loaded_dict = dictionary_utils.load_custom_syllable_dict(lang)
    assert loaded_dict == {}


def test_load_custom_syllable_dict_user_dict_not_exists_default_exists_invalid_json(test_env):
    _, test_resources_dir = test_env
    lang = "en"
    default_dict_path = dictionary_utils._get_default_dict_path(lang)
    # No need to create dirs here, fixture does it now
    with open(os.path.join(test_resources_dir, default_dict_path), 'w', encoding='utf-8') as f:
        f.write("invalid json")

    loaded_dict = dictionary_utils.load_custom_syllable_dict(lang)
    assert loaded_dict == {}


# --- Tests for overwrite_custom_dict ---
def test_overwrite_custom_dict_valid_json_file(test_env):
    test_config_dir, _ = test_env
    lang = "en"
    new_dict_content = {"CUSTOM_SYLLABLE_DICT": {"newword": 4, "anotherword": 5}}
    test_json_file = os.path.join(test_config_dir, "test_dict.json")
    with open(test_json_file, 'w', encoding='utf-8') as f:
        json.dump(new_dict_content, f)

    dictionary_utils.overwrite_custom_dict(test_json_file, lang)
    loaded_dict = dictionary_utils.load_custom_syllable_dict(lang)

    assert loaded_dict == new_dict_content["CUSTOM_SYLLABLE_DICT"]


def test_overwrite_custom_dict_file_not_found(test_env):
    test_config_dir, _ = test_env
    lang = "en"
    non_existent_file = os.path.join(test_config_dir, "nonexistent.json")
    with pytest.raises(FileNotFoundError):
        dictionary_utils.overwrite_custom_dict(non_existent_file, lang)


def test_overwrite_custom_dict_invalid_json_file(test_env):
    test_config_dir, _ = test_env
    lang = "en"
    invalid_json_file = os.path.join(test_config_dir, "invalid.json")
    with open(invalid_json_file, 'w', encoding='utf-8') as f:
        f.write("invalid json")

    with pytest.raises(json.JSONDecodeError):
        dictionary_utils.overwrite_custom_dict(invalid_json_file, lang)


def test_overwrite_custom_dict_invalid_dict_format(test_env):
    test_config_dir, _ = test_env
    lang = "en"
    invalid_format_file = os.path.join(test_config_dir, "badformat.json")
    bad_format_content = {"WRONG_KEY": {"word": 1}}
    with open(invalid_format_file, 'w', encoding='utf-8') as f:
        json.dump(bad_format_content, f)

    with pytest.raises(ValueError):
        dictionary_utils.overwrite_custom_dict(invalid_format_file, lang)


# --- Tests for add_term_to_custom_dict ---
def test_add_term_to_custom_dict_valid_term(test_env):
    test_config_dir, _ = test_env
    lang = "en"
    word_to_add = "testterm"
    syllable_count = 4

    dictionary_utils.add_term_to_custom_dict(word_to_add, syllable_count, lang)
    loaded_dict = dictionary_utils.load_custom_syllable_dict(lang)

    assert word_to_add in loaded_dict
    assert loaded_dict[word_to_add] == syllable_count


def test_add_term_to_custom_dict_invalid_syllable_count_zero(test_env):
    lang = "en"
    with pytest.raises(ValueError):
        dictionary_utils.add_term_to_custom_dict("word", 0, lang)


def test_add_term_to_custom_dict_invalid_syllable_count_negative(test_env):
    lang = "en"
    with pytest.raises(ValueError):
        dictionary_utils.add_term_to_custom_dict("word", -1, lang)


def test_add_term_to_custom_dict_invalid_syllable_count_not_int(test_env):
    lang = "en"
    with pytest.raises(ValueError):
        dictionary_utils.add_term_to_custom_dict("word", "not_an_int", lang)


# --- Tests for add_terms_from_file ---
def test_add_terms_from_file_valid_json_file(test_env):
    test_config_dir, _ = test_env
    lang = "en"
    new_terms_content = {"CUSTOM_SYLLABLE_DICT": {"fileword1": 2, "fileword2": 3}}
    test_json_file = os.path.join(test_config_dir, "terms.json")
    with open(test_json_file, 'w', encoding='utf-8') as f:
        json.dump(new_terms_content, f)

    dictionary_utils.add_terms_from_file(test_json_file, lang)
    loaded_dict = dictionary_utils.load_custom_syllable_dict(lang)

    for word, count in new_terms_content["CUSTOM_SYLLABLE_DICT"].items():
        assert word in loaded_dict
        assert loaded_dict[word] == count


def test_add_terms_from_file_file_not_found(test_env):
    test_config_dir, _ = test_env
    lang = "en"
    non_existent_file = os.path.join(test_config_dir, "nonexistent_terms.json")
    with pytest.raises(FileNotFoundError):
        dictionary_utils.add_terms_from_file(non_existent_file, lang)


def test_add_terms_from_file_invalid_json_file(test_env):
    test_config_dir, _ = test_env
    lang = "en"
    invalid_json_file = os.path.join(test_config_dir, "invalid_terms.json")
    with open(invalid_json_file, 'w', encoding='utf-8') as f:
        f.write("invalid json")

    with pytest.raises(json.JSONDecodeError):
        dictionary_utils.add_terms_from_file(invalid_json_file, lang)


def test_add_terms_from_file_invalid_dict_format(test_env):
    test_config_dir, _ = test_env
    lang = "en"
    invalid_format_file = os.path.join(test_config_dir, "badformat_terms.json")
    bad_format_content = {"WRONG_KEY": {"word": 1}}
    with open(invalid_format_file, 'w', encoding='utf-8') as f:
        json.dump(bad_format_content, f)

    with pytest.raises(ValueError):
        dictionary_utils.add_terms_from_file(invalid_format_file, lang)


# --- Tests for revert_custom_dict_to_default ---
def test_revert_custom_dict_to_default_user_dict_exists(test_env):
    test_config_dir, test_resources_dir = test_env
    lang = "en"
    user_dict_path = dictionary_utils._get_user_dict_path(lang)
    os.makedirs(os.path.dirname(user_dict_path), exist_ok=True)
    with open(user_dict_path, 'w', encoding='utf-8') as f:
        json.dump({"CUSTOM_SYLLABLE_DICT": {"userword": 100}}, f)

    default_dict_content = {"CUSTOM_SYLLABLE_DICT": {"defaultword": 2}}
    default_dict_path = dictionary_utils._get_default_dict_path(lang)
    # No need to create dirs here, fixture does it now
    with open(os.path.join(test_resources_dir, default_dict_path), 'w', encoding='utf-8') as f:
        json.dump(default_dict_content, f)

    dictionary_utils.revert_custom_dict_to_default(lang)
    loaded_dict = dictionary_utils.load_custom_syllable_dict(lang)

    assert loaded_dict == default_dict_content["CUSTOM_SYLLABLE_DICT"]


def test_revert_custom_dict_to_default_default_dict_not_found(test_env):
    _, test_resources_dir = test_env
    lang = "en"
    default_dict_path = dictionary_utils._get_default_dict_path(lang)
    default_dict_file = os.path.join(test_resources_dir, default_dict_path)
    if os.path.exists(default_dict_file):
        os.remove(default_dict_file)
    os.makedirs(os.path.dirname(default_dict_file), exist_ok=True) # Ensure lang dir exists

    with pytest.raises(FileNotFoundError):
        dictionary_utils.revert_custom_dict_to_default(lang)


def test_revert_custom_dict_to_default_invalid_json_in_default(test_env):
    _, test_resources_dir = test_env
    lang = "en"
    default_dict_path = dictionary_utils._get_default_dict_path(lang)
    # No need to create dirs here, fixture does it now
    with open(os.path.join(test_resources_dir, default_dict_path), 'w', encoding='utf-8') as f:
        f.write("invalid json")

    with pytest.raises(json.JSONDecodeError):
        dictionary_utils.revert_custom_dict_to_default(lang)

def test_load_custom_syllable_dict_case_sensitivity(test_env):
    _, test_resources_dir = test_env
    lang = "en"
    default_dict_content = {"CUSTOM_SYLLABLE_DICT": {"TestWord": 2}} # Mixed case in default
    default_dict_path = dictionary_utils._get_default_dict_path(lang)
    with open(os.path.join(test_resources_dir, default_dict_path), 'w', encoding='utf-8') as f:
        json.dump(default_dict_content, f)

    loaded_dict = dictionary_utils.load_custom_syllable_dict(lang)
    assert "testword" in loaded_dict # Assert lowercase lookup works (case-insensitive loading is assumed)
    assert loaded_dict["testword"] == 2 # Check correct count


def test_load_custom_syllable_dict_empty_default_dict_file(test_env):
    _, test_resources_dir = test_env
    lang = "en"
    default_dict_path = dictionary_utils._get_default_dict_path(lang)
    with open(os.path.join(test_resources_dir, default_dict_path), 'w', encoding='utf-8') as f:
        json.dump({}, f) # Empty JSON as default

    loaded_dict = dictionary_utils.load_custom_syllable_dict(lang)
    assert loaded_dict == {} # Should load as empty dict


# --- Additional Tests for overwrite_custom_dict ---
def test_overwrite_custom_dict_large_json_file(test_env):
    test_config_dir, _ = test_env
    lang = "en"
    large_dict_content = {"CUSTOM_SYLLABLE_DICT": {f"word_{i}": i % 5 + 1 for i in range(1000)}}
    test_json_file = os.path.join(test_config_dir, "large_dict.json")
    with open(test_json_file, 'w', encoding='utf-8') as f:
        json.dump(large_dict_content, f)

    dictionary_utils.overwrite_custom_dict(test_json_file, lang)
    loaded_dict = dictionary_utils.load_custom_syllable_dict(lang)
    assert loaded_dict == large_dict_content["CUSTOM_SYLLABLE_DICT"] # Verify content


def test_overwrite_custom_dict_verify_file_content(test_env):
    test_config_dir, _ = test_env
    lang = "en"
    new_dict_content = {"CUSTOM_SYLLABLE_DICT": {"filecheckword": 3}}
    test_json_file = os.path.join(test_config_dir, "temp_dict.json")
    with open(test_json_file, 'w', encoding='utf-8') as f:
        json.dump(new_dict_content, f)

    dictionary_utils.overwrite_custom_dict(test_json_file, lang)
    user_dict_path = dictionary_utils._get_user_dict_path(lang)
    with open(user_dict_path, 'r', encoding='utf-8') as f:
        file_dict_content = json.load(f)
    assert file_dict_content == new_dict_content # Verify file content directly


# --- Additional Tests for add_term_to_custom_dict ---
def test_add_term_to_custom_dict_existing_term_same_count(test_env):
    test_config_dir, _ = test_env
    lang = "en"
    word_to_add = "existingword"
    syllable_count = 2
    user_dict_path = dictionary_utils._get_user_dict_path(lang)
    os.makedirs(os.path.dirname(user_dict_path), exist_ok=True)
    with open(user_dict_path, 'w', encoding='utf-8') as f:
        json.dump({"CUSTOM_SYLLABLE_DICT": {word_to_add: syllable_count}}, f) # Dict exists with word

    dictionary_utils.add_term_to_custom_dict(word_to_add, syllable_count, lang) # Add again with same count
    loaded_dict = dictionary_utils.load_custom_syllable_dict(lang)
    assert loaded_dict[word_to_add] == syllable_count # Count should remain the same

def test_add_term_to_custom_dict_existing_term_different_count(test_env):
    test_config_dir, _ = test_env
    lang = "en"
    word_to_add = "existingword"
    initial_syllable_count = 2
    new_syllable_count = 3
    user_dict_path = dictionary_utils._get_user_dict_path(lang)
    os.makedirs(os.path.dirname(user_dict_path), exist_ok=True)
    with open(user_dict_path, 'w', encoding='utf-8') as f:
        json.dump({"CUSTOM_SYLLABLE_DICT": {word_to_add: initial_syllable_count}}, f) # Dict exists with word

    dictionary_utils.add_term_to_custom_dict(word_to_add, new_syllable_count, lang) # Add again with different count
    loaded_dict = dictionary_utils.load_custom_syllable_dict(lang)
    assert loaded_dict[word_to_add] == new_syllable_count # Count should be updated/overwritten


# --- Additional Tests for add_terms_from_file ---
def test_add_terms_from_file_empty_custom_syllable_dict_key(test_env):
    test_config_dir, _ = test_env
    lang = "en"
    empty_dict_file_content = {"CUSTOM_SYLLABLE_DICT": {}} # Empty dict for the key
    test_json_file = os.path.join(test_config_dir, "empty_dict_terms.json")
    with open(test_json_file, 'w', encoding='utf-8') as f:
        json.dump(empty_dict_file_content, f)

    dictionary_utils.add_terms_from_file(test_json_file, lang)
    loaded_dict = dictionary_utils.load_custom_syllable_dict(lang)
    assert loaded_dict == {} # Should remain or become empty


def test_add_terms_from_file_non_dict_value_for_custom_syllable_dict(test_env):
    test_config_dir, _ = test_env
    lang = "en"
    non_dict_file_content = {"CUSTOM_SYLLABLE_DICT": ["not", "a", "dict"]} # List instead of dict
    test_json_file = os.path.join(test_config_dir, "non_dict_terms.json")
    with open(test_json_file, 'w', encoding='utf-8') as f:
        json.dump(non_dict_file_content, f)

    with pytest.raises(ValueError):
        dictionary_utils.add_terms_from_file(test_json_file, lang)


# --- Additional Tests for revert_custom_dict_to_default ---
def test_revert_custom_dict_to_default_no_user_dict_exists(test_env):
    test_config_dir, test_resources_dir = test_env
    lang = "en"
    user_dict_path = dictionary_utils._get_user_dict_path(lang)
    if os.path.exists(user_dict_path): # Ensure no user dict exists before test
        os.remove(user_dict_path)
    user_dict_dir = os.path.dirname(user_dict_path)
    if os.path.exists(user_dict_dir) and not os.listdir(user_dict_dir):
        os.rmdir(user_dict_dir) # Remove user lang dir if empty

    default_dict_content = {"CUSTOM_SYLLABLE_DICT": {"defaultword": 2}}
    default_dict_path = dictionary_utils._get_default_dict_path(lang)
    with open(os.path.join(test_resources_dir, default_dict_path), 'w', encoding='utf-8') as f:
        json.dump(default_dict_content, f)

    dictionary_utils.revert_custom_dict_to_default(lang)
    loaded_dict = dictionary_utils.load_custom_syllable_dict(lang)
    assert loaded_dict == default_dict_content["CUSTOM_SYLLABLE_DICT"] # Should create user dict from default


def test_revert_custom_dict_to_default_empty_default_dict(test_env):
    _, test_resources_dir = test_env
    lang = "en"
    default_dict_path = dictionary_utils._get_default_dict_path(lang)
    with open(os.path.join(test_resources_dir, default_dict_path), 'w', encoding='utf-8') as f:
        json.dump({}, f) # Empty default dictionary

    dictionary_utils.revert_custom_dict_to_default(lang)
    loaded_dict = dictionary_utils.load_custom_syllable_dict(lang)
    assert loaded_dict == {} # Should revert to empty dict
