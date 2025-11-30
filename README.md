# Vail Client: Standalone ESP32 Morse Code Transceiver

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Platform: ESP32](https://img.shields.io/badge/Platform-ESP32-blue)
![Language: MicroPython](https://img.shields.io/badge/Language-MicroPython-green)

[![Vail Client Prototype](https://img.youtube.com/vi/6pTK0vWpM8Q/0.jpg)](https://www.youtube.com/watch?v=6pTK0vWpM8Q)

## 📡 Overview

This project is a standalone, ESP32-based, client for the **Vail-CW** Internet server. 

The Vail server is a software running *in the cloud*, and it acts as a
"repeater". It allows multiple users to connect via the Internet to practice
sending and receiving Morse Code in (quasi) real-time. While the standard client
for the Vail server is a web browser, **this project replaces the need of a PC/mobile entirely.**

It is a small physical device featuring:
* **WiFi Connectivity:** Connects directly to the Internet.
* **Paddle/Key Interface:** A standard 3.5mm (female) jack for connecting your Morse key.
* **Audio Output:** A buzzer to hear traffic from other users and your own sending.

This allows for an "always-on" practice station device that you can deploy
instantly without booting up a computer.

> **Note:** The original Vail-CW protocol and web client were created by Neale Pickett. 
You can find his running server [here](http://vail.woozle.org) and his original repository [here](https://github.com/Vail-CW/vail_repeater_depricated).


## 📖 The Backstory

I am a Radio Amateur, learning CW (Morse Code). I have sometimes found myself panicking
on-the-air due to a lack of solid practice. However, finding time to practice
is difficult, and practicing alone lacks motivation. I realized that the "human
factor" matters for me and that interacting with a real person was the missing piece.

I discovered existing web-based tools (like vail.woozle.org and VBAND), but I
wanted something tactile. Inspired by the flexibility of the Vail WebSocket
protocol, I built this dedicated hardware client. It allows me to keep a
"communication channel" literally open 24/7. If someone pops up on the server,
I might hear their traffic instantly and jump in for a QSO (i.e. a
conversation), all without touching a computer.

I chose **MicroPython** for this project simply as an excuse to learn it.
It has proven robust enough for the precise timing required by CW.
It allowed me to use a minimal scheme for websocket and web data exchanges,
without using any library (which never worked in my hands, using Arduino IDE or
PlatformIO).

## ✨ Features

* **Standalone:** Works with [Vail](https://vail.woozle.org/) via WiFi (no PC/phone/tablet required).
* **Dual Mode:** Supports both **Straight Key** and **Iambic Paddle (Mode B)** (default at boot).
* **Auto-Detect:** Hold your key down at boot to automatically switch to Straight Key mode.
* **Audio:** Local sidetone (600Hz) and distinct received pitch (700Hz).
* **Feedback:** Startup "Ba-Ding!" tone and LED status for connected clients.
* **Forgiving Timing:** Implements a jitter buffer to handle internet latency.
* **Easy Config:** All settings are isolated in a simple `config.py` file.


## 🔌 Hardware & Wiring

You need an **ESP32-WROOM** Development Board (30 or 38 pin), a passive buzzer, and a jack for your key.

**Pinout Configuration (ESP32 WROOM):**

| Component | Pin | Note |
| :--- | :--- | :--- |
| **Buzzer (+)** | **GPIO 21** | Connect negative leg to GND |
| **Dit Paddle** | **GPIO 22** | Or Straight Key signal line |
| **Dah Paddle** | **GPIO 23** | Left unconnected for Straight Key |
| **Status LED** | **GPIO 2** | Usually the onboard Blue LED |


> **Note:** If using an ESP32-S2 Mini or other variants, pin numbers in `main.py` may need adjustment.

# 🚀 Getting Started

### 1. Installation
1.  **Flash Firmware:** Follow the [MicroPython Firmware Guide](doc/FIRMWARE_GUIDE.md) to install the OS on your ESP32.
2.  **Upload Code:** Follow the [Code Upload Guide](doc/CODE_UPLOAD_GUIDE.md) to copy the 5 Python files (`config.py`, `keyer.py`, etc.) to the board.

### 2. Configuration
You don't need to touch the code logic. Just open **`config.py`** in Thonny to set your preferences:

```python
# config.py

# --- USER CREDENTIALS ---
SSID = "YOUR_WIFI_NAME"
PASSWORD = "YOUR_WIFI_PASSWORD"

# --- KEYER SETTINGS ---
WPM = 25                # Speed in Words Per Minute
IAMBIC_MODE_B = True    # True for Iambic B, False for Mode A
```

There are other settings (e.g. the frequency of the buzzer, when receiving/transmitting),
as well as the name of the channel, on the Vail server. 

Save the file, restart the board, and you should hear a startup "Ba-Ding!" tone 
from the onboard buzzer, indicating success in connection to the Vail server.



## 🔮 Future Roadmap

[ ] WiFi Manager (AP Mode) for setting credentials without editing code.
[ ] Hardware button to cycle Vail channels.
[ ] Battery management (Li-Ion) for a truly portable device.
[ ] Macro buttons (CQ, QRL?, etc.).
[ ] Improved audio via DAC/Amplifier instead of PWM buzzer.

## 🤝 Contributing
Contributions are welcome! If you have ideas for improvements or find bugs, please open an issue or submit a pull request.

If you find value in this project, feel free to [Buy Me A Coffee](https://buymeacoffee.com/mgiugliano).

## Comparison: Vail Client vs. Morserino-32

The **Morserino-32** is a mature, feature-rich, multi-functional device designed for learning and practicing Morse code. 
The **Vail Client** can't clearly compete with that project as it is a specialized, minimalist "appliance" designed exclusively for the Vail protocol. 

#### 1. Cost (The Major Advantage)
* **Vail Client:** **Extremely Low Cost (< $10 - $15 USD).**
    * ESP32 Dev Board: ~$5-6
    * Buzzer, Audio Jack, Wires: ~$2-3
    * Total build cost is negligible for anyone with a junk box of parts.

* **Morserino-32:** **Moderate Cost (~$60 - $90 USD + Shipping).**
    * It is sold as a kit (requiring assembly) or fully assembled. The cost reflects the custom PCB, display, battery management, and enclosure components.

#### 2. Advantages of Vail Client
* **"Always-On" Appliance Philosophy:**
    * Your project is designed to sit on a desk, connected to WiFi, waiting for traffic 24/7. It behaves like a real radio receiver squelched until someone transmits. The Morserino is designed more as a handheld gadget you turn on for a specific practice session.
* **Native Vail Protocol Support:**
    * Your client speaks the `binary.vail.woozle.org` protocol natively. While Morserino supports WiFi (via "QSO Bot" and other modes), connecting it specifically to the Vail server often requires specific firmware forks or bridges.
* **Simplicity of Code:**
    * The entire logic is contained in rather basic MicroPython script. This makes it incredibly easy for a beginner to understand, modify, or "hack" without needing to set up a complex PlatformIO C++ environment.
* **Use of Real Keys:**
    * While Morserino *can* take an external key, its primary interface is often its built-in capacitive touch paddles. The Vail Client **requires** an external key, encouraging the use of proper mechanical keys/paddles from day one.

#### 3. Disadvantages (Where Morserino Wins)
* **User Interface (The Screen):**
    * **Morserino:** Has an OLED display to show menus, decode Morse code to text, and adjust WPM/settings instantly.
    * **Vail Client:** Is "headless." Changing WiFi credentials or WPM currently requires editing code (until a WiFi Manager/Web Interface is implemented).
* **Offline Training Features:**
    * **Morserino:** Includes Koch method trainers, echo trainers, callsign generators, and file players that work without any internet connection.
    * **Vail Client:** Is currently dependent on the internet connection and the server to provide the interaction.
* **LoRa Connectivity:**
    * **Morserino:** Can transmit point-to-point over LoRa (433/868/915 MHz) without internet.
    * **Vail Client:** WiFi only.
* **Portability (Battery):**
    * **Morserino:** Has built-in LiPo battery management.
    * **Vail Client:** Requires an external USB power bank or a custom battery add-on (as noted in your "Future Features").

In summary:

| Feature | Vail Client (This Project) | Morserino-32 |
| :--- | :--- | :--- |
| **Cost** | **$ (~$10)** | **$$$ (~$80)** |
| **Primary Goal** | Dedicated Internet Repeater Client | Comprehensive CW Trainer |
| **Protocol** | Native Vail-CW | QSO Bot / LoRa / Custom |
| **Interface** | Headless (No Screen) | OLED Display + Menus |
| **Connectivity** | WiFi Only | WiFi + LoRa (RF) |
| **Modifiability** | High (Single Python Script) | Moderate (Complex C++ Firmware) |




**Author:** Michele GIUGLIANO (IU4TBF)
**License:** MIT
