from naoqi import ALProxy
from naoqi import ALBroker
import ast
from TouchEvent import ReactToTouch
from SpeechRecognition import SpeechRecognition
from NaoWitSpeech import NaoWitSpeech
import argparse
import time

def waitTouch():
    global ReactToTouch
    ReactToTouch = ReactToTouch("ReactToTouch")
    try:
        while ReactToTouch.touched is False:
            time.sleep(1)
    except KeyboardInterrupt:
        print
        print "Interrupted by user, shutting down"
        myBroker.shutdown()
        sys.exit(0)

def startAwareness():
    global awe
    awe = ALProxy("ALBasicAwareness")
    awe.setEngagementMode("FullyEngaged")
    awe.startAwareness()

def sayWelcome():
    global tts
    tts = ALProxy("ALAnimatedSpeech")
    tts.say("Welcome to Louis his hotel.")
    tts.say("It would be very helpful of you to give clear answers.")
    tts.say("What would you like to do?")

def makeSpeech():
    global Speecher
    Speecher = SpeechRecognition("Speecher")

def getResponse(wordlist, wordspotting):
    Speecher.getSpeech(wordlist, wordspotting)
    try:
        while Speecher.response is False:
            time.sleep(1)
    except KeyboardInterrupt:
        print
        print "Interrupted by user, shutting down"
        pythonBroker.shutdown()
        sys.exit(0)

def main(args):
    pst = ALProxy("ALRobotPosture")
    pst.goToPosture("Sit", 1.0)
    waitTouch() #wait for a touch
    startAwareness()
    sayWelcome() #say welcome, ask if person wants to be checked in
    makeSpeech()
    getResponse(["breakfast", "checkin", "pay", "checkout", "reservation"], True)
    choice = Speecher.value
    choice = choice[0].strip('<>. ')
    if "breakfast" in choice:
        tts.say("I heard you would like breakfast, you can pay with card at the counter.")
    elif "checkin" in choice:
        tts.say("I will check you in, do you have your reservation number?")
    elif "pay" in choice:
        tts.say("You can pay at the counter with your card.")
    global NaoWit
    NaoWit = NaoWitSpeech("NaoWit")
    NaoWit.startAudioTest(3)
    roomnumber = ast.literal_eval(NaoWit.reply)
    roomnumber = roomnumber['_text']
    tts.say("I've got your number.")
    room = "Your number is " + roomnumber
    tts.say(room)
    tts.say("Would you like to have more information about this hotel?")
    getResponse(["yes", "no"], False)
    choice = Speecher.value
    choice = choice[0].strip('<>. ')
    if "yes" in choice:
        tts.say("This hotel is established in 2016")
        tts.say("My master is Louis Vuurpile")
    elif "no" in choice:
        tts.say("Okay, bye")


if __name__ == "__main__":
    NAO_IP = "131.174.106.197"
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
    global pythonBroker
    pythonBroker = ALBroker("pythonBroker", "0.0.0.0", 9600, args.IP, args.PORT)
    main(args)
