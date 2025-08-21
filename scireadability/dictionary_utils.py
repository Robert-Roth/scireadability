from appdirs import user_config_dir
import json
import os
import pkg_resources

PACKAGE_NAME = "scireadability"


def _get_default_dict_path():
    """Returns the path to the default custom dictionary in the package."""
    return "resources/en/custom_dict.json"


def _get_user_dict_path():
    """Returns the path to the user's custom dictionary in the config directory."""
    config_dir = user_config_dir(PACKAGE_NAME)
    dict_dir = os.path.join(config_dir, "en")
    os.makedirs(dict_dir, exist_ok=True)
    return os.path.join(dict_dir, "custom_dict.json")


def load_custom_syllable_dict():
    """Loads the custom syllable dictionary, prioritizing user overrides.

    Loads the dictionary from the user's config directory if it exists,
    otherwise loads the default dictionary from the package resources.
    """
    user_dict_path = _get_user_dict_path()
    default_dict_path = _get_default_dict_path()
    loaded_dict = {}

    try:
        with open(user_dict_path, "r", encoding="utf-8") as f:
            user_data = json.load(f)
            if "CUSTOM_SYLLABLE_DICT" in user_data:
                # Convert keys to lowercase when loading from user dict
                loaded_dict.update(
                    {k.lower(): v for k, v in user_data["CUSTOM_SYLLABLE_DICT"].items()}
                )
                print(f"Loaded custom dictionary from user config: {user_dict_path}")
                return loaded_dict  # User dict takes precedence
    except FileNotFoundError:
        pass  # User dict is optional

    try:
        default_dict_string = pkg_resources.resource_string(
            __name__, default_dict_path
        ).decode("utf-8")
        default_data = json.loads(default_dict_string)
        if "CUSTOM_SYLLABLE_DICT" in default_data:
            loaded_dict.update(
                {k.lower(): v for k, v in default_data["CUSTOM_SYLLABLE_DICT"].items()}
            )
    except FileNotFoundError:
        print(
            f"Error: Default custom syllable dictionary file not found in package at "
            f"{default_dict_path}."
        )
    except json.JSONDecodeError as e:
        print(
            f"Error: Invalid JSON format in default dictionary file at {default_dict_path}. "
            f"Error: {e}"
        )

    return loaded_dict


def overwrite_custom_dict(file_path):
    """Overwrites the user's custom dictionary with the contents of a given JSON file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            new_dict_data = json.load(f)
            if (
                not isinstance(new_dict_data, dict)
                or "CUSTOM_SYLLABLE_DICT" not in new_dict_data
            ):
                raise ValueError(
                    "Invalid dictionary format in provided file.  "
                    "Should be a JSON with 'CUSTOM_SYLLABLE_DICT' key."
                )
            user_dict_path = _get_user_dict_path()
            with open(user_dict_path, "w", encoding="utf-8") as outfile:
                json.dump(new_dict_data, outfile, indent=4)
            print(
                f"Custom dictionary overwritten with file: {file_path}. Saved to {user_dict_path}"
            )
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except json.JSONDecodeError:
        raise json.JSONDecodeError(f"Invalid JSON in file: {file_path}", "", 0)
    except ValueError as ve:
        raise ve
    except Exception as e:
        raise Exception(
            f"An unexpected error occurred during dictionary overwrite: {e}"
        )


def add_term_to_custom_dict(word, syllable_count):
    """Adds a single term to the user's custom dictionary."""
    if not isinstance(syllable_count, int) or syllable_count < 1:
        raise ValueError("Syllable count must be a positive integer.")

    user_dict_path = _get_user_dict_path()
    current_dict = load_custom_syllable_dict()

    current_dict[word] = syllable_count

    dict_data_to_save = {
        "CUSTOM_SYLLABLE_DICT": current_dict
    }  # Re-wrap for JSON structure
    try:
        with open(user_dict_path, "w", encoding="utf-8") as outfile:
            json.dump(dict_data_to_save, outfile, indent=4)
        print(
            f"Added term '{word}': {syllable_count} syllables to custom dictionary. "
            f"Saved to {user_dict_path}"
        )
    except Exception as e:
        raise Exception(f"Error saving updated custom dictionary: {e}")


def add_terms_from_file(file_path):
    """Adds multiple terms from a JSON file to the user's custom dictionary."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            full_json_data = json.load(f)

        if "CUSTOM_SYLLABLE_DICT" not in full_json_data:
            raise ValueError(
                "Invalid dictionary format in provided file. "
                "Should be a JSON with 'CUSTOM_SYLLABLE_DICT' key containing a dictionary."
            )

        new_terms_data = full_json_data["CUSTOM_SYLLABLE_DICT"]

        if not isinstance(new_terms_data, dict):
            raise ValueError(
                "Invalid dictionary format in provided file. "
                "The value associated with 'CUSTOM_SYLLABLE_DICT' key must be a dictionary."
            )

        current_dict = load_custom_syllable_dict()
        current_dict.update(new_terms_data)

        dict_data_to_save = {"CUSTOM_SYLLABLE_DICT": current_dict}
        user_dict_path = _get_user_dict_path()

        with open(user_dict_path, "w", encoding="utf-8") as outfile:
            json.dump(dict_data_to_save, outfile, indent=4)
        print(
            f"Added terms from file: {file_path}. Updated dictionary saved to {user_dict_path}"
        )

    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except json.JSONDecodeError:
        raise json.JSONDecodeError(f"Invalid JSON in file: {file_path}", "", 0)
    except ValueError as ve:
        raise ve
    except Exception as e:
        raise Exception(f"Error adding terms from file: {e}")


def print_custom_dict():
    """Prints the currently loaded custom dictionary to the console."""
    current_dict = load_custom_syllable_dict()
    print(
        json.dumps({"CUSTOM_SYLLABLE_DICT": current_dict}, indent=4)
    )  # Print in readable JSON format


def revert_custom_dict_to_default():
    """Reverts the user's custom dictionary to the default dictionary
    that is included with the package. This effectively removes any
    customizations made by the user.
    """
    user_dict_path = _get_user_dict_path()
    default_dict_path = _get_default_dict_path()

    try:
        # Load the default dictionary content from the package resource
        resource_path = _get_default_dict_path()
        json_data = pkg_resources.resource_string(__name__, resource_path).decode(
            "utf-8"
        )
        default_dict_data = json.loads(json_data)

        # Write the default dictionary content to the user's custom dictionary path,
        # effectively overwriting the user's customizations.
        with open(user_dict_path, "w", encoding="utf-8") as outfile:
            json.dump(default_dict_data, outfile, indent=4)

        print(
            f"Custom dictionary reverted to the default package dictionary. "
            f"User customizations have been removed from: {user_dict_path}"
        )

    except FileNotFoundError:
        raise FileNotFoundError(
            f"Default dictionary file not found in package at: {default_dict_path}"
        )
    except json.JSONDecodeError:
        raise json.JSONDecodeError(
            f"Invalid JSON in default dictionary file at: {default_dict_path}", "", 0
        )
    except Exception as e:
        raise Exception(f"Error reverting custom dictionary to default: {e}")
