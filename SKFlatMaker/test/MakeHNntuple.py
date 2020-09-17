import os, sys
import commands as cmd

##channels = ["MuMu","EE","MuE","EMu"]
#channels = ["SF"]
##years = [2016, 2017, 2018]
#years = [2018]
#Nfiles = 100
#masses = [500]
##names = ["VBFTypeI_NLO_","DYTypeI_NLO_"]
#names = ["DYTypeI_NLO_"]

def makeNtuple(name, year, channel, mass, Nfiles):
  cwd = os.getcwd()
  name = name+'{0}_M{1}'.format(channel, mass)
  runningDir = cwd+'/'+name+'/'+str(year)
  os.system('cp HNtype1_RunSKFlatMaker.py '+runningDir)
  os.chdir(runningDir)
  print 'I\'m here:'
  print cmd.getoutput('pwd')
  print 'Now running:'
  if 'DY' in name:
    print 'cmsRun HNtype1_RunSKFlatMaker.py year='+str(year)+' Nfiles='+str(Nfiles)+' sampletype=PrivateMC ScaleIDRange=1001,1009 PDFErrorIDRange=1010,1110 PDFAlphaSIDRange=1111,1112 PDFAlphaSScaleValue=0.75,0.75 name='+name+' > '+name+'_'+str(year)+'_Ntuple.log 2>&1'
    os.system('cmsRun HNtype1_RunSKFlatMaker.py year='+str(year)+' Nfiles='+str(Nfiles)+' sampletype=PrivateMC ScaleIDRange=1001,1009 PDFErrorIDRange=1010,1110 PDFAlphaSIDRange=1111,1112 PDFAlphaSScaleValue=0.75,0.75 name='+name+' > '+name+'_'+str(year)+'_Ntuple.log 2>&1') #JH : for Schannel pdf systematics
  elif 'VBF' in name:
    print 'cmsRun HNtype1_RunSKFlatMaker.py year='+str(year)+' Nfiles='+str(Nfiles)+' sampletype=PrivateMC name='+name+' > '+name+'_'+str(year)+'_Ntuple.log 2>&1'
    os.system('cmsRun HNtype1_RunSKFlatMaker.py year='+str(year)+' Nfiles='+str(Nfiles)+' sampletype=PrivateMC name='+name+' > '+name+'_'+str(year)+'_Ntuple.log 2>&1') #JH : for Tchannel pdf systematics
  os.chdir(cwd)
  print 'Returned to:'
  print cmd.getoutput('pwd')
  return
 
name = sys.argv[1]
year = sys.argv[2]
channel = sys.argv[3]
mass = sys.argv[4]
Nfiles = sys.argv[5]

makeNtuple(name, year, channel, mass, Nfiles)

#for mass in masses:
#  for channel in channels:
#    for year in years:
#      for name in names:
#        makeNtuple(name, year, channel, mass, Nfiles)





#for mass in masses:
#  for channel in channels:
#    #name = 'HeavyMajoranaNeutrinoToDiLepton_Schannel_NLO_{0}_M{1}'.format(channel, mass)
#    name = 'HeavyMajoranaNeutrinoToDiLepton_Tchannel_NLO_{0}_M{1}'.format(channel, mass)
#    for year in years:
#      runningDir = cwd+'/'+name+'/'+str(year)
#      os.system('cp HNtype1_RunSKFlatMaker.py '+runningDir)
#      os.chdir(runningDir)
#      print 'I\'m here:'
#      print cmd.getoutput('pwd')
#      print 'Now running:'
#      #print 'cmsRun HNtype1_RunSKFlatMaker.py year='+str(year)+' sampletype=PrivateMC ScaleIDRange=1001,1009 PDFErrorIDRange=1010,1110 PDFAlphaSIDRange=1111,1112 PDFAlphaSScaleValue=0.75,0.75 name='+name+' > '+name+'_'+str(year)+'_Ntuple.log 2>&1'
#      #os.system('cmsRun HNtype1_RunSKFlatMaker.py year='+str(year)+' sampletype=PrivateMC ScaleIDRange=1001,1009 PDFErrorIDRange=1010,1110 PDFAlphaSIDRange=1111,1112 PDFAlphaSScaleValue=0.75,0.75 name='+name+' > '+name+'_'+str(year)+'_Ntuple.log 2>&1') #JH : for Schannel pdf systematics
#      print 'cmsRun HNtype1_RunSKFlatMaker.py year='+str(year)+' sampletype=PrivateMC name='+name+' > '+name+'_'+str(year)+'_Ntuple.log 2>&1'
#      os.system('cmsRun HNtype1_RunSKFlatMaker.py year='+str(year)+' sampletype=PrivateMC name='+name+' > '+name+'_'+str(year)+'_Ntuple.log 2>&1') #JH : for Tchannel pdf systematics
#      os.chdir(cwd)
#      print 'Returned to:'
#      print cmd.getoutput('pwd')
