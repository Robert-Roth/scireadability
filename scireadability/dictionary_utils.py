from importlib.resources import files
import json
import logging
import os
import re

from platformdirs import user_config_dir

PACKAGE_NAME = "scireadability"
DICT_KEY = "CUSTOM_SYLLABLE_DICT"
CONFIG_DIR_ENV_VAR = "SCIREADABILITY_CONFIG_DIR"

logger = logging.getLogger(__name__)


def _read_package_resource(resource_path: str) -> bytes:
    """Reads a package resource file and returns its contents as bytes."""
    return files("scireadability").joinpath(resource_path).read_bytes()


def _get_default_dict_path():
    """Returns the path to the default custom dictionary in the package."""
    return "resources/en/custom_dict.json"


def _get_user_dict_path():
    """Returns the path to the user's custom dictionary in the config directory."""
    config_dir = os.environ.get(CONFIG_DIR_ENV_VAR) or user_config_dir(PACKAGE_NAME)
    return os.path.join(config_dir, "en", "custom_dict.json")


def _normalize_word(word):
    """Lowercases a word and strips punctuation (e.g. hyphens) except apostrophes,
    matching how words are looked up during syllable counting."""
    return re.sub(r"[^\w']", "", word.lower())


def _is_positive_int(n):
    return isinstance(n, int) and not isinstance(n, bool) and n >= 1


def _validate_entries(entries, source):
    """Checks that a dictionary maps words to positive integer syllable counts."""
    if not isinstance(entries, dict):
        raise ValueError(
            f"Invalid dictionary format in {source}. "
            f"Should be a JSON object with a '{DICT_KEY}' key containing a dictionary."
        )
    for word, count in entries.items():
        if not _is_positive_int(count):
            raise ValueError(
                f"Invalid syllable count for '{word}' in {source}: {count!r}. "
                "Syllable counts must be positive integers."
            )


def _read_dict_file(file_path):
    """Reads and validates the entries of a dictionary JSON file."""
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict) or DICT_KEY not in data:
        raise ValueError(
            f"Invalid dictionary format in {file_path}. "
            f"Should be a JSON object with a '{DICT_KEY}' key."
        )
    _validate_entries(data[DICT_KEY], file_path)
    return {_normalize_word(k): v for k, v in data[DICT_KEY].items()}


def load_default_dict():
    """Loads the default custom syllable dictionary shipped with the package."""
    default_dict_path = _get_default_dict_path()
    try:
        data = json.loads(_read_package_resource(default_dict_path).decode("utf-8"))
    except FileNotFoundError:
        logger.warning("Default dictionary not found: %s", default_dict_path)
        return {}
    except json.JSONDecodeError as e:
        logger.warning("Invalid default dictionary %s: %s", default_dict_path, e)
        return {}
    return {_normalize_word(k): v for k, v in data.get(DICT_KEY, {}).items()}


def load_user_dict():
    """Loads the user's own dictionary entries (without the package defaults)."""
    user_dict_path = _get_user_dict_path()
    try:
        return _read_dict_file(user_dict_path)
    except FileNotFoundError:
        return {}
    except (json.JSONDecodeError, ValueError) as e:
        logger.warning("Ignoring invalid user dictionary %s: %s", user_dict_path, e)
        return {}


def load_custom_syllable_dict():
    """Loads the custom syllable dictionary: package defaults, overridden by any
    entries the user has added."""
    return {**load_default_dict(), **load_user_dict()}


def _save_user_dict(entries):
    user_dict_path = _get_user_dict_path()
    os.makedirs(os.path.dirname(user_dict_path), exist_ok=True)
    with open(user_dict_path, "w", encoding="utf-8") as outfile:
        json.dump({DICT_KEY: entries}, outfile, indent=4)
    return user_dict_path


def overwrite_custom_dict(file_path):
    """Replaces all of the user's entries with the contents of a JSON file.
    The package defaults still apply to words the file doesn't list."""
    user_dict_path = _save_user_dict(_read_dict_file(file_path))
    logger.info("User dictionary replaced from %s: %s", file_path, user_dict_path)


def add_term_to_custom_dict(word, syllable_count):
    """Adds a single term to the user's custom dictionary."""
    if not _is_positive_int(syllable_count):
        raise ValueError("Syllable count must be a positive integer.")

    entries = load_user_dict()
    entries[_normalize_word(word)] = syllable_count
    user_dict_path = _save_user_dict(entries)
    logger.info("Added '%s' (%d syllables): %s", word, syllable_count, user_dict_path)


def add_terms_from_file(file_path):
    """Adds multiple terms from a JSON file to the user's custom dictionary."""
    entries = load_user_dict()
    entries.update(_read_dict_file(file_path))
    user_dict_path = _save_user_dict(entries)
    logger.info("Added terms from %s. Saved to %s", file_path, user_dict_path)


def print_custom_dict():
    """Prints the currently loaded custom dictionary to the console."""
    print(json.dumps({DICT_KEY: load_custom_syllable_dict()}, indent=4))


def revert_custom_dict_to_default():
    """Removes all of the user's entries, leaving only the package defaults."""
    user_dict_path = _get_user_dict_path()
    try:
        os.remove(user_dict_path)
    except FileNotFoundError:
        pass
    logger.info("User dictionary removed: %s", user_dict_path)
