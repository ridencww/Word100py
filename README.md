# Word100py
Python adaption of KD8BXP's library for Patrick Thomas Mitchell's Little/Big Buddy Talker boards, primarily targeted for the Raspberry Pi.

EngineeringShock Electronics has produced a number of products that are designed to add speech to Arduino projects. The boards use APlus Integrated Circuits voice playback chips. The Little Buddy Talker (LBT) has a 254 vocabulary while the Big Buddy Talker (BBT) supports over 1000 words. The vocabulary supplied is suitable for radio/electronics, IoT applications (wx, home automation, etc.), games, and more. 

http://www.engineeringshock.com/little-buddy-talker.html

Because these boards communicate via SPI, they can be used with a number of micro-controllers/micro-computers. This Python library allows a Raspberry Pi to drive these boards.

## Hardware connections

The LBT and BBT boards require 3-5 volts and will drive headphones or line out. The interface to the Pi is via SPI, requiring a MOSI, CLK, and CS (or four CS on the BBT). The library bit-bangs the LBT/BBT and does not use the hardware SPI on the Pi. The pins dedicated to the hardware SPI (19, 23, 24, and 29) can be used if SPI is disabled. By default, the hardware SPI on the Pi is disabled, but may have been changed using the raspi-config utility. If you want to use hardware SPI for other chips, just choose three (six for the BBT) available I/O pins.

* The Pi's I/O ports ARE NOT 5 volt tolerant. Connect 3.3 volts and ground from the Raspiberry Pi to the board. Do not use the 5 volt supply.

* For compatibility across Pi versions, the I/O numbering is based on the expansion connector pin number, NOT the GPIO designations.

Search for Raspberry Pi expansion pin-outs for more information. Here is one link that I found useful, note the nice table of expansion port pin-outs for the Raspberry Pi versions:

https://pimylifeup.com/raspberry-pi-gpio/

## Using the library

Copy the .py files to a folder on the Pi. Two sample programs, DemoLBT.py and DemoBBT.py have been provided to get you started.

##### Create an instance of a talker class:

`talker = WordsLBT(MOSI, CLK, CS0)`

or

`talker = WordsBBT(MOSI, CLK, CS0, CS1, CS2, CS3)`

##### Speak the time in 12 hour format:

`talker.say_time(hour, minute, True)` 
 
 or 24 hour format:
 
 `talker.say_time(hour, minute, False)`

##### Speak a number

`talker.say_number(123456)`

##### Speak one or more words

`talker.say(HELLO)`

`talker.say(RED, ALERT)`

`talker.say(THE, TEMPERATURE, IS, 20, DEGREES, CELSIUS)`

One second and half-second pauses are defined as constants and can be used in a say() call:

`talker.say(ALERT, PAUSE_1000, INTRUDER)`

Variables can be created that represent phrases that can be spoken later. Sentences, numbers, and words can be mixed in a say() call. Note the use of the expansion operator "*" when speaking pre-defined phrases.

`s1 = (ALERT, PAUSE_5000, DOOR)`

`s2 = (IS, OPEN)`

`talker.say(*s1, 8, *s2)`

The BBT introduced the letters of the alphabet in several languages. The voice defaults to English-Female, but can be set by a talker function or by embedding language constants in the say() call. 

The constants are:

* LANG_ENGLISH_FEMALE
* LANG_ENGLISH_MALE
* LANG_FRENCH
* LANG_ITALIAN
* LANG_PORTUGUESE
* LANG_RUSSIAN
* LANG_SPANISH

`talker.set_language(LANG_FRENCH)`

or, if you want to save the last language setting:

`last_language = talker.set_language(LANG_FRENCH)`

`talker.say(A, LANG_ENGLISH_MALE, B, LANG_FRENCH, C, LANG_ENGLISH_FEMALE`

Please note that this only impacts the speaking of the letters of the alphabet and not the rest of the words supported by the boards.



## On the radar

The Big Buddy Talker is nearing release and I expect to have my boards very soon. When I receive them, I will confirm the word offsets as I spotted a few that will need testing when I get the actual hardware.

The word, "POINT" has been added with the BBT, and when I receive my board, I will be supporting floating point numbers in the say_number function.

A refactor is being considered that will break out each AP23 chip into a separate module. This will allow the use of a single class, "Talker", instead of a number of classes extending talker. The biggest advantange is that if ElectronicShock comes out with a family of plugable chips, the user will be able to pick and choose which chips to use in a project.

## Acknowledgments

The functionality and structure of this library was patterned after the fine work by LeRoy Miller, who wrote the library for the Arduino. LeRoy did the heavy lifting, gathering up the word tables and defining the say() routines that really make the boards shine. LeRoy credited Mark Ganis for contribution of the original saynumber code, and I will extend my appreciation for his work as well.

https://github.com/kd8bxp/Word100

## License

Word100py is licensed under the [MIT][1] license. Permission is granted to anyone to use this software for any purpose, including commercial applications.

[1]: http://www.opensource.org/licenses/MIT

