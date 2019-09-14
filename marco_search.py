from googletrans import Translator
from googlesearch import search
import requests
from bs4 import BeautifulSoup
from typing import List

class marcoSearch:
    def __init__(self, languages: List[str]) -> None:
        self.translator = Translator()
        self.languages = languages
        if 'en' not in self.languages:
            self.languages.append('en')

    def translate_string(self, list_of_strings: List[str] , destination_language: str) -> List[str]:
        translations = translator.translate(list_of_strings, dest = destination_language)
        #translated_strings = [s.text for s in translations]
        translated_strings = translations.text
        return(translated_strings)

    def search_single_query(self, query: str) -> dict:
        url_dict = {}
        for lang in self.languages:
            url_dict[lang] = []
            curr_query = self.translate_string(query, destination_language = lang)
            url_dict[lang].extend(search(query= curr_query, tld='com', lang=lang, num= 10, stop= 10))
        return(url_dict)

    def parse_page(self, url: str, translate: bool = True) -> List[str]:
        page = requests.get(url = url)
        soup = BeautifulSoup(page.text, 'html.parser')
        texts = [v.get_text() for v in soup.find_all('p')]
        if translate:
            translated_texts = self.translate_string(texts)
            return(translated_texts)
        else:
            return(texts)

    def search_query(self, query: str) -> List[str]:
        url_dict = self.search_single_query(query)
        docs = [self.parse_page(url = u, translate = False) for u in url_dict['en']]
        for lang in url_dict:
            if lang != 'en':
                docs.extend(self.parse_page(url = u) for u in url_dict[lang])
        return(docs)
    
    



