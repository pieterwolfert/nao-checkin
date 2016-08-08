from naoqi import ALProxy
from naoqi import ALBroker
from TouchEvent import ReactToTouch
from CheckInNao import CheckInNao
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
    awe = ALProxy("ALBasicAwareness")
    awe.startAwareness()

def sayWelcome():
    tts = ALProxy("ALAnimatedSpeech")
    tts.say("Welcome to Louis his hotel.")
    tts.say("I can help you with your check-in.")
    tts.say("It would be very helpful of you to give clear answers.")
    tts.say("Do you want me to check you in?")

def main(ip, port):
    myBroker = ALBroker("myBroker",
       "0.0.0.0",   # listen to anyone
       0,           # find a free port and use it
       ip,          # parent broker IP
       port)        # parent broker port
    waitTouch() #wait for a touch
    startAwareness()
    sayWelcome() #say welcome, ask if person wants to be checked in
    user = CheckInNao()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="131.174.106.197",
                        help="Robot ip address")
    parser.add_argument("--port", type=int, default=9559,
                        help="Robot port number")
    args = parser.parse_args()
    main(args.ip, args.port)
