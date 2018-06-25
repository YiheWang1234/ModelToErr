"""
datasample module

provide massive time series data for evaluation
"""

import numpy as np
import pandas as pd
import os.path
import urllib3
import zipfile

class M4DataSource:

    def __init__(self, end="2018-08-31 19:00:00", n=1000, n_test=0,
                 name="Hourly", method='const_increase', field_list=[0, 1, 4]):

        if not os.path.isfile("./M4DataSet/" + name + "-train.csv") and \
                not os.path.isfile("./data_provider/M4DataSet/" + name + "-train.csv"):
            print("File does not exist. will download online automatically")

            connection_pool = urllib3.PoolManager()
            url = 'https://www.m4.unic.ac.cy/wp-content/uploads/2017/12/M4DataSet.zip'
            resp = connection_pool.request('GET', url)
            f = open("M4DataSet.zip", 'wb')
            f.write(resp.data)
            f.close()
            resp.release_conn()

            zip_ref = zipfile.ZipFile("./M4DataSet.zip", 'r')
            zip_ref.extractall("./M4DataSet/")
            zip_ref.close()
            os.remove("./M4DataSet.zip")

        data_train_temp = pd.read_csv("./M4DataSet/" + name + "-train.csv", header=0, index_col=0).T
        self.data_train = data_train_temp.iloc[:, field_list]
        self.date_index = pd.date_range(end=end, periods=n, freq=name[0])
        self.need_extend = min((1 - self.data_train.isnull()).sum(axis=0)) < len(self.date_index)
        self.n = n
        self.n_test = n_test
        self.p = len(field_list)
        self.method = method
        if self.need_extend:
            self.extend_date()
        else:
            self.no_extend_data()

        self.data_test = self.data_train.iloc[self.n-self.n_test:, :]
        self.data_train = self.data_train.iloc[:self.n-self.n_test, :]

    def const_increase(self, current_ts, add_n, add_front=True):
        if add_front:
            return pd.Series(np.ones(add_n) * current_ts[0]).append(current_ts)
        else:
            return current_ts.append(pd.Series(np.ones(add_n) * current_ts[-1]))

    def extend_date(self):
        if self.method == 'const_increase':
            model_use = self.const_increase
        else:
            print("extend method not defined")
            return 1
        temp = np.zeros((len(self.date_index), self.p))
        for i in range(self.p):
            current_ts = self.data_train.iloc[:, i].dropna()
            add_n = len(self.date_index) - len(current_ts)
            if add_n > 0:
                update_ts = model_use(current_ts, add_n)
            else:
                update_ts = current_ts[:len(self.date_index)]
            temp[:, i] = update_ts
        self.data_train = pd.DataFrame(temp)
        self.data_train = self.data_train.set_index(self.date_index)

    def no_extend_data(self):
        self.data_train = self.data_train.iloc[0:self.n, ]
        self.data_train = self.data_train.set_index(self.date_index)


def fake_data(end="2018-08-31 19:00:00", n=50, p=10, name="Hourly", n_test=5, gen_function='linear'):
    np.random.seed(1234)
    index = pd.date_range(end=end, periods=n, freq=name[0])
    if gen_function == 'linear':
        data_mat = np.repeat(np.linspace(1, n, num=n).reshape(n, 1), p, axis=1)
    elif gen_function == 'sin':
        data_mat = np.sin(np.repeat(np.linspace(1, n, num=n).reshape(n, 1), p, axis=1))
    else:
        print("wrong gen_funcgion argument")
        return 1
    #temp = abs((data_mat + np.repeat(np.random.normal(0, 10, p).reshape(1, p), n, axis=0)) *\
    #        np.repeat(np.random.normal(0, 10, p).reshape(1, p), n, axis=0))
    temp = data_mat
    data_train = pd.DataFrame(temp)
    data_train = data_train.set_index(index)
    data_test = data_train.iloc[n - n_test:, :]
    data_train = data_train.iloc[:n - n_test, :]
    return {'data_test': data_test, 'data_train': data_train}


class DataSets:

    def __init__(self, end="2018-08-31 19:00:00", n=500, n_test=100, p=20, p_list=np.linspace(1,10,num=10), name="Hourly", method="M4"):
        self.end = end
        self.n = n
        self.n_test = n_test
        self.p = p
        if method == "M4":
            self.p = len(p_list)
        self.p_list = p_list
        self.name = name
        self.method = method

        if self.method == "M4":
            data = M4DataSource(end=self.end, n=self.n, n_test=self.n_test,
                                name=self.name, method='const_increase', field_list=self.p_list)
            self.data_train = data.data_train
            self.data_test = data.data_test
        elif self.method in ["linear", "sin"]:
            data = fake_data(end=self.end, n=self.n, p=self.p, name=self.name, n_test=self.n_test, gen_function=method)
            self.data_train = data["data_train"]
            self.data_test = data["data_test"]
        else:
            print("wrong method")
            self.data_train = "wrong method"
            self.data_test = "wrong method"
        self.start = self.data_train.index.values[0]
        self.n_train = self.n - self.n_test

    def get_data(self, date_start="2018-10-31 19:00:00", date_end="2018-12-31 19:00:00"):
        index = pd.date_range(start=date_start, end=date_end, freq=self.name[0])
        temp = np.zeros((len(index), self.p))
        for i in range(len(index)):
            if index[i] < self.start:
                temp_len = len(pd.date_range(start=index[i], end=self.start, freq=self.name[0]))
                temp[i, :] = self.data_train.iloc[self.n_train-temp_len % self.n_train, :]
            else:
                temp_len = len(pd.date_range(start=self.start, end=index[i], freq=self.name[0]))
                temp[i, :] = self.data_train.iloc[temp_len % self.n_train, :]
        output_data = pd.DataFrame(temp)
        output_data = output_data.set_index(index)
        return output_data
