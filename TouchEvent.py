import sys
import time

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule
import argparse


#Code is taken from aldebaran API documentation
ReactToTouch = None
memory = None

class ReactToTouch(ALModule):
    """ A simple module able to react
        to touch events.
    """
    def __init__(self, name):
        self.touched = False
        ALModule.__init__(self, name)
        # Subscribe to TouchChanged event:
        global memory
        memory = ALProxy("ALMemory")
        memory.subscribeToEvent("TouchChanged",
            "ReactToTouch",
            "onTouched")

    def onTouched(self, strVarName, value):
        """ This will be called each time a touch
        is detected.

        """
        memory.unsubscribeToEvent("TouchChanged", "ReactToTouch")
        self.touched = True
