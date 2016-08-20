import sys
import time

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule
from SoundRecorder import SoundRecorder

from optparse import OptionParser


NAO_IP = "131.174.106.197"
Wit = None
memory = None

class WitModule(ALModule):
    """ A simple module to send audiofile to WitAI

    """
    def __init__(self, name):
        try: #check whether the module object already exists, if yes, exit it.
            p=ALProxy(name)
            p.exit()
        except:
            pass
        ALModule.__init__(self, name)
        global memory
        memory = ALProxy("ALMemory")

    def sayThis(self, *_args):
        """ This will be called each time a word is
        detected.

        """


def main():
    """ Main entry point
    First some broker stuff, to be able to put a temporary module in the NAO
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
    myBroker = ALBroker("myBroker",
       "0.0.0.0",   # listen to anyone
       0,           # find a free port and use it
       pip,         # parent broker IP
       pport)       # parent broker port

    #first record a sound on the NAO
    sr = SoundRecorder(NAO_IP, 9559)
    sr.record()
    #Now we are going to use a local module to send the sound to Wit.ai
    global Wit
    Wit = WitModule("Wit")
    Wit.getFile()


if __name__ == "__main__":
    main()
