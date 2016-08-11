from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule
import pdb
import time


class SpeechRecognition(ALModule):
    """To make it easier to use NaoQI proxies.
    """
    def __init__(self, name):
        ALModule.__init__(self, name);
        self.response = False
        self.value = []
        global memory
        memory = ALProxy("ALMemory")
        self.name = name
        self.spr = ALProxy("ALSpeechRecognition")

    def getSpeech(self, wordlist, wordspotting):
        self.response = False
        self.value = []
        self.spr.setVocabulary(wordlist, wordspotting)
        memory.subscribeToEvent("WordRecognized", self.name, "onDetect")

    def onDetect(self, eventname, value, subscriber):
        """
        Should bind now
        """
        self.response = True
        self.value = value
        memory.unsubscribeToEvent("WordRecognized", self.name)
        self.spr.pause(True)


if __name__ == "__main__":
    IP = "131.174.106.197"
    PORT = 9559
    pythonBroker = ALBroker("pythonBroker", "0.0.0.0", 9600, IP, PORT)
    Speecher = SpeechRecognition("Speecher", ["breakfast", "pay", "checkin"], True)
    while Speecher.response is False:
        time.sleep(1)
