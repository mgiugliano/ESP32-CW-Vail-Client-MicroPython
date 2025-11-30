# MicroPython Vail Client for ESP32 with Iambic Keyer Support
# Connects to a Vail server over WebSocket and sends/receives Morse code audio
# using an Iambic keyer or straight key mode based on paddle input at boot.

# Configuration options are provided at the top of the script.
# Requires MicroPython with uasyncio and network support.

# Author: Michele GIUGLIANO (IU4TBF) - www.giugliano.info
# License: MIT

# config.py

# --- USER CREDENTIALS ---
SSID = "YOUR_WIFI_SSID"
PASSWORD = "YOUR_WIFI_PASSWORD"

# --- HARDWARE PINS (ESP32 WROOM) ---
# GPIO 18 is safe for Buzzer on WROOM
# GPIO 23/22 are standard input pins
BUZZER_PIN = 21 
LED_PIN = 2
DIT_PIN = 23 # Right Paddle
DAH_PIN = 22 # Left Paddle

# --- LOGIC CONFIGURATION ---
# False: Button connects to 3.3V (Active High / Pull-Down)
# True:  Button connects to GND  (Active Low  / Pull-Up)
KEY_ACTIVE_LOW = False 

# --- KEYER SETTINGS ---
WPM = 25                # Speed in Words Per Minute
IAMBIC_MODE_B = True    # True=Memory, False=Mode A

# --- AUDIO SETTINGS ---
RX_TONE_FREQ = 700      # Incoming pitch
TX_TONE_FREQ = 600      # Sidetone pitch
RX_DELAY_MS = 4000      # Jitter buffer delay in milliseconds (to accommodate network latency)

# --- SERVER SETTINGS ---
CHANNEL = "Example"  # Vail channel name
PATH = "/chat?repeater=" + CHANNEL
HOST = "vail.woozle.org"
PORT = 443
SUBPROTOCOL = "binary.vail.woozle.org"

# 1970 (Unix) vs 2000 (MicroPython) epoch delta
EPOCH_DELTA = 946684800
