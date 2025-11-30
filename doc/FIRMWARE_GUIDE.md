# MicroPython Installation Guide for ESP32

This guide will walk you through installing the **MicroPython** firmware onto your ESP32 microcontroller. This is a required step before you can load the Vail Client software.

**What is this doing?** Think of this like installing an Operating System (like Windows or macOS) onto a blank computer. The ESP32 needs the MicroPython "OS" to understand the Python code we will write to it.

---

## 🛠️ Prerequisites

Before you begin, ensure you have the following:

1.  **ESP32 Development Board:** This guide is written for the standard **ESP32-WROOM** (30-pin or 38-pin versions), although it has been already tested on the **ESP32-S2mini by WiMo**.
2.  **USB Cable:** You **must** use a high-quality data cable.
    * *Warning:* Many USB cables included with phone chargers are "Charge Only" and do not have **data** wires inside. If your computer does not make a sound when you plug the board in, try a different cable.
3.  **USB Drivers:**
    * Most ESP32 boards use a chip to talk to the computer (CP210x or CH340).
    * If you plug in the board and no new "COM Port" appears (Windows) or /dev/cu.usb* (macOS), download and install the **CP210x Universal Windows Driver** or **CH340 Driver**.

Note: In principle, any microcontroller able to run MicroPython and equipped with WiFi capabilities should work. 
---

## Method 1: The Web Installer

The MicroPython team provides a tool that runs directly in your web browser (Chrome or Edge required).

1.  **Download the Firmware:**
    * Go to the [MicroPython ESP32 Download Page](https://micropython.org/download/esp32/).
    * Scroll to the **Releases** section.
    * Download the latest **.bin** file (e.g., `v1.22.0.bin`). Do *not* download the "OTA" version.

2.  **Connect the Board:**
    * Plug your ESP32 into your computer via USB.

3.  **Open the Web Installer:**
    * Visit [https://micropython.org/download/esp32/](https://micropython.org/download/esp32/) again.
    * Look for a button that says **"Installation instructions"** or a link to the **Web Assembly Flasher**.
    * *Alternatively*, you can use the [ESP Web Flasher](https://espressif.github.io/esptool-js/).

4.  **Connect and Flash:**
    * Click the **Connect** button on the webpage.
    * Select the port labeled "USB Serial Device" or "CP210x".
    * **Important:** If the connection fails, you may need to put the board into **Boot Mode** manually:
        1.  Hold down the **BOOT** button on the ESP32.
        2.  Press and release the **EN** (Reset) button.
        3.  Release the **BOOT** button.
    * Select your downloaded `.bin` file and click **Program**.

---

## Method 2: The Command Line t Reliable)

If the web installer fails, this method gives you total control. It uses a Python tool called `esptool`.

### Step 1: Install Python
If you don't have Python installed:
* **Windows:** Download from [python.org](https://www.python.org/). **Crucial:** During installation, check the box that says **"Add Python to PATH"**.
* **Mac/Linux:** You likely already have it.

### Step 2: Install the Flashing Tool
Open your terminal (Command Prompt or PowerShell on Windows, Terminal on Mac) and run:

```bash
pip install esptool
```

### Step 3: Find your Port

Plug in your ESP32.

  * **Windows:** Open "Device Manager" and look under "Ports (COM & LPT)". Note the COM number (e.g., `COM3`).
  * **Mac/Linux:** Run `ls /dev/tty.*` in the terminal. It will look like `/dev/tty.usbserial-xxx`.

### Step 4: Erase the Flash

It is highly recommended to wipe the chip clean before installing.
*Replace `COM3` with your actual port.*

```bash
esptool.py --chip esp32 --port COM3 erase_flash
```

> **Troubleshooting:** If you see "Connecting........\_\_\_" and it times out:
>
> 1.  Run the command again.
> 2.  When "Connecting..." appears, hold the **BOOT** button on the ESP32 for 2 seconds, then release.

### Step 5: Write the Firmware

Now write the MicroPython file you downloaded in Method 1.
*Replace `COM3` with your port and `esp32-xxxx.bin` with the actual filename you downloaded.*

```bash
esptool.py --chip esp32 --port COM3 --baud 460800 write_flash -z 0x1000 esp32-2023xxxx-v1.20.0.bin
```

*Note: The `0x1000` at the end is the memory address. This is specific to the standard ESP32.*

-----

## 3\. Verifying the Installation

To confirm MicroPython is running:

1.  Download and install **[Thonny IDE](https://thonny.org/)** (it's free and excellent for beginners).
2.  Open Thonny.
3.  Go to the bottom-right corner of the window. Click on the text that says "Local Python 3" (or similar).
4.  Select **MicroPython (ESP32)**.
5.  If asked, select your COM Port / USB Serial device.
6.  Look at the **Shell** (bottom panel). You should see output similar to:

<!-- end list -->

```text
MicroPython v1.20.0 on 2023-04-26; ESP32 module with ESP32
Type "help()" for more information.
>>>
```

If you see the `>>>` prompt, congratulations\! Your board is ready for the Vail Adapter code.






