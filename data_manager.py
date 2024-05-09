import requests
import os


class DataManager:
    #This class is responsible for talking to the Google Sheet.

    def __init__(self):
        # シートデータの取得
        sheet_endpoint = "https://api.sheety.co/004700f3eb3e8292d552778cd3a65db2/flightDeals/prices"
        self.sheet_headers = {
            "Authorization": os.environ["BEARER"],
        }
        response = requests.get(url=sheet_endpoint, headers=self.sheet_headers)
        self.prices_sheet_data = response.json()["prices"]

        sheet_endpoint = "https://api.sheety.co/004700f3eb3e8292d552778cd3a65db2/flightDeals/users"
        response = requests.get(url=sheet_endpoint, headers=self.sheet_headers)
        self.user_list = response.json()["users"]

    def get_price_sheet_data(self):
        return self.prices_sheet_data

    # シートへIATAコードをセット
    def set_iata_code_to_sheet(self, iata_code_list):
        for row in iata_code_list:
            sheet_endpoint = f"https://api.sheety.co/004700f3eb3e8292d552778cd3a65db2/flightDeals/prices/{row[0]}"
            params = {
                "price": {
                    "iataCode": row[1],
                }
            }
            requests.put(url=sheet_endpoint, headers=self.sheet_headers, json=params)

    def get_address_list(self):
        address_list = []
        for user in self.user_list:
            address_list.append(user['email'])
        return address_list
