from setuptools import setup
from io import open

setup(
    name="scireadability",
    packages=["scireadability"],
    version="2.0.1",
    description="Calculate statistical features from text, mainly scientific literature",
    author="Robert Roth",
    author_email="rwroth5@gmail.com",
    url="https://github.com/robert-roth/scireadability",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    package_data={
        "": ["resources/en/easy_words.txt", "resources/en/custom_dict.json",
             "resources/en/cmudict.dict"]
    },
    include_package_data=True,
    install_requires=["setuptools", "appdirs"],
    license="MIT",
    python_requires=">=3.10",
    project_urls={
        "Documentation": "https://github.com/robert-roth/scireadability",
        "Demo": "https://scireadability-rwroth5.pythonanywhere.com/analyze/",
    },
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Topic :: Text Processing",
    ],
)
