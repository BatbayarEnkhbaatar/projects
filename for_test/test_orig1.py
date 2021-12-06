import requests as req
import pandas as pd
import json
from fake_useragent import UserAgent
from tqdm import tqdm
import get_proxy
import csv

ua = UserAgent()
url = 'https://www.car365.go.kr/web/program/usedcarpriceData.do'
user_agent = ua.chrome
headers = {
    'Referer': 'https://www.car365.go.kr/web/contents/usedcar_price.do',
    'User-Agent': user_agent
}
params = {
    'machineCode': '1',
    'menuType': '',
    'menuNation': '',
    'menuEntrps': '',
    'menuReprsnt': '',
    'menuModel': '',
    'menuPrye': '',
    'searchStr': ''
}

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
    res1 = req.get(url, headers=headers, params=params)
    js1 = res1.json()
    menu1 = js1['RESULT']['MENU']
    for m1 in menu1:
        code1 = m1['MENU_CODE']
        make = m1['MENU_STR']
        params['menuType'] = '2'
        params['menuEntrps'] = code1
        user_agent = ua.chrome
        headers['User-Agent'] = user_agent
        res2 = req.get(url, headers=headers, params=params)
        js2 = res2.json()
        menu2 = js2['RESULT']['MENU']
        for m2 in menu2:
            code2 = m2['MENU_CODE']
            car_name = m2['MENU_STR']
            params['menuType'] = '3'
            params['menuReprsnt'] = code2
            user_agent = ua.chrome
            headers['User-Agent'] = user_agent
            res3 = req.get(url, headers=headers, params=params)
            js3 = res3.json()
            menu3 = js3['RESULT']['MENU']
            for m3 in menu3:
                code3 = m3['MENU_CODE']
                model_name = m3['MENU_STR']
                params['menuType'] = '4'
                params['menuModel'] = code3
                user_agent = ua.chrome
                headers['User-Agent'] = user_agent
                res4 = req.get(url, headers=headers, params=params)
                js4 = res4.json()
                menu4 = js4['RESULT']['MENU']
                for m4 in menu4:
                    year = m4['MENU_STR']
                    params['menuType'] = 'carlist'
                    params['menuPrye'] = year
                    #                     print(params)
                    tmp = {}
                    tmp['파라미터'] = json.dumps(params)
                    tmp['구분'] = classify
                    tmp['제조사'] = make
                    tmp['대표차명'] = car_name
                    tmp['모델명'] = model_name
                    tmp['연식'] = year
                    params_list.append(tmp)

result_list = []
idx = 1
req_num = 1
max_req = 50

for par in tqdm(params_list[idx:idx + 100]):
    #     print(idx)
    while max_req < 5300:
        pxy = get_proxy.proxy_generator()
        while req_num < max_req:
            user_agent = ua.chrome
            headers['User-Agent'] = user_agent
            params = json.loads(par['파라미터'])
            res5 = req.request("get", url, headers=headers, params=params)
            print(res5.status_code)
            while res5.status_code != 200:
                print(pxy, "proxy is already blocked, SHIT!!!, getting new IP")
                pxy = get_proxy.proxy_generator()
                print("New IP is here: ", pxy)
                res5 = req.request("get", url, proxies=pxy, headers=headers, params=params)
            # res5 = req.get(url, headers=headers, params=params)
            # res5 = req.request("get", url, headers=headers, params=params)
            js5 = res5.json()
            tmp_df = pd.DataFrame(js5['RESULT']['CARLIST'])
                     #pd.DataFrame(js5['RESULT']['CARLIST'])
            # print(tmp_df)
            tmp_df = tmp_df.drop_duplicates(subset=['LIST_ID', 'LIST_GRAD'], keep='last')
            js6 = tmp_df.to_dict('records')
            for car in js6:
                tmp = {}

                A1 = ''
                A2 = ''
                A3 = ''
                A4 = ''
                A5 = ''
                A6 = ''

                grade = car['LIST_GRAD']

                lid = car['LIST_ID']
                if lid == 'A1':
                    A1 = car['LIST_AMOUNT']
                elif lid == 'A2':
                    A2 = car['LIST_AMOUNT']
                elif lid == 'A3':
                    A3 = car['LIST_AMOUNT']
                elif lid == 'A4':
                    A4 = car['LIST_AMOUNT']
                elif lid == 'A5':
                    A5 = car['LIST_AMOUNT']
                elif lid == 'A6':
                    A6 = car['LIST_AMOUNT']

                tmp['구분'] = par['구분']
                tmp['제조사'] = par['제조사']
                tmp['대표차명'] = par['대표차명']
                tmp['모델명'] = par['모델명']
                tmp['연식'] = par['연식']
                tmp['세부차종'] = grade
                tmp['전국자동차매매사업조합연합회'] = A1
                tmp['K Car'] = A2
                tmp['핀카'] = A3
                tmp['한국자동차매매사업조합연합회'] = A4
                tmp['현대캐피탈 플카'] = A5
                tmp['KB차차차'] = A6
                result_list.append(tmp)
            req_num += 1

        print("proxy IP has changed by ", pxy)
        max_req += 50
rdf = pd.DataFrame(result_list)
rdf = rdf.groupby(by=['구분', '제조사', '대표차명', '모델명', '연식', '세부차종'], as_index=False).sum()
rdf.to_excel(f'20211109_알씨아이파이낸셜코리아_car365_수집_데이터_결과_{idx}_{idx + 50}.xlsx', index=False)
