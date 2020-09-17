import os, sys
import commands as cmd

#channels = ["MuMu","EE","MuE","EMu"]
channels = ["SF"]
#years = [2016, 2017, 2018]
years = [2018]
Nfiles = 100
masses = [700]
#names = ["VBFTypeI_NLO_","DYTypeI_NLO_"]
names = ["DYTypeI_NLO_"]

try: os.environ["CMSSW_VERSION"]
except:
  print "Please run this after setting CMSSW. Exiting..."
  sys.exit()

for mass in masses:
  for channel in channels:
    for year in years:
      for name in names:
        os.system('python MakeHNntuple.py '+str(name)+' '+str(year)+' '+channel+' '+str(mass)+' '+str(Nfiles)+' &')

