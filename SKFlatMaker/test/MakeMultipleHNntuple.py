import os, sys
import commands as cmd
import argparse

def set_input(this_path, list_files, nTotFiles, nJobs):
  # -- split the input files -- #
  log_path = this_path+'/logs'
  Ntuple_path = this_path+'/Ntuples'
  os.system('mkdir -p '+log_path)
  os.system('mkdir -p '+Ntuple_path)
  nTotFilesPerJobs = int(nTotFiles/nJobs) # q for aq+b
  Remainder = nTotFiles - (nJobs)*(nTotFilesPerJobs) # b = nTotfiles - aq
  if Remainder >= nJobs:
    print "Remainder : "+str(Remainder)+" >= Divisor : "+str(nJobs)+"; Exit."
    sys.exit()

  Ranges = []
  EndOfHalfRanges = 0
  checksum = 0
  for b in range(0, Remainder): # Firstly, run loop (q+1) for b times; aq+b = b(q+1) + (a-b)q.
    Ranges.append(range( b*(nTotFilesPerJobs+1) , (b+1)*(nTotFilesPerJobs+1) ))
    EndOfHalfRanges = (b+1)*(nTotFilesPerJobs+1)
    checksum += len(range( b*(nTotFilesPerJobs+1) , (b+1)*(nTotFilesPerJobs+1) ))

  for aMb in range(0, nJobs-Remainder): # Secondly, run loop q for a-b times.
    Ranges.append(range( EndOfHalfRanges + aMb*(nTotFilesPerJobs) , EndOfHalfRanges + (aMb+1)*(nTotFilesPerJobs) ))
    checksum += len(range( EndOfHalfRanges + aMb*(nTotFilesPerJobs) , EndOfHalfRanges + (aMb+1)*(nTotFilesPerJobs) ))

  if not checksum == nTotFiles:
    print "checksum : "+str(checksum)+" != nTotFiles : "+str(nTotFiles)+"; Exit."
    sys.exit()

  for it_job in range(0, len(Ranges)):
    out = open(log_path+'/input_'+str(it_job)+'.txt', 'w')
    for it_file in Ranges[it_job]:
      out.write(list_files[it_file]+'\n')
    out.close()

# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----

if __name__ == "__main__":

  parser = argparse.ArgumentParser()
  parser.add_argument('-m', '--mode', type=str, default='condor', help='run mode : condor / bash')
  parser.add_argument('-n', '--nJobs', type=int, default=10, help='the number of jobs to run')
  args = parser.parse_args()
 
  nJobs = args.nJobs # a for nTotFiles = aq+b
  
  pwd = os.getcwd() # /data9/Users/jihkim/GeneratorTools/external/CMSSW_10_2_18/src/SKFlatMaker/SKFlatMaker/test FOR NOW.
          
  #channels = ["OS_EE"]
  #channels = ["SS_MuMu","SS_EE","OS_MuMu","OS_EE"]
  channels = ["SS_EMu","OS_EMu"]
  years = [2016, 2017, 2018]
  #years = [2016]
  #masses = [500,1000,1500]
  masses = [2000, 2500]
  names = ["VBFTypeI_NLO_DF","DYTypeI_NLO_DF"]
  #names = ["DYTypeI_NLO_SF"]
  
  try: os.environ["CMSSW_VERSION"]
  except:
    print "Please run this after setting CMSSW. Exiting..."
    sys.exit()
  
  if args.mode == "condor":
    for mass in masses:
      for channel in channels:
        for year in years:
          for name in names:
            print 'Now running : ./MakeHNntuple.sh '+str(name)+' '+str(year)+' '+channel+' '+str(mass)
            this_path = pwd+'/'+name+'_M'+str(mass)+'/'+str(year) # pwd+'/DYTypeI_NLO_SF_M2000/2017'
            list_files = cmd.getoutput('ls '+this_path+'/MiniAOD*.root').split('\n')
            nTotFiles = len(list_files)
            if nJobs > nTotFiles or nJobs == 0:
              nJobs = nTotFiles
            set_input(this_path, list_files, nTotFiles, nJobs)
            for nIter in range(0, nJobs):
              os.system('./MakeHNntuple.sh '+str(name)+' '+str(year)+' '+channel+' '+str(mass)+' '+str(nIter))
              #os.system('echo ./MakeHNntuple.sh '+str(name)+' '+str(year)+' '+channel+' '+str(mass)+' '+str(nIter)) # TEST
  
  elif args.mode == "bash":
    for mass in masses:
      for channel in channels:
        for year in years:
          for name in names:
            print 'Now running : python MakeHNntuple.py '+str(name)+' '+str(year)+' '+channel+' '+str(mass)+' &'
            this_path = pwd+'/'+name+'_M'+str(mass)+'/'+str(year) # pwd+'/DYTypeI_NLO_SF_M2000/2017'
            list_files = cmd.getoutput('ls '+this_path+'/MiniAOD*.root').split('\n')
            nTotFiles = len(list_files)
            if nJobs > nTotFiles or nJobs == 0:
              nJobs = nTotFiles
            set_input(this_path, list_files, nTotFiles, nJobs)
            for nIter in range(0, nJobs):
              os.system('python MakeHNntuple.py '+str(name)+' '+str(year)+' '+channel+' '+str(mass)+' '+str(nIter)+' &')
  
  else:
    print "Illegal run mode:",args.mode,"."
    print "choose condor or bash."
    sys.exit()
