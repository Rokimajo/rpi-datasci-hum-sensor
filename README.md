# rpi-datasci-hum-sensor

## Introduction
This repository contains all the elements involving my Data Science IoT project. I will be explaining why I chose this project, some steps I took along the way of developing this project, a short demo looking at the end product, and a tutorial to follow along. This project will be using a **Raspberry Pi 4 Model B** with the **Sense HAT V2** addon and is coded using **Python 3.11**. 

## Getting Started & My Project Idea
I had to think of a small, easy to implement idea that involves a working IoT prototype, and involves a personal problem that I want to solve. The only IoT device that I had a bit of experience with was the Raspberry Pi, so naturally that was my first option. This Raspberry Pi doesn't have a whole lot of sensors on it's own, so luckily mine came with the SenseHAT addon. This SenseHAT comes with several sensors:

- Gyroscope
- Accelerometer
- Magnetometer
- Temperature
- Barometric pressure
- Humidity
- Colour and brightness
> source: https://www.raspberrypi.com/documentation/accessories/sense-hat.html

Next up was choosing one or more of these sensors to solve a personal problem I had. Most of these are irrelevant to my situation, I wouldn't have much personal use for a Gyroscope or Magnetometer. The one that jumped out to me was **Humidity**, and let me explain why.

My room is on the highest floor, and sadly I have the problem of having quite a bit of humidity inside my room. This brings the annoying side effect of promoting mold growth if I don't watch this carefully. Luckily, I do have two windows that open on both sides, that can promote airflow and quickly get rid of this humidity.
But there is a catch. If the humidity outside is higher than inside, this will only worsen the effect.
> source on humidity & the effects of opening a window: https://housetrick.com/opening-windows-to-reduce-humidity/

So, the plan is this:
- Create a humidity measurement system so that I know when the humidity levels are too high, and I can go to my room to open a window.
- Use a Weather API to get the outside humidity of my location, and compare this to my room's humidity, if the humidity outside is greater, don't open your window. 

## The Process
First I had to know the humidity breakpoint where I would be in the "danger zone". I looked at alot of sources, and I found one that had a handy chart for alot of temperature levels, which has an impact on mold growth. The approximate point where risk would begin between all these temperatures would be a low 65% relative humidity level.
> source on chart: https://energyhandyman.com/knowledge-library/mold-chart-for-temperature-and-humidity-monitors/

Now I needed some way to get my local weather data because opening my window when the humidity is even worse outside, wouldn't help at all. After looking trough a couple API's, I landed at WeatherAPI.com because they offer you 1 million calls per month with a free account. Most other API's I found gave me only around 200-300 per day, WeatherAPI would give me considerably more.
> WeatherAPI.com: https://www.weatherapi.com/

```python
def get_weather_data():
	URL = f"http://api.weatherapi.com/v1/current.json?key={weatherAPI_key}&q={weatherAPI_city}&aqi=no"
	response = requests.get(URL)
	if response:
		print(f"Response OK! Code: {response}")
	else:
		print(f"Error occurred. Code: {response}")
	weather_data = response.json()["current"]["humidity"]
	return weather_data
 ```
I had some trouble figuring out how to exactly call WeatherAPI's data, but they have their call links readily available in their API explorer, At this point I only had to swap in the variables of my own api key, and the city I wanted the data from, and then isolate the humidity in their json with ```["current"]["humidity"]```

```python
hum_breakpoint = 65 # This is the humidity (%) breakpoint
open_window = True if local_hum >= hum_breakpoint and local_hum > city_hum else False
```
I wanted a nice and compact way of checking if I should open my window, from my experience with C# I knew that ternary operators might help me with this. This small code snippet checks if the humidity is equal or larger than 65%, which is the breakpoint I set earlier. It also checks if the humidity in your local space is larger than outside, because if it's not, opening your window would only worsen the effect.

```python
def send_sms():
	from twilio.rest import Client
	tw_client = Client(acc_SID, acc_AUTH)
	tw_client.messages.create(body=f"The humidity in your room is above your breakpoint ({hum_breakpoint}%). Open your window whenever possible.", from_=twilio_number, to=own_number)
	print("SMS OK!")
```

I also wanted the ability to send SMS messages if the user so wanted, so I set up a Twilio account, and installed their python package on my raspberry pi. I found out how to send SMS messages with Twilio in Python after searching around Twilio's own documentation. 
> source: https://www.twilio.com/docs/sms/tutorials/how-to-send-sms-messages-python
