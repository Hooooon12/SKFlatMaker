import os, sys
import commands as cmd

#channels = ["MuMu","EE","MuE","EMu"]
#channels = ["SS_MuMu","SS_EE"]
channels = ["OS_MuMu","OS_EE"]
#years = [2016, 2017, 2018]
years = [2018]
Nfiles = 100
masses = [500,700]
#names = ["VBFTypeI_NLO_SF_","DYTypeI_NLO_SF_"]
names = ["DYTypeI_NLO_SF_"]

try: os.environ["CMSSW_VERSION"]
except:
  print "Please run this after setting CMSSW. Exiting..."
  sys.exit()

for mass in masses:
  for channel in channels:
    for year in years:
      for name in names:
        os.system('python MakeHNntuple.py '+str(name)+' '+str(year)+' '+channel+' '+str(mass)+' '+str(Nfiles)+' &')

