{
TFile *file = TFile::Open("DYTypeI_NLO_SF_M500_OS_EE_2018_Ntuple.root");
TTree *tree = (TTree*)file->Get("recoTree/SKFlat");
vector<int> *LHE_ID;
tree->SetBranchAddress("LHE_ID",&LHE_ID);
int events = tree->GetEntries();
for(int i=0; i<events; i++){
	int isSS = 1;
  tree->GetEntry(i);
  cout << "==========" << i << "th event==========" << endl;
	for(unsigned int j=0; j<LHE_ID->size(); j++){
    //cout << j << "th particle PID : " << LHE_ID->at(j) << endl;
		if(LHE_ID->at(j)==13) isSS*=-1;
		if(LHE_ID->at(j)==-13) isSS*=1;
		if(abs(LHE_ID->at(j))==11) return;
	}
	if(isSS!=1) return;
}
}
