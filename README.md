# Word100py
Python adaption of KD8BXP's library for Patrick Thomas Mitchell's Little/Big Buddy Talker boards, primarily targeted for the Raspberry Pi.

### TODO
* Acknowledgements
* Instructions
* Pin diagram for Raspberry Pi
* Create Wiki

In demo program indicate that the pins used
for MOSI, CLOCK, and CS don't have to be the
actual hardware pins, but could be.  If using
the hardware pins, disable SPI support in raspi-config (show how)

Support floating point for BBT (skip for LBT) by way of a
class field that get sets to true for BBT

Support passing sentences - should already work, but
needs to be tested

Test clock - seems like 24 hour clock off
at 0158.
