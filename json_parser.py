import requests
from bs4 import BeautifulSoup
import lxml
import csv


def get_html(url):
    r = requests.get(url)
    return r


def write_csv(data):
    with open('to_csv.csv', 'a', encoding='utf-8') as f:
        order = ['name', 'url']
        writer = csv.DictWriter(f, fieldnames=order)
        writer.writerow(data)


def get_page_data(response):
    if 'html' in response.headers['Content-Type']:
        html = response.text
    else:
        html = response.json()['content_html']

    soup = BeautifulSoup(html, 'lxml')

    items = soup.find_all('h3', class_='yt-lockup-title')

    for item in items:
        name = item.text.strip()
        url = 'https://www.youtube.com/user/coolpropaganda/videos' + item.find('a').get('href')

        data = {'name': name,
                'url': url}

        write_csv(data)


def get_next(response):
    if 'html' in response.headers['Content-Type']:
        html = response.text
    else:
        html = response.json()['load_more_widget_html']

    soup = BeautifulSoup(html, 'lxml')

    try:
        url = 'https://www.youtube.com' + soup.find('button', class_='load-more-button').get('data-uix-load-more-href')
    except:
        url = ''

    return url


def main():
    url = 'https://www.youtube.com/user/coolpropaganda/videos'

    while True:
        response = get_html(url)
        get_page_data(response)

        url = get_next(response)

        if url:
            continue
        else:
            break


if __name__ == '__main__':
    main()
