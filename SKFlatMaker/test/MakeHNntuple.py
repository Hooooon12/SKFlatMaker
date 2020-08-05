import os
import commands as cmd

#channels = ["MuMu","EE","MuE","EMu"]
channels = ["MuMu"]
#years = [2016, 2017, 2018]
years = [2016]
masses = [20]

cwd = os.getcwd()

for mass in masses:
  for channel in channels:
    name = 'HeavyMajoranaNeutrinoToDiLepton_Schannel_NLO_{0}_M{1}'.format(channel, mass)
    for year in years:
      runningDir = cwd+'/'+name+'/'+str(year)
      os.system('cp HNtype1_RunSKFlatMaker.py '+runningDir)
      os.chdir(runningDir)
      print 'I\'m here:'
      print cmd.getoutput('pwd')
      print 'Now running:'
      print 'cmsRun HNtype1_RunSKFlatMaker.py year='+str(year)+' sampletype=PrivateMC ScaleIDRange=1001,1009 PDFErrorIDRange=1010,1110 PDFAlphaSIDRange=1111,1112 PDFAlphaSScaleValue=0.75,0.75 name='+name+' > '+name+'_'+str(year)+'_Ntuple.log 2>&1'
      os.system('cmsRun HNtype1_RunSKFlatMaker.py year='+str(year)+' sampletype=PrivateMC ScaleIDRange=1001,1009 PDFErrorIDRange=1010,1110 PDFAlphaSIDRange=1111,1112 PDFAlphaSScaleValue=0.75,0.75 name='+name+' > '+name+'_'+str(year)+'_Ntuple.log 2>&1')
      os.chdir(cwd)
      print 'Returned to:'
      print cmd.getoutput('pwd')
