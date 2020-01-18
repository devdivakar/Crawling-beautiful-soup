from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import requests
import sys
import pandas as pd
import uuid
import json
from models import crawler_master,crawler_result
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from configuration import config
from configuration import config
from models import crawler_result, crawler_master
from db_functions import save_data_from_csv_format


CRAWL_SITE = 'https://www.cardekho.com'



def get_car_dekho_reviews_rating(url,crawl_id,added_by,uuid,client_name,crawler_site,product_name):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    rating=list(soup.find_all(class_="ratingvalue")[0].children)[0]
    reviews=list(soup.find_all(class_="reviews")[0].children)[0].split()[0]
    jsondata = json.dumps({'rating':rating,'review':reviews})
    crawl_rslt = {'crawler_id':crawl_id,'crawler_result':jsondata,'uuid':uuid,'client_name':client_name,'added_by':'added_by','crawl_timestamp' : str(datetime.now(timezone.utc)),'crawler_site':crawler_site,'product_name':product_name}
    return crawl_rslt  


def get_crawl_params():
    engine = create_engine(config["sql_url"])
    Session = sessionmaker(bind=engine)
    session = Session()
    crawl_parameters_raw = session.query(crawler_master).filter(crawler_master.crawler_site==CRAWL_SITE)
    return crawl_parameters_raw


if __name__ == "__main__":
    crawl_parameters_raw = get_crawl_params()
    overall_rating_review = []
    for i in crawl_parameters_raw:
        crawl_parameters = i.__dict__
        row = get_car_dekho_reviews_rating(crawl_parameters['crawler_url'],crawl_parameters['id'],'added_by',str(uuid.uuid4()),crawl_parameters['client_name'],crawl_parameters['crawler_site'],crawl_parameters['product_name'])
        overall_rating_review.append(row)
    df = pd.DataFrame(overall_rating_review)
    save_data_from_csv_format(df)

