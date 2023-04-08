# rpi-datasci-measurements

## Introduction
This repository contains all the elements involving my Data Science IoT project. I will be explaining why I chose this project, some steps I took along the way of developing this project, a short demo looking at the end product, and a tutorial to follow along. This project will be using a **Raspberry Pi 4 Model B** with the **Sense HAT V2** addon and is coded using **Python 3.11**. 

## Getting Started & My Project Idea
I had to think of a small, easy to implement idea that involves a working IoT prototype, and involves a personal problem that I want to solve. The only IoT device that I had a bit of experience with was the Raspberry Pi, so naturally that was my first option. This Raspberry Pi doesn't have a whole lot of sensors on it's own, so luckily mine came with the SenseHAT addon. This SenseHAT comes with a modicum of sensors:

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
