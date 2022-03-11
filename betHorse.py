import time 
import chromedriver_binary
import requests
import numpy as np
import math
import bettime
import random
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from datetime import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup


# 楽天競馬の出馬表のURLより、投票したい競馬場を選び、以下Xの18桁のコードをbaseidへ設定する
# https://keiba.rakuten.co.jp/race_card/list/RACEID/XXXXXXXXXXXXXXXXXX?l-id=top_raceInfoTodayTrackName_raceList_20 

url = "https://keiba.rakuten.co.jp/odds/tanfuku/RACEID/"
baseid ="2022031120151805"

# 本スクリプトを実行したいレース番号を指定します
race_list = ['01','02','03','04','05','06','07','08','09','10','11','12']

# Environment(pip)
# Package             Version
# ------------------- --------------
# async-generator     1.10
# attrs               21.4.0
# beautifulsoup4      4.10.0
# boto3               1.21.14
# botocore            1.24.14
# certifi             2021.10.8
# cffi                1.15.0
# charset-normalizer  2.0.12
# chromedriver-binary 99.0.4844.51.0
# cryptography        36.0.1
# h11                 0.13.0
# idna                3.3
# jmespath            0.10.0
# numpy               1.21.5
# outcome             1.1.0
# pip                 20.1.1
# pycparser           2.21
# pyOpenSSL           22.0.0
# PySocks             1.7.1
# python-dateutil     2.8.2
# requests            2.27.1
# s3transfer          0.5.2
# selenium            3.141.0
# setuptools          47.1.0
# six                 1.16.0
# sniffio             1.2.0
# sortedcontainers    2.4.0
# soupsieve           2.3.1
# trio                0.20.0
# trio-websocket      0.9.2
# typing-extensions   4.1.1
# urllib3             1.26.8
# wsproto             1.1.0

def getOdds(raceid):

        #print("getOdds()")

        # D E B U G 
        # import pdb; pdb.set_trace()

        # Create BeautifulSoup Object
        res = requests.get(url + raceid)
        soup = BeautifulSoup(res.text,'html.parser')

        # For Loading Page
        time.sleep(2)

        position_data = []
        number_data = []
        name_data = []
        win_data = []
        place_datau = []
        place_datad = []

        # Odds Data
        for single_odds in soup.find_all("tbody", class_="singleOdds"):

                for position in single_odds.find_all("td", class_="position"):
                        position_data.append(position.get_text())


                for horce_number in single_odds.find_all("th", class_="number"):
                        number_data.append(horce_number.get_text())

                for td in single_odds.find_all("td", class_="horse"):
                        for a in td.findAll("a",href=True,target="_blank"): 
                                name_data.append(a.text.strip())

                for td in single_odds.find_all("td", class_="win"):
                        for win in td.find_all("span"):
                                win_data.append(win.text.strip()) 

                for td in single_odds.find_all("td", class_="place"):
                        i = 1
                        for place in td.find_all("span"):
                                if i == 1:
                                        #print(place)
                                        place_datau.append(place.text.strip())
                         
                                i = i + 1                
 
                                if i == 4:
                                        #print(place)
                                        place_datad.append(place.text.strip()) 
                                        i = 1 

        # Remove Data            
        posi = math.floor(int(len(position_data))/2)

        del position_data[posi:]
        del number_data[posi:]
        del name_data[posi:]
        del win_data[posi:]
        del place_datau[posi:]
        del place_datad[posi:]

        odds_data = [position_data,number_data,name_data,win_data,place_datau,place_datad]
        npodds_data = np.array(odds_data)

        # Sort of HorceNumber
        np_odds_data = npodds_data[:, npodds_data[1,:].argsort()]
 
        return np_odds_data

def doRace(raceid):

        #print("doRace()")

        # D E B U G 
        #import pdb; pdb.set_trace()

        # Create Beautiful Soup Object
        res = requests.get(url + raceid)
        soup = BeautifulSoup(res.text,'html.parser') 

        # Race Title
        title_text = soup.find('title').get_text()
        print(title_text)

        # default time 
        betting_time = "18:00"

        # Betting Time
        for bettingTime in soup.find_all("dd", class_="bettingTime"):
                betting_time = bettingTime.get_text()
                #print(betting_time)

        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        print("Now time:                        " + now)

        # before 1mitutes
        betting_time = bettime.bettingTime(betting_time)
        bbtime = datetime.now().strftime("%Y-%m-%d")
        bbtime = bbtime + " " + betting_time
        print("Race Start time before 1mitutes: " + bbtime)        
        body_text = body_text + "Race Start time before 1mitutes: " + bbtime + "<br/>"

        # before 2minutes
        betting_time = bettime.bettingTime(betting_time)
        btime = datetime.now().strftime("%Y-%m-%d")
        btime = btime + " " + betting_time
        print("Race Start time before 2minutes: " + btime)
        body_text = body_text + "Race Start time before 2minutes: " + btime + "<br/>" 

        i = 1
        j = 1
        k = 1
        storm = 0

        while True:
         
                if i == 1:
                        before_placeu = getOdds(raceid)[4]
                        print("#### Progressing....... ####")
                        body_text = body_text + "#### Progressing....... ####" + "<br/>"

                time.sleep(random.randint(10,15))

                while True:

                        time.sleep(random.randint(10,15))
                        now = datetime.now().strftime("%Y-%m-%d %H:%M")

                        if now == btime and j == 1:
                 
                                current_placeu = getOdds(raceid)[4]
                                placeu_diff = current_placeu.astype(np.float16) - before_placeu.astype(np.float16)

                                odds_data = getOdds(raceid)
                                npoddsdata = np.insert(odds_data,6,placeu_diff,axis=0) 

                                # Sort of Fukusho
                                print("#### before 2mitutes Odds   ")
                                body_text = body_text + "#### before 2mitutes Odds   " + "<br/>"
                                print("[['人気順' '馬番' '馬名' '単勝オッズ' '複勝オッズ' '複勝オッズ'")
                                body_text = body_text + "[['人気順' '馬番' '馬名' '単勝オッズ' '複勝オッズ' '複勝オッズ'" + "<br/>"
                                print(npoddsdata[:, npoddsdata[4,:].argsort()].T)
                                body_text = body_text + str(npoddsdata[:, npoddsdata[4,:].argsort()].T).replace('\n','<br/>') + "<br/>"
                                before_placeu = current_placeu 

                                now = datetime.now().strftime("%Y-%m-%d %H:%M")
                                j = 0

                        if now == bbtime and k == 1:

                                current_placeu = getOdds(raceid)[4]
                                placeu_diff = current_placeu.astype(np.float16) - before_placeu.astype(np.float16)

                                odds_data = getOdds(raceid)
                                npoddsdata = np.insert(odds_data,6,placeu_diff,axis=0)

                                print("#### before 1mitutes Odds   ")
                                body_text = body_text + "#### before 1mitutes Odds   " + "<br/>"
                                print("[['人気順' '馬番' '馬名' '単勝オッズ' '複勝オッズ' '複勝オッズ'")
                                body_text = body_text + "[['人気順' '馬番' '馬名' '単勝オッズ' '複勝オッズ' '複勝オッズ'" + "<br/>"
                                print(npoddsdata[:, npoddsdata[4,:].argsort()].T)
                                body_text = body_text + str(npoddsdata[:, npoddsdata[4,:].argsort()].T).replace('\n','<br/>') + "<br/>"

                                no_race = getOdds(raceid)

                                b = 0 

                                for index in range(len(no_race[0,:])):

                                        if index == 0:
                                                b = no_race[1,index]                             

                                        if b > no_race[1,index]:
                                                storm = storm + 1

                                        if index == len(no_race[0, :]):
                                                break

                                        b = no_race[1,index]

                                if len(no_race[0,:]) < 8:
                                        print("[NOTICE] Less than 8 horse!! No Race!!")
                                        body_text = body_text + "[NOTICE] Less than 8 horse!! No Race!!" + "<br/>"
                                        break

                                if int(storm) > 2 and len(no_race[0,:]) > 12:
                                        print("Storm: " + str(storm))
                                        print("[NOTICE] S.T.O.R.M  No way!! No Race!!")
                                        body_text = body_text + "[NOTICE] S.T.O.R.M  No way!! No Race!!" + "<br/>"
                                        break

                                if int(storm) > 2 and len(no_race[0,:]) > 14:
                                        print("Storm: " + str(storm))
                                        print("[NOTICE] S.T.O.R.M  No way!! No Race!!")
                                        body_text = body_text + "[NOTICE] S.T.O.R.M  No way!! No Race!!" + "<br/>"
                                        break
                         
                                betno = str(npoddsdata[:, npoddsdata[4,:].argsort()].T[0,1])
                                tan_odds = float(npoddsdata[:, npoddsdata[4,:].argsort()].T[0,3])
                 
                                if tan_odds > 1.5:
                                        print("[NOTICE] Tansho High Odds!! No Race!!")
                                        body_text = body_text + "[NOTICE] Tansho High Odds!! No Race!!" + "<br/>"
                                        break

                                print("#### Betting....        ####")
                                body_text = body_text + "#### Betting....        ####" + "<br/>"

                                # BET HORSE
                                #betHorse(raceid,betno)

                                print("#### Betting Complete!! ####")
                                body_text = body_text + "#### Betting Complete!! ####" + "<br/>"
                                print("Horce Number is " +  betno)
                                body_text = body_text + "Horce Number is " +  betno + "<br/>"
                                k = 0

                                break
                break

def main():

    for raceno in race_list:

        doRace(baseid+raceno)


main()
