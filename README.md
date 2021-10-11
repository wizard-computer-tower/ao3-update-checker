# AO3 Update Checker

This is a simple program that checks for updates to works and updates from authors on ArchiveOfOurOwn.Org (AO3). It is meant to be used by people who don't have AO3 accounts, but would like to keep track of works and authors they like.

Note: please do not run this too many times too quickly, as you may get rate-limited by AO3. I haven't tested how many works or authors you can check at a time before rate-limiting kicks in.

## Requires
- [Python 3](https://www.python.org/downloads/) to run the program (I think it comes with datetime and webbrowser modules, which are also needed)
- [ao3_api for Python 3](https://github.com/ArmindoFlores/ao3_api) to send requests to AO3 and receive data

## Installation instructions
- Install dependencies (see below) first
- Download this repository and put it anywhere on your computer
  - Click the button that says "Code" right above all the files and folders in this repo
  - Download ZIP and extract anywhere in your computer
  - You can optionally make a shortcut to the program track_ao3.py and put it wherever you like
- Go to the folder called "data"
  - Create two files called "authors.txt" and "works.txt"
  - Add the usernames of any author you wish to track to "authors.txt" with no commas or spaces and each username being on a new line/row
  - Add the work IDs (the first 8-digit number in the URL to the work) of any work you wish to track to "works.txt" with no commas or spaces and each number being on a new line/row
  - Write the earliest date you want to see in "last_ran.txt" on the first line in YYYY-MM-DD format. By default I left it on midnight, January 1, 2010 (2010-01-01)

### Installing dependencies
- Python 3 can be installed from [the official Python downloads page](https://www.python.org/downloads/)
- ao3_api is a package that can be installed using pip. [Check the Python Packaging User Guide for instructions](https://packaging.python.org/tutorials/installing-packages/#installing-from-pypi)
  - Type one of the following into your command line editor
    - Unix/macOS try: `python3 -m pip install ao3_api`
    - Windows try: `py -m pip install ao3_api`

## Usage
Run the file called "track_ao3.py"
