from .scireadability import scireadability


__version__ = (0, 6, 4)


for attribute in dir(scireadability):
    if callable(getattr(scireadability, attribute)):
        if not attribute.startswith("_"):
            globals()[attribute] = getattr(scireadability, attribute)
