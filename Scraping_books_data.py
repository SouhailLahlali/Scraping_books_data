import requests
from bs4 import BeautifulSoup
import pandas as pd
titles,prices,number_stars=[],[],[]
def get_data(index):
    titles,prices,number_stars=[],[],[]
    url=f'https://books.toscrape.com/catalogue/page-{index}.html'
    response=requests.get(url)
    if response.status_code==200:
        #Request was successful !
        html=response.text
        soup=BeautifulSoup(html,'lxml')
        titles=get_book_titles(soup)
        prices=get_book_price(soup)
        number_stars=get_book_stars_ratings(soup)
        return [titles,prices,number_stars]
    else:
        #Request failed !
        return f'Request failed with status code {response.status_code}'

def get_book_titles(soup):
    list_titles=[]
    list_tags=soup.find_all('h3')
    for tag in list_tags:
        title= tag.find('a')['title']
        list_titles.append(title)
    return list_titles

def get_book_price(soup):
    list_prices=[]
    list_tags=soup.find_all('div',class_='product_price')
    for tag in list_tags:
        price=tag.find('p',class_='price_color')
        for p in price:
            list_prices.append(p.text[1:])
    return list_prices

def get_book_stars_ratings(soup):
    list_stars=[]
    list_tags=soup.find_all('p',class_='star-rating')
    for stars in list_tags:
        number_stars=stars.attrs['class'][-1]
        list_stars.append(number_stars)
    return list_stars




def save_data():
    data={
    'Titles':[],
    'Prices':[],
    'Number_stars':[]
    }
    for i in range(1,51):
        get_data(i)
        data['Titles'].extend(get_data(i)[0])
        data['Prices'].extend(get_data(i)[1])
        data['Number_stars'].extend(get_data(i)[2])
    df=pd.DataFrame(data,columns=['Titles','Prices','Number_stars'])
    df.to_csv("books_data.csv",index=False,header=True)
    
save_data()
