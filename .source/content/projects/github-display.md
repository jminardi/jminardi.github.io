title: Displaying Realtime Github Activity on a Full Color LED Matrix
date: 13/10/2013

## Overview

![LED Matrix](|filename|/images/project-banners/gh-display.png)

The goal of this project was to display real time activity from my companies
Github feed. I used an RGB LED matrix to display information about the last 30
events, including the username of whoever is responsible for the most recent
event.

Here is a video of the display operating.

<iframe width="600" height="450" src="//www.youtube.com/embed/zrsNJpTwHrw" frameborder="0" allowfullscreen></iframe>

This project uses the following hardware:

* Arduino
* [Electric Imp][50] and [Breakout Board][51]
* [TiM Board][52] (8x16 RGB LED Display)
* 4.5 V power supply.
* A few jumper cables

[50]: https://www.sparkfun.com/products/11395
[51]: https://www.sparkfun.com/products/11400
[52]: http://www.seeedstudio.com/depot/tim-p-1516.html

You can find all the software on
[Github](https://github.com/jminardi/github-events-display) or at the end of
this article.

## Free Hardware!

I met Justin Shaw at SciPy 2013, where we talked about software development and
open hardware hacking. He told me about his company [Wyolum][0] that focuses on
open source hardware. He explained that they have a [Google+ Page][1] where
they routinely give away hardware to people who promise to do cool things with
it.

I joined immediately and the first hardware giveaway was a full color 8x16
smart LED matrix known as [The intelligent Matrix (TiM board)][2]. I applied
with the idea of building a real time Github activity display for the breakroom
at my office. My idea was selected and Wyolum sent me a TiM board. (In fact,
everyone who entered with an idea was sent one -- You should join now!)

[0]: http://wyolum.com/
[1]: https://plus.google.com/communities/101981201962256466651
[2]: http://www.seeedstudio.com/depot/tim-p-1516.html

## The intelligent Matrix

The TiM board is made made up of 128 "Smart Pixels", which are full
color RGB LEDs. Each LED has its own control circuit, making it easy to
control many LEDs with a single GPIO pin. The specific type of smart pixels used
in the TiM board are 5050-WS2811. You can find more details about the board in
the [User Guide][3]

[3]: https://docs.google.com/a/minardi.org/document/d/1szTSpMLkoYj53_0VNPQfEkWC-Doyp6mj_TT7GCWduIA/edit

I decided to operate my board in serial mode, so I soldered the pads on the
back. I also soldered a couple of header pins to make it easier for me to
connect power and signal to the board. See below for photos of the soldered 
pads and header pins:

<a href='/images/gh-display/shorted-pads.jpg', id='borderless'>
<img src='/images/gh-display/shorted-pads.jpg' id='borderless' width=400>
</a>

_Connecting these pads lets me operate the TiM board in "serial mode"._

<a href='/images/gh-display/header-pins.jpg', id='borderless'>
<img src='/images/gh-display/header-pins.jpg' id='borderless' width=400>
</a>

_I soldered on some header pins to make connections easier._

## The Internet of Things with an Electric Imp

I needed some method to collect data about github events. Luckily for me,
Github makes it incredibly easy to get activity information using their
[API][4]. All I had to do was generate an access token for my account and I was
able to easily request the latest organization events using this URL:

    https://api.github.com/orgs/enthought/events?access_token=<mytoken>

Since I built this project with an Arduino, I needed some way to access the 
Internet easily. There are a couple of methods for connecting an Arduino to the
Internet, and in the end I choose to use an [Electric Imp][5] and breakout
board. (I choose this because the company was giving them away at the
[YCombinator Hardware Hackathon][6], so I just had one lying around.)

[4]: http://developer.github.com/
[5]: http://electricimp.com/
[6]: /raspberry_pi/ycombinator-hardware-hackathon/

The Electric Imp breakout board I have has to be programmed in a language
called [Squirrel][7], which is a C like language designed for embedded
platforms. Programming with the Imp involves writing code for two platforms:
The "Agent" which is some machine in the cloud, and the "Imp" which is the
actual hardware on my desk. The Imp sends a message to the agent, which hits
the Github API and returns the desired data.

[7]: http://www.squirrel-lang.org/doc/squirrel3.html

## Simplifying Display Logic with Adafruit's NeoMatrix Library

On the Arduino side of things I decided to use Adafruit's [NeoMatrix][8]
library to drive the LED display. While the TiM board I am using is not an
Adafruit product, I was still able to make use of their open source software
libraries. Yay for open source!

[8]: http://learn.adafruit.com/adafruit-neopixel-uberguide/neomatrix-library

## Data Flow

I wanted to centralize all my processing to the Arduino, and treat the Imp like
a dumb component. However due to memory constraints on the Arduino I had to
offload some of the computation to the Imp. The general dataflow I implemented
is:

1. Arduino sends a load request ("l") to the Imp over serial.

2. The Imp receives this request and sends a message to the "Agent" to request
 the Github data

3. The agent receives this request, loads the data, and sends it as a response.

4. The Imp receives the Github data and stores it.

5. Arduino sends a next chunk request ("c") over serial. Chunk size is 60 bytes.

6. Imp receives this chunk request and sends the next chunk of Github data
 over serial.

7. Arduino keeps requesting the next chunk of data until the end of message
 character ("$") arrives.

8. Once the whole message has been transmitted, the Arduino processes it and
 outputs to the LED display.

9. Rinse and repeat.

## Parting Thoughts

I am by no means an expert programmer on the Arduino or Electric Imp. The code
I ended up with works, but I make no promises that it is the best way to do
things.

While I was able to build what I set out to build, I can't help but feel that
I'm not using this brilliant color LED matrix to its full potential. At any
given time I am only displaying ~10 different colors, while the board is
capable of displaying 2^24 different colors per pixel! I think my next step is
to display the users downsampled avatar on the display. It will be cool to see
just how much detail a viewer can discern on a 8x16 display. Stay tuned for
updates in that area!

Question? Reach out to me on [twitter](https://www.twitter.com/jackminardi)

## Appendix

### Connections

I should probably do a proper diagram, but for know I will simply list the
connections needed for the software to work:

* Arduino 5V -> Imp VIN
* Arduino Gnd -> Imp GND
* Arduino Pin 9 -> Imp Pin5
* Arduino Pin 10 -> Imp Pin7
* Arduino Pin 6 -> TiM Serial Data In
* Power Supply 5V and Ground -> TiM Power Pins

### Code

If you'd rather git pull than copy/paste go
[here](https://github.com/jminardi/github-events-display).

#### Arduino

```
#include <SoftwareSerial.h>
#include <Adafruit_GFX.h>
#include <Adafruit_NeoMatrix.h>
#include <Adafruit_NeoPixel.h>

#define PIN 6
#define WIDTH 16
#define HEIGHT 8

// Parameter 1 = number of pixels in strip
// Parameter 2 = pin number (most are valid)
// Parameter 3 = pixel type flags, add together as needed:
//   NEO_KHZ800  800 KHz bitstream (most NeoPixel products w/WS2812 LEDs)
//   NEO_KHZ400  400 KHz (classic 'v1' (not v2) FLORA pixels, WS2811 drivers)
//   NEO_GRB     Pixels are wired for GRB bitstream (most NeoPixel products)
//   NEO_RGB     Pixels are wired for RGB bitstream (v1 FLORA pixels, not v2)

Adafruit_NeoMatrix matrix = Adafruit_NeoMatrix(WIDTH, HEIGHT, PIN,
  NEO_MATRIX_TOP     + NEO_MATRIX_RIGHT +
  NEO_MATRIX_ROWS    + NEO_MATRIX_PROGRESSIVE,
  NEO_GRB            + NEO_KHZ800);
 
//defining the Pins for TX and RX serial communication
SoftwareSerial electricimpSerial = SoftwareSerial(9,10);

char character;
String content;

char eventSeparator = ',';
char itemSeparator = '.';
String lastActor;
String first = "^";
String last = "$"; 

byte ghEvents[30];

void setup() {
    Serial.begin(9600);
    electricimpSerial.begin(9600);
    
    electricimpSerial.print("l");  //load giithub data
    delay(500);
    electricimpSerial.print("c");  //prepare first chunk
    
    matrix.begin();
    matrix.setTextWrap(false);
    matrix.setBrightness(255);
 }

void loop() {
  while(electricimpSerial.available() > 0) {
     character = electricimpSerial.read();
     content += character;
  }
  if (character == '$') {
    electricimpSerial.print("l");
    delay(500);
    Serial.println(content);
    processContent();
    content = "";
  }
  electricimpSerial.print("c");
  delay(500);
 }
 
void processContent() {
  if (!content.startsWith(first) || !content.endsWith(last))
    return;  // bail if content string is invalid
    
  int start_idx = 0;
  int end_idx = 0;
  int loop_idx = 0;
  while (end_idx != -1) {
    
    if (loop_idx > 0) {
      String sub = content.substring(start_idx+1, end_idx);      
      int item_break = sub.indexOf(itemSeparator);
      String actor = sub.substring(0, item_break);
      String event = sub.substring(item_break+1);
      Serial.println(actor + "***" + event);
      
      byte x = (loop_idx-1) % (WIDTH/2);
      byte y = (loop_idx-1) / (WIDTH/2);
      
      if (loop_idx-1 < sizeof(ghEvents))
        ghEvents[loop_idx-1] = (byte)event[0];
      if (loop_idx == 1) lastActor = actor;
    }
    
    start_idx = end_idx;
    end_idx = content.indexOf(eventSeparator, end_idx+1);
    loop_idx++;

  }
  
  drawText();
}

void drawText() {
  
  for (int i; i < 100; i++) {
    drawData();  
    matrix.setCursor(WIDTH-i, 0);
    matrix.print(lastActor);
    matrix.setTextColor(matrix.Color(255, 255, 255));
    matrix.show();
    delay(70);
  }
}

void drawData() {
  int len = sizeof(ghEvents);
  matrix.fillScreen((ghEvents[0]*10)<<8);
  for (int i = 0; i < len; i++) {
    byte val = ghEvents[i];
    byte x = (i+2) % (WIDTH/2);
    byte y = (i+2) / (WIDTH/2);
    set2x2(x, y, val);
  }
  matrix.drawPixel(15, 0, matrix.Color(0, 255, 0));
}

void set2x2(byte x, byte y, byte e) {
  x = 2*x;
  y = 2*y;
  matrix.drawRect(x, y, 2, 2, (e*10)<<8); 
}
```

#### Agent

```
function HttpGetWrapper (url, headers) {
  local request = http.get(url, headers);
  local response = request.sendsync();
  return response;
}

function pollGithub(param) {
    local url = "https://api.github.com/orgs/enthought/events?access_token=nope";
    local result = HttpGetWrapper(url, {});
    local body = result["body"];
    local obj = http.jsondecode(body);
    //server.log(param);
    local to_send = "";
    foreach(event in obj) {
        local actor = event["actor"]["login"];
        local type = event["type"];
        type = ::eventMap[type];
        to_send += actor + "." + type + ",";
    }
    device.send("res", to_send)
}

device.on("req", pollGithub)

::eventMap <- {
    "CommitCommentEvent": "a"
    "CreateEvent": "b"
    "DeleteEvent": "c"
    "DownloadEvent": "d"
    "FollowEvent": "e"
    "ForkEvent": "f"
    "ForkApplyEvent": "g"
    "GistEvent": "h"
    "GollumEvent": "i"
    "IssueCommentEvent": "j"
    "IssuesEvent": "k"
    "MemberEvent": "l"
    "PublicEvent": "m"
    "PullRequestEvent": "n"
    "PullRequestReviewCommentEvent": "o"
    "PushEvent": "p"
    "ReleaseEvent": "q"
    "StatusEvent": "r"
    "TeamAddEvent": "s"
    "WatchEvent": "t"
}
```

#### Imp

```
local old_payload = "";

function readSerial() {
 
    local result = hardware.uart57.read();
    if (result == 99) {  //"c" in ASCII
        server.log("chunk - " + result);
        server.log("calling sendNextChunk()")
        sendNextChunk();
    } else if (result == 108) { //"l" in ASCII
        server.log("load - " + result);
        server.log("sending req to agent")
        agent.send("req", result);
    }
    imp.wakeup(0.1, readSerial);
}

function sendNextChunk() {
    server.log("sendNextChunk() called");
    local chunk_size = 60;
    local to_send = "";
    if (old_payload.len() < chunk_size) {
        to_send = old_payload;
        old_payload = "";
    } else {
        to_send = old_payload.slice(0, chunk_size);
        old_payload = old_payload.slice(chunk_size);
    }
    server.log("to_send: " + to_send)
    hardware.uart57.write(to_send);
}

function saveGithub(payload) {
  server.log("payload: " + payload);
  old_payload = "^" + payload + "$";
}
 
agent.on("res", saveGithub);

hardware.uart57.configure(9600, 8, PARITY_NONE, 1, NO_CTSRTS);
server.log("starting...");
readSerial();
```
