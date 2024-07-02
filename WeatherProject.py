"""
Project:

Description: This program obtains weather data from Wundeground and delivers
             weather information to a user via Twilio's SMS service. It also
             recommends attire based on certain weather parameters.

Name: Shadab Sharif

Date: 3/4/2021

Notes:       You must install the Twilio library, the jsonschema library, and the urllib3 library

             using the SSH Terminal:

             sudo pip install urllib3
             sudo pip install twilio
             sudo pip install jsonschema

             or PyCharm > Preferences > Project Interpreter > "+"
             then enter urllib3 and click "install package"
             then enter twilio and click "install package"
             then enter jsonschema and click "install package"
             95cdc3a5e809c5e13ee862746f4dfd4e
"""

# -------------------------------------------------------------------------------

import json
import ssl
import urllib.request

from twilio.rest import Client

ssl._create_default_https_context = ssl._create_unverified_context


# TO DO: ADD YOUR CODE HERE
class Communication():
    """
    Class to get weather and send the created message
    """
    def __init__(self):
        self.temperature = ""
        self.weather = ""
        self.city = ""
        self.message = ""

    def get_weather(self, zipcode):
        """
        Retrieves weather from weather source and prints weather
        :param zipcode: Area to check the weather
        :return: Weather in given zipcode
        """
        url = "https://api.openweathermap.org/data/2.5/weather?zip=" + zipcode + "&APPID=95cdc3a5e809c5e13ee862746f4dfd4e" #website to get weather from
        f = urllib.request.urlopen(url)  # request the URL from openweathermap
        json_string = f.read()  # read the data returned into a string variable
        print('json_string: {}'.format(json_string))
        parsed_json = json.loads(json_string)  # convert the string to a json object
        self.city = parsed_json['name']
        self.temperature = parsed_json['main']['temp']
        self.weather = parsed_json['weather'][0]['description']
        self.message = "Current temperature in {} is: {} and there are {} ".format(self.city, self.temperature,
                                                                                   self.weather)
        f.close()  # close the URL request
        print(self.message)

    def send_sms(self, phone, message):
        """
        Sends the message with weather found
        :param phone: where to send the message
        :param message: Message to send to the phone
        :return:
        """

        account_sid = "AC56f3b6d84cd7303737b2c4954126eb10"  # token and account id from twilio
        auth_token = "5845d3f9cb10d1ea2441fe20f291a2ee"
        client = Client(account_sid, auth_token)

        try:
            client.api.account.messages.create(
                body=message,
                to=phone,
                from_=19202509816
            )
        except:
            print("There was an error sending your message")

    def create_message(self):
        """
        Creates the message to send
        :return: Returns message with information about the weather
        """
        msg = self.message
        temp = float(self.temperature)
        if self.weather.find("rain") >= 0 or self.weather.find("drizzle") >= 0 or self.weather.find(
                "thunderstorm") >= 0 or self.weather.find("snow") >= 0:
            msg += " You should take a raincoat"
        if temp <= 323.15:
            if self.weather.find("sunny") >= 0 or self.weather.find("clear") >= 0 or self.weather.find("clouds") >= 0:
                msg += " Wear a coat "
        print(msg)
        return msg


if __name__ == "__main__":
    com = Communication()
    com.get_weather("10128")
    com.send_sms("9174567572", com.create_message())  # Use your phone number, not this one.

