# **YoungerSibling**

## **Overview**
YoungerSibling is a Python-based terminal utility script designed for educational purposes. It provides a set of useful tools to perform tasks like searching the web, performing lookups (Google search, IP lookup, username lookup, etc.), and extracting metadata from images, directly from the terminal. This project aims to help students, developers, and hobbyists learn about web scraping, API usage, and terminal interaction with Python.
![Preview](image.png)
## **Features**
- **Google Search**: Perform web searches from the terminal.
- **IP Lookup**: Get geolocation information about an IP address.
- **Username Lookup**: Check if a username exists across popular social media platforms.
- **Email Lookup**: Get Mail Exchange (MX) records for an email domain.
- **Exif Data Extraction**: Extract and display EXIF metadata from image files.

## **Technologies Used**
- **Python**: The main programming language used to create the script.
- **Requests**: For making HTTP requests for data fetching.
- **BeautifulSoup**: For web scraping (specifically Google search results).
- **DNS Resolver**: For querying MX records of email domains.
- **ExifRead**: For extracting EXIF metadata from image files.
- **TerminalTables**: To display results in a neat, readable table format.
- **Colorama**: For colorizing terminal output for better readability.

## **Installation**

To install the `youngersibling` package, follow these steps:

### Using pip from PyPI

You can install `youngersibling` directly from PyPI using pip:

```bash
$ pip install youngersibling
```
### From Source
If you'd like to install youngersibling from the source code, follow these steps:

1. Clone the repository:
   ```bash
   $ git clone https://github.com/Mostafizur-Rahman8391/YoungerSibling.git
   ```
2. Navigate to project folder
```bash
$ cd YoungerSibling
```
3. Install the package:
   ```bash
   $ pip install .
   ```
## **Usage**

After installation, you can run the script by typing `youngersibling` in your command-line terminal

### 1. **Run the Script**
   ```bash
   $ youngersibling
   ```
### 2. **Available Options**
After launching the script, you will be presented with a menu of options:
```bash
Choose an option:
1. Google Search
2. IP Lookup
3. Email Lookup
4. Username Lookup
5. Exif Data Extraction
6. Exit
```
- Google Search: Enter a search query, and the script will fetch and display results from Google in a table.
- IP Lookup: Provide an IP address, and the script will retrieve geolocation data like country, region, city, and ISP.
- Email Lookup: Enter an email address, and the script will display MX records for the email's domain.
- Username Lookup: Provide a username, and the script will check its presence across multiple social media platforms.
- Exif Data Extraction: Supply the path to an image file, and the script will extract and display its EXIF metadata.

## **Developer Information**
- Author: Mostafizur Rahman
- Developer Contact: mostafizurrahman8391@gmail.com
- Version: 1.0
- License: MIT

## **Educational Purposes**

**YoungerSibling** is an educational tool designed to help users explore web scraping, networking, and cybersecurity concepts. It provides practical experience in interacting with APIs, performing DNS lookups, extracting EXIF data, and scraping web content. The tool is perfect for:

- **Web Scraping**: Learn how to fetch and parse data from websites using BeautifulSoup.
- **DNS Lookups**: Understand DNS resolution and email routing by querying MX records.
- **EXIF Data**: Extract metadata from images to understand file structures.
- **API Interactions**: Work with real-world APIs to retrieve data in JSON format.
- **CLI Tools**: Build simple command-line tools that fetch and display data.
- **Cybersecurity**: Gain insights into digital footprints, username tracking, and email validation.

**YoungerSibling** offers a hands-on approach to understanding these concepts with minimal setup, making it ideal for students, developers, and anyone interested in networking and security.

### **Disclaimer**
The owner shall not be responsible for any misuse of the tool. It is intended for educational purposes only. Users should ensure they adhere to legal and ethical standards when using this tool.

