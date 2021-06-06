import SNPclass
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
signalPath = r"C:\Users\objorkqv\cernbox\Documents\Python\MKI workspace\Field adder\data\magnetInput.txt"
sparamPath = r"E:\CST\MKIcool\MKIcool_redrawn\Propagation through cells\Frequency domain\simulated\FD 1 sparam model\MKI_propagation_freq_domain_sparam.s2p"
# sparamPath = r"E:\CST\MKIcool\MKIcool_redrawn\Propagation through cells\Time domain\simulated\simulated 4\MKIcool_sparam.s2p"
fullwaveSignalModelPath = r"E:\CST\MKIcool\MKI signal model\Circuit model\signals_through_circuit_equivalent.txt"
fullwaveSignalModelPath_output = r"E:\CST\MKIcool\MKI signal model\Circuit model\signals_through_circuit_equivalent_out.txt"

def importPSpiceSignal(signalPath):
    data=np.loadtxt(signalPath,skiprows=1)
    
    t = data[:,0]
    signal = data[:,1]
    
    return t,signal

def getSingleSidedSpectrum(original_t,original_y,S):
    #Sampling freq
    dt = 2e-9
    #Zero pad for higher frequency domain resolution:
    zeropad_t,zeropad_y = zeropad(original_t,original_y)
    
    #Create new equidistant time variable
    new_t = np.arange(0,zeropad_t[-1],dt)
    
    #Resample signal over new time variable
    y_temp = interpolate.interp1d(zeropad_t,zeropad_y)
    y_resampled = y_temp(new_t)
    
    #FFT
    y_fft = np.fft.rfft(y_resampled)
    fs = 1/dt
    normalization = (2)/(new_t[-1]/original_t[-1])
    y_fft = y_fft*normalization
    new_f = np.linspace(0,0.5/dt,len(y_fft))
    
    #Resample fft at correct frequency points
    y_fft_temp = interpolate.interp1d(new_f,y_fft)
    y_fft_interp = y_fft_temp(S.freq*np.asarray(1e6))
    return y_fft_interp

def plotSignals(t1,sig1,t2,sig2):
    plt.figure()
    plt.plot(t1,sig1)
    plt.plot(t2,sig2)


def plotSpectrum(f,s1,s2,s3):
    plt.figure()
    plt.plot(f,20*np.log10(s1/np.max(s1)))
    plt.plot(f,20*np.log10(s2/np.max(s2)))
    plt.plot(f,20*np.log10(s3/np.max(s3)))
    plt.plot()
    plt.legend(['Magnet transfer function','Input signal from PSpice','Convoluted output signal'])
    plt.ylim([-40,5])
    plt.xlim([0, 5])
    plt.ylabel('Normalized, [dB]')
    plt.xlabel('Frequency [MHz]')
    plt.grid()
    
def zeropad(x,y):
    N = 100
    timeScaling=10
    x_pad = np.concatenate((x,np.linspace(x[-1]+x[1],timeScaling*x[-1],N)),axis=0)
    y_pad = np.concatenate((y,np.zeros(N)),axis=0)
    return x_pad,y_pad

def getConvolution(FDsig1,FDsig2,S):
    FDconv = FDsig1*FDsig2
    plotSpectrum(S.freq, np.abs(FDsig1), np.abs(FDsig2), np.abs(FDconv))
    TDconv = np.fft.irfft(FDconv)
    dt = 1/(2*S.freq[-1]*1e6)
    t = np.arange(0,dt*(len(TDconv)),dt)
    return t,TDconv
    
def interp_signal(t,t2,signal,N):
    signal_temp = interpolate.interp1d(t,signal)
    signal_interp = signal_temp(t2[0:N])
    return signal_interp
        
def integrate(x,y):
    primitiveFunction=[]
    for i in range(0,len(y)):
        integrated=np.trapz(y[0:i],x[0:i])
        primitiveFunction=np.concatenate((primitiveFunction,[integrated]),axis=0)
    
    return primitiveFunction

def getCircuitModelSignal(path1):
    data=np.loadtxt(path1,skiprows=2)
    return data
    

def main():    
    #Load PSpice input signal
    t,signal=importPSpiceSignal(signalPath)
    #Load magnet Sparam
    S = SNPclass.SNPfile(sparamPath)
    #Get correctly sampled fft of signal
    y_fft_interp=getSingleSidedSpectrum(t, signal, S)
    #Perform convolution between signal and sparam
    t2,convSignal=getConvolution(S.S21complex, y_fft_interp, S)
    #Get original signal and convolved signal sampled at exactly same points
    N=2000
    originalSignal_interp = interp_signal(t,t2,signal,N)
    #Integrate to get field
    field = integrate(t2[0:N],originalSignal_interp-convSignal[0:N])
    
    
    circuitSignal=getCircuitModelSignal(fullwaveSignalModelPath_output)
    
    plotSignals(t*1e6, signal, t2*1e6, convSignal)
    
    plt.figure()
    plt.plot(t2[0:N],field/field[700])
    
    
    plt.figure()
    plt.plot(t*1e6, signal)
    plt.plot(t2*1e6, convSignal)
    plt.plot(circuitSignal[:,0]/1e3,circuitSignal[:,1])
    plt.grid()
    plt.legend(['Input signal','Output: Manual convolution of full wave s parameter','Output: Circuit equivalent'])
    
    
    
    plt.show()
    
if __name__ == "__main__":
    main()