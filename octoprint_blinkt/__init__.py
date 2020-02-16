# coding=utf-8
from __future__ import absolute_import, division

from blinkt import set_pixel, set_brightness, show, clear, set_all

import colorsys

import time

import math

import octoprint.plugin

class BlinktPlugin(octoprint.plugin.ProgressPlugin, octoprint.plugin.EventHandlerPlugin):
    def on_event(self, event, payload):

        self._logger.info("Received event " + event)

        if event == "CaptureStart":
            clear()
            set_all(255, 255, 255, 0.1)
            show()

        if event == "CaptureDone":
            clear()
            # Restore the progress
            self._set_progress(self._blinkt_progress)
            show()

        if event == "PrintDone":
            clear()
            show()

    def on_print_progress(self, storage, path, progress):

        self._logger.info("Got progress")
        self._logger.info("On progress " + str(progress))
        self._blinkt_progress = progress
        self._set_progress(progress)

    def _set_progress(self, progress):
        clear()

        pulse = round(math.sin(math.radians(time.time()/1000)),1)
        if pulse < 0:
    	       pulse = 0-pulse

        set_brightness(0.3)

        spacing = 360.0 / 16.0
        hue = 0
        numpixels = 9

        hue = int(progress * 100) % 360
        for x in range(int((progress/100)*numpixels)):
            offset = x * spacing
            h = ((hue + offset) % 360) / 360.0
            r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(h, 1.0, 1.0)]
            set_pixel(x, r, g, b)

        show()

__plugin_name__ = "Blinkt Progress"
__plugin_version__ = "1.0.0"
__plugin_description__ = "Show the print progress on a Pimoroni Blinkt"
__plugin_implementation__ = BlinktPlugin()
