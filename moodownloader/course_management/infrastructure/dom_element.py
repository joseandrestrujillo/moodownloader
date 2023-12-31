from bs4 import BeautifulSoup
from typing import List, Dict

from ..domain.element import Element


class DomElement(Element):
    def __init__(self, soup: BeautifulSoup) -> None:
        self.soup = soup
        self.text = self.soup.text
    
    def _convert_soup_into_dom_element(self, soup: BeautifulSoup) -> "DomElement":
        return DomElement(soup)


    def find_all(self, tag: str, params: Dict) -> List["DomElement"]:
        soups = self.soup.find_all(tag, params)
        
        res = []
        for soup in soups:
            res.append(self._convert_soup_into_dom_element(soup))

        return res
    
    
    def find(self, tag: str, params: Dict) -> "Element":
        return self._convert_soup_into_dom_element(self.soup.find(tag, params))
    
    def __getattr__(self, name):
        return self.soup[name]

    