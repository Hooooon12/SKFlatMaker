import os
import subprocess

lines = open('ToCheck.txt').readlines()

mydas = '/cvmfs/cms.cern.ch/common/dasgoclient '

for line in lines:

  line = line.strip('\n')

  if "#" in line:
    continue

  alias = line.split('/')[1].replace('*','XXX')

  filename_samplelist = 'samples_'+alias+'.txt'
  os.system(mydas+'--query="dataset='+line+'" > tmp_'+filename_samplelist)

  resultfile = open(filename_samplelist,'w')

  samples = open('tmp_'+filename_samplelist).readlines()

  for sample in samples:

    sample = sample.strip('\n')

    #print sample
    cmd = mydas+'''--query="summary dataset='''+sample+'''" | sed 's,\\"nevents\\":,\\nHERE,g' | grep "HERE" | sed 's,\,,\\n,g' | head -1 | sed 's,HERE,,'''+"g'"

    result = subprocess.check_output(cmd, shell=True).strip('\n')
    print sample+'\t'+result
    resultfile.write(sample+'\t'+result+'\n')
  resultfile.close()
  os.system('rm tmp_'+filename_samplelist)
