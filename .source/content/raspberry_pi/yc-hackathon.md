title: YCombinator Hardware Hackathon
date: 05/3/2013

I recently participated in the [Upverter + YCombinator Hardware
Hackathon](http://upverter.com/hackathons/yc-hackathon-2013/), where my team
placed first overall.

You can find my TechCrunch interview about the event here:
[http://techcrunch.com/2013/02/26/y-combinator-hardware-hackathon-winner/](
http://techcrunch.com/2013/02/26/y-combinator-hardware-hackathon-winner/)

I went it with only an idea, and spent the first half hour trying to convince
other people to spend their day hacking with me.

The hackathon lasted about 10 hours, and the goal was to design and build a
prototype hardware device. For our entry, my team built a wearable force
feedback glove. When worn, the glove is able to simulate the feeling of holding
a physical object.

Here is a picture of the completed glove:

<img src='/images/hackathon/glove.jpg' width=600>

A device like this could be used for gaming, surgical assistance, or a number
of other augmented reality applications. I have been interested in expanding
the human-computer interface for a while, and this project allowed me to open
up another channel for computers to feed back information to humans.

Mechanical Design
-----------------
A length of twine is connected from the glove's fingertips, through two guiding
braces, and back to a hobby servo. This is repeated for each finger. The servo
is connected to a platform which is connected to the back of the glove. When
the servo is actuated it pulls back on the twine holding the fingers open.
Through this process we are able to simulate the resistive force of an object
holding the wearers hand open.

<img src='/images/hackathon/diagram.jpg' width=600>

_-Drawing by teammember Tom Sherlock_

For the demo at the competition, we used a distance sensor to set the hand
position. The closer your hand was to the distance sensor, the more your
fingers were pulled open. This simulated the feeling of squeezing a virtual
object in your hand.

The distance sensor used was a HC-SR04 Ping Sensor:

<img src='/images/hackathon/hc-sr04.jpg' width=600>

Hardware I/O
------------
To control servos and read from sensors usually you use GPIO pins. In our case
we used the GPIO pins on a Raspberry Pi. If you would like to know more about
hardware control with a Raspberry Pi check out my
[article](/raspberry_pi/opendevreal_world/) on that
topic.

The basic idea is that you can set the voltage on a GPIO pin high (5 volts) or
low (0 volts). Sending the correct sequence of high and low pulses to a servo
will cause it to go to a certain position. You can also read whether a certain
pin is high or low. If you connect a sensor to GPIO pin, it is able to
communicate information by sending specific sequences of high and low pulses.


Control Software
----------------
To control the GPIO pins I wrote a Python script that you can find here:
[https://gist.github.com/jminardi/5022297](https://gist.github.com/jminardi/5022297)

This script uses a library I wrote called
[RobotBrain](https://github.com/jminardi/RobotBrain). It sits on top of
[RPi.GPIO](https://pypi.python.org/pypi/RPi.GPIO) and provides a higher level
interface for controlling individual pins and motors. The only module used in
this project was the Servo, which makes it easy to set a servo to a given
position. The Servo module uses the
[ServoBlaster](https://github.com/richardghirst/PiBits/tree/master/ServoBlaster)
kernal module under the covers, which exposes the servo as device in the
filesystem.

Conclusion
----------
In the end I had a great time at the hackathon. I think we were able to put
together a winning demo in part because of the power of Python. With just a few
libraries you are able to reason at a high level about what you wanted your hardware
to do and what your sensors are seeing. If you have ever tried doing hardware
control in a lower level language, you know just how hard that can be, and as
you can see, how easy Python makes it.

<img src='/images/hackathon/team.jpg' width=600>

_The team after our victory_
