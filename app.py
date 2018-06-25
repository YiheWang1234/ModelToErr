from flask import request
from flask import Flask
import m4datasource
import numpy as np
import json

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
#@app.route('/')
def main():

    if request.method == 'GET':
        return "Use Post Please."
    # end = request.headers.get("end", "")
    # n = request.headers.get("n", "")
    # n_test = request.headers.get("ntest", "")
    # p = request.headers.get("p", "")
    # p_list = request.headers.get("plist", "")
    # name = request.headers.get("name", "")
    # method = request.headers.get("method", "")
    # date_start = request.headers.get("datestart", "")
    # date_end = request.headers.get("dateend", "")

    print("a")
    end = request.form["end"]
    n = request.form["n"]
    n_test = request.form["ntest"]
    p = request.form["p"]
    p_list = request.form["plist"]
    name = request.form["name"]
    method = request.form["method"]
    date_start = request.form["datestart"]
    date_end = request.form["dateend"]
    print("b")

    if p_list == '':
        data = m4datasource.DataSets()
        output = data.get_data()
        return output.to_json()
    else:
        temp_list = np.linspace(0, int(p_list) - 1, num=int(p_list))
        data = m4datasource.DataSets(end=end, n=int(n), n_test=int(n_test),
                                     p=int(p), p_list=temp_list, name=name, method=method)
        output = data.get_data(date_start=date_start, date_end=date_end)
        return output.to_json()

    #return json.dumps({"end": end, "n": n, "p_list": p_list, "n_test": n_test, "method": method, "name": name, "date_start": date_start})
