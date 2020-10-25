import os, sys
import commands as cmd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--mode', type=str, default='condor', help='run mode : condor / bash')
args = parser.parse_args()

#channels = ["OS_EE"]
channels = ["SS_MuMu","SS_EE","OS_MuMu","OS_EE"]
#years = [2016, 2017, 2018]
years = [2018]
#Nfiles = 100
Nfiles = 98
#masses = [1000,1200,1500]
masses = [300]
#names = ["VBFTypeI_NLO_SF","DYTypeI_NLO_SF"]
names = ["DYTypeI_NLO_SF"]

try: os.environ["CMSSW_VERSION"]
except:
  print "Please run this after setting CMSSW. Exiting..."
  sys.exit()

if args.mode == "condor":
  for mass in masses:
    for channel in channels:
      for year in years:
        for name in names:
          os.system('./MakeHNntuple.sh '+str(name)+' '+str(year)+' '+channel+' '+str(mass)+' '+str(Nfiles))

elif args.mode == "bash":
  for mass in masses:
    for channel in channels:
      for year in years:
        for name in names:
          os.system('python MakeHNntuple.py '+str(name)+' '+str(year)+' '+channel+' '+str(mass)+' '+str(Nfiles)+' &')

else:
  print "Illegal run mode:",args.mode,"."
  print "choose condor or bash."
  sys.exit()
