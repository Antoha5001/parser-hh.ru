import requests
from bs4 import BeautifulSoup as bs
import pprint

header = {
    'accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
}
keyword = 'Python'
base_url = f'https://novosibirsk.hh.ru/search/vacancy?L_is_autosearch=false&area=4&clusters=true&enable_snippets=true&text={keyword}&page=0'
def get_parse(base_url, headers):
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
       soup = bs(request.content, 'html.parser')
       cards = soup.find_all('div',{'data-qa' : 'vacancy-serp__vacancy'})
       for card in cards:
           title = card.find('a', {'data-qa':'vacancy-serp__vacancy-title'}).text
           href = card.find('a', {'data-qa':'vacancy-serp__vacancy-title'})['href']
           employer = card.find('a', {'data-qa':'vacancy-serp__vacancy-employer'}).text
           text1 = card.find('div', {'data-qa':'vacancy-serp__vacancy_snippet_responsibility'}).text
           text2 = card.find('div', {'data-qa':'vacancy-serp__vacancy_snippet_requirement'}).text
           content = f'{text1} {text2}'
           print(content)
    else:
        print('Error')
get_parse(base_url, header)