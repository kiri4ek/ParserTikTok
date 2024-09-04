import os
import datetime
import logging
import random
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

# Initialize Pygame
pg.init()

# Configure logging
logging.basicConfig(filename="Output.log", level=logging.INFO)
logging.info("%s | =========================New START",
    str(datetime.datetime.now()))

# Clear the console
cls = lambda: os.system('cls' if os.name == 'nt' else 'clear')
cls()

# Get user input
nik = input("Введите ник пользователя TikTok без @: ")
url_tiktok = URL_TIKTOK_PREFIX + nik
logging.info("%s |  Введите ник пользователя TikTok без @: %s",
    str(datetime.datetime.now()), nik)

# Function to handle connection errors
def handle_connection_error():
    """Handles server connection errors."""
    print("Connection refused by the server..")
    logging.info("%s | Connection refused by the server..",
        str(datetime.datetime.now()))

    random.seed(str(datetime.datetime.now()))
    rand_time = random.uniform(10, 30)

    print(f"Let me sleep for {str(rand_time)} seconds")
    logging.info("%s | Let me sleep for %s seconds", 
        str(datetime.datetime.now()), str(rand_time))
    print("ZZzzzz...")
    logging.info("%s | ZZzzzz...", str(datetime.datetime.now()))
    time.sleep(rand_time)

    print("Was a nice sleep, now let me continue...")
    logging.info("%s Was a nice sleep, now let me continue...",
        str(datetime.datetime.now()))

# Function to get HTML content with retry mechanism
def get_html(url, par_headers, params=''):
    """Retrieves the HTML code of the page, taking into account connection errors."""
    while True:
        try:
            req = requests.get(url, headers=par_headers, params=params)
            break
        except Exception as e:
            handle_connection_error()
            print(f"Error during request: {e}")
            logging.error("%s | Error during request: %s",
                str(datetime.datetime.now()), e)
    return req

# Function to get a page with error handling
def get_page(url):
    """Gets a page with error handling of the 503 status."""
    html = get_html(url, HEADERS)
    while html.status_code == 503:
        print('\nОшибка страница ' + url + ' на данный момент '
              'недоступна! Код ошибки: '+ str(html.status_code) + 
              ' Победа близка, продолжаем дальше!\n')
        logging.info("%s | Ошибка страница %s"
            "на данный момент недоступна! Код ошибки: %s"
            "Победа близка, продолжаем дальше!", str(datetime.datetime.now()), url, str(html.status_code))
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
    print("Наконец-то! Пользователь " + nik + " опубликовал новое "
          "видео по ссылке: " + new_video['URL_Video_TikTok'] + 
          " \nНажми пробел чтобы остановить музыку!\n")
    logging.info("%s | +"
                "Наконец-то! Пользователь %s опубликовал новое "
                "видео по ссылке: %s"
                " \nНажми пробел чтобы остановить музыку!\n",
                str(datetime.datetime.now()), nik, new_video['URL_Video_TikTok'])
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
        print(f'Ошибка №{html.status_code} при получении {url_tiktok}')
        logging.info("%s | Ошибка №%s "
                    "при получении %s",
                    datetime.datetime.now(), html.status_code, url_tiktok)
    else:
        videos_first = get_content2(html.text)

    while True:
        print(f'\nПарсим страницу: {url_tiktok}\n')
        logging.info("%s | Парсим страницу: "
                    "%s\n", datetime.datetime.now(), url_tiktok)
        random.seed(str(datetime.datetime.now()))
        rand_time = random.uniform(10, 30)
        print(f"ZZzzzz...timeout {rand_time} sec")
        logging.info("%s | ZZzzzz...timeout "
                    "%s sec", datetime.datetime.now(), rand_time)
        time.sleep(rand_time)

        html = get_page(url_tiktok)
        if html.status_code != 200:
            print(f'Ошибка №{html.status_code} при получении {url_tiktok}')
            logging.info("%s | Ошибка №%s "
                        "при получении %s",
                        datetime.datetime.now(), html.status_code, url_tiktok)
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
                    print("Все как обычно ничего нового\n")
                    logging.info("%s | Все как "
                                "обычно ничего нового",
                                datetime.datetime.now())
            else:
                print(f"У пользователя {nik} нету видео или вернулась "
                      "пустая строка попробуем еще...\n")
                logging.info("%s | У пользователя %s "
                            "нету видео или вернулась пустая строка "
                            "попробуем еще...", datetime.datetime.now(), nik)

# Function for keyboard listener 
def on_release(key):
    """Stops playing music by pressing the space bar."""
    if key == keyboard.Key.space:
        print("Слежка за " + nik + " продолжилась...\n")
        logging.info("%s | Слежка за %s продолжилась...",
                    str(datetime.datetime.now()), nik)
        return False

# Main execution block
if __name__ == "__main__":
    try:
        parser()
    except KeyboardInterrupt:
        print('Прасинг прерван пользователем!')
        logging.warning("%s | Прасинг прерван "
                        "пользователем!", datetime.datetime.now())
    except Exception as e:
        print(e)
        logging.error("%s | %s", datetime.datetime.now(), e)
        traceback.print_tb(e.__traceback__)
