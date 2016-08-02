from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule
from naoqi import ALSoundExtractor
import time

from optparse import OptionParser

NAO_IP = "131.174.106.197"

AudioFileProcessor = None

class AudioFileProcessorModule(ALSoundExtractor):
    """ Processes raw audiostream from NAO

    """
    def __init__(self, name):
        try: #check whether the module object already exists, if yes, exit it.
            p=ALProxy(name)
            p.exit()
        except:
            pass
        ALModule.__init__(self, name)
        adp = ALProxy("ALAudioDevice")
        adp.subscribe(name)
        time.sleep(2)
        adp.unsubscribe(name)

    def process(self, nbOfChannels, nbrOfSamplesByChannel, buffer, timeStamp):
        """ This is called to process audio
        """
        time.sleep(2)
        print "hello world"
        #process(const int & nbOfChannels, const int & nbrOfSamplesByChannel, const AL_SOUND_FORMAT * buffer, const ALValue & timeStamp)





def main():
    #add broker object for remote execution of module
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
    global AudioFileProcessor
    AudioFileProcessor = AudioFileProcessorModule("AudioFileProcessor")

if __name__ == "__main__":
    main()
