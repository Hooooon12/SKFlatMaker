import os, sys

txtfilename = sys.argv[1]
#txtfilename = '2016_DATA.txt'
#txtfilename = '2016_MC.txt'
#txtfilename = '2017_DATA.txt'
#txtfilename = '2017_MC.txt'
#txtfilename = '2018_DATA.txt'
#txtfilename = '2018_MC.txt'

SKFlatTag = os.environ['SKFlatTag']
SKFlatWD = os.environ['SKFlatWD']

year = "-1"
if "2016" in txtfilename:
  year = "2016"
elif "2017" in txtfilename:
  year = "2017"
elif "2018" in txtfilename:
  year = "2018"
else:
  print "Wrong year from txtfilename : "+txtfilename
  sys.exit()

lines = open(txtfilename).readlines()

str_sample = "DATA"
isData = False
isPrivateMC = False
if ("DATA" in txtfilename) or ("Data" in txtfilename) or ("data" in txtfilename):
  str_sample = "DATA"
  isData = True
  isPrivateMC = False
else:
  str_sample = "MC"
  isData = False
  isPrivateMC = False
if ("Private" in txtfilename) or ("private" in txtfilename):
  str_sample = "PrivateMC"
  isData = False
  isPrivateMC = True

base_dir = SKFlatTag+'/'+year+'/crab_submission_'+str_sample+'/'

os.system('mkdir -p '+base_dir)
os.system('cp '+SKFlatWD+'/SKFlatMaker/test/RunSKFlatMaker.py '+base_dir)

hostname = os.environ['HOSTNAME']

for line in lines:

  if "#" in line:
    continue
  if line.count('/')!=3:
    continue

  line = line.strip('\n')

  #### incase the line contains # of event,
  line = line.split()[0]

  samplePDs = line.split("/")

  #continue if blank line or invalid format
  if len(samplePDs)<4:
    continue
  
  sample = samplePDs[1]
  confs = samplePDs[2]

  #### get extension info
  #### _ext1-v2
  extension = ''
  for w in range(0,len(confs)):
    if confs[w:w+4]=='_ext':
      extension = confs[w:]
      break

  cmd = 'crab submit -c SubmitCrab__'+sample+'__'+confs+'.py'

  #### AD-HOC for 2018 periodD, which has different GT
  if isData and year=="2018" and "Run2018D" in confs and "PromptReco" in confs:
    print "#### 2018 DATA periodD :"+sample+"/"+confs+"/MINIAOD"
    str_sample = "DATA2018Prompt"

  ArgsListString = "['sampletype="+str_sample+"','year="+year+"'"
  # ['sampletype="+str_sample+"','PDFIDShift="+pdfshift+"','PDFOrder="+order+"','PDFType="+gentype+"','year="+year+"']
  if not isData:
    HasFile = os.path.isfile(SKFlatWD+'/SKFlatMaker/script/MCPDFInfo/'+year+'/'+sample+'.txt')

    if HasFile:

      MCInfoLines = open(SKFlatWD+'/SKFlatMaker/script/MCPDFInfo/'+year+'/'+sample+'.txt').readlines()
      words = MCInfoLines[0].split()
      # 1001,1009 gaussian  2001,2100 2101,2102 1.5,1.5
      ScaleIDRange = words[0]
      PDFErrorType = words[1]
      PDFErrorIDRange = words[2]
      PDFAlphaSIDRange = words[3]
      PDFAlphaSScaleValue = words[4]

      #ArgsListString += ",'PDFErrorType="+PDFErrorType+"'"
      ArgsListString += ",'ScaleIDRange="+ScaleIDRange+"'"
      ArgsListString += ",'PDFErrorIDRange="+PDFErrorIDRange+"'"
      ArgsListString += ",'PDFAlphaSIDRange="+PDFAlphaSIDRange+"'"
      ArgsListString += ",'PDFAlphaSScaleValue="+PDFAlphaSScaleValue+"'"

      if "999" in MCInfoLines[0]:
        print '#### Has Issue : '+sample
        #continue

    #### If WR sample
    elif 'WRtoNLtoLLJJ' in sample:
      ArgsListString += ",'ScaleIDRange=1001,1045'"
      ArgsListString += ",'PDFErrorIDRange=1046,1146'"
      ArgsListString += ",'PDFAlphaSIDRange=1147,1148'"
      ArgsListString += ",'PDFAlphaSScaleValue=0.75,0.75'"

    else:
      ### to avoid exit()
      print '#### No MCPDFInfo : '+sample
      #ArgsListString += ",'PDFErrorType="+"hessian"+"'"

  ArgsListString += "]"


  sk_lines = open('skeleton/SubmitCrab.py').readlines()

  outname = base_dir+'/SubmitCrab__'+sample+'__'+confs+'.py'
  out = open(outname,'w')

  for sk_line in sk_lines:
    if "config.General.requestName" in sk_line:
      if isData:
        out.write("config.General.requestName = '"+sample+"__"+confs+"'\n")
      else:
        out.write("config.General.requestName = '"+sample+extension+"'\n")
    elif "config.JobType.pyCfgParams" in sk_line:
      out.write("config.JobType.pyCfgParams = "+ArgsListString+"\n")
    elif "config.Data.inputDataset" in sk_line:
      out.write("config.Data.inputDataset = '"+line+"'\n")
      if isPrivateMC:
        out.write("config.Data.inputDBS = 'phys03'\n")
        out.write("config.Data.ignoreLocality = True\n")
        out.write("config.Site.whitelist = ['T2*']\n")

    elif 'config.Data.splitting' in sk_line:
      if isData:
        out.write("config.Data.splitting = 'LumiBased'\n")
      else:
        out.write("config.Data.splitting = 'FileBased'\n")
    elif 'config.Data.unitsPerJob' in sk_line:
      if isData:
        out.write("config.Data.unitsPerJob = 50\n")
      else:
        out.write("config.Data.unitsPerJob = 1\n")
    elif 'config.Data.outputDatasetTag' in sk_line:
      if isData:
        period = ""
        if year+"A" in confs:
          period = "A"
        elif year+"B" in confs:
          period = "B"
          if year=="2016":
            if "ver1" in confs:
              period = "B_ver1"
            if "ver2" in confs:
              period = "B_ver2"
        elif year+"C" in confs:
          period = "C"
        elif year+"D" in confs:
          period = "D"
        elif year+"E" in confs:
          period = "E"
        elif year+"F" in confs:
          period = "F"
        elif year+"G" in confs:
          period = "G"
        elif year+"H" in confs:
          period = "H"

        out.write("config.Data.outputDatasetTag = 'SKFlat_"+SKFlatTag+"_period"+period+"'\n")
      else:
        out.write("config.Data.outputDatasetTag = 'SKFlat_"+SKFlatTag+"'\n")

    elif 'config.Data.outLFNDirBase' in sk_line:
      out.write("config.Data.outLFNDirBase = '/store/user/%s/SKFlat/"+year+"/' % (getUsernameFromSiteDB())\n")

    elif 'config.Site.storageSite' in sk_line:
      #if isPrivateMC:
      #  out.write("config.Site.storageSite = 'T2_KR_KNU'\n")
      #else:
      #  out.write("config.Site.storageSite = 'T3_KR_KISTI'\n")
      out.write("config.Site.storageSite = 'T2_KR_KNU'\n")
    else:
      out.write(sk_line)

  if isData:
    if year=="2016":
      #### https://hypernews.cern.ch/HyperNews/CMS/get/physics-validation/3358.html
      out.write("config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/ReReco/Final/Cert_271036-284044_13TeV_ReReco_07Aug2017_Collisions16_JSON.txt'\n")
    elif year=="2017":
      out.write("config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/ReReco/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON.txt'\n")
    elif year=="2018":
      out.write("config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/ReReco/Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt'\n")
    else:
      print "Wrong year : "+year

  print cmd

  out.close()
