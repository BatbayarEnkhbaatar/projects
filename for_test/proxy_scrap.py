import csv

import pandas as pd
from Proxy_List_Scrapper import Scrapper, Proxy, ScrapperException

scrapper = Scrapper(category='ALL', print_err_trace=False)

# Get ALL Proxies According to your Choice
data = scrapper.getProxies()

proxy = []
header = ["proxy_ip"]
# Print These Scrapped Proxies
print("Scrapped Proxies:")


for item in data.proxies:
    #print(item)
    IPaddr= item.ip+":"+item.port

    #print('{}:{}'.format(item.ip, item.port))
    proxy.append(IPaddr)
    #print(proxy)

ip_add = pd.DataFrame(proxy)
exported_proxy = ip_add.to_csv("proxy_lists.csv")

# Print the size of proxies scrapped
print("Total Proxies")
print(data.len)
# Print the Category of proxy from which you scrapped
print("Category of the Proxy")
print(data.category)