#!/bin/bash

if [ -z "$1" -o -z "$2" -o -z "$3" ]
then
    echo "usage: $0 name year index"
    echo "example: $0 DYTypeI_NLO_SF 2018 6"
    exit 1
fi

if [ -z $CMSSW_VERSION ]
then
    echo No CMSSW. Exiting...
    exit 1
fi 

name=$1
year=$2
index=$3

baseDir=/data9/Users/jihkim/GeneratorTools/external/CMSSW_10_2_18/src/SKFlatMaker/SKFlatMaker/test
name=${name}
#runningDir=${baseDir}/ttHTobb_M125/${year} #JH : directory where the Ntuples will be stored
runningDir=${baseDir} #JH : directory where the Ntuples will be stored
#cp /tmp/x509up_u5565 $runningDir
#cp -n ${baseDir}/ttHTobb_RunSKFlatMaker.py $runningDir

cd $runningDir

SCRIPT=MakeTestNtuple_${index}_${year}.sh
echo "#!/bin/bash" > $SCRIPT

echo cd $runningDir >> $SCRIPT
echo "echo I\'m here:" >> $SCRIPT
echo pwd >> $SCRIPT
echo >> $SCRIPT
echo "echo ls \/tmp\/:" >> $SCRIPT
echo ls /tmp/ >> $SCRIPT
#echo "cp \"x509up_u\"* \"/tmp/x509up_u\"`id -u`" >> $SCRIPT
echo >> $SCRIPT
echo echo Now running: >> $SCRIPT
echo >> $SCRIPT
#echo "echo cmsRun ttHTobb_RunSKFlatMaker.py year=${year} sampletype=MC name=${name} index=${index} \> ${index}_${year}_Ntuple.log 2\>\&1" >> $SCRIPT
#echo "cmsRun ttHTobb_RunSKFlatMaker.py year=${year} sampletype=MC name=${name} index=${index} > ${index}_${year}_Ntuple.log 2>&1" >> $SCRIPT
echo "echo cmsRun Test_RunSKFlatMaker.py year=${year} sampletype=PrivateMC name=${name} \> ${name}_${year}_${index}_Ntuple.log 2\>\&1" >> $SCRIPT
echo "cmsRun Test_RunSKFlatMaker.py year=${year} sampletype=PrivateMC name=${name} > ${name}_${year}_${index}_Ntuple.log 2>&1" >> $SCRIPT
echo >> $SCRIPT

chmod +x $SCRIPT

condor_submit -batch-name TestNtuple_${year} << EOF
executable = $SCRIPT
universe = vanilla
log = MakeTestNtuple_${name}_${year}_${index}_log.txt
output = MakeTestNtuple_${name}_${year}_${index}_out.txt
error = MakeTestNtuple_${name}_${year}_${index}_error.txt
getenv = True
request_cpus = 10
request_memory = 8G
accounting_group = group_cms
should_transfer_files = YES
when_to_transfer_output = ON_EXIT
#concurrency_limits = n50.jihkim
queue
EOF

