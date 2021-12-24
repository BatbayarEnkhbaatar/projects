import logging
import json
import time
import pandas as pd
from fake_useragent import UserAgent
import requests as req
import timeit
from io import StringIO
estimated_time = StringIO()
start = timeit.default_timer()


# for reading nested data [0] represents
# the index value of the list
df = pd.read_csv("params.csv", sep=",", index_col=0)

par = df[["파라미터", "구분", "제조사", "대표차명", "모델명", "연식"]]

end = int(len(par))
print(end)