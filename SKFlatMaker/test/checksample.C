{
ifstream in("samples.txt");
string line;

while(getline(in,line)){
  istringstream is(line);
  TString this_line = line;
  if(this_line.Contains("#")||this_line=="") continue;

  TString sample, year, channel;
  is >> sample;
  is >> channel;
  is >> year;

  cout << "In " << year << " " << sample << " " << channel << ":" << endl;

  //TFile *file = TFile::Open(sample+"/"+year+"/"+sample+"_"+channel+"_"+year+"_Ntuple.root");
  //TTree *tree = (TTree*)file->Get("recoTree/SKFlat");
  TChain *fChain = new TChain("recoTree/SKFlat");
  fChain->Add(sample+"/"+year+"/Ntuples/"+sample+"_"+channel+"_"+year+"_Ntuple*.root");
  vector<int> *LHE_ID=NULL; //JH : Set NULL then SetBranchAddress will assign memory via "new". Otherwise no address to store vector so segmentation violation.
  //tree->SetBranchAddress("LHE_ID",&LHE_ID);
  fChain->SetBranchAddress("LHE_ID",&LHE_ID);
  //int events = tree->GetEntries();
  int events = fChain->GetEntries();
  cout << "//"+channel+"//" << endl;
  cout << events << endl;
  for(int i=0; i<events; i++){
    int isSS = 1;
    int isEMu = 0;
    //tree->GetEntry(i);
    fChain->GetEntry(i);
    if(i%1000==0) cout << "==========" << i << "th event==========" << endl;
    for(unsigned int j=0; j<LHE_ID->size(); j++){
      //cout << j << "th particle PID : " << LHE_ID->at(j) << endl;
      if(LHE_ID->at(j)==11){
        isSS*=-1;
        isEMu+=1;
      }
      if(LHE_ID->at(j)==-11){
        isSS*=1;
        isEMu+=1;
      }
      if(LHE_ID->at(j)==13){
        isSS*=-1;
        isEMu-=1;
      }
      if(LHE_ID->at(j)==-13){
        isSS*=1;
        isEMu-=1;
      }
    }
    if( (channel.Contains("SS")&&isSS!=1) || (channel.Contains("OS")&&isSS==1) || (channel.Contains("EE")&&isEMu!=2) || (channel.Contains("MuMu")&&isEMu!=-2) || (channel.Contains("EMu")&&isEMu!=0) ){
      cout << "!!Wrong sample!!" << endl;
      cout << "Channel is " << channel << " but isSS : " << isSS << ", isEMu : " << isEMu << "." << endl;
      cout << "Exiting..." << endl;
      return;
    }
  }
}
}
