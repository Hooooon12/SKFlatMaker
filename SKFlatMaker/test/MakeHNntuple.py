import os, sys
import commands as cmd

def makeNtuple(name, year, channel, mass):
  cwd = os.getcwd()
  name = name+'_M'+str(mass)
  runningDir = cwd+'/'+name+'/'+str(year) #JH : directory that contains MiniAODs.. can be modified
  os.system('cp -n HNtype1_RunSKFlatMaker.py '+runningDir)
  os.chdir(runningDir)
  print 'I\'m here:'
  print cmd.getoutput('pwd')
  print 'Now running:'
  if 'DY' in name:
    print 'cmsRun HNtype1_RunSKFlatMaker.py year='+str(year)+' sampletype=PrivateMC ScaleIDRange=1001,1009 PDFErrorIDRange=1010,1110 PDFAlphaSIDRange=1111,1112 PDFAlphaSScaleValue=0.75,0.75 name='+name+' channel='+channel+' > '+name+'_'+channel+'_'+str(year)+'_Ntuple.log 2>&1'
    os.system('cmsRun HNtype1_RunSKFlatMaker.py year='+str(year)+' sampletype=PrivateMC ScaleIDRange=1001,1009 PDFErrorIDRange=1010,1110 PDFAlphaSIDRange=1111,1112 PDFAlphaSScaleValue=0.75,0.75 name='+name+' channel='+channel+' > '+name+'_'+channel+'_'+str(year)+'_Ntuple.log 2>&1') #JH : for Schannel pdf systematics
  elif 'VBF' in name:
    print 'cmsRun HNtype1_RunSKFlatMaker.py year='+str(year)+' sampletype=PrivateMC ScaleIDRange=1001,1009 PDFErrorIDRange=1010,1110 name='+name+' channel='+channel+' > '+name+'_'+channel+'_'+str(year)+'_Ntuple.log 2>&1'
    os.system('cmsRun HNtype1_RunSKFlatMaker.py year='+str(year)+' sampletype=PrivateMC ScaleIDRange=1001,1009 PDFErrorIDRange=1010,1110 name='+name+' channel='+channel+' > '+name+'_'+channel+'_'+str(year)+'_Ntuple.log 2>&1') #JH : for Tchannel pdf systematics
  os.chdir(cwd)
  print 'Returned to:'
  print cmd.getoutput('pwd')
  return
 
name = sys.argv[1]
year = sys.argv[2]
channel = sys.argv[3]
mass = sys.argv[4]

makeNtuple(name, year, channel, mass)
