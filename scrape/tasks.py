from selenium import webdriver
from selenium.webdriver.support.ui import Select
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime, timedelta
from django.utils import timezone
from bs4 import BeautifulSoup

from stock_scrape import celery_app
from .models import Stock, StockRecord


@celery_app.task
def add(x, y):
    time.sleep(5)
    return x + y


option = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}

option.add_experimental_option("prefs", prefs)

option.add_argument(
    "user-agent=Mozilla/5.0 (X11; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.")
option.add_argument('headless')


days = 180
date_to = datetime.now().date()
date_from = (date_to-timedelta(days=days))
print(date_to, date_from)

with open('scrape/symbols.json') as f:
    symbols_json = json.load(f)

@celery_app.task
def scrape(symbol,date_from=date_from,date_to=date_to):
    try:
        driver = None
        if symbol not in symbols_json['symbols']:
            raise Exception(f"Symbol {symbol} doesn't exist!")
        driver = webdriver.Chrome(options=option)

        print(f"Started extracting {symbol}.. ")

        url = f'https://www.nepalipaisa.com/CompanyDetail.aspx?quote={symbol}'
        driver.get(url)
        driver.find_element_by_id('nav-pricehistory').click()
        date_from_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "txtFromDate"))
        )
        date_from_input.clear()
        date_from_input.send_keys(str(date_from))
        driver.find_element_by_id('txtToDate').clear()
        driver.find_element_by_id('txtToDate').send_keys(str(date_to))
        driver.find_element_by_id('btnSearchPriceHistory').click()
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        table = soup.find('table', {'id': 'tblFloorList'})

        tbody = table.find('tbody')
        rows = tbody.find_all('tr')

        records = []

        print(f"Writing to {symbol}-{str(date_from)}-{str(date_to)}...")

        stock,created = Stock.objects.get_or_create(name=symbol)
        stock.updated_at = timedelta(days = -1)

        for row in rows:

            cols = row.find_all('td')
            cols = [ele.label.text.strip() for ele in cols]
        
            if not created:
                StockRecord.objects.filter(stock=stock).delete()

            record = StockRecord(**create_records_array_to_dict(cols),stock=stock)
            records.append(record)
        
        created = StockRecord.objects.bulk_create(records)
 
        stock.state = 'ready'
        stock.updated_at = timezone.now()

        stock.save()
        print(f"Write Complete {symbol}-{str(date_from)}-{str(date_to)}...")
  

    except Exception as e:
        print(e)
    finally:
        if driver:
            driver.close()
        print(f"Closed Driver for {symbol}")


def create_records_array_to_dict(data):
    record_to_model_map = {
        1: 'date',
        2: 'transactions_num',
        3: 'max_price',
        4: 'min_price',
        5: 'close_price',
        6: 'traded_shares',
        7: 'total_amt',
        8: 'prev_close',
    }
    mappings = {}
    mappings['date'] = datetime.strptime(data[1],'%Y-%m-%d')
    for i,val in enumerate(data[2:9]):
        mappings[record_to_model_map[i+2]] = float(val)
    mappings[record_to_model_map[6]] = int(mappings[record_to_model_map[6]])
    return mappings
    
@celery_app.task
def scrape_all_symbols(symbols):
    n = int(.2 *len(symbols))
    print(n)
    scrape.chunks(zip(symbols),n)()
    
