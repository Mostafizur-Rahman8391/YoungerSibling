from setuptools import setup, find_packages
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()
setup(
    name="youngersibling",  # PyPI package name
    version="1.2",
    description="An educational OSINT toolkit for research and analysis.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Mostafizur Rahman",
    author_email="mostafizurrahman8391@gmail.com",
    url="https://github.com/Mostafizur-Rahman8391/YoungerSibling",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4",
        "colorama",
        "terminaltables",
        "dnspython",
        "exifread",
        "tqdm",
        "python-whois",
        "datetime",
        "phonenumbers"
    ],
    entry_points={
        "console_scripts": [
            "youngersibling=youngersibling.main:main",  # Command-line script
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
        package_data={
        "youngersibling": ["data.json"],  # Include the data.json file in the package
    },
)
