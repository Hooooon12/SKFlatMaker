{
TFile *file = TFile::Open("####FILENAME");
TTree *tree = (TTree*)file->Get("recoTree/SKFlat");
double weight, weight_SKFlat;
tree->SetBranchAddress("gen_weight",&weight);
int events = tree->GetEntries();
double totWeight = 0.;
for(int i=0; i<events; i++){
  tree->GetEntry(i);
  if(weight>0.) weight_SKFlat = 1.;
  else if(weight<0.) weight_SKFlat = -1.;
  else{
    cout << "Check the weight : " << weight << endl;
    exit(1);
  }
  totWeight+=weight_SKFlat;
}
cout << "total events : " << events << endl;
cout << "sum of (sign of) weights : " << totWeight << endl;

ofstream info;
info.open("####ALIAS.txt");
info << "# alias PD xsec nmc sumw\n" << "####ALIAS\t####PD\t####XSEC\t" << events << "\t" << totWeight;
info.close();
}
