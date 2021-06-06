
import numpy as np


def main():
    
    #Create parameter file 1
    path = r'./'
    fileName='MKIcool_pspice_param.inc'
    fullPath = path + fileName
    sourceFile = r"V:\LIBRARY\PSpice-inc\Coupling_Params_2x12stripes.inc"
    param=readParameterCopy(sourceFile)
    #writeParameterCopy(param,fullPath)

    #Create coupling file for coupling from shunt inductor to beam screen
    couplingStatements = writeCouplingStatements()
    fileName2 = r'./MKIcool_pspice_couplingStatements.inc'
    writeCouplingStatementsToFile(fileName2,couplingStatements)
    
    #Create coupling file for coupling from HV conductor to beam screen
    spiralScreen = False
    couplingStatements2 = writeCouplingStatements2(spiralScreen)
    fileName3 = r'./MKI_pspice_couplingStatements_HV_to_screen.inc'
    writeCouplingStatementsToFile(fileName3,couplingStatements2)
    
    

def writeCouplingStatements2(spiralScreen):
    couplingStatementsToWrite = []
    couplingName = 'K'
    coupledComponent = 'L_Kmag33_12metA_1_'
    if(not spiralScreen):
        for i in range(1,34):
            couplingStatementsToWrite.append('* Magnet column number: ' + str(i))
            for j in range(1,13):
                coupling = couplingName + str(j) + '_' + str(i)
                component1 = coupledComponent + 'KmClF' + str(i) + '_L1'
                component2 = coupledComponent + 'Ls' + str(j) + '_c' + str(i)
                value = '{' + 'Kms' + str(j) + '}'
                statement = coupling + '  ' + component1 + '  ' + component2 + '  ' + value
                couplingStatementsToWrite.append(statement)
                print(statement)
    
    if(spiralScreen):
        paramIndex=np.linspace(1,12,12)
        for i in range(1,34):
            couplingStatementsToWrite.append('* Magnet column number: ' + str(i))
            for j in range(1,13):
                coupling = couplingName + str(j) + '_' + str(i)
                component1 = coupledComponent + 'KmClF' + str(i) + '_L1'
                component2 = coupledComponent + 'Ls' + str(j) + '_c' + str(i)
                value = '{' + 'Kms' + str(np.int(paramIndex[j-1])) + '}'
                print(value)
                statement = coupling + '  ' + component1 + '  ' + component2 + '  ' + value
                couplingStatementsToWrite.append(statement)
            paramIndex = np.roll(paramIndex,-1)  
    return couplingStatementsToWrite



def writeCouplingStatements():
    couplingStatementsToWrite = []
    couplingName = 'Kn_Kmag33_12metA_1_K'
    coupledComponent = 'L_Kmag33_12metA_1_'
    for i in range(1,34):
        couplingStatementsToWrite.append('* Magnet column number: ' + str(i))
        for j in range(1,12):
            for k in range(j+1,13):
                coupling = couplingName + 'Ls' + str(j) + '_c' + str(i) + '_Ls' + str(k) + '_c' + str(i)
                component1 = coupledComponent + 'Ls' + str(j) + '_c' + str(i)
                component2 = coupledComponent + 'Ls' + str(k) + '_c' + str(i)
                value = '{' + 'kLs' + str(j) + 'Ls' + str(k) + '}'
                statement = coupling + '  ' + component1 + '  ' + component2 + '  ' + value
                couplingStatementsToWrite.append(statement)
                #print(statement)
                
    return couplingStatementsToWrite

def writeCouplingStatementsToFile(path,statements):
    file = open(path,"w")
    for i in range(0,len(statements)):
        line = statements[i] + '\n'
        file.write(line)
        
                  
def writeParameterCopy(param,path):
    file = open(path,"w")
    for i in range(0,len(param)):
        name = param[i][0]
        value = param[i][1]
        line='.PARAM ' + name + '=' + value + '\n'
        file.write(line)
        

def readParameterCopy(sourceFile):
    file=open(sourceFile,'r')
    #file=open('MKI_PostLS1_impedance.txt','r')
    lines=file.readlines()
    lines = lines[5:]
    param = [['',''] for i in range(0,len(lines))]
    for i in range(0,len(lines)):
        line = lines[i].split('PARAM ')[1]
        line2 = line.split('=')
        param[i][0] = line2[0]
        param[i][1] = line2[1].split('\n')[0]
    return param


if __name__ == "__main__":
    main()
