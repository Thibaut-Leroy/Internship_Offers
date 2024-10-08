import requests
import pandas as pd
from bs4 import BeautifulSoup
import datetime as dt
from datetime import datetime
from playwright.sync_api import sync_playwright

# Fonctions pour récuperer les offres de stages
def get_links_SG(url):
    with sync_playwright() as p:
        browser = p.webkit.launch(headless=True)  # headless=True pour exécuter en arrière-plan
        page = browser.new_page()
        page.goto(url)

        page.wait_for_selector('div.hit-overflow-wrapper')
        elements = page.query_selector_all('a.hit-text.display-block')
        offers_links = []
        for element in elements:
            link = element.get_attribute('href')
            offers_links.append("https://careers.societegenerale.com/" + link)
    return offers_links

def get_stage_offers_SG(url):

    banque = 'SG'
    response=requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    datas = soup.find_all('div', class_='entity-offer')
 
    offer_data = []
    for data in datas:
        bank = banque
        title = data.find('span', id='page_title')['data-value']
        contract = data.find('span', id='contract_type_id')['data-value']
        iso_date = data.find('span', id='startup_date')['data-value']
        dt_object = datetime.strptime(iso_date, "%Y-%m-%dT%H:%M:%SZ")
        beginning_date = dt_object.strftime("%d/%m/%Y")
        location = data.find('span', id='localisation_id')['data-value']
        link = url
            
        offer_data.append({
            'Banque' : bank,
            'Titre': title,
            'Contrat': contract,
            'Date de début': beginning_date,
            'Lieu': location,
            'Lien': link
            })
        
    offer_data = pd.DataFrame(offer_data)

    return offer_data   

def main_SG():
    df = pd.DataFrame(columns=['Banque','Titre','Contrat','Date de début','Lieu','Lien'])
    main_url_SG = "https://careers.societegenerale.com/rechercher?refinementList[jobType][0]=INTERNSHIP&refinementList[jobFunction][0]=KJ697"
    links = get_links_SG(main_url_SG)

    for link in links:
        offer = get_stage_offers_SG(link)
        a = pd.DataFrame(offer, columns=['Banque','Titre','Contrat','Date de début','Lieu','Lien'])
        df = pd.concat([df,a], ignore_index=True)

    print("SG Done")
    return df        

if __name__ == "__main__":
    main_SG()