# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 18:50:01 2023

@author: admin
"""
from bs4 import BeautifulSoup
import requests

def search_idefix_by_title_or_isbn(titleOrIsbn):
    search_url = f"https://www.idefix.com/search/?q={titleOrIsbn}&cat=0"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.content, "html.parser")
    # İlk kitabın URL'sini al
    try:
        first_book_url = soup.find("div", class_="cart-product-box-view").find("a")["href"]
        book_page_response = requests.get("https://www.idefix.com" + first_book_url)
        book_page_soup = BeautifulSoup(book_page_response.content, "html.parser")
        
        # Kitap adı
        book_title =  book_page_soup.find("div", {"class": "product-info-list"}).find("span", text="Kitap Adı:").find_next_sibling("a").text
        # Yazar adı
        book_author =  book_page_soup.find("div", {"class": "product-info-list"}).find("span", text="Yazar: ").find_next_sibling("span").find("a").text    
        # Fiyat
        book_price = book_page_soup.find("div", class_="current-price").text.replace("TL","").strip()
        # ISBN
        book_isbn13 = book_page_soup.find("div", {"class": "product-info-list"}).find("span", text="Barkod:").find_next_sibling("a").text
    
        data = {"authors": book_author,"title": book_title, "price": book_price, "isbn13": book_isbn13}
        return data
    except:
        return None  
    
    
def search_dr_by_title_or_isbn(titleOrIsbn):
    search_url = f"https://www.dr.com.tr/search/?q={titleOrIsbn}&cat=0"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    # İlk kitabın URL'sini al
    try:
        first_book_url = soup.find("div", class_="prd-content-wrapper").find("a")["href"]
        book_page_response = requests.get("https://www.dr.com.tr" + first_book_url)
        book_page_soup = BeautifulSoup(book_page_response.content, "html.parser")
   
        # Kitap adı
        book_title =  book_page_soup.find("div", {"class": "product-property"}).find("strong", text=" Kitap Adı").find_next_sibling("span").text.strip()
        # Yazar adı
        book_author =  book_page_soup.find("div", {"class": "product-property"}).find("strong", text=" Yazar").find_next_sibling("span").text.strip()    
        # Fiyat
        book_price = book_page_soup.find("div", class_="salePrice").find("span").text.replace("TL","").strip()
        # ISBN
        book_isbn13 = book_page_soup.find("div", {"class": "product-property"}).find("strong", text=" Barkod").find_next_sibling("span").text.strip()
        
        data = {"authors": book_author,"title": book_title, "price": book_price, "isbn13": book_isbn13}
        return data                      
    except:
        return None
    