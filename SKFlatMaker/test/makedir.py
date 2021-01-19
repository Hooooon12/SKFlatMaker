###Run this at /gv0/DATA/SKFlat/Run2Legacy_v4/<YEAR>/PrivateMC/HNtypeI

import os

masses = [200,500,1000,1500]
processes = ['DY','VBF']
#processes = ['VBF']
#channels = ['OS_EE','OS_MuMu','SS_EE','SS_MuMu']
channels = ['NLO_DF']
years = ['2016','2017','2018']

for year in years:
  for mass in masses:
    for process in processes:
      for channel in channels:
        if process is 'DY':
          os.system("mkdir -p "+process+"TypeI_"+channel+"_M"+str(mass)+"/"+year)
        if process is 'VBF':
          if mass > 400:
            os.system("mkdir -p "+process+"TypeI_"+channel+"_M"+str(mass)+"/"+year)
