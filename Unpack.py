import numpy as np
import os
import sys
import glob as glob
import rigolread

'''
Take txt files created by rigolread.py, ask for desired discrimination values and create a text files with decay times excluded according to discrimination value.
Roberto Mandujano 2018
'''

#compile data file list
file_list = glob.glob('muon*')
decaytimes = []

#provide discriminator values and create a list out of the input
disc_input = input('Enter comma separated discrimination levels between 2.1 & 2.7: ')
disc_input = disc_input.split(',')
disc_input = np.array(disc_input)
discr = -1 * disc_input.astype(np.float) #peaks are negative


print('Extracting decays from ' + str(len(file_list)) + ' files')

def exclusion(d):
'''
    Defines exclusion procedure to identify frames with decays, and find time interval between first detection of particles and decay. 
    Input: 
        d -- Discriminator level (recommended values from 2.1-2.7)

    Output:
        Txt file filled with all decay times found at discriminator level 
'''
    
    decaytimes = []
    for file_path in file_list:
    	arr = np.genfromtxt(file_path, delimiter=',')
    	for n in range(len(arr[:,0])-1):
            a = arr[n,:] #getting single frames
            m = np.amin(a[110:]) #finding a minimum after characteristic peak 
            if m <= d:
                orig = np.argmin(a)
                dec = np.argmin(a[110:]) + 110
                t = (dec - orig) * 0.01881 #converting to microseconds (if connected to oscilloscope, you could also use rigolread.timeinc)
                decaytimes.append(t)
    
    #Announce decays extracted and saving to file
    print('Total Decays at level'  + str(d) + ' : ' +str(len(decaytimes)))   		
    np.savetxt(fname='decays'+str(d)+'.txt',X=decaytimes,delimiter=',') 

for d in discr:
    exclusion(d)

       
