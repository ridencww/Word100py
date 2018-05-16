import datetime

from WordsBBT import *

# Create an instance of the LBT class. Must specify the PIN numbers (not GPIO numbers)
# on the Pi's expansion connector for MOSI, CLK, and CS respectively.
# These are the same pins used for the hardware SPI. Be sure that SPI is disabled in
# the raspi-config utility or if you need hardware SPI, use six unused I/O ports.
talker = WordsBBT(19, 23, 24, 29, 31, 33)

# Saying numbers
talker.say_number(123456)
time.sleep(0.5)
talker.say_number(-112)

time.sleep(1)

# Current time in 12 hour and 24 hour formats
now = datetime.datetime.now()
talker.say_time(now.hour, now.minute, True)
time.sleep(0.5)
talker.say_time(now.hour, now.minute, False)

time.sleep(1)

# Pre-defined sentence
# When saying pre-defined sentences, be sure to use the expansion operator "*"
s1 = (INCOMING, MESSAGE, RECEIVED)
talker.say(*s1)

time.sleep(1)

# Alert combining words, pauses, and numbers
talker.say(INTRUDER, INTRUDER, PAUSE_1000, DEACTIVATE, SECURITY, DOOR, 12, WEST)

time.sleep(1)

# Reduce inter-word time (will be choppy in _PLAY mode)
old_delay = talker.set_delay(0.4)
talker.say_number(13223456)
time.sleep(0.5)
talker.say_number(-123)

time.sleep(1)

# Switch to _LOAD mode, which is a bit quicker
talker.set_load_mode()
talker.say_number(13223456)
time.sleep(0.5)
talker.say_number(-123)

# Restore to defaults
talker.set_play_mode()
talker.set_delay(old_delay)

time.sleep(3)

# Say all the words
talker.say_all()
