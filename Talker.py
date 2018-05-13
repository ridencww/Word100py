import time

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO.  Do you need to use sudo?")

PAUSE_500 = ("p", 0.5)
PAUSE_1000 = ("p", 1.0)


class Talker(object):
    clk = 0
    mosi = 0
    cs = []
    
    NUMBER_ONES = None
    NUMBER_TEENS = None
    NUMBER_TENS = None
    NUMBER_MISC = None

    # Sound chip commands from AP23.pdf specificaiton sheet
    # https://www.es.co.th/Schemetic/PDF/AP23.PDF
    #
    # Play sound, interrupting currently playing sound, if necessary
    _PLAY = 0x98
    # load sound and play after current sound has finished,
    _LOAD = 0x94 
    # Power up chip, raising output voltage to midway point to avoid pops
    _POWER_UP_WITH_RAMP = 0XA8
    # Power down chip, decreasing output voltage to zero to avoid pops
    _POWER_DOWN_WITH_RAMP = 0xB8
    # POWER_UP_WITHOUT_RAMP (0xA4), POWER_DOWN_WITHOUT_RAMP (0xB4),
    # PAUSE (0x64), RESUME(0x68), REWIND (0x74),
    # VOLUME_SET (0x44), VOLUME_UP (0x54), and VOLUME_DOWN (0x48)
    # are not used by this library at present

    interword_delay = 0.7;
    playback_mode = _PLAY;

    def __init__(self, pin_mosi, pin_clk, *pins_cs):
        self.NUMBER_ONES = []
        self.NUMBER_TEENS = []
        self.NUMBER_TENS = []
        self.NUMBER_MISC = []

        self.clk = pin_clk
        self.mosi = pin_mosi
        self.cs = pins_cs
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.clk, GPIO.OUT)
        GPIO.setup(self.mosi, GPIO.OUT)
        for cs in pins_cs:
            GPIO.setup(cs, GPIO.OUT)
            GPIO.output(cs, GPIO.HIGH)
            self._send(cs, self._POWER_UP_WITH_RAMP << 8)

    def __del__(self):
        self.cleanup()

    def cleanup(self):
        for pin_cs in self.cs:
            self._send(pin_cs, self._POWER_DOWN_WITH_RAMP << 8)
        GPIO.cleanup()

    def say(self, *words):
        for word in words:
            if type(word) is int:
                self.say_number(word)
            elif word[0] == 'p':
                time.sleep(word[1])
            else:
                self.say_word(word[1], word[2])
                time.sleep(self.interword_delay)

    def say_number(self, number):
        if number == 0:
            self.say(self.NUMBER_ONES[0])
        else:
            if number < 0:
                self.say(self.NUMBER_MISC["minus"])
                number = -number

            nf = number // 1000000000
            if nf != 0:
                self.say_number_fragment(nf)
                self.say(self.NUMBER_MISC['billion'])
                number -= nf * 1000000000

            nf = number // 1000000
            if nf != 0:
                self.say_number_fragment(nf)
                self.say(self.NUMBER_MISC['million'])
                number -= nf * 1000000

            nf = number // 1000
            if nf != 0:
                self.say_number_fragment(nf)
                self.say(self.NUMBER_MISC["thousand"])
                number -= nf * 1000

            self.say_number_fragment(number)

    def say_number_fragment(self, number):
        nf = number // 100
        if nf != 0:
            self.say(self.NUMBER_ONES[nf])
            self.say(self.NUMBER_MISC["hundred"])
            number -= nf * 100

        nf = number // 10
        if nf == 1:
            self.say(self.NUMBER_TEENS[number - 10])
            number = 0
            return

        if nf > 1:
            self.say(self.NUMBER_TENS[nf])
            number -= nf * 10

        if number != 0:
            self.say(self.NUMBER_ONES[number])

    def say_time(self, hr, min, twelve_hour_mode):
        am = hr < 12

        if hr == 0 and twelve_hour_mode:
            hr = 24
            am = True

        if twelve_hour_mode:
            if hr >= 13:
                hr -= 12

        self.say_number(hr)

        if twelve_hour_mode == False:
            self.say(self.NUMBER_MISC["hundred"])

        if min > 0:
            if min < 10:
                self.say(self.NUMBER_MISC["oh"])
            self.say_number(min)
            
        if twelve_hour_mode:
            if am:
                ampm = self.NUMBER_MISC["am"]
            else:
                ampm = self.NUMBER_MISC["pm"]
            self.say(ampm)

    def say_word(self, bank, word):
        self._send(self.cs[bank], self.playback_mode << 8 | word)

    def _send(self, bank, data):
        GPIO.output(bank, GPIO.LOW)
        for bit in range(0, 16):
            if data & 0x8000:
                GPIO.output(self.mosi, GPIO.HIGH)
            else:
                GPIO.output(self.mosi, GPIO.LOW)
            GPIO.output(self.clk, GPIO.HIGH)
            GPIO.output(self.clk, GPIO.LOW)
            data <<= 1
        GPIO.output(bank, GPIO.HIGH)

    def set_delay(self, seconds):
        old_value = self.interword_delay
        self.interword_delay = seconds
        return old_value
    
    def set_load_mode(self):
        self.playback_mode = self._LOAD
        
    def set_play_mode(self):
        self.playback_mode = self._PLAY        
