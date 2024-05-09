import requests
import smtplib
from email.mime.text import MIMEText
import os


class NotificationManager:

    def __init__(self):
        self.bot_token = os.environ["BOT_TOKEN"]
        self.bot_chatID = os.environ["BOT_CHATID"]

    def telegram_bot_send_text(self, flights_list):
        for flight in flights_list:
            bot_message = f"Low price alert! Only {flight.price}yen to fly from Tokyo-TYO to {flight.arrival_city}-{flight.arrival_iata_code}, from {flight.departure_date} to {flight.arrival_date}."

            endpoint = ('https://api.telegram.org/bot' + self.bot_token + '/sendMessage?chat_id=' +
                        self.bot_chatID + '&parse_mode=Markdown&text=' + bot_message)

            response = requests.get(endpoint)

            return response.json()

    def send_email(self, address_list, flights_list):
        my_email = os.environ["MY_EMAIL"]
        password = os.environ["PASSWORD"]

        for address in address_list:
            for flight in flights_list:
                text = f"Low price alert! Only {flight.price}yen to fly from Tokyo-TYO to {flight.arrival_city}-{flight.arrival_iata_code}, from {flight.departure_date} to {flight.arrival_date}."

                # MIMETextオブジェクトを作成し、メールの内容を設定する
                msg = MIMEText(text, 'plain', 'utf-8')
                msg['Subject'] = "Discounted flight information"
                msg['From'] = my_email
                msg['To'] = address

                with smtplib.SMTP("smtp.gmail.com") as connection:
                    connection.starttls()
                    connection.login(user=my_email, password=password)
                    connection.send_message(msg)