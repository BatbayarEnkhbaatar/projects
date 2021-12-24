import requests.auth
import requests
from bs4 import BeautifulSoup
from random import choice
import pandas as pd
import os


def proxy_generator():
    response = requests.get("https://sslproxies.org/")
    soup = BeautifulSoup(response.content, 'html5lib')
    proxy = {'https': choice(list(map(lambda x: x[0] + ':' + x[1], list(
        zip(map(lambda x: x.text, soup.findAll('td')[::8]), map(lambda x: x.text, soup.findAll('td')[1::8]))))))}
    #print("Proxy IP:  ", proxy)
    return proxy


def proxy_generator1():
    proxy_ip = pd.read_csv("proxy_lists.csv", index_col=0, skiprows=0)
    ip_list = []
    #print("ip_list type: ", ip_list)
    for ip in proxy_ip["0"]:
        ip_list.append(ip)
    proxy_ip_addr = ip_list[0]
    ip_list.remove(proxy_ip_addr)
    os.remove("proxy_lists.csv")
    new_proxy_list = pd.DataFrame(ip_list)
    num_of_proxy = len(new_proxy_list)
    new_proxy_list.to_csv("proxy_lists.csv")

    return proxy_ip_addr, num_of_proxy
    #return proxy_ip_addr

def proxy_generator3(user: str, password: str, endpoint: str):
    EndPoint = endpoint
    Username = user
    Password = password
    proxy = {
        "http": f"http://{Username}:{Password}@{EndPoint}",
        "https": f"http://{Username}:{Password}@{EndPoint}",
    }
    return proxy


# for testing purpose
#url = "https://ip.oxylabs.io/"
#
# req1 = requests.request("get", url)
# print("RESPONSE WITHOUT PROXY:")
# print(req1.text)
# OxyLabs
# EndPoint = "pr.oxylabs.io:7777"
# Username = "rspiderkim"
# Password = "7QPP6LlPQQ"
# Cheap-Proxy
# EndPoint = "proxy.proxy-cheap.com:31112"
# Username = "dyrw3ey2"
# Password = "CqTHKYtUfCwrPRu7"
# proxy_server = proxy_generator3(Username, Password, EndPoint)
# req = requests.get(url, proxies=proxy_server)
# print("RESPONSE WITH PROXY:")
# print(req.text)
