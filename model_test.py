import requests
import json
import pandas as pd
response = requests.post("https://app-models.dominodatalab.com:443/models/5b2cf88ee4b0941477d689d8/latest/model",
                         auth=(
                             "ublYY9FcLTuLJKnkVVjuL07njcHhCEBVYvfMbkQDNtoe8zXkM1VNs10C78QAOR21",
                             "ublYY9FcLTuLJKnkVVjuL07njcHhCEBVYvfMbkQDNtoe8zXkM1VNs10C78QAOR21"
                         ),
                         json={
                                "data": {"end": "2018-08-31 19:00:00", "n": 500, "ntest": 100, "p": 20, "plist": 20,
                                         "name": "Hourly", "method": "sin", "datestart": "2018-10-31 19:00:00",
                                         "dateend": "2018-10-31 23:00:00"}
                         }
                         )

data = pd.read_json(json.loads(response.content)["result"])
data
