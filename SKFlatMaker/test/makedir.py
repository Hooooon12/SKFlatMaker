###Run this at /gv0/DATA/SKFlat/Run2Legacy_v4/<YEAR>/PrivateMC/HNtypeI

import os

masses = [100,300,500,700,1000,1200,1500]
processes = ['DY','VBF']
channels = ['OS_EE','OS_MuMu','SS_EE','SS_MuMu']


for mass in masses:
  for process in processes:
    for channel in channels:
      if process is 'DY':
        os.system("mkdir -p "+process+"TypeI_"+channel+"_M"+str(mass))
      if process is 'VBF':
        if mass > 300:
          os.system("mkdir -p "+process+"TypeI_"+channel+"_M"+str(mass))
