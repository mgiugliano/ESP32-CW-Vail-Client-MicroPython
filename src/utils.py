# MicroPython Vail Client for ESP32 with Iambic Keyer Support
# Connects to a Vail server over WebSocket and sends/receives Morse code audio
# using an Iambic keyer or straight key mode based on paddle input at boot.

# Configuration options are provided at the top of the script.
# Requires MicroPython with uasyncio and network support.

# Author: Michele GIUGLIANO (IU4TBF) - www.giugliano.info
# License: MIT

# utils.py
import uasyncio as asyncio

class AsyncQueue:
    """ A simple asyncio Queue implementation for MicroPython """
    def __init__(self):
        self._q = []

    async def put(self, item):
        self._q.append(item)

    async def get(self):
        while not self._q:
            await asyncio.sleep_ms(10)
        return self._q.pop(0)
