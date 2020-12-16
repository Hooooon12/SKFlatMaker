{
TFile *file1 = TFile::Open("DYTypeI_NLO_SF_M1500/2016/DYTypeI_NLO_SF_M1500_OS_EE_2016_Ntuple.root");
TFile *file2 = TFile::Open("DYTypeI_NLO_SF_M1500/2016/DYTypeI_NLO_SF_M1500_OS_MuMu_2016_Ntuple.root");
TFile *file3 = TFile::Open("DYTypeI_NLO_SF_M1500/2016/DYTypeI_NLO_SF_M1500_SS_EE_2016_Ntuple.root");
TFile *file4 = TFile::Open("DYTypeI_NLO_SF_M1500/2016/DYTypeI_NLO_SF_M1500_SS_MuMu_2016_Ntuple.root");
TTree *tree1 = (TTree*)file1->Get("recoTree/SKFlat");
TTree *tree2 = (TTree*)file2->Get("recoTree/SKFlat");
TTree *tree3 = (TTree*)file3->Get("recoTree/SKFlat");
TTree *tree4 = (TTree*)file4->Get("recoTree/SKFlat");
vector<int> *LHE_ID_1;
vector<int> *LHE_ID_2;
vector<int> *LHE_ID_3;
vector<int> *LHE_ID_4;
tree1->SetBranchAddress("LHE_ID",&LHE_ID_1);
tree2->SetBranchAddress("LHE_ID",&LHE_ID_2);
tree3->SetBranchAddress("LHE_ID",&LHE_ID_3);
tree4->SetBranchAddress("LHE_ID",&LHE_ID_4);
int events = tree1->GetEntries();
cout << "//OS_EE//" << endl;
for(int i=0; i<events; i++){
	int isSS = 1;
  tree1->GetEntry(i);
  if(i%1000==0) cout << "==========" << i << "th event==========" << endl;
	for(unsigned int j=0; j<LHE_ID_1->size(); j++){
    //cout << j << "th particle PID : " << LHE_ID_1->at(j) << endl;
		if(LHE_ID_1->at(j)==11) isSS*=-1;
		if(LHE_ID_1->at(j)==-11) isSS*=1;
		if(abs(LHE_ID_1->at(j))==13) return;
	}
	if(isSS!=-1) return;
}
events = tree2->GetEntries();
cout << "//OS_MuMu//" << endl;
for(int i=0; i<events; i++){
	int isSS = 1;
  tree2->GetEntry(i);
  if(i%1000==0) cout << "==========" << i << "th event==========" << endl;
	for(unsigned int j=0; j<LHE_ID_2->size(); j++){
    //cout << j << "th particle PID : " << LHE_ID_2->at(j) << endl;
		if(LHE_ID_2->at(j)==13) isSS*=-1;
		if(LHE_ID_2->at(j)==-13) isSS*=1;
		if(abs(LHE_ID_2->at(j))==11) return;
	}
	if(isSS!=-1) return;
}
events = tree3->GetEntries();
cout << "//SS_EE//" << endl;
for(int i=0; i<events; i++){
	int isSS = 1;
  tree3->GetEntry(i);
  if(i%1000==0) cout << "==========" << i << "th event==========" << endl;
	for(unsigned int j=0; j<LHE_ID_3->size(); j++){
    //cout << j << "th particle PID : " << LHE_ID_3->at(j) << endl;
		if(LHE_ID_3->at(j)==11) isSS*=-1;
		if(LHE_ID_3->at(j)==-11) isSS*=1;
		if(abs(LHE_ID_3->at(j))==13) return;
	}
	if(isSS!=1) return;
}
events = tree4->GetEntries();
cout << "//SS_MuMu//" << endl;
for(int i=0; i<events; i++){
	int isSS = 1;
  tree4->GetEntry(i);
  if(i%1000==0) cout << "==========" << i << "th event==========" << endl;
	for(unsigned int j=0; j<LHE_ID_4->size(); j++){
    //cout << j << "th particle PID : " << LHE_ID_4->at(j) << endl;
		if(LHE_ID_4->at(j)==13) isSS*=-1;
		if(LHE_ID_4->at(j)==-13) isSS*=1;
		if(abs(LHE_ID_4->at(j))==11) return;
	}
	if(isSS!=1) return;
}
}
