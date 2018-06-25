import pandas as pd
import numpy as np
#import sys
#sys.path.append("../data_provider")
#sys.path.append("../yihewang1234/data_provider")
import m4datasource
import json


class ModelToError:

    def __init__(self, model="missing", dataset="M4", name="Hourly", random_time="2018-08-31 19:00:00", n_train=500, p=20,
                 start_train="2018-10-31 19:00:00", end_train="2018-11-01 19:00:00", end_test="2018-11-02 19:00:00",
                 err_method="MAE"):

        if model == 'missing':
            self.model = self.default_model
        else:
            ldict = locals()
            exec(model, globals(), ldict)
            mymodel = ldict['mymodel']
            self.model = mymodel

        self.p = p
        self.data = m4datasource.DataSets(end=random_time, n=n_train, n_test=0, p=p,
                                          p_list=np.linspace(0, p-1, num=p).astype(int), name=name, method=dataset)

        self.data_train = self.data.get_data(date_start=start_train, date_end=end_train)
        self.data_test = self.data.get_data(date_start=end_train, date_end=end_test)
        self.n_test = self.data_test.shape[0]
        self.estimate = self.model(self.data_train, self.n_test)
        temp_err = self.err_measure(data=self.estimate, prediction=self.data_test, err_method=err_method, h=self.n_test)
        self.err = temp_err["err"]
        self.err_curve = temp_err["err_curve"]

    def err_measure(self, data, prediction, h, err_method="MAE"):

        if err_method == "MAE":
            errfun = self.MAE
        elif err_method == "sMAPE":
            errfun = self.sMAPE
        else:
            print("Wrong err_method: ", err_method)

        err_final = 0
        err_curve_final = np.zeros((1, h))

        for i in range(self.p):

            observation = np.array(data.iloc[:, i]).reshape((1, h))
            estimation = np.array(prediction.iloc[:, i]).reshape((1, h))
            temp = errfun(observation, estimation)
            err_curve_final += temp
            err_final += np.mean(temp)

        return {"err": err_final/self.p, "err_curve": err_curve_final/self.p}

    def MAE(self, observation, estimation):
        return abs(observation - estimation)

    def sMAPE(self, observation, estimation):
        return 2*abs(observation - estimation)/(abs(observation) + abs(estimation))

    def default_model(self, data_train, n_test):
        return pd.DataFrame(np.repeat(np.array(data_train.iloc[-1:, :]), n_test, axis=0))


def model_to_error(model="missing", dataset="M4", name="Hourly", random_time="2018-08-31 19:00:00", n_train=500, p=20,
                   start_train="2018-10-31 19:00:00", end_train="2018-11-01 19:00:00", end_test="2018-11-02 19:00:00",
                   err_method="MAE"):
    model_err = ModelToError(model=model, dataset=dataset, name=name, random_time=random_time, n_train=n_train, p=p,
                             start_train=start_train, end_train=end_train, end_test=end_test, err_method=err_method)

    return json.dumps({"err": model_err.err, "err curve": model_err.err_curve.tolist()[0][1:]})
