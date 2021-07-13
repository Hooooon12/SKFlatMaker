#!/bin/bash

if [ -z "$1" -o -z "$2" ]
then
    echo "usage: $0 name year channel mass"
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
nIter=$5

#baseDir=/data9/Users/jihkim/GeneratorTools/external/CMSSW_10_2_18/src/SKFlatMaker/SKFlatMaker/test
baseDir=`pwd`
name=${name}_M${mass}
#runningDir=${baseDir}/${name}/${year} #JH : directory that contains MiniAODs.. can be modified
runningDir=${baseDir}/${name}/${year}/logs
cp -n ${baseDir}/HNtype1_RunSKFlatMaker.py $runningDir #JH : Be careful when the HNtypeI_RunSKFlatMaker.py file is updated. The change will NOT propagate.

cd $runningDir

SCRIPT=MakeHNntuple_${name}_${channel}_${year}_${nIter}.sh
echo "#!/bin/bash" > $SCRIPT

echo cd $runningDir >> $SCRIPT
echo "echo I\'m here:" >> $SCRIPT
echo pwd >> $SCRIPT
echo >> $SCRIPT
echo echo Now running: >> $SCRIPT
echo >> $SCRIPT
echo "if [[ \"$name\" == *\"DY\"* ]];" >> $SCRIPT
echo then >> $SCRIPT
echo "    echo cmsRun HNtype1_RunSKFlatMaker.py year=${year} sampletype=PrivateMC ScaleIDRange=1001,1009 PDFErrorIDRange=1010,1110 PDFAlphaSIDRange=1111,1112 PDFAlphaSScaleValue=0.75,0.75 name=${name} channel=${channel} nIter=${nIter} \> ${name}_${channel}_${year}_Ntuple_${nIter}.log 2\>\&1" >> $SCRIPT
echo "    cmsRun HNtype1_RunSKFlatMaker.py year=${year} sampletype=PrivateMC ScaleIDRange=1001,1009 PDFErrorIDRange=1010,1110 PDFAlphaSIDRange=1111,1112 PDFAlphaSScaleValue=0.75,0.75 name=${name} channel=${channel} nIter=${nIter} > ${name}_${channel}_${year}_Ntuple_${nIter}.log 2>&1 #JH : for Schannel pdf systematics" >> $SCRIPT
echo >> $SCRIPT
echo "elif [[ \"$name\" == *\"VBF\"* ]];" >> $SCRIPT
echo then >> $SCRIPT
echo "    echo cmsRun HNtype1_RunSKFlatMaker.py year=${year} sampletype=PrivateMC ScaleIDRange=1001,1009 PDFErrorIDRange=1010,1110 name=${name} channel=${channel} nIter=${nIter} \> ${name}_${channel}_${year}_Ntuple_${nIter}.log 2\>\&1" >> $SCRIPT
echo "    cmsRun HNtype1_RunSKFlatMaker.py year=${year} sampletype=PrivateMC ScaleIDRange=1001,1009 PDFErrorIDRange=1010,1110 name=${name} channel=${channel} nIter=${nIter} > ${name}_${channel}_${year}_Ntuple_${nIter}.log 2>&1 #JH : for Tchannel pdf systematics" >> $SCRIPT
echo fi >> $SCRIPT

chmod +x $SCRIPT

condor_submit -batch-name ${name}_${channel}_${year}_Ntuple << EOF
executable = $SCRIPT
universe = vanilla
log = MakeHNntuple_${name}_${channel}_${year}_log_${nIter}.txt
output = MakeHNntuple_${name}_${channel}_${year}_out_${nIter}.txt
error = MakeHNntuple_${name}_${channel}_${year}_error_${nIter}.txt
getenv = True
#request_cpus = 10
#request_memory = 8G
accounting_group = group_cms
should_transfer_files = YES
when_to_transfer_output = ON_EXIT
queue
EOF

