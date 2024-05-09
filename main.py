from flight_search import FlightSearch
from data_manager import DataManager
from notification_manager import NotificationManager
from datetime import datetime, timedelta


flight_search = FlightSearch()
data_manager = DataManager()
prices_sheet_data = data_manager.get_price_sheet_data()

iata_code_list = flight_search.get_iata_code_list(prices_sheet_data)
data_manager.set_iata_code_to_sheet(iata_code_list)

address_list = data_manager.get_address_list()

notification_manager = NotificationManager()

for row in prices_sheet_data:
    now = datetime.now()

    # for x in range(60):
    for x in range(1):
        next_day = now + timedelta(days=x)
        formatted_date = next_day.strftime("%Y-%m-%d")

        flights_list = flight_search.check_flights(formatted_date, int(row['lowestPrice']), row['iataCode'], row['city'])

        # notification_manager.telegram_bot_send_text(flights_list)
        notification_manager.send_email(address_list, flights_list)