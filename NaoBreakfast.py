from naoqi import ALProxy
import time

class NaoBreakfast:
    def __init__(self, tts, Speecher):
        self.Speecher = Speecher
        tts.say("I heard you would like breakfast, what type of breakfast would you like?")
        self.getResponse(["options", "english", "continental"], True)
        choice = Speecher.value
        choice = choice[0].strip('<>. ')
        if "options" in choice:
            tts.say("I can offer you an english or continental breakfast.")
            self.getResponse(["options", "english", "continental"], True)
            choice = Speecher.value
            choice = choice[0].strip('<>. ')
            if "english" or "continental" in choice:
                tts.say("I will forward your choice")

        elif "english" or "continental" in choice:
            tts.say("I will forward your choice")


    def getResponse(self, wordlist, wordspotting):
        self.Speecher.getSpeech(wordlist, wordspotting)
        try:
            while self.Speecher.response is False:
                time.sleep(1)
        except KeyboardInterrupt:
            print
            print "Interrupted by user, shutting down"
            pythonBroker.shutdown()
            sys.exit(0)
