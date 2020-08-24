#!/usr/bin/env python
# coding: utf-8

from bs4 import BeautifulSoup
import requests
from splinter import Browser
import time
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd



def get_car_url_list():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    base_url = 'https://www.cazoo.co.uk'
    url = 'https://www.cazoo.co.uk/used-cars/'
    car_list = []

    browser.visit(url)
    soup = BeautifulSoup(browser.html,'html.parser')
    next_page = soup.findAll('a', class_='paginationstyles__StyledPaginationItem-sc-1pjwu78-1')
    page_count = int(next_page[-2]['href'][-2:])
    url_part = next_page[-2]['href'][:-2]


    for page in range(1,page_count+1):
        # if page ==  2:
        #     break
        url = base_url + url_part + str(page)
        browser.visit(url)
        div_list = soup.find_all('div',class_='vehicle-cardstyles__InfoWrap-sc-1bxv5iu-1 bEIKmT')
        for div in div_list:
            car_list.append(base_url +div.find('a')['href'])

        time.sleep(0.5)

    return car_list

def insert(df, row):
    insert_loc = df.index.max()

    if pd.isna(insert_loc):
        df.loc[0] = row
    else:
        df.loc[insert_loc + 1] = row

def extract_data(soup, df):

    v = soup.find('h1')
    make = ''
    if(v):
        make = v.text

    v = soup.find('p',class_='sc-hZSUBg ggtemb')
    model = ''
    if(v):
        model = v.text.split(' ')[1]

    v = soup.find('li',class_='key-features-and-iconsstyles__KeyFeature-sc-13a1tsx-2 inYPYT')
    reg_year = ''
    if(v):
        reg_year = v.find_all('p')[1].text

    v = soup.find_all('li',class_='key-features-and-iconsstyles__KeyFeature-sc-13a1tsx-2 inYPYT')
    meleage = ''
    fuel_type = '' 
    transmission = ''  
    seats = '' 
    engine = ''
    if(v):
        meleage = v[1].find_all('p')[1].text
        fuel_type = v[2].find_all('p')[1].text
        transmission = v[3].find_all('p')[1].text
        seats = v[4].find_all('p')[1].text
        engine = v[5].find_all('p')[1].text
    
    v = soup.find("div", {"data-test-id" : "summary-vehicle-history"})

    last_srv_date = ''
    last_srv_mile = ''
    if(v):
        hist_list = v.find_all('h3')
        if(hist_list):
            for hist in hist_list:                
                if hist.text == 'Last service':
                    p_list = hist.find_parent('div').find_all('p')
                    if len(p_list) == 1:
                        last_srv_date = hist.find_parent('div').find_all('p')[0].text
                    else:   
                        last_srv_date = hist.find_parent('div').find_all('p')[0].text
                        last_srv_mile = hist.find_parent('div').find_all('p')[1].text

    v = soup.find("div", {"data-test-id" : "Body type"})
    body_type = ''
    doors = ''    
    if(v):
        body_type = v.find('dd').text.split(' ')[-1]  
        doors = v.find('dd').text.split(' ')[0]

    v = soup.find("div", {"data-test-id" : "Gearbox"})
    Gearbox = ''
    if(v):
        Gearbox = v.find('dd').text.split(' ')[0][:-1]

    v = soup.find("div", {"data-test-id" : "Registration number"})
    Registration = ''

    if(v):
        Registration = v.find('dd').text

    v = soup.find("div", {"data-test-id" : "Number of keys"})
    number_keys = ''
    if(v):
        number_keys = v.find('dd').text

    v = soup.find("div", {"data-test-id" : "Exterior colour"})
    ext_color = ''
    if(v):
        ext_color = v.find('dd').text

    v = soup.find("div", {"data-test-id" : "Drive type"})
    drive_type = ''
    if(v):
        drive_type = v.find('dd').text

    v = soup.find("div", {"data-test-id" : "Previous owners"})
    prev_owners = ''
    if(v):
        prev_owners = v.find('dd').text

    car_ext_features_list = soup.find(id = 'exterior-features').find_all('li')
    car_ext_list = ''
    if(car_ext_features_list):
        for feature in car_ext_features_list:
            car_ext_list =  f"{car_ext_list} '{feature.text}'"   

    car_int_features_list = soup.find(id = 'interior-features').find_all('li')
    car_int_list = ''
    if(car_int_features_list):
        for feature in car_int_features_list:
            car_int_list = f"{car_int_list} '{feature.text}'"

    v = soup.find("div", {"data-test-id" : "Top speed"})
    top_speed = ''
    if(v):
        top_speed = v.find('dd').text

    v = soup.find("div", {"data-test-id" : "Acceleration (0-62 mph)"})
    acceleration = ''
    if(v):
        acceleration = v.find('dd').text

    v = soup.find("div", {"data-test-id" : "Engine power"})
    engine_power = ''
    if(v):
        engine_power = v.find('dd').text        

    v = soup.find("div", {"data-test-id" : "Length"})
    length = ''
    if(v):
        length = v.find('dd').text 

    v = soup.find("div", {"data-test-id" : "Fuel tank capacity"})
    fuel_cap = ''
    if(v):
        fuel_cap = v.find('dd').text 

    v = soup.find("div", {"data-test-id" : "Boot space (seats-up)"})
    boot_cap = ''
    if(v):
        boot_cap = v.find('dd').text 
      
    v = soup.find("img", {"data-test-id" : "default-hero-image"}) 
    
    image = '' 
    if(v):
        image = f"<img src='{v['src']}' width='100' height='80'>" 

    v = soup.find("p", class_='pricingstyles__PriceValue-sc-10yqv22-3')
    price = ''
    if(v):
        price = v.text   

    insert(df,[image,price,make,model,reg_year,meleage,fuel_type,transmission,seats,engine,body_type,doors,     \
        Gearbox,Registration,number_keys,ext_color,drive_type,prev_owners,car_ext_list,car_int_list,\
        top_speed,acceleration,engine_power,length,fuel_cap,boot_cap,last_srv_date,last_srv_mile])


def scrape():
    df = pd.DataFrame(columns=['image','price','make','model','reg_year','meleage','fuel_type','transmission','seats', \
        'engine','body_type','doors','Gearbox','Registration','number_keys','ext_color','drive_type',  \
        'prev_owners','car_ext_list','car_int_list','top_speed','acceleration','engine_power','length',\
        'fuel_cap','boot_cap','last_srv_date','last_srv_mile'])
    url_list = get_car_url_list()
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    for url in url_list:        
        try:
            browser.visit(url)
        except:
            continue

        soup = BeautifulSoup(browser.html,'html.parser')
        time.sleep(1)
        extract_data(soup, df)  
    browser.quit()    
    df.to_csv('export.csv',index = False)
    # return df.to_html()






