import time
import requests
from sense_hat import SenseHat

# Fill in all these fields with your own data.
# variables
hum_breakpoint = 65 # This is the humidity (%) breakpoint
update_interval = 300 # amount of seconds you want between posting

# WeatherAPI.com
weatherAPI_key = "" # The read key for WeatherAPI
weatherAPI_city = "" # The city name where WeatherAPI will get your data from. i.e: "Rotterdam"

# ThingSpeak
ts_writekey = "" # the write key of your ThingSpeak channel
ts_channelid = 0 # ThingSpeak channel ID

# Twilio (Optional)
send_sms = False # Enable whether you want to send sms messages to yourself.
				# Set this to false if you don't have Twilio or don't want to send messages.
acc_SID = "" # Your Twilio account SID
acc_AUTH = "" # Your twilio account Auth Token
twilio_number = +0 # Your twilio phone number, find this in account info after making a trial account.
own_number = +0 # Your own number, where twilio sends the message to.



# get the humidity from WeatherAPI.com (in %)
def get_weather_data():
	URL = f"http://api.weatherapi.com/v1/current.json?key={weatherAPI_key}&q={weatherAPI_city}&aqi=no"
	response = requests.get(URL)
	if response:
		print(f"Response OK! Code: {response}")
	else:
		print(f"Response error occurred. Code: {response}")
	weather_data = response.json()["current"]["humidity"]
	return weather_data
	
# get the humidity from your raspberry pi (in &)
def get_raspberry_data():
	sense = SenseHat()
	return sense.get_humidity()
	
# field 1 = Local Humidity
# field 2 = City Humidity
# field 3 = Difference
# field 4 = Open window?
def post_data(local_hum, city_hum, difference, open_window):
	ts_URL = f"https://api.thingspeak.com/update?api_key={ts_writekey}&field1={local_hum}&field2={city_hum}&field3={difference}&field4={int(open_window)}"
	response = requests.post(ts_URL)
	if (response):
		print(f"Post OK! Code: {response}")
	else:
		print(f"Post error occurred. Code {response}")

# make sure you've installed twilio with (pip install twilio) otherwise portion of code will crash.
# this ONLY applies if send_sms is set to True
def send_sms():
	from twilio.rest import Client
	tw_client = Client(acc_SID, acc_AUTH)
	tw_client.messages.create(body=f"The humidity in your room is above your breakpoint ({hum_breakpoint}%). Open your window whenever possible.", from_=twilio_number, to=own_number)
	print("SMS OK!")

def main():
	local_hum = get_raspberry_data()
	city_hum = get_weather_data()
	difference = abs(local_hum - city_hum)
	open_window = True if local_hum >= hum_breakpoint else False
	post_data(local_hum, city_hum, difference, open_window)
	if (send_sms and open_window):
		send_sms()
	
	
if __name__ == "__main__":
	while True:
		main()
		print(f"Sleeping for {update_interval / 60} minutes.\n")
		time.sleep(update_interval)
