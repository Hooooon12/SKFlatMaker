#!/bin/bash

if [ -z "$1" -o -z "$2" ]
then
    echo "usage: $0 name year channel mass Nfiles"
    echo "example: $0 DYTypeI_NLO_SF 2018 SS_MuMu 100 100"
    exit 1
fi

if [ -z $CMSSW_VERSION ]
then
    echo No CMSSW. Exiting...
    exit 1
fi 

name=$1
year=$2
channel=$3
mass=$4
Nfiles=$5

baseDir=/data8/Users/jihkim/GeneratorTools/external/CMSSW_10_2_18/src/SKFlatMaker/SKFlatMaker/test
name=${name}_M${mass}
runningDir=${baseDir}/${name}/${year} #JH : directory that contains MiniAODs.. can be modified
cp -n ${baseDir}/HNtype1_RunSKFlatMaker.py $runningDir #JH : prevent overwriting

cd $runningDir

SCRIPT=MakeHNntuple_${name}_${channel}_${year}.sh
echo "#!/bin/bash" > $SCRIPT

echo cd $runningDir >> $SCRIPT
echo "echo I\'m here:" >> $SCRIPT
echo pwd >> $SCRIPT
echo >> $SCRIPT
echo echo Now running: >> $SCRIPT
echo >> $SCRIPT
echo "if [[ \"$name\" == *\"DY\"* ]];" >> $SCRIPT
echo then >> $SCRIPT
echo "    echo cmsRun HNtype1_RunSKFlatMaker.py year=${year} Nfiles=${Nfiles} sampletype=PrivateMC ScaleIDRange=1001,1009 PDFErrorIDRange=1010,1110 PDFAlphaSIDRange=1111,1112 PDFAlphaSScaleValue=0.75,0.75 name=${name} channel=${channel} \> ${name}_${channel}_${year}_Ntuple.log 2\>\&1" >> $SCRIPT
echo "    cmsRun HNtype1_RunSKFlatMaker.py year=${year} Nfiles=${Nfiles} sampletype=PrivateMC ScaleIDRange=1001,1009 PDFErrorIDRange=1010,1110 PDFAlphaSIDRange=1111,1112 PDFAlphaSScaleValue=0.75,0.75 name=${name} channel=${channel} > ${name}_${channel}_${year}_Ntuple.log 2>&1 #JH : for Schannel pdf systematics" >> $SCRIPT
echo >> $SCRIPT
echo "elif [[ \"$name\" == *\"VBF\"* ]];" >> $SCRIPT
echo then >> $SCRIPT
echo "    echo cmsRun HNtype1_RunSKFlatMaker.py year=${year} Nfiles=${Nfiles} sampletype=PrivateMC ScaleIDRange=1001,1009 PDFErrorIDRange=1010,1110 name=${name} channel=${channel} \> ${name}_${channel}_${year}_Ntuple.log 2\>\&1" >> $SCRIPT
echo "    cmsRun HNtype1_RunSKFlatMaker.py year=${year} Nfiles=${Nfiles} sampletype=PrivateMC ScaleIDRange=1001,1009 PDFErrorIDRange=1010,1110 name=${name} channel=${channel} > ${name}_${channel}_${year}_Ntuple.log 2>&1 #JH : for Tchannel pdf systematics" >> $SCRIPT
echo fi >> $SCRIPT

chmod +x $SCRIPT

condor_submit -batch-name ${name}_${channel}_${year}_Ntuple << EOF
executable = $SCRIPT
universe = vanilla
log = MakeHNntuple_${name}_${channel}_${year}_log.txt
output = MakeHNntuple_${name}_${channel}_${year}_out.txt
error = MakeHNntuple_${name}_${channel}_${year}_error.txt
getenv = True
request_cpus = 10
accounting_group = group_cms
should_transfer_files = YES
when_to_transfer_output = ON_EXIT
queue
EOF

