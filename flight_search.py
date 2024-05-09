import requests
from flight_data import FlightData
import os


class FlightSearch:
    #This class is responsible for talking to the Flight Search API.

    def __init__(self):
        # アクセストークンの取得
        token_endpoint = "https://test.api.amadeus.com/v1/security/oauth2/token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "client_credentials",
            "client_id": os.environ["CLIENT_ID"],
            "client_secret": os.environ["CLIENT_SECRET"],
        }
        response = requests.post(url=token_endpoint, headers=headers, data=data)
        self.access_token = response.json()["access_token"]

    # シートへIATAコードをセット
    def get_iata_code_list(self, sheet_data):
        # アクセストークンをヘッダにセット
        headers = {
            "Authorization": f"Bearer {self.access_token}",
        }
        # IATAコードリストの初期化
        iata_code_list = []
        # 都市名からIATAコードを取得
        for row in sheet_data:
            location_endpoint = "https://test.api.amadeus.com/v1/reference-data/locations"
            params = {
                "subType": "CITY",
                "keyword": row["city"],
            }
            response = requests.get(url=location_endpoint, headers=headers, params=params)
            iata_code_list.append([row["id"], response.json()["data"][0]["iataCode"]])
        return iata_code_list

    def check_flights(self, formatted_date, lowest_price, iata_code, city):
        headers = {
            "Authorization": f"Bearer {self.access_token}",
        }
        shopping_endpoint = "https://test.api.amadeus.com/v2/shopping/flight-offers"
        params = {
            "originLocationCode": "TYO",
            "destinationLocationCode": iata_code,
            "departureDate": formatted_date,
            "adults": 1,
            # "nonStop": "true",
            "currencyCode": "JPY",
            "maxPrice": lowest_price,
        }
        response = requests.get(url=shopping_endpoint,headers=headers, params=params)
        data = response.json()["data"]
        found_flights_list = []
        for x in data:
            flight_data = FlightData(
                round(float(x['price']['total'])),
                city,
                x['itineraries'][0]['segments'][-1]['arrival']['iataCode'],
                x['itineraries'][0]['segments'][0]['departure']["at"][0:10],
                x['itineraries'][0]['segments'][-1]['arrival']["at"][0:10]
            )
            found_flights_list.append(flight_data)
        return found_flights_list