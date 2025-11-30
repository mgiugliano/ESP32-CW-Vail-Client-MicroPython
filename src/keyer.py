# MicroPython Vail Client for ESP32 with Iambic Keyer Support
# Connects to a Vail server over WebSocket and sends/receives Morse code audio
# using an Iambic keyer or straight key mode based on paddle input at boot.

# Configuration options are provided at the top of the script.
# Requires MicroPython with uasyncio and network support.

# Author: Michele GIUGLIANO (IU4TBF) - www.giugliano.info
# License: MIT

# keyer.py
import uasyncio as asyncio
import time
import struct
import config

async def task_straight(hw, queue, history, active_pin_obj):
    print("MODE: Straight Key")
    base_epoch_ms = int((time.time() + config.EPOCH_DELTA) * 1000)
    base_ticks = time.ticks_ms()
    
    was_pressed = False
    press_start = 0
    
    while True:
        # We manually poll the active pin for straight key mode
        is_pressed = (active_pin_obj.value() == (0 if config.KEY_ACTIVE_LOW else 1))
        now = time.ticks_ms()
        
        if is_pressed and not was_pressed:
            was_pressed = True
            press_start = now
            hw.tx_tone_on()
            print("DEBUG: Key Down")
            
        elif not is_pressed and was_pressed:
            was_pressed = False
            hw.tone_off()
            duration = time.ticks_diff(now, press_start)
            print(f"DEBUG: Key Up {duration}ms")
            
            if duration > 20:
                diff = time.ticks_diff(press_start, base_ticks)
                ts = base_epoch_ms + diff
                # Pack and Send
                packet = struct.pack(">QHH", ts, 0, duration)
                await queue.put(packet)
                history.append((ts, duration))
                if len(history) > 10: history.pop(0)
                
        await asyncio.sleep_ms(5)

async def task_iambic(hw, queue, history):
    print(f"MODE: Iambic ({config.WPM} WPM)")
    
    DOT_MS = int(1200 / config.WPM)
    DASH_MS = DOT_MS * 3
    
    base_epoch_ms = int((time.time() + config.EPOCH_DELTA) * 1000)
    base_ticks = time.ticks_ms()

    latch_dit = False
    latch_dah = False
    last_element = None

    while True:
        # 1. Process IRQ Events (High precision latching)
        while True:
            evt = hw.get_irq_event()
            if not evt: break
            # We don't use the timestamp for iambic logic, just the state
            # Logic: If any press event occurred, latch it
            _, is_pressed = evt
            # Note: This is a simplified latch. Real logic below uses get_paddles
            # but IRQ ensures we don't miss fast taps.

        # 2. Check Realtime State
        d, D = hw.get_paddles()
        if d: latch_dit = True
        if D: latch_dah = True

        element = None
        
        if latch_dit and not latch_dah: element = 'dit'
        elif latch_dah and not latch_dit: element = 'dah'
        elif latch_dit and latch_dah:
            element = 'dah' if last_element == 'dit' else 'dit'
            
        if element:
            duration = DOT_MS if element == 'dit' else DASH_MS
            last_element = element
            
            # Reset latch for current
            if element == 'dit': latch_dit = False
            if element == 'dah': latch_dah = False
            
            # Start TX
            hw.tx_tone_on()
            start_ticks = time.ticks_ms()
            
            # Send Packet
            diff = time.ticks_diff(start_ticks, base_ticks)
            ts = base_epoch_ms + diff
            packet = struct.pack(">QHH", ts, 0, duration)
            await queue.put(packet)
            history.append((ts, duration))
            if len(history) > 10: history.pop(0)
            
            # Play Tone
            end_time = start_ticks + duration
            while time.ticks_ms() < end_time:
                d, D = hw.get_paddles()
                # Squeeze Latch
                if element == 'dit' and D: latch_dah = True
                if element == 'dah' and d: latch_dit = True
                await asyncio.sleep_ms(5)
            
            hw.tone_off()
            
            # Space
            space_end = time.ticks_ms() + DOT_MS
            while time.ticks_ms() < space_end:
                d, D = hw.get_paddles()
                if element == 'dit' and D: latch_dah = True
                if element == 'dah' and d: latch_dit = True
                await asyncio.sleep_ms(5)
                
            # Forgiving check at end
            d_end, D_end = hw.get_paddles()
            if element == 'dit' and d_end: latch_dit = True
            if element == 'dah' and D_end: latch_dah = True
        else:
            await asyncio.sleep_ms(5)
