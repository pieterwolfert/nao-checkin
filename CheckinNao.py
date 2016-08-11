from naoqi import ALProxy

class CheckInNao():
    def __init__(self):
        self.spr = ALProxy("ALSpeechRecognition")

    def binaryQuestion(self):
        wordlist = ["yes", "no"]
        wordspotting = False
        self.memory = ALProxy("ALMemory")
        self.spr.setVocabulary(wordlist, wordspotting)
        
