import os

years = [2016, 2017, 2018]
masses = [40, 60, 70, 300, 1000]

for mass in masses:
  os.system('cmsRun RunSKFlatMaker.py year=2018 sampletype=PrivateMC ScaleIDRange=1001,1009 PDFErrorIDRange=1010,1110 PDFAlphaSIDRange=1111,1112 PDFAlphaSScaleValue=0.75,0.75 mass='+str(mass)+' maxEvents=100000 > HeavyMajoranaNeutrino_SSDiLepton_Schannel_NLO_MuMu_M'+str(mass)+'_SKFlatNtuple_2018_MC_numEvent100000.log 2>&1')
