### Loads a touchstone S2P file into np arrays



import numpy as np
import matplotlib.pyplot as plt

class SNPfile:
    def __init__(self,filePath):
        self.S11lin = []
        self.S21lin = []
        self.S12lin = []
        self.S22lin = []
        self.freq = []
        self.S11db = []
        self.S21db = []
        self.S12db = []
        self.S22db = []
        self.S11angle = []
        self.S21angle = []
        self.S12angle = []
        self.S22angle = []
        self.S21complex = []
        path = filePath
        self.extractSParamData(filePath)
        self.getComplexParam()
        
    def extractSParamData(self,filePath):
        file=open(filePath,'r')
        lines=file.readlines()
        for i in range(0,len(lines)):
            data = self.separateParameters(lines[i])
            data=data[0].split()
            try:
                self.freq = self.freq + [np.double(data[0])]
                self.S11lin = self.S11lin + [np.double(data[1])]
                self.S21lin = self.S21lin + [np.double(data[3])]
                self.S12lin = self.S12lin + [np.double(data[5])]
                self.S22lin = self.S22lin + [np.double(data[7])]
                self.S11angle = self.S11angle + [np.double(data[2])]
                self.S21angle = self.S21angle + [np.double(data[4])]
                self.S12angle = self.S12angle + [np.double(data[6])]
                self.S22angle = self.S22angle + [np.double(data[8])]
            except:
                print('Removing SNP header')
        
    def getComplexParam(self):
        for i in range(0,len(self.S21lin)):
            im=np.array([0+1j])
            im=im[0]
            self.S21complex = self.S21complex + [self.S21lin[i]*(np.cos(np.pi*self.S21angle[i]/180)+np.sin(np.pi*self.S21angle[i]/180)*im)]
        
    def separateParameters(self,line):
        line=line.strip('\n')
        line=line.split('\t')
        return line
    
    def plotParam(self,Sparam):
        plt.figure()
        plt.plot(self.freq,Sparam)
        plt.show()
    
    def dBtoLin(self,dBdata):
        linData = np.power(10,dBdata/20)
        return linData
        
    def getImpulseResponse(self):
        self.s21_impulse = np.fft.irfft(self.S21complex)
        dt = 1/(1e6*self.freq[-1])
        self.s21_t = np.linspace(0,(len(self.s21_impulse)-1)*dt,len(self.s21_impulse))
        
        
