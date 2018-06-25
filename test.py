import pandas as pd
import sys
import os
import numpy as np
sys.path.append("../data_provider")
sys.path.append("../yihewang1234/data_provider")
import m4datasource

def testfun(x):
    return x*2


model="missing"; dataset="M4"; name="Hourly";
random_time="2018-08-31 19:00:00"; n_train=500; p=20;
start_train="2018-10-31 19:00:00"; end_train="2018-11-01 19:00:00";
end_test="2018-11-02 19:00:00"; err_method="MAE"