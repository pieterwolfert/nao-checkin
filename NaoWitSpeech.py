#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time, argparse
import requests
import httplib
import time
import StringIO

from naoqi import ALProxy
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
    def __init__( self, strName, args):
        """
        Writing audio to temporary file.
        """
        ALModule.__init__( self, strName );
        self.saveFile = StringIO.StringIO()
        try :
            self.ALAudioDevice = ALProxy("ALAudioDevice", args.IP, args.PORT)
        except Exception, e:
            print "Error when creating proxy on ALAudioDevice:"
            print str(e)
            exit(1)
        channels = [0,1,0,0]
        isDeinterleaved = False
        isTimeStampped = True # in fact this parameter is not read. Time stamps are always calculated.
        self.ALAudioDevice.setClientPreferences(self.getName(), args.rate, channels, 0, 0)

    def startAudioTest(self, duration):
        """
        Subscribe for audio data.
        """
        self.startWit()
        self.ALAudioDevice.subscribe(self.getName())
        time.sleep(duration)
        self.ALAudioDevice.unsubscribe(self.getName())
        self.startUpload(self.saveFile)

    def startUpload(self, datafile):
        """
        Start upload of speechfile.
        """
        conn = httplib.HTTPSConnection("api.wit.ai")
        conn.request("POST", "/speech", datafile.getvalue(), self.headers)
        response = conn.getresponse()
        data = response.read()
        print data

    def process(self, nbOfInputChannels, nbOfInputSamples, timeStamp, inputBuff):
        #just in case you want to run this locally on the NAO
        self.processRemote(self, nbOfInputChannels, nbOfInputSamples, timeStamp, inputBuff)

    def processRemote(self, nbOfInputChannels, nbOfInputSamples, timeStamp, inputBuff):
        """
        Incoming method for data, writes it to savefile. For remote use.
        """
        self.saveFile.write(inputBuff)

    def startWit(self):
        self.headers = {'Authorization': 'Bearer 4KQMHH5QWJDMD7QSOM4RLDRFJ7Q6HALP'}
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
    NaoWit = NaoWitSpeech("NaoWit",args)
    NaoWit.startAudioTest(3)
