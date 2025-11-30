# How to Upload the Vail Adapter Software

The Vail Client software is split into several files to make it easier to manage. You will upload 5 separate Python scripts to your ESP32.

---

## 🛠️ Prerequisites

1.  **ESP32 Board** with MicroPython firmware installed (see `FIRMWARE_GUIDE.md`).
2.  **Thonny IDE** installed and connected to your board.
3.  **WiFi Credentials** (SSID and Password).

---

## Step 1: Create the Files

You need to create the following 5 files on your ESP32. For each file listed below, follow these steps:

1.  In Thonny, click **File > New**.
2.  Copy the code for that specific file from the repository.
3.  Paste it into Thonny.
4.  Click **File > Save As...**
5.  Select **MicroPython Device**.
6.  Enter the exact filename (e.g., `config.py`) and click **OK**.

### The File List

1.  **`config.py`**
    * *Contains your settings (WiFi, Pins, Speed).*
    * **Action:** Save this first. You will edit this file in Step 2.
2.  **`utils.py`**
    * *Contains helper tools and queues.*
    * **Action:** Copy, Paste, Save. Do not edit.
3.  **`hardware.py`**
    * *Handles the Buzzer, LED, and Paddles.*
    * **Action:** Copy, Paste, Save. Do not edit.
4.  **`keyer.py`**
    * *Contains the logic for Straight Key and Iambic modes.*
    * **Action:** Copy, Paste, Save. Do not edit.
5.  **`main.py`**
    * *The startup script that runs everything.*
    * **Action:** Copy, Paste, Save. Do not edit.

---

## Step 2: Configure Your Device

You only need to edit **one** file to set up your device.

1.  In Thonny, look at the **Files** sidebar on the left.
2.  Under **MicroPython Device**, double-click **`config.py`**.
3.  Update the lines at the top with your WiFi info:
    ```python
    SSID = "MyHomeNetwork"
    PASSWORD = "SecretPassword"
    ```
4.  (Optional) Change your Morse speed:
    ```python
    WPM = 20
    ```
5.  Press **Ctrl+S** to save the changes.

---

## Step 3: Run and Test

1.  Press the **Stop/Restart** button (Red Sign) in the toolbar.
    * This reboots the ESP32.
2.  Watch the **Shell** (bottom panel). You should see:
    ```text
    --- STARTING VAIL CLIENT (MODULAR) ---
    BOOT: Normal -> Iambic Keyer
    WiFi Connected: ...
    Handshake OK.
    ```
3.  You should hear the "Ba-Ding!" startup tone.

---

## Troubleshooting

* **"ImportError: no module named..."**
    * This means you forgot to save one of the files, or you spelled the filename wrong.
    * Check the **Files** sidebar. You must see all 5 files: `config.py`, `hardware.py`, `keyer.py`, `main.py`, `utils.py`.


