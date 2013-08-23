title: Android Controlled Toy Car
date: 9/12/2012

I wanted to build something fun that would introduce me to hardware control 
with the Raspberry Pi. I decided to build a small car that could be
controlled with my phone's accelerometer.

Here is a picture of the fully assembled car:

<img src='/static/images/toycar/assembled.jpg' width=600>

I wrote an [android app](https://github.com/jminardi/RobotBrain-Controller)
that streams the accelerometer data from the phone to the pi over a simple
socket.  The pi then uses this data to drive the DC motor and the servo motor.
Tilting the phone to control the car feels very natural.

In this pic you can see the wifi dongle I've used:

<img src='/static/images/toycar/raspberrypi.jpg' width=600>

I am using Adafruit [Occidental
v0.2](http://learn.adafruit.com/adafruit-raspberry-pi-educational-linux-distro/occidentalis-v0-dot-2)
as my OS because it has support for my wifi dongle. It also makes some hardware
interaction easier and comes pre-installed with a few good python libraries.

Here is a picture of the breadboard:

<img src='/static/images/toycar/breadboard.jpg' width=600>

I am using the
[L293DNE](http://www.mouser.com/ProductDetail/Texas-Instruments/L293DNE/?qs=sGAEpiMZZMtYFXwiBRPs0wSafWlCmJbc)
hbridge chip for DC motor control. The two black wires you see coming off the
board connect to the motor.

In this pic is the battery pack I am using to power the pi:

<img src='/static/images/toycar/charger.jpg' width=600>

I purchased it on amazon
[here](http://www.amazon.com/PowerGen-External-Blackberry-Sensation-Thunderbolt/dp/B005VBNYDS).

Here is a pic of the battery pack I am using for the DC motor:

<img src='/static/images/toycar/batterypack.jpg' width=600>

Here is a closeup of the steering servo:

<img src='/static/images/toycar/servo.jpg' width=600>

It is an [HS-55](http://www.servocity.com/html/hs-55_sub-micro.html) and I
power it directly from the pi's 5v rail. To control it I use the [servoblaster
kernal module](https://github.com/richardghirst/PiBits) and my own servo
control library [RobotBrain](https://github.com/jminardi/RobotBrain)

My next plans are to add some sensors and make it autonomous.
