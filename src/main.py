# MicroPython Vail Client for ESP32 with Iambic Keyer Support
# Connects to a Vail server over WebSocket and sends/receives Morse code audio
# using an Iambic keyer or straight key mode based on paddle input at boot.

# Configuration options are provided at the top of the script.
# Requires MicroPython with uasyncio and network support.

# Author: Michele GIUGLIANO (IU4TBF) - www.giugliano.info
# License: MIT

## main.py
import network
import socket
import ssl
import time
import struct
import uasyncio as asyncio
import ubinascii
import os
import ntptime
import esp32

# Modules
import config
import hardware
import utils
import keyer

# --- GLOBAL SHARED STATE ---
tx_queue = utils.AsyncQueue()
recently_sent = []
connected_clients = 0

async def setup_network():
    try:
        esp32.brownout_setup();
    except: pass
    
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print(f'Connecting to {config.SSID}...')
        wlan.connect(config.SSID, config.PASSWORD)
        while not wlan.isconnected():
            await asyncio.sleep(1)
            print('.', end='')
        print('')
    print('WiFi Connected:', wlan.ifconfig())
    
    # NTP
    try:
        ntptime.settime();
        print("NTP Synced");
    except: pass

async def setup_socket():
    print(f"Connecting SSL {config.HOST}...")
    s = socket.socket()
    ai = socket.getaddrinfo(config.HOST, config.PORT)
    s.connect(ai[0][-1])
    s = ssl.wrap_socket(s, server_hostname=config.HOST)
    s.setblocking(False)
    
    # Handshake
    key = ubinascii.b2a_base64(os.urandom(16)).strip()
    req = (
        f"GET {config.PATH} HTTP/1.1\r\n"
        f"Host: {config.HOST}\r\n"
        "Upgrade: websocket\r\n"
        "Connection: Upgrade\r\n"
        f"Sec-WebSocket-Key: {key.decode()}\r\n"
        f"Sec-WebSocket-Protocol: {config.SUBPROTOCOL}\r\n"
        "Sec-WebSocket-Version: 13\r\n"
        "User-Agent: MicroPython-Vail/1.0\r\n"
        f"Origin: https://{config.HOST}\r\n\r\n"
    )
    s.write(req.encode())
    
    # We can't use await s.read() easily here without Async wrapper yet, 
    # so we do a quick blocking read for handshake
    s.setblocking(True)
    while True:
        line = s.readline()
        if line == b'\r\n': break
        if b"101 Switching Protocols" in line:
            print("Handshake OK.")
    s.setblocking(False)
    
    return s

async def task_sender(writer):
    while True:
        packet = await tx_queue.get()
        # Framing
        length = len(packet)
        header = bytearray([0x82, 0x80 | length])
        mask = os.urandom(4)
        header.extend(mask)
        payload = bytearray(length)
        for i in range(length): payload[i] = packet[i] ^ mask[i % 4]
        
        writer.write(header)
        writer.write(payload)
        await writer.drain()
        print(f"[TX] {length}b")

async def task_receiver(reader, hw):
    global connected_clients
    print("RX Task Started")
    clock_offset = None
    
    while True:
        try:
            b1 = await reader.read(1)
            if not b1: break
            arrival = time.ticks_ms()
            
            opcode = b1[0] & 0x0f
            b2 = await reader.read(1)
            if not b2: break
            length = b2[0] & 0x7f
            if length == 126:
                length = struct.unpack(">H", (await reader.read(2)))[0]
            elif length == 127:
                length = struct.unpack(">Q", (await reader.read(8)))[0]
            
            payload = await reader.read(length)
            
            if opcode == 0x2 and len(payload) >= 10:
                ts, clients = struct.unpack(">QH", payload[:10])
                connected_clients = clients
                
                # Echo Cancel
                durations = payload[10:]
                count = len(durations) // 2
                is_echo = False
                if count == 1:
                    rxd = struct.unpack(">H", durations)[0]
                    for i, (sts, sdur) in enumerate(recently_sent):
                        if abs(ts - sts) < 200 and sdur == rxd:
                            is_echo = True
                            del recently_sent[:i+1]
                            break
                if is_echo: continue

                # Clock Sync
                if clock_offset is None:
                    clock_offset = arrival - ts
                    print(f"Sync Offset: {clock_offset}")
                    continue
                
                # Jitter Buffer
                target = ts + clock_offset + config.RX_DELAY_MS
                wait = time.ticks_diff(target, arrival)
                
                if count == 0:
                    print(f"[RX] Heartbeat | Clients: {clients}")
                else:
                    d_list = struct.unpack(f">{count}H", durations)
                    print(f"[RX] Seq: {d_list} | Wait: {wait}ms")
                    
                    if wait > 0: await asyncio.sleep_ms(wait)
                    
                    try:
                        is_tone = True
                        for ms in d_list:
                            if is_tone: hw.rx_tone_on()
                            else: hw.tone_off()
                            await asyncio.sleep_ms(ms)
                            is_tone = not is_tone
                    finally:
                        hw.tone_off()

        except Exception as e:
            print(f"RX Error: {e}")
            break

async def task_led(hw):
    while True:
        if connected_clients > 1:
            hw.led.value(1); await asyncio.sleep_ms(100)
            hw.led.value(0); await asyncio.sleep_ms(100)
        else:
            hw.led.value(0); await asyncio.sleep_ms(500)

async def main():
    time.sleep(2) # USB Safety
    print("--- STARTING VAIL CLIENT (MODULAR) ---")
    
    hw = hardware.VailHardware()
    
    # Boot Check
    d, D = hw.get_paddles()
    if d:
        print("BOOT: Dit Held -> Straight Key")
        # We pass the specific pin object to the straight key task
        key_task = keyer.task_straight(hw, tx_queue, recently_sent, hw.dit_key)
    elif D:
        print("BOOT: Dah Held -> Straight Key")
        key_task = keyer.task_straight(hw, tx_queue, recently_sent, hw.dah_key)
    else:
        print("BOOT: Normal -> Iambic Keyer")
        # Enable IRQ only for Iambic
        hw.enable_irq()
        key_task = keyer.task_iambic(hw, tx_queue, recently_sent)

    await setup_network()
    
    sock = await setup_socket()
    reader = asyncio.StreamReader(sock)
    writer = asyncio.StreamWriter(sock, {})
    
    hw.play_startup_tone()
    
    await asyncio.gather(
        task_receiver(reader, hw),
        task_sender(writer),
        task_led(hw),
        key_task
    )

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Stopped.")

