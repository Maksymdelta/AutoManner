''' File Input-Output Module
    ========================
    Functions starting with the prefix "toyExample" are sample datasets
    created for testing while writing various sections of the code.
    Other functions are created to load and preprocess the original dataset.
-------------------------------------------------------------------------------
    Coded by Md. Iftekhar Tanveer (itanveer@cs.rochester.edu)
    Rochester Human-Computer Interaction (ROCHCI)
    University of Rochester
-------------------------------------------------------------------------------
'''
import numpy as np
import os
import plotskeleton as ps

#################################### FILE IO ##################################
# Read point definition file
def readPointDic(dicFilename):
    with open(dicFilename) as f:
        pointName = [dat.strip().split('=') for dat in f.readlines()]
        points = dict((elem[0].strip(),int(elem[1])) for elem in pointName)
        return points

# Read the speech boundary file. This file contains information on where the
# actual speech started and where finished
# Returns videoList, start_End_time_List
def readSpeechBoundary(csvFileName):
    with open(csvFileName) as f:
        f.readline()
        temp = [x.split(',') for x in f.readlines()]
        videoList = [x[0] for x in temp]
        starEndList = np.array([x[1:] for x in temp]).astype(np.int)
    return videoList,starEndList

# Reads the skeleton data file (csv)
# returns data, data_header, ScreenXY, ScreenXY_header, Orientation, Orien_Head
def readDataFile(readDataFile):
    # read datafile
    with open(readDataFile) as f:
        header = f.readline().split(',')[0:-1]
        temp = [x.split(',') for x in f.readlines()]
        temp = np.array([x[0:-1] for x in temp]).astype(np.float)
    # Read indices
    scnIdx=[i for i,x in enumerate(header) if x == 'ScreenX' or x == 'ScreenY']
    orientIdx = range(scnIdx[-1]+1,len(header))
    datIdx = [x for x in range(scnIdx[-1]+1) if x not in scnIdx]
    return temp[:,datIdx], [header[L] for L in datIdx],\
    temp[:,orientIdx],[header[L] for L in orientIdx],\
    temp[:,scnIdx],[header[L] for L in scnIdx]
    
# We delete the first and last nSec * 30 frames because that is usually garbage
def clean(dat,nSec = 10):
    return dat[30*nSec:-30*nSec,:,:]
# Normalization of the skeleton data. x,y,z components are individually
# meansubtracted and divided by
def normalizeDat(dat):    
    datMean = np.mean(dat,axis=0)
    dat = (dat - datMean)
    datStd = np.max(np.std(dat,axis=0),axis=1)
    for j in xrange(np.size(dat,axis=1)):
        dat[:,j,:]/=datStd[j]
    return dat
# Reads all the skeleton tracking file in a folder and concatenates to 
# to a single 3 dimensional array. First dimension is for frame number. 2nd and 
# 3rd dimension is for jointID and (x,y,z) values respectively 
# returns a tensor containing the data from all files
# Applies some rudimentary preprocessing if preprocess is turned on
def readAllFiles_Concat(fullFiles,suffix,preprocess,joints=(),nSec = 10):
    if not joints:
        m = 20
    else:
        m = len(joints)
    allData = np.zeros((1,m,3))
    boundDic = {}
    bound = (-1,-1)
    for root,folder,files in os.walk(fullFiles):
        for afile in files:
            if afile.lower().endswith(suffix.lower()):
                # create full filename and print
                fullPath = os.path.join(root,afile)
                print fullPath
                # Read file. 
                dat,_,_ = readDataFile(fullPath,joints)
                # Preprocess
                if preprocess:
                    dat = normalizeDat(clean(dat,nSec))
                # Keep a record of where each file starts and ends 
                bound = (bound[1]+1,bound[1]+np.size(dat,axis=0))
                boundDic[bound] = fullPath
                # Concatenate all the data
                allData = np.concatenate((allData,dat),axis=0)
    allData=np.delete(allData,0,axis=0)
    allData = np.transpose(allData,axes=[0,2,1])
    return allData,boundDic
# Given any row index and the doundary dictionary it returns from which
# file the row is coming. Important to trace back for finding the frame in
# the video
def findWhichFile(rowIndx,boundDic):
    rowNumber = np.where((np.array(boundDic.keys())[:,0]<rowIndx) & \
    (np.array(boundDic.keys())[:,1]>rowIndx))[0][0]
    return boundDic.values()[rowNumber]
# Generate and return a toy data
def toyExample_small():
    alpha = np.zeros((16,1))
    alpha[4] = 1
    alpha[12] = -0.5
    psi = np.zeros((4,1,1))
    psi[:,0,0] = [1,2,1,-1]
    psi[:,1,0] = [1,2,-1,1]
    psi[:,2,0] = [0.5,1,0.5,0]
    return alpha,psi    
# Generate and return a toy data
def toyExample_medium():
    alpha = np.zeros((256,1))
    alpha[35] = 0.5
    alpha[140] = -0.5
    alpha[160] = 1
    alpha[220] = -1
    xVal = np.linspace(-1,1,32)*np.pi
    psi = np.zeros((len(xVal),3,1))
    psi[:,0,0] = np.sin(xVal)
    psi[:,1,0] = np.sin(2*xVal-np.pi)
    psi[:,2,0] = np.sin(4*xVal-np.pi/4)
    return alpha,psi
# Generate and return a toy data
def toyExample_medium_boostHighFreq():
    alpha = np.zeros((256,1))
    alpha[35] = 0.5
    alpha[140] = -0.5
    alpha[160] = 1
    alpha[220] = -1
    xVal = np.linspace(-1,1,32)*np.pi
    psi = np.zeros((len(xVal),3,1))
    psi[:,0,0] = 0.5*np.sin(xVal)
    psi[:,1,0] = np.sin(2*xVal-np.pi)
    psi[:,2,0] = 2*np.sin(4*xVal-np.pi/4)
    return alpha,psi
# Generate and return a toy data
def toyExample_medium_boostLowFreq():
    alpha = np.zeros((256,1))
    alpha[35] = 0.5
    alpha[140] = -0.5
    alpha[160] = 1
    alpha[220] = -1
    xVal = np.linspace(-1,1,32)*np.pi
    psi = np.zeros((len(xVal),3,1))
    psi[:,0,0] = 2*np.sin(xVal)
    psi[:,1,0] = np.sin(2*xVal-np.pi)
    psi[:,2,0] = 0.5*np.sin(4*xVal-np.pi/4)
    return alpha,psi
# Generate and return a toy data
def toyExample_medium_1d():
    alpha = np.zeros((256,1))
    alpha[35] = 0.5
    alpha[140] = -0.5
    alpha[160] = 1
    alpha[220] = -1
    xVal = np.linspace(-1,1,32)*np.pi
    psi = np.zeros((len(xVal),1,1))
    psi[:,0,0] = np.sin(xVal)
    return alpha,psi
# Generate and return a toy data
def toyExample_medium_1d_multicomp():
    alpha = np.zeros((256,2))
    alpha[35,0] = 0.5
    alpha[140,0] = -0.5
    alpha[160,0] = 1
    alpha[220,0] = -1
    alpha[50,1] = 0.5
    alpha[100,1] = -0.5
    alpha[200,1] = 1
    xVal = np.linspace(-1,1,32)*np.pi
    psi = np.zeros((len(xVal),1,2))
    psi[:,0,0] = np.sin(xVal)
    psi[:,0,1] = np.pi - np.abs(xVal)
    return alpha,psi
# Generate and return a toy data
def toyExample_medium_3d_multicomp():
    alpha = np.zeros((256,2))
    alpha[35,0] = 0.5
    alpha[140,0] = -0.5
    alpha[160,0] = 1
    alpha[220,0] = -1
    alpha[50,1] = 0.5
    alpha[100,1] = -0.5
    alpha[200,1] = 1
    xVal = np.linspace(-1,1,32)*np.pi
    psi = np.zeros((len(xVal),3,2))
    psi[:,0,0] = np.sin(xVal)
    psi[:,1,0] = np.sin(xVal/2.0)
    psi[:,2,0] = np.sin(xVal/2.0 + np.pi/2)
    psi[:,0,1] = np.pi - np.abs(xVal)
    psi[:,1,1] = np.pi - np.abs(xVal/2.0)
    psi[:,2,1] = np.abs(xVal/2.0)
    return alpha,psi
# Generate and return a toy data
def toyExample_large_3d_multicomp(N=8192,M=64):
    alpha = np.zeros((N,2))
    alpha[np.random.rand(N)>0.9975,0]=1.0
    alpha[np.random.rand(N)>0.9975,1]=1.0
    xVal = np.linspace(-1,1,M)*np.pi
    psi = np.zeros((len(xVal),3,2))
    psi[:,0,0] = np.sin(xVal)
    psi[:,1,0] = np.sin(xVal/2.0)
    psi[:,2,0] = np.sin(xVal/4.0 + np.pi/2)
    psi[:,0,1] = np.pi - np.abs(xVal)
    psi[:,1,1] = np.pi - np.abs(xVal/2.0)
    psi[:,2,1] = np.abs(xVal/2.0)
    return alpha,psi
############################## End File IO ####################################
def moduleTest():
    jointId = readPointDic('Data/pointDef.dic')
    videName,startEnd = readSpeechBoundary('Data/Speech_Boundary.dat')
    data,dataHead,orient,orientHead,_,_ = readDataFile('Data/test_Data.csv')
    
    ps.animate(data,orient)
    
if __name__ == '__main__':
    moduleTest()