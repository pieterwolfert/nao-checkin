from naoqi import ALProxy
from naoqi import ALModule
from naoqi import ALBroker
import time
import argparse

IP = "131.174.106.197"
PORT = 9559

class FaceDetect(ALModule):
    """
    This string is mandatory.
    """
    def __init__(self, strName):
        try:
            p = ALProxy(strName)
            p.exit()
        except:
            pass
        ALModule.__init__( self, strName );
        memory = ALProxy("ALMemory", IP, PORT)
        facep = ALProxy("ALFaceDetection", IP, PORT)
        facep.subscribe("Test_Face", 500, 0.0 )
        memory.subscribeToEvent("FaceDetected", "face", "faceCall")

    def faceCall(self, key, value, message):
        """
        Method which is called when a face is detected.
        """
        a = value
        faceInfo = a[1]
        facesInfo = faceInfo[1]
        print len(facesInfo)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pip",
                      help="IP adress of the robot",
                      dest="IP",
                      default=IP)

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
    face = FaceDetect("face")
    while True:
        time.sleep(2)
