# TikTok User Tracker

Проект "TikTok User Tracker" представляет собой эффективный инструмент, разработанный для мониторинга активности пользователей в популярной социальной сети TikTok. Этот скрипт обеспечивает автоматизированное отслеживание видеоконтента пользователей, позволяя анализировать их активность с легкостью и эффективностью.

Благодаря данному инструменту вы можете получать уведомления о новых видеозаписях, отслеживать изменения в активности выбранных пользователей и анализировать их контент без необходимости постоянного вручную проверки страниц.

## Описание проекта

Данный скрипт позволяет отслеживать появления нового видео пользователя TikTok, а также выводить ссылки на эти видео для последующего анализа.

## Использование

1. Установите необходимые библиотеки, запустив следующую команду:
   pip install -r requirements.txt

2. Запустите скрипт parserTikTok.py:
   python parserTikTok.py
   
3. Введите имя пользователя TikTok без символа @.

4. Для остановки слежения нажмите пробел.

## Требования к окружению

- Python 3.x
- Библиотеки: requests, BeautifulSoup, pygame, pynput

## Примечания

- Скрипт будет записывать данные о своей работе в файл Output.log.
- При возникновении ошибок, вызванных недоступностью сервера, скрипт будет делать попытку повторного соединения через случайное время.


