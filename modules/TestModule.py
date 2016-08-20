# -*- encoding: UTF-8 -*-
""" Test for a new module.

"""

import sys
import time

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

from optparse import OptionParser

NAO_IP = "131.174.106.197"


# Global variable to store the HumanGreeter module instance
Testing = None


class TestingModule(ALModule):
    """ A simple module able to react
    to facedetection events

    """
    def __init__(self, name):
        try: #check whether the module object already exists, if yes, exit it.
            p=ALProxy(name)
            p.exit()
        except:
            pass
        ALModule.__init__(self, name)
        self.tts = ALProxy("ALTextToSpeech")

    def myMethod(self, *args_):
        """ This will be called each time a face is
        detected.

        """
        self.tts.say("Hello, you")

def main():
    """ Main entry point

    """
    parser = OptionParser()
    parser.add_option("--pip",
        help="Parent broker port. The IP address or your robot",
        dest="pip")
    parser.add_option("--pport",
        help="Parent broker port. The port NAOqi is listening to",
        dest="pport",
        type="int")
    parser.set_defaults(
        pip=NAO_IP,
        pport=9559)

    (opts, args_) = parser.parse_args()
    pip   = opts.pip
    pport = opts.pport

    # We need this broker to be able to construct
    # NAOqi modules and subscribe to other modules
    # The broker must stay alive until the program exists
    myBroker = ALBroker("myBroker",
       "0.0.0.0",   # listen to anyone
       0,           # find a free port and use it
       pip,         # parent broker IP
       pport)       # parent broker port


    # Warning: HumanGreeter must be a global variable
    # The name given to the constructor must be the name of the
    # variable
    global Testing
    Testing = TestingModule("Testing")
    Testing.myMethod()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print
        print "Interrupted by user, shutting down"
        myBroker.shutdown()
        sys.exit(0)



if __name__ == "__main__":
    main()
