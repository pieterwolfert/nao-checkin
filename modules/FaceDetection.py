import time
from naoqi import ALProxy

#Module for FaceDetection which might make your life easier :)
#Author: Pieter Wolfert 

#Class for using FaceDetection in the NAO
#Is basically responsible for a proxy to the NAO, all other methods
#of the NAO can be accessed as well
class FaceDetection:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
    
    def makeProxy(self):
        try:
            self.faceProxy = ALProxy("ALFaceDetection", self.ip, self.port)
        except Exception, e:
            print "Error when creating face detection proxy:"
            print str(e)
            exit(1)
    
    #This method tests facial recognition, prints sizes and does this 20
    #times
    def detectFace(self, period, name):
        self.faceProxy.subscribe(name, period, 0.0)
        self.memoryProxy()
        mem = "FaceDetected" #key to access face recognition data
        for i in range(0, 20):
            time.sleep(0.5)
            val = self.memory.getData(mem)
            print ""
            print "\****"
            print ""
            if(val and isinstance(val, list) and len(val) >= 2):
                timeStamp = val[0]
                faceInfoArray = val[1]
                self.readFaceInfo(faceInfoArray)
        self.faceProxy.unsubscribe(name)
        print "FaceRec Test terminated succesfully."
   
    #Makes a memory proxy for getting the data
    def memoryProxy(self):
        try:
            self.memory = ALProxy("ALMemory", self.ip, self.port)
        except Exception, e:
            print "Error when creating memory proxy:"
            print str(e)
            exit(1)

    #Stops after faces are detected
    #might detect more than one face
    def detectOneFace(self, period, name):
        self.faceProxy.subscribe(name, period, 0.0)
        self.memoryProxy()
        mem = "FaceDetected"
        val = self.memory.getData(mem)
        while(val and isinstance(val, list) and len(val) < 2):
            time.sleep(0.5)
            val = self.memory.getData(mem)
        timeStamp = val[0]
        faceInfoArray = val[1]
        self.countFaces(faceInfoArray)
        self.readFaceInfo(faceInfoArray)

    #reads out the face info array and gives information about the size
    #might contain several faces
    def readFaceInfo(self, infoarray):
        try:
            for j in range( len(infoarray)-1 ):
                faceInfo = infoarray[j]
                faceShapeInfo = faceInfo[0]
                faceExtraInfo = faceInfo[1]
                print " alpha %.3f - beta %.3f" %\
                        (faceShapeInfo[1], faceShapeInfo[2])
                print " width %.3f - height %.3f" %\
                        (faceShapeInfo[3], faceShapeInfo[4])
        except Exception, e:
            print "Faces detected but cannot read from getData()"
            print e
    
    #counts the number of faces inside the information array
    def countFaces(self, infoarray):
        number = len(infoarray) -1
        print number

#Main(ly) for testing purposes
def main():
    IP = "131.174.106.197"
    PORT = 9559
    job = FaceDetection(IP, PORT)
    job.makeProxy()
    job.detectOneFace(500, "Pieter")

if __name__ == "__main__":
    main()
