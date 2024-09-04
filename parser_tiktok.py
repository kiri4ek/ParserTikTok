import datetime
import logging
import os
import random
import sys
import time
import traceback
import webbrowser

import requests
from bs4 import BeautifulSoup
import pygame as pg
from pynput import keyboard

# Constants
URL_TIKTOK_PREFIX = 'https://www.tiktok.com/@'

# Define headers for requests
HEADERS = {
    'accept': '*/*',
    'accept-language': 'ru,en;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.50'
}

# create logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler(stream=sys.stdout)
ch.setLevel(logging.INFO)
logger.addHandler(ch)
fh = logging.FileHandler('Output.log', "w", "utf-8")
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

# Initialize Pygame
pg.init()

# Configure logging
logger.debug("=========================New START")

# Clear the console
cls = lambda: os.system('cls' if os.name == 'nt' else 'clear')
cls()

# Get user input
nik = input("Введите ник пользователя TikTok без @: ")
url_tiktok = URL_TIKTOK_PREFIX + nik
logger.debug("Введите ник пользователя TikTok без @: %s", nik)

# Function to handle connection errors
def handle_connection_error():
    """Handles server connection errors."""
    logger.debug("Connection refused by the server..")

    random.seed(str(datetime.datetime.now()))
    rand_time = random.uniform(10, 30)

    logger.info("Let me sleep for %s seconds", str(rand_time))
    logger.info("ZZzzzz...")
    time.sleep(rand_time)
    logger.info("Was a nice sleep, now let me continue...")

# Function to get HTML content with retry mechanism
def get_html(url, par_headers, params=''):
    """Retrieves the HTML code of the page, taking into account connection errors."""
    while True:
        try:
            req = requests.get(url, headers=par_headers, params=params)
            break
        except Exception as e:
            handle_connection_error()
            logger.error("Error during request: %s", e)
    return req

# Function to get a page with error handling
def get_page(url):
    """Gets a page with error handling of the 503 status."""
    html = get_html(url, HEADERS)
    while html.status_code == 503:
        logger.info("Ошибка страница %s"
            "на данный момент недоступна! Код ошибки: %s"
            "Победа близка, продолжаем дальше!",
            url, str(html.status_code))
        time.sleep(10)
        html = get_html(url, HEADERS)
    return html

# Function to extract video URLs from HTML content
def get_content2(html):
    """Extracts video links from the HTML code."""
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='tiktok-x6y88p-DivItemContainerV2 '
                          'e1z53d07')
    videos = []

    for item in items:
        link_videos = item.find('div',
                                class_='tiktok-x6f6za-DivContainer-'
                                        'StyledDivContainerV2 e6ubv1j0').find(
            'div', class_='tiktok-yz6ijl-DivWrapper e1u9v4ua1'
        ).find('a').get('href')
        videos.append({'URL_Video_TikTok': link_videos})

    return videos

# Function to handle a new video upload
def uploaded_new_video(new_video):
    """Processes the download of a new video."""
    logger.info("Наконец-то! Пользователь %s опубликовал новое "
                "видео по ссылке: %s"
                " \nНажми пробел чтобы остановить музыку!\n",
                nik, new_video['URL_Video_TikTok'])
    pg.mixer.music.load('Sound/Sound.mp3')
    pg.mixer.music.play(loops=-1)
    with keyboard.Listener(on_release=on_release) as listener:
        listener.join()
    pg.mixer.music.stop()
    webbrowser.open_new_tab(new_video['URL_Video_TikTok'])

# Function for main parsing logic
def parser():
    """
    Checks the availability of the page to receive data and 
    performs parsing of new videos.
    """
    # Первый парсинг
    html = get_page(url_tiktok)
    if html.status_code != 200:
        logger.info("Ошибка №%s "
                    "при получении %s", html.status_code, url_tiktok)
    else:
        videos_first = get_content2(html.text)

    while True:
        logger.info("Парсим страницу: %s\n", url_tiktok)
        random.seed(str(datetime.datetime.now()))
        rand_time = random.uniform(10, 30)
        logger.info("ZZzzzz...timeout %s sec", rand_time)
        time.sleep(rand_time)

        html = get_page(url_tiktok)
        if html.status_code != 200:
            logger.info("Ошибка №%s при получении %s",
            html.status_code, url_tiktok)
        else:
            videos_second = get_content2(html.text)

            # Отладочные
            # print(videos_first[0])
            # print(videos_second[0])
            # print(len(videos_second))

            if videos_second and len(videos_second) > 0:
                if videos_first[0] != videos_second[0]:
                    uploaded_new_video(videos_second[0])
                else:
                    logger.info("Все как обычно ничего нового")
            else:
                logger.info("У пользователя %s "
                            "нету видео или вернулась пустая строка "
                            "попробуем еще...", nik)

# Function for keyboard listener 
def on_release(key):
    """Stops playing music by pressing the space bar."""
    if key == keyboard.Key.space:
        logger.info("Слежка за %s продолжилась...", nik)
        return False

# Main execution block
if __name__ == "__main__":
    try:
        parser()
    except KeyboardInterrupt:
        logger.warning("Прасинг прерван пользователем!")
    except Exception as e:
        logger.error("%s", e)
        traceback.print_tb(e.__traceback__)
