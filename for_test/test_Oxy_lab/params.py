from typing import Dict
import requests as req
import time
from bs4 import BeautifulSoup
from random import choice
from fake_useragent import UserAgent
import pandas as pd
import json
ua = UserAgent()
user_agent = ua.chrome
headers = {
    'Referer': 'https://www.car365.go.kr/web/contents/usedcar_price.do',
    'User-Agent': user_agent
}
target = 'https://www.car365.go.kr/web/program/usedcarpriceData.do'

params: Dict[str, str] = {
    'machineCode': '1',
    'menuType': '',
    'menuNation': '',
    'menuEntrps': '',
    'menuReprsnt': '',
    'menuModel': '',
    'menuPrye': '',
    'searchStr': ''
}


def get_params():
    params_list = []
    for sortation in range(1, 3):
        if sortation == 1:
            classify = '국산'
        else:
            classify = '수입'

        params['menuType'] = '1'
        params['menuNation'] = str(sortation)
        user_agent = ua.chrome
        headers['User-Agent'] = user_agent
        time.sleep(1)
        res1 = req.get(target, headers=headers, params=params)
        js1 = res1.json()
        menu1 = js1['RESULT']['MENU']
        for m1 in menu1:
            code1 = m1['MENU_CODE']
            make = m1['MENU_STR']
            params['menuType'] = '2'
            params['menuEntrps'] = code1
            user_agent = ua.chrome
            headers['User-Agent'] = user_agent
            time.sleep(1)
            res2 = req.get(target, headers=headers, params=params)
            js2 = res2.json()
            menu2 = js2['RESULT']['MENU']
            for m2 in menu2:
                code2 = m2['MENU_CODE']
                car_name = m2['MENU_STR']
                params['menuType'] = '3'
                params['menuReprsnt'] = code2
                user_agent = ua.chrome
                headers['User-Agent'] = user_agent
                time.sleep(1)
                res3 = req.get(target, headers=headers, params=params)
                js3 = res3.json()
                menu3 = js3['RESULT']['MENU']
                for m3 in menu3:
                    code3 = m3['MENU_CODE']
                    model_name = m3['MENU_STR']
                    params['menuType'] = '4'
                    params['menuModel'] = code3
                    user_agent = ua.chrome
                    headers['User-Agent'] = user_agent
                    time.sleep(1)
                    res4 = req.get(target, headers=headers, params=params)
                    js4 = res4.json()
                    menu4 = js4['RESULT']['MENU']
                    for m4 in menu4:
                        year = m4['MENU_STR']
                        params['menuType'] = 'carlist'
                        params['menuPrye'] = year
                        tmp = {'파라미터': json.dumps(params), '구분': classify, '제조사': make, '대표차명': car_name,
                               '모델명': model_name, '연식': year}
                        params_list.append(tmp)
                        #print(params_list)
                        data = pd.DataFrame(params_list)
                        data.to_csv("params_02_01.csv")
                        print("Json has been exported")
                        # with open('data.json', 'w') as jsonfile:
                        #     json.dump(params_list, jsonfile)


    return params_list
get_params()