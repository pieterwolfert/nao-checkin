import sys
import time

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

from optparse import OptionParser

NAO_IP = "131.174.106.197"

WordDetect = None
memory = None
#Example class for reacting to events, and how to subscribe to them.

class WordDetectModule(ALModule):
    """ A simple module able to react
    to worddetection events

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
        tts = ALProxy("ALTextToSpeech")
        tts.say("Are you happy?")
        memory.subscribeToEvent("WordRecognized",
            "WordDetect",
            "recognizedWord")

    def recognizedWord(self, *_args):
        """ This will be called each time a word is
        detected.

        """
        print memory.getData("WordRecognized")
        memory.unsubscribeToEvent("WordRecognized", "WordDetect")

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
    myBroker = ALBroker("myBroker",
       "0.0.0.0",   # listen to anyone
       0,           # find a free port and use it
       pip,         # parent broker IP
       pport)       # parent broker port

    #### Adding speechrecognition proxy
    try:
        proxy = ALProxy("ALSpeechRecognition", NAO_IP, 9559)
    except Exception, e:
        print "Oops, couldn't start a proxy"
        print str(e)
    proxy.setVocabulary(["yes", "no"], False)

    global WordDetect
    WordDetect = WordDetectModule("WordDetect")

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
