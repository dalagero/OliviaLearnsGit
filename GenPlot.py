import numpy as np
import os
import scipy
import pandas as pd
from scipy import stats
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import glob

'''
Plotting and fitting for all decay time txt files in current directory.
Roberto Mandujano 2018 
'''

#Define fit model 
def exp_func(t,n,k,b):
    return n * np.exp(-t/k) + b 

#Empty arrays to fill with data/fit parameters
ndecays = []
chi2s = []
taus = []
t_err = []
discr = []


dec_files = glob.glob('decays-*')
i = 1

def plot(f):

    """ 
    Takes a txt file with decay times and produces a histogram with an exponential fit
    Inputs:
    f -- text file with a column or row of decay times

    Output:
    Produces a matplotlib figure with the histogram and fit, displaying relevant parameters
    Produces and prints pandas dataframe with fit and data paramaters for each discrimination 
    """
    #Generate array 
    decaytimes = np.genfromtxt(f,delimiter=',')

    #Creating histograms and removing empty bins
    yhistn, xhistn = np.histogram(decaytimes, bins=24)
    tdel = np.where(yhistn == 0)
    yhistm = np.delete(yhistn,tdel)
    xhist0 = np.delete(xhistn,tdel)

    #Eliminating unreasonable outliers
    ind = [len(yhistm)-1,len(yhistm)]
    xhist_bc = np.delete(xhist0,0) #this is necessary for proper binning
    xhist = np.delete(xhist0,ind)
    yhist = np.delete(yhistm,ind)

    #Define bin centers, error array, and parameter guess
    bin_cen = 0.5*(xhist_bc[1:] + xhist_bc[:-1])
    error = yhist ** (0.5)
    n = np.sum(yhist)
    ndecays.append(n)
    guess = [n,2.1,2.5]

    #Fit using scipy library
    popt, pcov = curve_fit(exp_func,bin_cen,yhist,sigma=error,absolute_sigma=True,p0=guess)
    par_err = np.sqrt(np.diag(pcov))
    t_err.append(par_err[1])
    taus.append(popt[1])

    #Calculate Chi squared and degrees of freedom
    chi2, p = scipy.stats.chisquare(yhist,exp_func(bin_cen,*popt))
    chi2s.append(chi2)

    #Get discrimination level from filename
    dstr = str(f[7]) + str(f[8]) + str(f[9])
    if str(f[10]).isdigit() == True:
        dstr += str(f[10])
        if str(f[11]).isdigit() == True:
            dstr += str(f[11])
    d = float(dstr)
    discr.append(d)

    #Plotting
    plt.subplot(3,3,i)
    plt.title('Muon Decay Times at ' + str(d))
    plt.errorbar(bin_cen,yhist,yerr=error,fmt='ro',label='data')
    plt.plot(bin_cen, exp_func(bin_cen,*popt),label='fit')
    plt.yscale('log')
    plt.xlim(0,12)
    plt.legend(title=r'$\chi^2 = $' +str(round(chi2,2)))
    plt.xlabel('Times in Microseconds')
    plt.ylabel('Counts')

for f in dec_files:
    plot(f)
    i += 1

#Produce Array with relevant parameters (using pandas for simplicity)
result = np.array([discr,ndecays,taus,t_err,chi2s])
pdindex = ['Discrimination','Decays','Lifetime','Error','Chi Squared']
df = pd.DataFrame(result, index=pdindex)
print(df.to_string())

plt.subplots_adjust(wspace=0.2,hspace=0.5)
plt.show()

