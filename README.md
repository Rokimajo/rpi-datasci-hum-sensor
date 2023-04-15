# rpi-datasci-hum-sensor

## Introduction
This repository contains all the elements involving my Data Science IoT project. I will be explaining why I chose this project, some steps I took along the way of developing this project, a short demo looking at the end product, and a tutorial to follow along. This project will be using a **Raspberry Pi 4 Model B** with the **Sense HAT V2** addon and is coded using **Python 3.9.2** alongside [ThingSpeak](https://thingspeak.com/) for data visualization and [Twilio](https://www.twilio.com/en-us) for SMS sending. 

## Getting Started & My Project Idea
I had to think of a small, easy to implement idea that involves a working IoT prototype, and involves a personal problem that I want to solve. The only IoT device that I had a bit of experience with was the Raspberry Pi, so naturally that was my first option. This Raspberry Pi doesn't have a whole lot of sensors on it's own, so luckily mine came with the SenseHAT addon. This SenseHAT comes with several sensors[^1]:

- Gyroscope
- Accelerometer
- Magnetometer
- Temperature
- Barometric pressure
- Humidity
- Colour and brightness

Next up was choosing one or more of these sensors to solve a personal problem I had. Most of these are irrelevant to my situation, I wouldn't have much personal use for a Gyroscope or Magnetometer. The one that jumped out to me was **Humidity**, and let me explain why.

My room is on the highest floor, and sadly I have the problem of having quite a bit of humidity inside my room. This brings the annoying side effect of promoting mold growth if I don't watch this carefully. Luckily, I do have two windows that open on both sides, that can promote airflow and quickly get rid of this humidity.
But there is a catch. If the humidity outside is higher than inside, this will only worsen the effect[^2].

So, the plan is this:
- Create a humidity measurement system so that I know when the humidity levels are too high, and I can go to my room to open a window.
- Use a Weather API to get the outside humidity of my location, and compare this to my room's humidity, if the humidity outside is greater, don't open your window. 

## The Process
First I had to know the humidity breakpoint where I would be in the "danger zone". I looked at alot of sources, and I found one[^3] that had a handy chart for alot of temperature levels, which has an impact on mold growth. The approximate point where risk would begin between all these temperatures would be a low 65% relative humidity level.

Now I needed some way to get my local weather data because opening my window when the humidity is even worse outside, wouldn't help at all. After looking trough a couple API's, I found the site [WeatherAPI](https://www.weatherapi.com/), they offer you 1 million calls per month with a free account. Most other API's I found gave me only around 200-300 per day, WeatherAPI would give me considerably more.

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

I also wanted the ability to send SMS messages if the user so wanted, so I set up a [Twilio](https://www.twilio.com/en-us) account, and installed their python package on my raspberry pi. I found out how to send SMS messages with Twilio in Python after searching around Twilio's own documentation[^4]. 

## Conclusion
Apart from a few complications which I talked about in **The Process**, the project went pretty smoothly. I never used push notifications before in a project, and using another API to grab data based on location was fun to try out. This was also the first time I used ThingSpeak to visualize the data easily, I've had a few other projects where I visualized data, but it was always using python's ```matplotlib```. ThingSpeak is alot easier to set up and modify. I think this project does a pretty good job showing you all the data, so you can make an accurate decision on whether to air out your room or not. Especially if you opt-in to use Twilio for the SMS push notifications.

## Video Demo
For the purposes of this demo, I've set the ```update_interval``` to **15** seconds and set the ```hum_breakpoint``` to **20%**. I also turned off the check that looks at the ```City Humidity (%)``` field, because during my testing the city's humidity was always around 60. Normally you will only get a push message if your local humidity is above your set breakpoint AND the city's humidity is lower than your local. Hopefully this will show how this project is supposed to work if your local humidity is too high. Note: The lamp next to Field 4 turns bright green when you are supposed to open your window. 


https://user-images.githubusercontent.com/103335427/232224833-9f850fbf-bc48-4bd0-9b87-b3e02a3e3311.mp4

## Tutorial
You will need:
- A Raspberry Pi compatible with the Sense HAT addon *(All Raspberry Pi's with 40 pin connectors are compatible.)*
- A Sense HAT
- A [ThingSpeak](https://thingspeak.com/) Account
- A [WeatherAPI](https://www.weatherapi.com/)
- A [Twilio](https://www.twilio.com/en-us) Account *(Optional)*


### [ThingSpeak](https://thingspeak.com/) ------------------------
After you've made your ThingSpeak account, make a channel. You should see this bright green button.

![Capture](https://user-images.githubusercontent.com/103335427/232225411-3a24bfad-8fe1-4f57-a70b-70cdd4099ff5.PNG)


Now, create these four fields in this order and save the channel on the button below.

![Capture](https://user-images.githubusercontent.com/103335427/232225591-7552d021-3a00-4e88-8777-53c93c0c9bdb.PNG)

![Capture](https://user-images.githubusercontent.com/103335427/232225626-2b6871f6-2601-420c-a7e5-b4d3dffc4dc6.PNG)

Now, for Fields **1-3** you should make these 3 widgets. Go to **Add Widgets**:

![Capture](https://user-images.githubusercontent.com/103335427/232225744-f61e28c2-d613-4a98-83ea-f1109a219b2d.PNG)

Click on **Numeric Display**:

![Capture](https://user-images.githubusercontent.com/103335427/232225802-85bbaf0c-2b73-4129-bbf1-0ef77ed01eb2.PNG)

For widgets 1, 2 and 3 enter the same name as the Channel Field name we gave them. [**Local Humidity (%), City Humidity (%), Difference (%)**]
Don't forget to make them an integer, because they're supposed to be whole percentages.

![Capture](https://user-images.githubusercontent.com/103335427/232225966-09f42785-3f5f-4604-9d1e-5a0281042e6f.PNG)

When that's done, you're ready to create widget 4. Go back to the widget menu and choose **Lamp Indicator**:

![Capture](https://user-images.githubusercontent.com/103335427/232226066-cab80ef0-36c0-43ec-94f5-bb15cb74f4a6.PNG)

And enter the following settings. This will make the lamp turn on when [hum_sensor.py](https://github.com/Rokimajo/rpi-datasci-hum-sensor/blob/main/hum_sensor.py) sends ```True``` to ThingSpeak.

![Capture](https://user-images.githubusercontent.com/103335427/232226161-5deae121-a306-4d7e-9c78-470a25ad2d85.PNG)

Now that your fields are all set up, you can go into the code and modify the fields you need:

```python
# ThingSpeak
ts_writekey = "key_here" # the write key of your ThingSpeak channel
ts_channelid = 0 # ThingSpeak channel ID
```
You can find your API Write Key under the ```API Keys``` tab in ThingSpeak:

![Capture](https://user-images.githubusercontent.com/103335427/232227152-63e20693-eaed-44e8-8e2d-944da6aeb2f1.PNG)

And you can find your Channel ID in the top left, when you are inside the channel:

![Capture](https://user-images.githubusercontent.com/103335427/232227237-e0fd480c-8278-4b56-bf20-88a02391723e.PNG)


### [WeatherAPI](https://www.weatherapi.com/) ------------------------

Go to the [WeatherAPI](https://www.weatherapi.com/) website, and create an account.
After you've made an account, make sure you're on the dashboard page:


![tempsnip](https://user-images.githubusercontent.com/103335427/232227561-58a256ee-308a-485c-95f3-132a09a1bd4a.png)

As you can see the API key is right there, now simply copy your key and paste it in the right [hum_sensor.py](https://github.com/Rokimajo/rpi-datasci-hum-sensor/blob/main/hum_sensor.py) section:
```python
# WeatherAPI.com
weatherAPI_key = "key_here" # The read key for WeatherAPI
weatherAPI_city = "city_here" # The city name where WeatherAPI will get your data from. i.e: "Rotterdam"
```
Also don't forget to enter the city you want to get the data from.

Great! Now you're done. If you let [hum_sensor.py](https://github.com/Rokimajo/rpi-datasci-hum-sensor/blob/main/hum_sensor.py) run for a while, you should see something like this:

![Capture](https://user-images.githubusercontent.com/103335427/232226277-99062be6-8dc9-489a-b590-7e97ab565a01.PNG)

### [Twilio](https://www.twilio.com/en-us) (Optional) ------------------------
If you want to send push notifications to yourself, follow this second part of the tutorial aswell.
First. Install twilio on your Raspberry Pi machine, You can do this by typing ```pip install twilio``` in your raspberry's terminal.
It should look something like this:

![2023-04-15-122843_1920x1080_scrot](https://user-images.githubusercontent.com/103335427/232226469-be931ef9-1f25-4156-bbf2-3b2568c7500b.png)

Now, make a [Twilio](https://www.twilio.com/en-us) account. After you've succesfully made an account and verified your email, you should see a screen that looks like this:


![Capture](https://user-images.githubusercontent.com/103335427/232226626-957622d1-2878-4ab4-9a47-089148d4a4d7.PNG)

Since this is a new account, you won't have a virtual twilio phone number like I do in this picture, You should see a button somewhere under Step 1 that allows you to quickly make one after you've verified your e-mail, when you have the green checkmark like in the picture, you're good to go.

Now, take note of your following account info, because you'll need to insert these into the [hum_sensor.py](https://github.com/Rokimajo/rpi-datasci-hum-sensor/blob/main/hum_sensor.py) code:

![Capture](https://user-images.githubusercontent.com/103335427/232226780-e8e52291-d757-4a5b-a809-46f984567f58.PNG)

```python
# Twilio (Optional)
send_sms = False # Enable whether you want to send sms messages to yourself. 
				# Set this to false if you don't have Twilio or don't want to send messages.
acc_SID = "SID_here" # Your Twilio account SID
acc_AUTH = "AUTH_here" # Your twilio account Auth Token
twilio_number = +0 # Your twilio phone number, find this in account info after making a trial account.
own_number = +0 # Your own number, where twilio sends the message to.
```
Set send_sms to ```True``` if you're planning to send SMS messages to yourself, and fill all the fields with your own account information.
After that, you're all done! You should now get SMS messages if your humidity passes your given breakpoint and it's not more humid outside.

### Other Resources
[My ThingSpeak Channel](https://thingspeak.com/channels/2108056)

### Reference List

[^1]: https://www.raspberrypi.com/documentation/accessories/sense-hat.html
[^2]: https://housetrick.com/opening-windows-to-reduce-humidity/
[^3]: https://energyhandyman.com/knowledge-library/mold-chart-for-temperature-and-humidity-monitors/
[^4]: https://www.twilio.com/docs/sms/tutorials/how-to-send-sms-messages-python
