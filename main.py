from naoqi import ALProxy
from naoqi import ALBroker
import ast
from TouchEvent import ReactToTouch
from SpeechRecognition import SpeechRecognition
from NaoWitSpeech import NaoWitSpeech
from NaoBreakfast import NaoBreakfast
from NaoCheckin import NaoCheckin
import argparse
import time

def waitTouch():
    """
    NAO responds when any of the touchable areas is activated.
    """
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
    """
    Basic awareness with face tracking, fully engaged with the person talking,
    to the NAO.
    """
    global awe
    awe = ALProxy("ALBasicAwareness")
    awe.setEngagementMode("FullyEngaged")
    awe.startAwareness()

def sayWelcome():
    """
    Welcome method.
    """
    global tts
    tts = ALProxy("ALAnimatedSpeech")
    tts.say("Welcome to Louis his hotel.")
    tts.say("It would be very helpful of you to give clear answers.")

def makeSpeech():
    """
    Makes speecher object, is globally accesible within all modules.
    """
    global Speecher
    Speecher = SpeechRecognition("Speecher")

def getResponse(wordlist, wordspotting):
    """
    Speech recognition method for getting a response.

    Args:
    - wordlist (give a list of words to recognize)
    - wordspotting (either True or False, can recognize words within sentences)
    """
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
    global NaoWit
    NaoWit = NaoWitSpeech("NaoWit")
    end = False
    while end is False:
        tts.say("What would you like to do?")
        getResponse(["breakfast", "checkin", "pay", "checkout",
                    "reservation", "stop", "information", "pizza"], True)
        choice = Speecher.value
        choice = choice[0].strip('<>. ')
        if "breakfast" in choice:
            nbr = NaoBreakfast(tts, Speecher)
        elif "checkin" in choice:
            nci = NaoCheckin(tts, NaoWit)
        elif "pay" in choice:
            tts.say("You can pay at the counter with your card.")
        elif "stop" in choice:
            tts.say("Thank you for choosing me!")
            end = True
            awe.stopAwareness()
        elif "information" in choice:
            tts.say("This hotel is established in 2016")
            tts.say("My master is Louis Vuurpile")
        elif "pizza" in choice:
            tts.say("I will order a pizza doner now,\
                    it will be delivered in Nijmegen")

if __name__ == "__main__":
    NAO_IP = "10.0.1.6"
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
