import os
from ROOT import *

#masses = [100,300,500,700,1000,1200,1500]
#processes = ['DY','VBF']
#channels = ['OS_EE','OS_MuMu','SS_EE','SS_MuMu']
#years = [2017,2018]
masses = [200,500,1000,1500]
processes = ['DY','VBF']
channels = ['OS_EMu','SS_EMu']
years = [2016]

cwd = os.getcwd()

with open('Sch_NLO_XsecEE_BRmultiplied_SS.txt') as f1:
  Sch_xsecs_SF = f1.readlines()
with open('Tch_NLO_XsecEE_BRmultiplied_SS.txt') as f2:
  Tch_xsecs_SF = f2.readlines()
with open('Sch_NLO_XsecEE_BRmultiplied.txt') as f3: #JH : EMu(emu+mue) channel bare xsec = 2*EE(MuMu).
  Sch_xsecs_DF = f3.readlines()
with open('Tch_NLO_XsecEE_BRmultiplied.txt') as f4:
  Tch_xsecs_DF = f4.readlines()

for year in years:
  infoDir = "/data6/Users/jihkim/SKFlatAnalyzer/data/Run2Legacy_v4/"+str(year)+"/Sample/CommonSampleInfo/"
  ForSNUDir = "/data6/Users/jihkim/SKFlatAnalyzer/data/Run2Legacy_v4/"+str(year)+"/Sample/ForSNU/"
  infoDir_public = "/data8/Users/jihkim_public/SampleInfo/"+str(year)+"/CommonSampleInfo/"
  ForSNUDir_public = "/data8/Users/jihkim_public/SampleInfo/"+str(year)+"/ForSNU/"
  for mass in masses:
    for process in processes:
      for channel in channels:
        if 'EMu' in channel:
          name = process+"TypeI_NLO_DF_M"
          Sch_xsecs = Sch_xsecs_DF
          Tch_xsecs = Tch_xsecs_DF
        else:
          name = process+"TypeI_NLO_SF_M"
          Sch_xsecs = Sch_xsecs_SF
          Tch_xsecs = Tch_xsecs_SF
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

          with open(infoDir+alias+'.txt','w') as infoFile:
            infoFile.write('# alias PD xsec nmc sumw\n')
            infoFile.write(alias+'\t'+PD+'\t'+xsec+'\t'+str(Nevents)+'\t'+str(totWeight))
          os.system('cp '+infoDir+alias+'.txt '+infoDir_public)

          with open(ForSNUDir+alias+'.txt','w') as pathFile:
            pathFile.write(targetDir+"/"+filename)
          os.system('cp '+ForSNUDir+alias+'.txt '+ForSNUDir_public)

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

            with open(infoDir+alias+'.txt','w') as infoFile:
              infoFile.write('# alias PD xsec nmc sumw\n')
              infoFile.write(alias+'\t'+PD+'\t'+xsec+'\t'+str(Nevents)+'\t'+str(totWeight))
            os.system('cp '+infoDir+alias+'.txt '+infoDir_public)

            with open(ForSNUDir+alias+'.txt','w') as pathFile:
              pathFile.write(targetDir+"/"+filename)
            os.system('cp '+ForSNUDir+alias+'.txt '+ForSNUDir_public)

            os.chdir(cwd)
