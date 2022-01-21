from selenium import webdriver
from selenium.webdriver.common.by import By
import os
from time import sleep
from sqlalchemy import create_engine

os.system("cls")

currency = str(input("Enter code of currency (See in README on git): "))
print(f"Code is {currency}. Start jobe.")

#db config
host = "127.0.0.1"
port = "5432"
name = ""
password = ""
db_name = ""

engine = create_engine(f"postgresql+psycopg2://{name}:{password}@{host}/{db_name}", echo=False) # connect to postqres. echo=False - логи отключены

url = f"https://cbr.ru/currency_base/dynamics/?UniDbQuery.Posted=True&UniDbQuery.so=1&UniDbQuery.mode=1&UniDbQuery.date_req1=&UniDbQuery.date_req2=&UniDbQuery.VAL_NM_RQ={currency}&UniDbQuery.From=01.07.1992"

try:
	driver = webdriver.PhantomJS()
	#os.system("cls")
	sleep(2)
	driver.get(url)
	sleep(2)
except Exception as e:
	print(e)

engine.execute(f"CREATE TABLE IF NOT EXISTS {currency} (DATE text, AMOUNT text, PRICE text)") # create new table

start_index = 3
num = 0
st = driver.find_element(By.XPATH, f"/html/body/main/div/div/div/div[2]/div[1]/table/tbody/tr[{start_index}]").text
try:
	while len(st) != 0:
		data = driver.find_element(By.XPATH, f"/html/body/main/div/div/div/div[2]/div[1]/table/tbody/tr[{start_index}]").text
		print(data)
		date = data.partition(" ")[0]#date-ok
		date = date.replace('.', '-')
		date = f"'{date}'"
		print(date)
		amount = data.partition(" ")[2]
		amount = amount.partition(" ")[0] 
		print(amount)
		price = data.partition(" ")[2]
		price = price.partition(" ")[2]
		price = price.partition(" ")[0]
		price = price.replace(',', '.')
		print(price)
		
		engine.execute(f"INSERT INTO {currency} (DATE, AMOUNT, PRICE) VALUES ({date}, {amount}, {price})")
		start_index += 1
		num += 1
		os.system("cls")
except Exception as e:
	print(e)
print("Jobe with site done.\nAll courses is add in the PostgeSql.")
print(f"The result is : add {num} courses.\nShow data in 3, 2, 1...")
sleep(3)
for i in engine.execute(f"SELECT * FROM {currency} "): 
	print(f'''
	-------------------------
	date - {i[0]}
	amount - {i[1]}
	price - {i[2]}
	-------------------------
		''')