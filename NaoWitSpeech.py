#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time, argparse
import requests
import httplib
import time
import StringIO

try:
    from naoqi import ALModule
    from naoqi import ALProxy
    from naoqi import ALBroker

except ImportError, err:
    print "Error when creating proxy:"
    print str(err)
    raise err
    exit(1)

NAO_IP = '131.174.106.197'

class NaoWitSpeech(ALModule):
    """
    NAO Module which can interact with wit.ai, for natural speech processing,
    can be run directly onto the NAO (that's probably faster)
    """
    def __init__( self, strName):
        """
        Writing audio to temporary file.
        """
        ALModule.__init__( self, strName );
        self.saveFile = StringIO.StringIO()
        try :
            self.ALAudioDevice = ALProxy("ALAudioDevice")
        except Exception, e:
            print "Error when creating proxy on ALAudioDevice:"
            print str(e)
            exit(1)
        channels = [0,1,0,0]
        isDeinterleaved = False
        isTimeStampped = True # in fact this parameter is not read. Time stamps are always calculated.
        self.ALAudioDevice.setClientPreferences(self.getName(), 48000, channels, 0, 0)

    def startAudioTest(self, duration):
        """
        Subscribe for audio data.
        """
        self.startWit()
        spr = ALProxy("ALAudioPlayer")
        spr.playFile("/usr/share/naoqi/wav/begin_reco.wav")
        self.ALAudioDevice.subscribe(self.getName())
        time.sleep(duration)
        spr.playFile("/usr/share/naoqi/wav/end_reco.wav")
        self.ALAudioDevice.unsubscribe(self.getName())
        print "stop"
        self.startUpload(self.saveFile)

    def startUpload(self, datafile):
        """
        Start upload of speechfile.
        """
        conn = httplib.HTTPSConnection("api.wit.ai")
        conn.request("POST", "/speech", datafile.getvalue(), self.headers)
        response = conn.getresponse()
        data = response.read()
        self.reply = data
        print data

    def process(self, nbOfInputChannels, nbOfInputSamples, timeStamp, inputBuff):
        #just in case you want to run this locally on the NAO
        #process is only called when ran locally on the NAO
        self.processRemote(self, nbOfInputChannels, nbOfInputSamples, timeStamp, inputBuff)

    def processRemote(self, nbOfInputChannels, nbOfInputSamples, timeStamp, inputBuff):
        """
        Incoming method for data, writes it to savefile. For remote use.
        """
        self.saveFile.write(inputBuff)

    def startWit(self):
        """
        Method for creating the call to wit.ai, change bearer to own API KeyboardInterrupt
        """
        self.headers = {'Authorization': 'Bearer *OWN API CODE*'}
        self.headers['Content-Type'] = 'audio/raw;encoding=signed-integer;bits=16;rate=48000;endian=little'

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pip",
                      help="IP adress of the robot",
                      dest="IP",
                      default=NAO_IP)

    parser.add_argument("--pport",
                      help="Port of communication with the robot",
                      dest="PORT",
                      default=9559)

    parser.add_argument("--rate",
                    help="Sampling rate",
                    dest="rate",
                    default=48000)

    args=parser.parse_args()
    args.rate = int(args.rate)
    args.PORT = int(args.PORT)
    pythonBroker = ALBroker("pythonBroker", "0.0.0.0", 9600, args.IP, args.PORT)
    global NaoWit
    NaoWit = NaoWitSpeech("NaoWit")
    NaoWit.startAudioTest(3)
