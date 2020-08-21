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
        if (page == 2):
            break;
        url = base_url + url_part + str(page)
        browser.visit(url)
        div_list = soup.find_all('div',class_='vehicle-cardstyles__InfoWrap-sc-1bxv5iu-1 bEIKmT')
        for div in div_list:
            car_list.append(base_url +div.find('a')['href'])

        time.sleep(0.25)

    return car_list

def insert(df, row):
    insert_loc = df.index.max()

    if pd.isna(insert_loc):
        df.loc[0] = row
    else:
        df.loc[insert_loc + 1] = row

def extract_data(soup, df):
    make = soup.find('h1').text 
    model = soup.find('p',class_='sc-hZSUBg ggtemb').text.split(' ')[1]
    reg_year = soup.find('li',class_='key-features-and-iconsstyles__KeyFeature-sc-13a1tsx-2 inYPYT').find_all('p')[1].text
    meleage = soup.find_all('li',class_='key-features-and-iconsstyles__KeyFeature-sc-13a1tsx-2 inYPYT')[1].find_all('p')[1].text
    fuel_type = soup.find_all('li',class_='key-features-and-iconsstyles__KeyFeature-sc-13a1tsx-2 inYPYT')[2].find_all('p')[1].text
    transmission = soup.find_all('li',class_='key-features-and-iconsstyles__KeyFeature-sc-13a1tsx-2 inYPYT')[3].find_all('p')[1].text
    seats = soup.find_all('li',class_='key-features-and-iconsstyles__KeyFeature-sc-13a1tsx-2 inYPYT')[4].find_all('p')[1].text
    engine  = soup.find_all('li',class_='key-features-and-iconsstyles__KeyFeature-sc-13a1tsx-2 inYPYT')[5].find_all('p')[1].text
    body_type = soup.find("div", {"data-test-id" : "Body type"}).find('dd').text.split(' ')[-1]
    doors = soup.find("div", {"data-test-id" : "Body type"}).find('dd').text.split(' ')[0]
    Gearbox = soup.find("div", {"data-test-id" : "Gearbox"}).find('dd').text.split(' ')[0][:-1]
    Registration = soup.find("div", {"data-test-id" : "Registration number"}).find('dd').text
    number_keys = soup.find("div", {"data-test-id" : "Number of keys"}).find('dd').text
    ext_color = soup.find("div", {"data-test-id" : "Exterior colour"}).find('dd').text
    drive_type = soup.find("div", {"data-test-id" : "Drive type"}).find('dd').text
    prev_owners = soup.find("div", {"data-test-id" : "Previous owners"}).find('dd').text
    car_ext_features_list = soup.find(id = 'exterior-features').find_all('li')
    car_ext_list = ''
    for feature in car_ext_features_list:
        car_ext_list =  f"{car_ext_list} '{feature.text}'"   

    car_int_features_list = soup.find(id = 'interior-features').find_all('li')
    car_int_list = ''
    for feature in car_int_features_list:
        car_int_list = f"{car_int_list} '{feature.text}'"

    top_speed = soup.find("div", {"data-test-id" : "Top speed"}).find('dd').text
    acceleration = soup.find("div", {"data-test-id" : "Acceleration (0-62 mph)"}).find('dd').text
    engine_power = soup.find("div", {"data-test-id" : "Engine power"}).find('dd').text
    length = soup.find("div", {"data-test-id" : "Length"}).find('dd').text
    fuel_cap = soup.find("div", {"data-test-id" : "Fuel tank capacity"}).find('dd').text
    boot_cap = soup.find("div", {"data-test-id" : "Boot space (seats-up)"}).find('dd').text 
    insert(df,[make,model,reg_year,meleage,fuel_type,transmission,seats,engine,body_type,doors,Gearbox,Registration,number_keys,ext_color,drive_type,prev_owners,car_ext_list,car_int_list,top_speed,acceleration,engine_power,length,fuel_cap,boot_cap])


def scrape():
    df = pd.DataFrame(columns=['make','model','reg_year','meleage','fuel_type','transmission','seats','engine','body_type','doors','Gearbox','Registration','number_keys','ext_color','drive_type','prev_owners','car_ext_list','car_int_list','top_speed','acceleration','engine_power','length','fuel_cap','boot_cap'])
    url_list = get_car_url_list()
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    for url in url_list:
        browser.visit(url)
        soup = BeautifulSoup(browser.html,'html.parser')
        time.sleep(0.25)
        extract_data(soup, df)  
    browser.quit()    
    df.to_csv('export.csv',index = False)
    # return df.to_html()






