from naoqi import ALProxy

#author Pieter Wolfert

#Combination of animated and non-animated speech
#See for more information on animating your speech the aldebaran NaoQI API
class TextToSpeech:
    def __init__(self, IP, PORT, direct, animated):
        self.ip = IP
        self.port = PORT
        if direct:
            if animated:
                self.makeAnimated()
            else:
                self.makeProxy()
    
    #Makes a standard proxy for TextToSpeech
    def makeProxy(self):
        try:
            self.proxy = ALProxy("ALTextToSpeech", self.ip, self.port)
        except Exception, e:
            print "Oops, couldn't connect to TextToSpeech module on NAO"
            print str(e)

    #Makes a proxy for animated text to speech
    def makeAnimated(self):
        try:
            self.animatedProxy =\
                    ALProxy("ALAnimatedSpeech", self.ip, self.port)
        except Exception, e:
            print "Oops, couldn't load AnimatedSpeech"
            print e

    def sayAnimated(self, text, configuration):
        self.animatedProxy.say(text, configuration)

#Example of how to use animated speech
def main():
    IP = "131.174.106.197"
    PORT = 9559
    job = TextToSpeech(IP, PORT, True, True)
    configuration = {"bodyLanguageMode":"random"}
    job.sayAnimated("Hello! ^start(animations/Sit/BodyTalk/BodyTalk_1)\
            Nice to meet you!", configuration)
        
if __name__ == "__main__":
    main()


