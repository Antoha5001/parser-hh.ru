import time
import requests
from bs4 import BeautifulSoup as bs
import pprint

header = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
}
keyword = 'Повар'
base_url = f'https://novosibirsk.hh.ru/search/vacancy?L_is_autosearch=false&area=4&clusters=true&enable_snippets=true&text={keyword}&page=0'

def getFind(obj, elem, attr,  valueAttr):
    try:
       bsObj = obj.find(elem, {attr: valueAttr}).text
       return bsObj
    except:
        return 'не указано'

def getCardText(card):

    href = card.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})['href']
    # Поиск контактных данных на странице с вакансией
    card_request = requests.get(href, headers=header)

    if card_request.status_code == 200:
        card_html = bs(card_request.content, 'lxml')
        # contact_person = card_html.find('p', {'data-qa': 'vacancy-contacts__fio'}).text
        contact_person = getFind(card_html, 'p', 'data-qa', 'vacancy-contacts__fio')
        contact_phone = getFind(card_html, 'p', 'data-qa', 'vacancy-contacts__phone')

        try:
            contact_mob = card_html.find_all('p', {'data-qa': 'vacancy-contacts__phone'})[1].text
        except:
            contact_mob = 'не указано'
        try:
            contact_email = card_html.find('a', {'data-qa': 'vacancy-contacts__email'}).text
        except:
            contact_email = 'не указано'
        # print(contact_person)

        # title = card.find('a', {'data-qa': 'vacancy-serp__vacancy-title'}).text
        title = getFind(card, 'a', 'data-qa', 'vacancy-serp__vacancy-title')
        pay = getFind(card, 'div', 'data-qa', 'vacancy-serp__vacancy-compensation')

        employer = card.find('a', {'data-qa': 'vacancy-serp__vacancy-employer'}).text or "Работадатель не указан"
        text1 = card.find('div', {'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}).text or "не указано"
        text2 = card.find('div', {'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}).text or "не указано"
        cardInfo = f"""{title}
Работодатель: {employer}
Зарплата: {pay}
{text1}
Требование: {text2}
Контактная информация: {contact_person}
тел.: {contact_phone}
моб.: {contact_mob}
e-mail: {contact_email}\n"""

   # else:
        #cardInfo = "Что то не так"
        return cardInfo

def get_parse(base_url, headers):
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        urls = []
        start = time.time()
        soup = bs(request.content, 'lxml')
        # pager = soup.find('div', {'data-qa': 'pager-block'})
        last_page = soup.find_all('a', {'data-qa': 'pager-page'})[-1].text or '0'
        for ra in range(0, int(last_page)):
            url = f'https://novosibirsk.hh.ru/search/vacancy?L_is_autosearch=false&area=4&clusters=true&enable_snippets=true&text={keyword}&page={ra}'
            if url not in urls:
                urls.append(url)
            else:
                urls.append(base_url)
        # print(urls)
        for url in urls:
            cards = soup.find_all('div', {'data-qa': 'vacancy-serp__vacancy'})
            # print(f"{url}")
            for card in cards:
                print(getCardText(card))
                # return

    else:
        print('Error123')
get_parse(base_url, header)