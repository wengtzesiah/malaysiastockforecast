#scrape entire stock list from Bursa Malaysia

import requests
from bs4 import BeautifulSoup
from .models import Stock


def scrape_stock_list():
    url = "https://www.malaysiastock.biz/Stock-Screener.aspx"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find(id="MainContent2_tbAllStock")
    rows = table.find_all("tr")

    for row in rows[1:]:
        cells = row.find_all("td")
        symbol = cells[0].text.strip()
        lastprice = cells[1].text.strip()
        exchange = cells[2].text.strip()
        stock = Stock(symbol=symbol, lastprice=lastprice, exchange=exchange)
        stock.save()

def add_stock_name():
    stocks = Stock.objects.all()
    for stock in stocks:
        if stock.symbol == "ABMB":
            stock.name = "ALLIANCE BANK MALAYSIA BERHAD"
            stock.save()
        elif stock.symbol == "AFUJIYA":
            stock.name = "ABM FUJIYA BHD"
            stock.save()
        elif stock.symbol == "AHB":
            stock.name = "AHB HOLDING BERHAD"
            stock.save()
        elif stock.symbol == "AHEALTH":
            stock.name = "APEX HEALTHCARE BERHAD"
            stock.save()
        elif stock.symbol == "AIM":
            stock.name = "ADVANCE INFORMATION MARKETING BERHAD"
            stock.save()
        elif stock.symbol == "CAPITALA":
            stock.name = "CAPITAL A BERHAD"
            stock.save()
        elif stock.symbol == "AIRPORT":
            stock.name = "MALAYSIA AIRPORTS HOLDINGS BERHAD"
            stock.save()
        elif stock.symbol == "PARKWD":
            stock.name = "PARKWOOD HOLDINGS BERHAD"
            stock.save()
        elif stock.symbol == "AJI":
            stock.name = "AJINOMOTO (MALAYSIA) BERHAD"
            stock.save()
        elif stock.symbol == "AJIYA":
            stock.name = "AJIYA BERHAD"
            stock.save()
        elif stock.symbol == "RGTBHD":
            stock.name = "RGT BERHAD"
            stock.save()
        elif stock.symbol == "ALAM":
            stock.name = "ALAM MARITIM RESOURCES BHD"
            stock.save()
        elif stock.symbol == "ALAQAR":
            stock.name = "AL-AQAR HEALTHCARE REIT"
            stock.save()
        elif stock.symbol == "ALCOM":
            stock.name = "ALCOM GROUP BERHAD"
            stock.save()
        elif stock.symbol == "ALLIANZ":
            stock.name = "ALLIANZ MALAYSIA BERHAD"
            stock.save()
        elif stock.symbol == "AMBANK":
            stock.name = "AMMB HOLDINGS BERHAD"
            stock.save()
        elif stock.symbol == "AMEDIA":
            stock.name = "ASIA MEDIA GROUP BERHAD"
            stock.save()
        elif stock.symbol == "AMFIRST":
            stock.name = "AMFIRST REAL ESTATE INVESTMENT TRUST"
            stock.save()
        elif stock.symbol == "AMTEL":
            stock.name = "AMTEL HOLDINGS BERHAD"
            stock.save()
        elif stock.symbol == "AMWAY":
            stock.name = "AMWAY (MALAYSIA) HOLDINGS BERHAD"
            stock.save()
        elif stock.symbol == "ANALABS":
            stock.name = "ANALABS RESOURCES BERHAD"
            stock.save()
        elif stock.symbol == "ANCOMNY":
            stock.name = "ANCOM NYLEX BERHAD"
            stock.save()
        elif stock.symbol == "ANCOMLB":
            stock.name = "ANCOM LOGISTICS BERHAD"
            stock.save()
        elif stock.symbol == "ANNJOO":
            stock.name = "ANN JOO RESOURCES BERHAD"
            stock.save()
        elif stock.symbol == "APB":
            stock.name = "APB RESOURCES BHD"
            stock.save()
        elif stock.symbol == "APEX":
            stock.name = "APEX EQUITY HOLDINGS BHD"
            stock.save()
        elif stock.symbol == "APM":
            stock.name = "APM AUTOMOTIVE HOLDINGS BERHAD"
            stock.save()
        elif stock.symbol == "APOLLO":
            stock.name = "APOLLO FOOD HOLDINGS BERHAD"
            stock.save()
        elif stock.symbol == "ARANK":
            stock.name = "A-RANK BERHAD"
            stock.save()
        elif stock.symbol == "ARK":
            stock.name = "ARK RESOURCES HOLDINGS BERHAD"
            stock.save()
        elif stock.symbol == "ARMADA":
            stock.name = "BUMI ARMADA BERHAD"
            stock.save()
        elif stock.symbol == "ARREIT":
            stock.name = "AMANAHRAYA REITS"
            stock.save()
        elif stock.symbol == "ASB":
            stock.name = "ADVANCE SYNERGY BERHAD"
            stock.save()
        elif stock.symbol == "ASDION":
            stock.name = "ASDION BERHAD"
            stock.save()
        elif stock.symbol == "FINTEC":
            stock.name = "FINTEC GLOBAL BERHAD"
            stock.save()
        elif stock.symbol == "ASIABRN":
            stock.name = "ASIA BRANDS BERHAD"
            stock.save()
        elif stock.symbol == "GFM":
            stock.name = "GFM SERVICES BERHAD"
            stock.save()
        elif stock.symbol == "ASIAFLE":
            stock.name = "ASIA FILE CORPORATION BHD"
            stock.save()
        elif stock.symbol == "ASIAPAC":
            stock.name = "ASIAN PAC HOLDINGS BERHAD"
            stock.save()
        elif stock.symbol == "ASIAPLY":
            stock.name = "ASIA POLY HOLDINGS BERHAD"
            stock.save()
        elif stock.symbol == "ASTINO":
            stock.name = "ASTINO BERHAD"
            stock.save()
        elif stock.symbol == "ASTRO":
            stock.name = "ASTRO MALAYSIA HOLDINGS BERHAD"
            stock.save()
        elif stock.symbol == "VIZIONE":
            stock.name = "VIZIONE HOLDINGS BERHAD"
            stock.save()
        else:
            pass


        # elif stock.symbol == "":
        #     stock.name = ""
        #     stock.save()

	
	
	









































	
	
	


