import os, sys
import commands as cmd
import argparse
from datetime import datetime

today = datetime.today()
timestamp = today.strftime("%Y%m%d")+"__"+today.strftime("%H%M%S")

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--mode', type=str, default='condor', help='run mode : condor / bash')
args = parser.parse_args()

#years = [2016, 2017, 2018]
years = [2017]
names = []

try: os.environ["CMSSW_VERSION"]
except:
  print "Please run this after setting CMSSW. Exiting..."
  sys.exit()

if args.mode == "condor":
  for year in years:
    if year == 2016:
      names = cmd.getoutput("dasgoclient -query=\"file dataset=/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM\"")
    if year == 2017:
      names = cmd.getoutput("dasgoclient -query=\"file dataset=/ttHTobb_M125_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM\"")
    if year == 2018:
      print "2018 not supported yet."
      sys.exit()

    with open("/data9/Users/jihkim/GeneratorTools/external/CMSSW_10_2_18/src/SKFlatMaker/SKFlatMaker/test/ttHTobb_M125/"+str(year)+"/filelist_"+timestamp+".txt",'w') as f:
      f.write(names)

    names = names.split('\n')

    #print year, "samples:"
    #print names
    #for i in range(50):
    #  print 'Now running : ./MakeTestNtuple.sh '+names[i]+' '+str(year)+' '+str(i)
    #  os.system('./MakeTestNtuple.sh '+names[i]+' '+str(year)+' '+str(i)) #JH : To run files in a range
    for i in range(len(names)):
      print 'Now running : ./MakeTestNtuple.sh '+names[i]+' '+str(year)+' '+str(i)
      os.system('./MakeTestNtuple.sh '+names[i]+' '+str(year)+' '+str(i))
    #print 'Now running : ./MakeTestNtuple.sh '+names[0]+' '+str(year)+' '+str(0)
    #os.system('./MakeTestNtuple.sh '+names[0]+' '+str(year)+' '+str(0)) #JH : To run single file

#elif args.mode == "bash":
#  for mass in masses:
#    for channel in channels:
#      for year in years:
#        for name in names:
#          workArea = name+'_M'+str(mass)+'/'+str(year)
#          print 'Now running : python MakeHNntuple.py '+str(name)+' '+str(year)+' '+channel+' '+str(mass)+' &'
#          os.system('python MakeHNntuple.py '+str(name)+' '+str(year)+' '+channel+' '+str(mass)+' &')

else:
  print "Illegal run mode:",args.mode,"."
  print "choose condor or bash."
  sys.exit()
