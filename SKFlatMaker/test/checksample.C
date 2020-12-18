{
ifstream in("samples.txt");
string line;

while(getline(in,line)){
  istringstream is(line);
  TString this_line = line;
  if(this_line.Contains("#")) continue;

  TString sample, year;
  is >> sample;
  is >> year;

  cout << "In " << year << " " << sample << ":" << endl;

  TFile *file1 = TFile::Open(sample+"/"+year+"/"+sample+"_OS_EE_2016_Ntuple.root");
  TFile *file2 = TFile::Open(sample+"/"+year+"/"+sample+"_OS_MuMu_2016_Ntuple.root");
  TFile *file3 = TFile::Open(sample+"/"+year+"/"+sample+"_SS_EE_2016_Ntuple.root");
  TFile *file4 = TFile::Open(sample+"/"+year+"/"+sample+"_SS_MuMu_2016_Ntuple.root");
  TTree *tree1 = (TTree*)file1->Get("recoTree/SKFlat");
  TTree *tree2 = (TTree*)file2->Get("recoTree/SKFlat");
  TTree *tree3 = (TTree*)file3->Get("recoTree/SKFlat");
  TTree *tree4 = (TTree*)file4->Get("recoTree/SKFlat");
  vector<int> *LHE_ID_1=NULL;
  vector<int> *LHE_ID_2=NULL;
  vector<int> *LHE_ID_3=NULL;
  vector<int> *LHE_ID_4=NULL; //JH : Set NULL then SetBranchAddress will assign memory via "new". Otherwise no address to store vector so segmentation violation.
  tree1->SetBranchAddress("LHE_ID",&LHE_ID_1);
  tree2->SetBranchAddress("LHE_ID",&LHE_ID_2);
  tree3->SetBranchAddress("LHE_ID",&LHE_ID_3);
  tree4->SetBranchAddress("LHE_ID",&LHE_ID_4);
  int events1 = tree1->GetEntries();
  cout << "//OS_EE//" << endl;
  cout << events1 << endl;
  for(int i=0; i<events1; i++){
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
  int events2 = tree2->GetEntries();
  cout << "//OS_MuMu//" << endl;
  cout << events2 << endl;
  for(int i=0; i<events2; i++){
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
  int events3 = tree3->GetEntries();
  cout << "//SS_EE//" << endl;
  cout << events3 << endl;
  for(int i=0; i<events3; i++){
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
  int events4 = tree4->GetEntries();
  cout << "//SS_MuMu//" << endl;
  cout << events4 << endl;
  for(int i=0; i<events4; i++){
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

}
