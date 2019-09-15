from googletrans import Translator
from googlesearch import search
import requests
from bs4 import BeautifulSoup
from typing import List
import re
import json

class marcoSearch:
    def __init__(self, languages: List[str]) -> None:
        self.translator = Translator()
        self.languages = languages
        if 'en' not in self.languages:
            self.languages.append('en')

    def translate_string(self, list_of_strings: List[str] , destination_language: str) -> List[str]:
        if type(list_of_strings) != list:
            list_of_strings = [list_of_strings]
        translations = self.translator.translate(list_of_strings, dest = destination_language)
        translated_strings = [s.text for s in translations]
        #translated_strings = translations.text
        return(translated_strings)

    def search_single_query(self, query: str) -> dict:
        url_dict = {}
        for lang in self.languages:
            url_dict[lang] = []
            curr_query = self.translate_string(query, destination_language = lang)
            url_dict[lang].extend(search(query= curr_query[0], tld='com', lang=lang, num= 10, stop= 10))
        return(url_dict)

    def parse_page(self, url: str, translate: bool = True) -> List[str]:
        page = requests.get(url = url)
        soup = BeautifulSoup(page.text, 'html.parser')
        texts = [v.get_text() for v in soup.find_all('p')]
        texts = list(map(self.clean_text, texts))
        texts = list(filter(lambda x: x != '', texts))
        if translate:
            translated_texts = self.translate_string(texts, destination_language = 'en')
            return(translated_texts)
        else:
            return(texts)

    def search_query(self, query: str) -> List[str]:
        print('Retrieving URLs')
        url_dict = self.search_single_query(query)
        docs = {}
        docs['en'] = [self.parse_page(url = u, translate = False) for u in url_dict['en']]
        #print(docs)
        print('Translating pages')
        for lang in url_dict:
            if lang != 'en':
                docs[lang] = []
                docs[lang].extend([self.parse_page(url = u) for u in url_dict[lang]])
        return(docs)

    @staticmethod
    def clean_text(html_text: str) -> str:
        clean_text = re.sub('<.*>', '', html_text)
        return(clean_text)

    @staticmethod
    def get_marco_vectors(strings: List[str]) -> List[dict]:
        query = 'curl https: // api.msturing.org/gen/encode - H "Ocp-Apim-Subscription-Key: 9b6108ed020a4e9e85449bd398f0fdd8" - -data \'{"queries":'
        strings = ','.join(strings)
        strings = '[' + strings + ']'
        query = query + strings + '}\''
        result = subprocess.check_output(st, shell=True)
        result_json = json.loads(result)
        return(result_json)