from naoqi import ALProxy
import time

channels = [0, 0, 1, 0]

class SoundRecorder:
    def __init__(self, ip, port):
        try:
            self.proxy = ALProxy("ALAudioRecorder", ip, port)
        except Exception as e:
            print e

    def record(self):
        self.proxy.startMicrophonesRecording("/home/nao/test.wav", "wav", 16000, channels)
        time.sleep(5)
        self.proxy.stopMicrophonesRecording()

def main():
    sr = SoundRecorder("131.174.106.197", 9559)
    sr.record()
    try:
        aup = ALProxy("ALAudioPlayer", "131.174.106.197", 9559)
    except Exception,e:
        print "Could not create proxy to ALAudioPlayer"
        print "Error was: ",e
    aup.post.playFile("/home/nao/test.wav")

if __name__ == '__main__':
    main()
