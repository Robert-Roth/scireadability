from .textstatsci import textstatsci


__version__ = (0, 5, 0)


for attribute in dir(textstatsci):
    if callable(getattr(textstatsci, attribute)):
        if not attribute.startswith("_"):
            globals()[attribute] = getattr(textstatsci, attribute)
