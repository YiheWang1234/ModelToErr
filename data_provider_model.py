import m4datasource
import numpy as np
import json

def data_provider(end="2018-08-31 19:00:00", n=500, ntest=100, p=20, plist=20,
                  name="Hourly", method="M4", datestart="2018-10-31 19:00:00", dateend="2018-11-01 19:00:00"):

    data = m4datasource.DataSets(end=end, n=n, n_test=ntest, p=p, p_list=np.linspace(0, plist-1, num=plist),
                                 name=name, method=method)
    data_out = data.get_data(date_start=datestart, date_end=dateend)
    return data_out.to_json()
    #return data_out.shape[0]
