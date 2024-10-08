from playwright.sync_api import sync_playwright
import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt

def get_links_CACIB(main_url_CACIB):
    with sync_playwright() as p:
        browser = p.webkit.launch(headless=True)
        page = browser.new_page()
        page.goto(main_url_CACIB)

        page.wait_for_selector('div.ts-offer-card.Layer')
        elements = page.query_selector_all('a.ts-offer-card__title-link')
        offers_links_CACIB = []
        for element in elements:
                link = element.get_attribute('href')
                offers_links_CACIB.append("https://jobs.ca-cib.com" + link)
        
        return offers_links_CACIB

def get_stage_offers_CACIB(url):
    with sync_playwright() as p:
        browser = p.webkit.launch(headless=True)
        page = browser.new_page()
        page.goto(url)

        page.wait_for_selector('div.ts-offer-page__content')
        datas = page.query_selector_all('div.ts-offer-page__block.ts-block.ts-block-1')
        datas2 = page.query_selector('div.ts-offer-page__block.ts-block.ts-block-2')

        banque = 'CACIB'
        offer_data = []

        for data in datas:
            bank = 'CACIB'
            title = data.query_selector('p#fldjobdescription_jobtitle').inner_text()
            contract = data.query_selector('p#fldjobdescription_contract').inner_text()
            
            try:
                beginning_date = data.query_selector('p#fldjobdescription_date1')
                if beginning_date:
                    beginning_date = beginning_date.inner_text()
            except AttributeError:
                pass

            link = url

            location = datas2.query_selector('p#fldlocation_location_geographicalareacollection').inner_text()

            offer_data.append({
                'Banque' : bank,
                'Titre': title,
                'Contrat': contract,
                'Date de début': beginning_date,
                'Lieu' : location,
                'Lien': link
            })

    offer_data = pd.DataFrame(offer_data)

    return offer_data

def main_CACIB():
    df = pd.DataFrame(columns=['Banque','Titre','Contrat','Date de début','Lieu','Lien'])
    main_url_CACIB = "https://jobs.ca-cib.com/offre-de-emploi/liste-offres.aspx?changefacet=1&facet_Contract=579"
    links = get_links_CACIB(main_url_CACIB)

    for link in links:
        offer = get_stage_offers_CACIB(link)
        a = pd.DataFrame(offer, columns=['Banque','Titre','Contrat','Date de début','Lieu','Lien'])
        df = pd.concat([df,a], ignore_index=False)

    print("CACIB Done")
    return df


if __name__ == "__main__":
    main_CACIB()