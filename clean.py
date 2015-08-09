from argparse import ArgumentParser
from sisc_optimizer import *
import scipy.io as sio
import fileio as fio
import time
import numpy as np
import csv
import copy
import os
import webbrowser

#gencsv('skeleton_test/41.1.csv','temp/result_9_M=64_D=5_beta=0.2__13_13_54.mat')

def gencsv(inputfile,matfile):
    
    dat = sio.loadmat(matfile)
    M,K,D=np.shape(dat['psi_comp'])
    tdp = np.zeros((M,np.size(dat['princmp'],axis=0),D));
    for d in xrange(D):
        temp = dat['psi_comp'][:,:,d]
        tdp[:,:,d] = temp.dot(dat['princmp'].T)

    saveAscsv(inputfile,dat['alpha_recon'],dat['psi_recon'],30.2,tdp,dat['xmean'])

def saveAscsv(inputfile,alpha,psi,speed, tdp, Xmean):
    #print str(inputfile)[14:-4];

    speed = float(speed);
    directory = 'Results/'+str(inputfile)[14:-4];
    if not os.path.exists(directory):
        os.makedirs(directory);

    timeline = [];
    skeleton = [];
    
    for i in range(5):
        maxalpha = [];
        tempa = alpha[:,i];
        stablist = tempa.tolist();
        totalmax = max(stablist)*0.32;
        for ele in range(len(stablist)):
            if stablist[ele] <= totalmax:
                stablist[ele] = 0;
        templist = copy.copy(stablist);
        rangelist = len(templist);
        #print max(templist);
        maxalpha.append(max(templist));

        checkmaxval = [];
        j=0;
        checkloop = 0;
        while checkloop != 1:
            writelist = [];
            writelist.append(str(i)+'.'+str(j));
            j=j+1;
            tempmaxval = max(templist);
            #print tempmaxval;
            if tempmaxval > totalmax:
                maxindex = templist.index(tempmaxval);
                #print maxindex;
                ckv = 0;
                while ckv != 1:
                    #print maxindex;
                    if templist[maxindex] <= totalmax:
                        break;
                    if len(checkmaxval)>0:
                        for c in checkmaxval:
                            if abs(maxindex-c) < 64:
                                templist[maxindex] = 0;
                                stablist[maxindex] = 0;
                                maxindex = templist.index(max(templist));
                                ckv = 0;
                                break;
                            else:
                                ckv = 1;
                    else:
                        ckv = 1;

                checkmaxval.append(maxindex);
                #print maxindex;
                templist[maxindex] = 0;
                tempstart = maxindex;
                tempend = maxindex;
                for k in range(32):
                    tempstart = tempstart-1;
                    tempend = tempend+1;
                    if tempstart>=0:
                        templist[tempstart]=0;
                        stablist[tempstart]=0;
                    if tempend < rangelist:
                        templist[tempend]=0;
                        stablist[tempstart]=0;
                if tempstart<0:
                    tempstart=0;
                if tempend >= rangelist:
                    tempend = rangelist-1;
                writelist.append(int(tempstart/speed));
                writelist.append(int(tempend/speed));
                timeline.append(writelist);
                if max(templist)<=totalmax:
                    checkloop=1;

            else:
                break;

    '''
    for i in range(5):
        psilist = psi[:,:,i].tolist();
        #psilist = psi[:,:,i].tolist();
        skelelist = [];
        for row in psilist:
            skelelist.append(row);

        writename = 'Results/'+str(inputfile)[14:-4]+'/skele_'+str(i)+'_'+str(inputfile)[14:-4]+'.csv';
        #skelelist = [skeletitle]+skelelist;
        with open(writename,'w') as writefile:
            writer = csv.writer(writefile);
            writer.writerows(skelelist);
    '''
    xeach = Xmean.tolist()[0];
    for i in range(5):
        tdplist = tdp[:,:,i].tolist();
        tempskele = [];
        for row in tdplist:
            if row != '':
                tempskele.append(row);
        tempskele.append(xeach);
        writename = 'Results/'+str(inputfile)[14:-4]+'/tdp_'+str(i)+'_'+str(inputfile)[14:-4]+'.csv';
        with open(writename,'wb') as writefile:
            writer = csv.writer(writefile);
            writer.writerows(tempskele);
    
    timetitleline = ['vpname', 'starttime', 'endtime'];
    finaltimeline = [];
    timecount = 0;
    parrcount = '';
    for ele in range(len(timeline)):
        if ele==0:
            timecount=1;
            parrcount = str(timeline[ele][0])[0];
        else:
            tempparrnum = str(timeline[ele][0])[0];
            if tempparrnum==parrcount:
                timecount = timecount+1;
            else:
                if timecount > 3:
                    for timeele in timeline:
                        if str(timeele[0])[0]==parrcount:
                            finaltimeline.append(timeele);
                timecount=1;
                parrcount = tempparrnum;

    if timecount > 3:
        for timeele in timeline:
            if str(timeele[0])[0]==parrcount:
                finaltimeline.append(timeele);

    finaltimeline = [timetitleline]+finaltimeline;
    timewritename = 'Results/'+str(inputfile)[14:-4]+'/timeline_'+str(inputfile)[14:-4]+'.csv';
    with open(timewritename,'wb') as writefile1:
        writer1 = csv.writer(writefile1);
        writer1.writerows(finaltimeline);
