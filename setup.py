from setuptools import setup, find_packages

setup(
    name="youngersibling",  # PyPI package name
    version="1.0.1",
    description="An educational OSINT toolkit for research and analysis.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Mostafizur Rahman",
    author_email="mostafizurrahman8391@gmail.com",
    url="https://github.com/Mostafizur-Rahman8391/YoungerSibling",
    license="MIT",
    packages=find_packages(),  # Automatically discovers the youngersibling module
    install_requires=[
        "requests",
        "beautifulsoup4",
        "colorama",
        "terminaltables",
        "dnspython",
        "exifread"
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
)
