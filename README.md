# AO3 Update Checker

This is a simple program that checks for updates to works and updates from authors on ArchiveOfOurOwn.Org (AO3).

This is meant to be used by people who don't have AO3 accounts, but would like to keep track of works and authors they like.

Note: please do not run this too many times too quickly, as you may get rate-limited by AO3. I haven't tested how many works or authors you can check at a time before rate-limiting kicks in.

## Requires/dependencies
- [Python 3](https://www.python.org/downloads/) to run the program (I think it comes with datetime and webbrowser modules, which are also needed)
- [ao3_api for Python 3](https://github.com/ArmindoFlores/ao3_api) to send requests to AO3 and receive data

## Installation instructions
- Install dependencies (see below) first
- Download this repository and put it anywhere on your computer
- Go to the folder called "data"
  - Create two files called "authors.txt" and "works.txt"
  - Add the usernames of any author you wish to track to "authors.txt" with no commas or spaces and each username being on a new line/row
  - Add the work IDs (the first 8-digit number in the URL to the work) of any work you wish to track to "works.txt" with no commas or spaces and each number being on a new line/row
  - Write the earliest date you want to see in "last_ran.txt" on the first line in YYYY-MM-DD format. By default I left it on midnight, January 1, 2010 (2010-01-01)
- Run the file called "track_ao3.py"

### Installing dependencies
- Python 3 can be installed from [the official Python downloads page](https://www.python.org/downloads/)
- ao3_api is a package that can be installed using pip. [Check the Python Packaging User Guide for instructions](https://packaging.python.org/tutorials/installing-packages/#id18)

## What it does (step by step)
- Gets the date the program was last ran from the file called "last_ran.txt" in the "data" folder
- Gets a list of all works updated on or after that date
  - Gets all tracked works from "works.txt" and converts them to ao3_api Work objects
  - Does the same but with authors and turns them to ao3_api User objects
  - Uses ao3_api to send a request to AO3 for all the works by each author
  - Takes all of these works from above steps and asks AO3 which of them are complete, then returns those
- Puts all the information in a list in an HTML document so the user can see it and click on the links to read the works
- Updates the file "last_ran.txt" with the current date
- Opens the HTML document in the user's browser

## What I plan on making it do
- Automatically remove completed works from "works.txt"
  - The function is already written, named "remove_completed_works", so I just need to add one line of code to call it
  - I'm not sure if that would be useful, though, I don't want people to be surprised when they're missing a work in their "works.txt"
  - I'd need to create a new file, something like "no_longer_tracking.txt", and putting those works in there
- Make the program create blank files named "authors.txt" and "works.txt" if they're gone
