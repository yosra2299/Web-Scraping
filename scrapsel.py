from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import datetime

def xpath_element (xpath):
    try:
       element = driver.find_element(By.XPATH,xpath)
    except NoSuchElementException :
        element =[]
    return element



    return element

def real_time_price(stock_code):
    url='https://www.ilboursa.com/marches/cotation_'& stock_code

    driver.get(url)
    ################ price
    xpath='//*[@id="cot1c"]/div[2]/div[2]'
    stock_price_info = xpath_element (xpath)

    if stock_price_info != []:
        stock_price_temp =stock_price_info.text.split()[0]
        if stock_price_temp.find('+')!=-1:
            price= stock_price_temp.split('+')[0]
            try:
                change = '+' + stock_price_temp.split('+')[1] +' '+stock_price_info.text.split()[1]
            except IndexError:
                change=[]
        elif stock_price_temp.find('-')!=-1:
            price = stock_price_temp.split('-')[0]
            try:
               change = '-' + stock_price_temp.split('-')[1] + ' ' + stock_price_info.text.split()[1]
            except IndexError:
                change = []
        else:
            price, change = [], []
    else:
        price,change=[],[]
################## volume
    xpath='//*[@id="quote-summary"]/div[1]'
    volume_temp=xpath_element(xpath)

    if volume_temp != []:
        #approach 1
        #volume= volume_temp.text.split()[-4]
        #approach 2 : search for volume no matter the place
        for i, text in enumerate(volume_temp.text.split()):
            if text == 'Volume':
                volume=volume_temp.text.split()[i+1] # the next index contains the value
                break
            else :
                volume=[]
    else:
        volume=[]

        ################## one year target
    xpath='//*[@id="quote-summary"]/div[2]'
    target_temp=xpath_element(xpath)
    if target_temp != []:
    # approach 1
    # one_year_target= volume_temp.text.split()[-1]
    # approach 2 : search for est no matter the place
        for i, text in enumerate(target_temp.text.split()):
            if text == 'Est':
                if target_temp.text.split()[i+1] != 'N/A':
                   one_year_target = target_temp.text.split()[i + 1]  # the next index contains the value
                   break
                else :
                   one_year_target=[]

            else:
              one_year_target = []
    else:
        one_year_target = []
        ################## latest patten
    latest_pattern=[]
    ##################

    return price, change , volume , latest_pattern , one_year_target


chrome_options = Options()
chrome_options.add_argument("--headless") #not show the chrome window
PATH = "C:\\Users\\Dell\\Desktop\\chromedriver.exe"
driver = webdriver.Chrome(PATH,options=chrome_options)


Stock=['AAPL']
while (True):
    info=[]
    #shift to us time 7 hours ahead from tunisia
    time_stamp = datetime.datetime.now()-datetime.timedelta(hours=7)
    time_stamp=time_stamp.strftime("%Y-%m-%d %H:%M:%S")
    for stock_code in Stock :
        price, change, volume, latest_pattern, one_year_target = real_time_price(stock_code)
        info.append(price)
        info.extend([change])
        info.extend([volume])
        info.extend([latest_pattern])
        info.extend([one_year_target])
    col=[time_stamp]
    col.extend(info)
    df=pd.DataFrame(col)
    df=df.T

pd.df_csv()

driver.quit()
