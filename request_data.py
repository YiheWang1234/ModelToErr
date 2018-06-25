import requests
import numpy as np
import pandas as pd


def get_data(url="https://app.dominodatalab.com/u/yihewang1234/data_provider/app", end="2018-08-31 19:00:00", n=500,
             ntest=100, p=10, plist=10, name="Hourly", method="M4",
             datestart="2018-06-15 19:00:00", dateend="2018-07-01 19:00:00"):
    n = str(n)
    ntest = str(ntest)
    p = str(p)
    plist = str(plist)
    # r = requests.get(url, headers={"end": end, "n": n, "ntest": ntest, "p": p, "plist": plist, "name": name,
    #                                "method": method, "datestart": datestart, "dateend": dateend})

    new_url = requests.get(url, allow_redirects=False).next.url
    r = requests.post(new_url, data={"end": end, "n": n, "ntest": ntest, "p": p, "plist": plist, "name": name,
                                   "method": method, "datestart": datestart, "dateend": dateend})

    return pd.read_json(r.content)

