import logging
import json
import time
import pandas as pd
from fake_useragent import UserAgent
import requests as req
import timeit
from io import StringIO
import get_proxy
estimated_time = StringIO()
start = timeit.default_timer()
def proxy_generator3(user: str, password: str, endpoint: str):
    EndPoint = endpoint
    Username = user
    Password = password
    proxy = {
        "http": f"http://{Username}:{Password}@{EndPoint}",
        "https": f"http://{Username}:{Password}@{EndPoint}",
    }
    return proxy

logging.basicConfig(level=logging.DEBUG, filename="machine1.log", format="%(asctime)s:%(levelno)s:%(message)s")
# Opening JSON file
ua = UserAgent()
url = 'https://www.car365.go.kr/web/program/usedcarpriceData.do'
user_agent = ua.chrome
headers = {
    'Referer': 'https://www.car365.go.kr/web/contents/usedcar_price.do',
    'User-Agent': user_agent}

# for reading nested data [0] represents
# the index value of the list
df = pd.read_csv("params.csv", sep=",", index_col=0)

par = df[["파라미터", "구분", "제조사", "대표차명", "모델명", "연식"]]

end = int(len(par))
req_num = 0
one_time_max: int = 50
result_list = []
params0 = []
num_of_proxy = 1
num_of_fail = 0

# Proxy Credentials
EndPoint = "pr.oxylabs.io:7777"
Username = "rspiderkim"
Password = "7QPP6LlPQQ"

while one_time_max < end:
    try:
        proxy_info = get_proxy.proxy_generator1()
        # proxy_info = proxy_generator3(Username, Password, EndPoint)
        print("Req#: ", req_num)
        while req_num < one_time_max:
                user_agent = ua.chrome
                headers['User-Agent'] = user_agent
                par = df.iloc[[req_num]]
                params0.append(par)
                params = json.loads(par.to_json())
                # params = json.loads(params)
                params1 = json.loads(params['파라미터'][str(req_num)])
                time.sleep(2)
                res5 = req.request("get", url, headers=headers, proxies=proxy_info, params=params1, timeout=3)
                print("Response time: ", res5.elapsed.total_seconds())
                print("Please wait!, it is scrapping...")
                print("HTTP response: ", res5.status_code, "Proxy IP: ", ip_add)
                js5 = res5.json()
                # print(js5)
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
        rdf.to_excel(f'RESULTS/result_machine1_{req_num}.xlsx', index=False)
        result_list.clear()
        req_num = one_time_max + 1
        one_time_max += 50
        num_of_proxy += 1
    except:
        # proxy_err = ip_add + " is not working "
        num_of_fail +=1
        print("Failed attempt :", num_of_fail, proxy_info)
        logging.exception(proxy_info, "The proxy is not working")

print("scape has run sucessfully")
stop = timeit.default_timer()
# Print total execution time
print('Total executed time=',stop - start)
logging.exception("Total executed time= ", stop - start)