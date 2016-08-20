from naoqi import ALProxy
from NaoWitSpeech import NaoWitSpeech
import ast

class NaoCheckin():
    def __init__(self, tts, NaoWit):
        """
        Example of checkin module, uses external speech recognition for more
        freedom of recognizing natural speech. 
        """
        tts.say("I will check you in, do you have your reservation number?")
        NaoWit.startAudioTest(3)
        roomnumber = ast.literal_eval(NaoWit.reply)
        roomnumber = roomnumber['_text']
        tts.say("I've got your number.")
        room = "Your number is " + roomnumber
        tts.say(room)
