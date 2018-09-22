import csv   
import xlsxwriter
import time 
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options 
from datetime import datetime  
from datetime import timedelta 

#112

def get_datestring(da):
    cur_year = da.year
    cur_month = da.month
    cur_day = da.day
    month = str(cur_month)
    month = month.zfill(2)
    day = str(cur_day)
    day = day.zfill(2)
    datestring = str(cur_year)+"-"+month+"-"+day
    return datestring
    
chrome_options = Options()  
chrome_options.add_argument("--headless")  


now = datetime.now()
after_two = datetime.now()+timedelta(days=2)

nowstring = get_datestring(now)
afterstring = get_datestring(after_two)



chrome_path = r"chromedriver.exe"
driver = webdriver.Chrome(chrome_path,chrome_options=chrome_options)
path="https://www.google.com/flights/#flt="
driver.get(path)


fields=[]
for h in range(1,113):
    fields.append(str(h))

timeout = 50
data=[]
workbook = xlsxwriter.Workbook("fights.xlsx")
worksheet = workbook.add_worksheet()
worksheet.write(0, 0, 'Start Airport')
worksheet.write(0, 1, 'Stop Airport')
worksheet.write(0, 2, 'Start Date')
worksheet.write(0, 3, 'Return Date')
worksheet.write(0, 4, 'Price')
worksheet.write(0, 5, 'Airline Name')
row_count = 1
with open("List Of All Airports In US.csv") as in_file:
    csv_reader = csv.DictReader(in_file, fieldnames=fields)
    for rep in range(1,114,2):
        state_name=""
        code=""
        count=0
        in_file.seek(0)
        for row in csv_reader:
            if count != 0:
                if count == 1:
                    state_name=row[str(rep)]
                    code=row[str(rep+1)]
                else:
                    airport_name = row[str(rep)]
                    airport_code = row[str(rep+1)]
                    if airport_name != "" and airport_code!="":
                        for trep in range(1,112,2):
                            if rep != trep:
                                tstate_name=""
                                tcode=""
                                tcount=0
                                in_file.seek(0)
                                for trow in csv_reader:
                                    if tcount != 0:
                                        if tcount == 1:
                                            tstate_name=trow[str(trep)]
                                            tcode=trow[str(trep+1)]
                                        else:
                                            tairport_name = trow[str(trep)]
                                            tairport_code = trow[str(trep+1)]
                                            if tairport_name != "" and tairport_code!="":
                                                url = "https://www.google.com/flights/#flt="+airport_code+"."+tairport_code+"."+nowstring+"*"+tairport_code+"."+airport_code+"."+afterstring+";c:USD;e:1;sd:1;t:f"
                                                driver.get(url)
                                                time.sleep(1)
                                                try:
                                                    best_list = driver.find_element_by_class_name("gws-flights-results__result-list")
                                                    top_air = best_list.find_elements_by_css_selector("li")[0]

                                                    airline_contain = top_air.find_element_by_css_selector("div > div.gws-flights-widgets-expandablecard__header.gws-flights-results__itinerary-card-header > div.gws-flights-results__itinerary-card-summary.gws-flights-results__result-item-summary.gws-flights__flex-box > div.gws-flights-results__select-header.gws-flights__flex-filler > div.gws-flights-results__collapsed-itinerary.gws-flights-results__itinerary > div.gws-flights-results__itinerary-times.gws-flights__ellipsize > div.gws-flights-results__carriers.gws-flights__ellipsize.gws-flights__flex-box.gws-flights__align-center > span:nth-child(4)")
                                                    airline_elements = airline_contain.find_elements_by_tag_name("span")
                                                    airline_string = ""
                                                    data=[]
                                                    for elem in airline_elements:
                                                        flag=0
                                                        for d in data:
                                                            if d == elem.text:
                                                                flag=1
                                                        if flag == 0 and elem.text!="":
                                                            data.append(elem.text.replace(" ",""))
                                                    
                                                    for e in data:
                                                        airline_string += e+","
                                                    airline_string = airline_string[0:len(airline_string)-1]
                                                    data=[]
                                                    price_contain = best_list.find_element_by_class_name("gws-flights-results__cheapest-price")
                                                    price = price_contain.find_element_by_xpath('//jsl[@jstcache="8424"]').text
                                                    rowstring = airport_name.replace(","," ")+","+tairport_name.replace(","," ")+","+nowstring.replace(","," ")+","+afterstring.replace(","," ")+","+price.replace(","," ")+","+airline_string.replace(","," ")+"\n"
                                                    print(rowstring)

                                                except Exception:
                                                    airline_string=""
                                                    price = ""
                                                    data=[]
                                                worksheet.write(row_count, 0, airport_name)
                                                worksheet.write(row_count, 1, tairport_name)
                                                worksheet.write(row_count, 2, nowstring)
                                                worksheet.write(row_count, 3, afterstring)
                                                worksheet.write(row_count, 4, price)
                                                worksheet.write(row_count, 5, airline_string)
                                                row_count = row_count + 1
                                                
                                    tcount=tcount + 1

            count = count+1
workbook.close()
