import os
import tempfile

# Keep tests independent of the developer's real user dictionary. This must be
# set before scireadability is imported, since it loads the dictionary on import.
os.environ["SCIREADABILITY_CONFIG_DIR"] = tempfile.mkdtemp(prefix="scireadability-")
