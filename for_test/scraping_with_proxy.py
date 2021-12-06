import logging
import json
import time
import pandas as pd
from fake_useragent import UserAgent
import requests as req
from requests.exceptions import ProxyError
import get_proxy
import sys

logging.basicConfig(level=logging.DEBUG, filename="learning_fundtion.log", format="%(asctime)s:%(levelno)s:%(message)s")
# Opening JSON file
ua = UserAgent()
url = 'https://www.car365.go.kr/web/program/usedcarpriceData.do'
user_agent = ua.chrome
headers = {
    'Referer': 'https://www.car365.go.kr/web/contents/usedcar_price.do',
    'User-Agent': user_agent}

# for reading nested data [0] represents
# the index value of the list
df = pd.read_csv("params_02.csv", sep=",", index_col=0)

# with open("params_01.csv") as df:
#     params = csv.DictReader(df)
#     for param in params:
#         machineCode = param["machineCode"]
#         data[machineCode] = param
par = df[["파라미터", "구분", "제조사", "대표차명", "모델명", "연식"]]

# par1 = par1.to_json()
# print("Here is the list: ", par1)
req_num = 0
one_time_max = 50
result_list = []
params0 = []
# get Proxy IP from Proxy database with 1000 distict proxy lists.
#proxy_ip = pd.read_csv("proxy_lists.csv", index_col=0, skiprows=0)
# Open CSV

proxy_ip = pd.read_csv("proxy_lists.csv", index_col=0, skiprows=0)
ip_list = []
# print("ip_list type: ", ip_list)
for ip in proxy_ip["0"]:
    ip_list.append(ip)

while one_time_max < 5300:
    try:
        seq = one_time_max
        # Select IP from CSV file
        proxy_info = get_proxy.proxy_generator1()
        ip_add = {'https': proxy_info[0], 'http': proxy_info[0]}
        num_proxy = proxy_info[1]
        if num_proxy == 0:
            print("All proxy has been rotated successfully")
            break
        else:
            print("Attempt# : ", num_proxy)
            while req_num < one_time_max:
                    user_agent = ua.chrome
                    headers['User-Agent'] = user_agent
                    par = df.iloc[[req_num]]
                    params0.append(par)
                    params = json.loads(par.to_json())
                    # params = json.loads(params)
                    params1 = json.loads(params['파라미터'][str(req_num)])
                    time.sleep(5)
                    res5 = req.request("get", url, headers=headers, params=params1, timeout=10)
                    print("Response time: ", res5.elapsed.total_seconds())
                    print("Proxy IP ", ip_add, "Please wait!, it is scrapping...")
                    # print("HTTP response: ", res5.status_code, "Proxy IP: ", ip_add)
                    js5 = res5.json()
                    logging.debug(js5)
                    tmp_df = pd.DataFrame(js5['RESULT']['CARLIST'])
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

                        tmp['구분'] = params['구분'][str(req_num)]
                        tmp['제조사'] = params['제조사'][str(req_num)]
                        tmp['대표차명'] = params['대표차명'][str(req_num)]
                        tmp['모델명'] = params['모델명'][str(req_num)]
                        tmp['연식'] = params['연식'][str(req_num)]
                        tmp['세부차종'] = grade
                        tmp['전국자동차매매사업조합연합회'] = A1
                        tmp['K Car'] = A2
                        tmp['핀카'] = A3
                        tmp['한국자동차매매사업조합연합회'] = A4
                        tmp['현대캐피탈 플카'] = A5
                        tmp['KB차차차'] = A6
                        result_list.append(tmp)
                    req_num += 1
            rdf = pd.DataFrame(result_list)
            rdf = rdf.groupby(by=['구분', '제조사', '대표차명', '모델명', '연식', '세부차종'], as_index=False).sum()
            rdf.to_excel(f'result_{req_num}.xlsx', index=False)
            result_list.clear()
            req_num = one_time_max + 1
            one_time_max += 50
    except:
        # proxy_err = ip_add + " is not working "
        print(ip_add, "is  has already blocked Or not working")
        logging.exception("The proxy is not working")
