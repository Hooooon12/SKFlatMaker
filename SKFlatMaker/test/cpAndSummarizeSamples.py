import os
from ROOT import *

#masses = [100,300,500,700,1000,1200,1500]
#processes = ['DY','VBF']
#channels = ['OS_EE','OS_MuMu','SS_EE','SS_MuMu']
#years = [2017,2018]
masses = [500,700,1000,1100,1200,1300,1500]
processes = ['VBF']
channels = ['OS_EE','OS_MuMu','SS_EE','SS_MuMu']
years = [2016]

cwd = os.getcwd()

with open('Sch_NLO_XsecEE_BRmultiplied_SS.txt') as f1:
  Sch_xsecs = f1.readlines()
with open('Tch_NLO_XsecEE_BRmultiplied_SS.txt') as f2:
  Tch_xsecs = f2.readlines()

for year in years:
  infoDir = "/data6/Users/jihkim/SKFlatAnalyzer/data/Run2Legacy_v4/"+str(year)+"/Sample/CommonSampleInfo/"
  ForSNUDir = "/data6/Users/jihkim/SKFlatAnalyzer/data/Run2Legacy_v4/"+str(year)+"/Sample/ForSNU/"
  for mass in masses:
    for process in processes:
      for channel in channels:
        name = process+"TypeI_NLO_SF_M"
        filepath = name+str(mass)+"/"+str(year)+"/"+name+str(mass)+"_"+channel+"_"+str(year)+"_Ntuple.root"
        filename = name+str(mass)+"_"+channel+"_"+str(year)+"_Ntuple.root"
        targetDir = "/gv0/DATA/SKFlat/Run2Legacy_v4/"+str(year)+"/PrivateMC/HNtypeI/"+process+"TypeI_"+channel+"_M"+str(mass)
        os.system("mkdir -p "+targetDir)

        if process is 'DY':
          os.system("cp "+filepath+" "+targetDir)

          ####Now prepare info file
          alias = process+"TypeI_"+channel+"_M"+str(mass)
          PD = name+str(mass)+"_"+str(year)
          xsec = ''
          for line in Sch_xsecs:
            if line.split('\t')[0] == str(mass):
              xsec += line.split('\t')[1].strip()
          os.chdir(targetDir)

          ####Then produce the info file
          myfile = TFile.Open(filename)
          mytree = myfile.Get("recoTree/SKFlat")
          weight_SKFlat = 0
          totWeight = 0
          Nevents = mytree.GetEntries()
          for i in range(Nevents):
            mytree.GetEntry(i)
            if mytree.gen_weight > 0.:
              weight_SKFlat = 1
            elif mytree.gen_weight < 0.:
              weight_SKFlat = -1
            totWeight += weight_SKFlat

          print "#### Sample name :",alias,"####"
          print "total events :", mytree.GetEntries()
          print "sum of (sign of) weights :", totWeight

          with open(alias+'.txt','w') as infoFile:
            infoFile.write('# alias PD xsec nmc sumw\n')
            infoFile.write(alias+'\t'+PD+'\t'+xsec+'\t'+str(Nevents)+'\t'+str(totWeight))

          os.system('cp '+alias+'.txt '+infoDir)
          with open(ForSNUDir+alias+'.txt','w') as pathFile:
            pathFile.write(targetDir+"/"+filename)

          os.chdir(cwd)

        if process is 'VBF':
          if mass > 400:
            os.system("cp "+filepath+" "+targetDir)

            ####Now prepare info file
            alias = process+"TypeI_"+channel+"_M"+str(mass)
            PD = name+str(mass)+"_"+str(year)
            xsec = ''
            for line in Tch_xsecs:
              if line.split('\t')[0] == str(mass):
                xsec += line.split('\t')[1].strip()
            os.chdir(targetDir)

            ####Then produce the info file
            myfile = TFile.Open(filename)
            mytree = myfile.Get("recoTree/SKFlat")
            weight_SKFlat = 0
            totWeight = 0
            Nevents = mytree.GetEntries()
            for i in range(Nevents):
              mytree.GetEntry(i)
              if mytree.gen_weight > 0.:
                weight_SKFlat = 1
              elif mytree.gen_weight < 0.:
                weight_SKFlat = -1
              totWeight += weight_SKFlat

            print "#### Sample name :",alias,"####"
            print "total events :", mytree.GetEntries()
            print "sum of (sign of) weights :", totWeight

            with open(alias+'.txt','w') as infoFile:
              infoFile.write('# alias PD xsec nmc sumw\n')
              infoFile.write(alias+'\t'+PD+'\t'+xsec+'\t'+str(Nevents)+'\t'+str(totWeight))

            os.system('cp '+alias+'.txt '+infoDir)
            with open(ForSNUDir+alias+'.txt','w') as pathFile:
              pathFile.write(targetDir+"/"+filename)

            os.chdir(cwd)
