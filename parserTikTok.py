import requests
from bs4 import BeautifulSoup
import traceback
import time
import random
import pygame as pg
from pynput import keyboard
import webbrowser
import os
import datetime
import logging
import sys 


#sys.setrecursionlimit(99999)
pg.init()
logging.basicConfig(filename="Output.log", level=logging.INFO)
logging.info(str(datetime.datetime.now()) + " | " + "=========================New START")
#cls linux
cls = lambda: os.system('cls' if os.name == 'nt' else 'clear') 
cls()

nik = input("Введите ник пользователя TikTok без @: ")
URL_TikTok = 'https://www.tiktok.com/@' + nik
logging.info(str(datetime.datetime.now()) + " | " + "Введите ник пользователя TikTok без @: " + nik)
# proxies = {
#   "http": "http://50.206.25.106:80",
#   "https": "https://98.12.195.129:443",
# }


def on_release(key):
    if key == keyboard.Key.space:
        print("Слежка за " + nik + " продолжилась...\n")
        logging.info(str(datetime.datetime.now()) + " | " + "Слежка за " + nik + " продолжилась...")
        # Stop listener
        return False

videos_first = []
videos_second = []

HEADERS = {
    'accept': '*/*',
    'accept-language': 'ru,en;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.50'
}

def get_content2(html):
    soup = BeautifulSoup(html, 'html.parser')
    #items1 = soup.find_all('div', class_='tiktok-1qb12g8-DivThreeColumnContainer e140s4uj2')
    items = soup.find_all('div', class_='tiktok-x6y88p-DivItemContainerV2 e1z53d07')
    #print(items)
    videos = []


    for i in range(len(items)):

        link_videos = items[i].find('div', class_='tiktok-x6f6za-DivContainer-StyledDivContainerV2 e6ubv1j0').find('div', class_='tiktok-yz6ijl-DivWrapper e1u9v4ua1').find('a').get('href')
        
        # add
        videos.append({'URL_Video_TikTok': link_videos})

    return videos

def get_html(url, par_headers, params=''):
    while True:
        try:
            req = requests.get(url, headers=par_headers, params=params)
            break
        except: 
            print("Connection refused by the server..")
            logging.info(str(datetime.datetime.now()) + " | " + "Connection refused by the server..")

            random.seed(str(datetime.datetime.now()))
            rand_rime = random.uniform(10, 30)

            print(f"Let me sleep for {str(rand_rime)} seconds")
            logging.info(str(datetime.datetime.now()) + " | " + f"Let me sleep for {str(rand_rime)} seconds")
            print("ZZzzzz...")
            logging.info(str(datetime.datetime.now()) + " | " + "ZZzzzz...")
            
            time.sleep(rand_rime)

            print("Was a nice sleep, now let me continue...")
            logging.info(str(datetime.datetime.now()) + " | " + "Was a nice sleep, now let me continue...")
    
    return req

def get_page(url):
    html = get_html(url, HEADERS)
    while(html.status_code == 503):
        print('\nОшибка страница ' + url + ' на данный момент недоступна! Код ошибки: '+ str(html.status_code) +' Победа близка, продолжаем дальше!\n')
        logging.info(str(datetime.datetime.now()) + " | " + 'Ошибка страница ' + url + ' на данный момент недоступна! Код ошибки: '+ str(html.status_code) +' Победа близка, продолжаем дальше!')
        time.sleep(10)
        html = get_html(url, HEADERS)
    return html

def Uploaded_New_Video(New_video):
    print("Наконец-то! Пользователь " + nik + " опубликовал новое видео по ссылке: " + New_video['URL_Video_TikTok'] + " \nНажми пробел чтобы остановить музыку!\n")
    logging.info(str(datetime.datetime.now()) + " | " + "Наконец-то! Пользователь " + nik + " опубликовал новое видео по ссылке: " + New_video['URL_Video_TikTok'] + " \nНажми пробел чтобы остановить музыку!\n")
    pg.mixer.music.load('Sound/Sound.mp3')
    pg.mixer.music.play(loops = -1)
    with keyboard.Listener(on_release=on_release) as listener:
        listener.join()    
    pg.mixer.music.stop()
    webbrowser.open_new_tab(New_video['URL_Video_TikTok'])

def parser():
    #Проверка страниц на доступность получения данных
    global videos_first
    global videos_second
    global URL_TikTok
    New_video = False
    html = get_page(URL_TikTok)
    #Первый парсинг
    if html.status_code != 200:
        print(f'Ошибка №{html.status_code} при получении {URL_TikTok}')
        logging.info(str(datetime.datetime.now()) + " | " + f'Ошибка №{html.status_code} при получении {URL_TikTok}')
    else:
        videos_first = get_content2(html.text)
    
    while(not New_video):
        # cls()
        print(f'\nПарсим страницу: {URL_TikTok}\n')
        logging.info(str(datetime.datetime.now()) + " | " + f'Парсим страницу: {URL_TikTok}\n')
        random.seed(str(datetime.datetime.now()))
        rand_rime = random.uniform(10, 30)
        print("ZZzzzz...timeout " + str(rand_rime) + " sec")
        logging.info(str(datetime.datetime.now()) + " | " + "ZZzzzz...timeout " + str(rand_rime) + " sec")
        time.sleep(rand_rime)
        html = get_page(URL_TikTok)

        if html.status_code != 200:
            print(f'Ошибка №{html.status_code} при получении {URL_TikTok}')
            logging.info(str(datetime.datetime.now()) + " | " + f'Ошибка №{html.status_code} при получении {URL_TikTok}')
        else:
            videos_second = get_content2(html.text)

            # Отладочные
            #print(videos_first[0])
            #print(videos_second[0])
            #print(len(videos_second))
            
            if ((videos_second != None) and (videos_second != []) and (len(videos_second) != 0)):
                if (videos_first[0] != videos_second[0]):
                    Uploaded_New_Video(videos_second[0])
                    New_video = True
                else:
                    print("Все как обычно ничего нового\n")
                    logging.info(str(datetime.datetime.now()) + " | " + "Все как обычно ничего нового")
            else:
                print("У пользователя " + nik + " нету видео или вернулась пустая строка попробуем еще...\n")
                logging.info(str(datetime.datetime.now()) + " | " + "У пользователя " + nik + " нету видео или вернулась пустая строка попробуем еще...")

try:
    while True:
        parser()
except KeyboardInterrupt:
    print('Прасинг прерван пользователем!')
    logging.warning(str(datetime.datetime.now()) + " | " + 'Прасинг прерван пользователем!')
except Exception as E:
    print(E)
    logging.error(str(datetime.datetime.now()) + " | " + E)
    traceback.print_tb(E.__traceback__)