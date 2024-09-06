# TikTok User Tracker

The TikTok User Tracker project is an effective tool designed to monitor user activity on the popular TikTok social network. This script provides automated tracking of users' video content, allowing you to analyze their activity with ease and efficiency.

Thanks to this tool, you can receive notifications about new videos, track changes in the activity of selected users and analyze their content without having to constantly manually check the pages.

## Description of the project

This script allows you to track the appearance of a new video by the user TikTok, as well as display links to these videos for subsequent analysis.

## Использование

1. Install the necessary libraries by running the following command:
   pip install -r requirements.txt

2. Run the script parserTikTok.py:
   python parserTikTok.py
   
3. Enter the user name Tik Tok without the @ symbol.

4. To stop tracking, press the space bar.

## Environment requirements

- Python 3.x
- Libraries: requests, BeautifulSoup, pygame, pynput

## Примечания

- The script will write data about its work to a file Output.log.
- If errors occur due to server unavailability, the script will attempt to reconnect after a random time.


