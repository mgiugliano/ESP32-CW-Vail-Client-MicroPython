# MicroPython Vail Client for ESP32 with Iambic Keyer Support
# Connects to a Vail server over WebSocket and sends/receives Morse code audio
# using an Iambic keyer or straight key mode based on paddle input at boot.

# Configuration options are provided at the top of the script.
# Requires MicroPython with uasyncio and network support.

# Author: Michele GIUGLIANO (IU4TBF) - www.giugliano.info
# License: MIT

# hardware.py
import machine
import time
import config

# --- IRQ BUFFER ---
# We keep this global within the module for speed
IRQ_BUF_SIZE = 64
irq_times = [0] * IRQ_BUF_SIZE
irq_values = [0] * IRQ_BUF_SIZE
irq_head = 0
irq_tail = 0

def _key_isr(pin):
    """ Internal Interrupt Handler """
    global irq_head
    t = time.ticks_ms()
    v = pin.value()
    irq_times[irq_head] = t
    irq_values[irq_head] = v
    irq_head = (irq_head + 1) % IRQ_BUF_SIZE

class VailHardware:
    def __init__(self):
        # 1. Buzzer
        try:
            self.pwm = machine.PWM(machine.Pin(config.BUZZER_PIN), freq=config.TX_TONE_FREQ, duty_u16=0)
        except ValueError:
            print(f"HW ERROR: PWM fail on Pin {config.BUZZER_PIN}")
            raise

        # 2. Keys/Paddles
        pull_mode = machine.Pin.PULL_UP if config.KEY_ACTIVE_LOW else machine.Pin.PULL_DOWN
        self.dit_key = machine.Pin(config.DIT_PIN, machine.Pin.IN, pull_mode)
        self.dah_key = machine.Pin(config.DAH_PIN, machine.Pin.IN, pull_mode)
        
        # 3. LED
        self.led = machine.Pin(config.LED_PIN, machine.Pin.OUT)
        self.led.value(0)

    def enable_irq(self):
        """ Enable interrupts (call after boot is safe) """
        print("Enabling Hardware Interrupts...")
        trigger = machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING
        self.dit_key.irq(trigger=trigger, handler=_key_isr)
        self.dah_key.irq(trigger=trigger, handler=_key_isr)

    def get_paddles(self):
        d = self.dit_key.value()
        D = self.dah_key.value()
        # Normalize to True = Pressed
        if config.KEY_ACTIVE_LOW:
            return (d == 0, D == 0)
        return (d == 1, D == 1)

    def get_irq_event(self):
        """ Retrieve one event from ring buffer if available """
        global irq_tail, irq_head
        if irq_tail == irq_head:
            return None # Buffer empty
            
        t = irq_times[irq_tail]
        v = irq_values[irq_tail]
        irq_tail = (irq_tail + 1) % IRQ_BUF_SIZE
        
        # Normalize value to boolean (True = Pressed)
        is_pressed = (v == 0) if config.KEY_ACTIVE_LOW else (v == 1)
        return (t, is_pressed)

    def rx_tone_on(self):
        self.pwm.freq(config.RX_TONE_FREQ)
        self.pwm.duty_u16(32768)

    def tx_tone_on(self):
        self.pwm.freq(config.TX_TONE_FREQ)
        self.pwm.duty_u16(32768)
        
    def play_startup_tone(self):
        self.pwm.duty_u16(32768)
        self.pwm.freq(1500)
        time.sleep_ms(100)
        self.pwm.freq(2000)
        time.sleep_ms(150)
        self.pwm.duty_u16(0)
        self.pwm.freq(config.TX_TONE_FREQ)

    def tone_off(self):
        self.pwm.duty_u16(0)
