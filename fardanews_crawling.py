import requests
from bs4 import BeautifulSoup
from newspaper import Article
from tqdm import tqdm
import pandas as pd

def repetitive(links, urls):
    for link in links:
        if link.a['href'] in urls:
            return True
    return False

def scrap_year(year: int):
    """crawl data from website"""
    print('it is wokring')
    page = 0
    scraped_data = []
    url_list = []
    page_to_crawl = 'https://www.fardanews.com/newsstudios/archive/'

    while page < 300: # just in case of going too much
        page +=1 
        html = requests.get(page_to_crawl).text  # Download html of the page

        soup = BeautifulSoup(html, features='lxml')

        links = soup.find_all('h2')
        
        if repetitive(links, url_list):
            print('duplicate link so break')
            break
    
        for link in tqdm(links):
            page_url = 'https://fardanews.com/' + link.a['href']
            url_list.append(link.a['href'])
            try:
                article = Article(page_url)
                article.download()
                article.parse()
                scraped_data.append({'url': page_url, 'text': article.text, 'title': article.title})
            except:
                print(f"Failed to process page: {page_url}")
                
        # find next page url by its footer tag
        next_page_tag = soup.find('footer')
        # ic(next_page_tag)
        next_page_url = next_page_tag.find_all('a')[-1]['href']
        
        if next_page_url:
            page_to_crawl = 'https://fardanews.com/' +  next_page_url
        
    
    df = pd.DataFrame(scraped_data)
    # TODO: pick one
    # df.to_excel(f'fardanews2-{year}.xlsx')
    df.to_csv(f'fardanews2-{year}.csv')


if __name__ == '__main__':
    scrap_year(1400)
    
    