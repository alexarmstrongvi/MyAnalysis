//////////////////////////////////////////////////////////////////////////////////////////
// \project:    ATLAS Experiment at CERN's LHC
// \package:    MyAnalysis
// \file:       $Id$
// \author:     Alaettin.Serhan.Mete@cern.ch
// \history:    N/A 
// 
// Copyright (C) 2016 University of California, Irvine
//////////////////////////////////////////////////////////////////////////////////////////

// analysis include(s)
#include "Superflow/Superflow.h"     
#include "Superflow/Superlink.h"
#include "SusyNtuple/ChainHelper.h"
#include "SusyNtuple/string_utils.h"
#include "SusyNtuple/KinematicTools.h"
//#include "SusyNtuple/SusyNt.h"
//#include "SusyNtuple/SusyDefs.h"
//#include "SusyNtuple/SusyNtObject.h"
//#include "SusyNtuple/SusyNtTools.h"

using namespace sflow;
//using namespace Susy;

///////////////////////////////////////////////////////////////////////
// Usage
///////////////////////////////////////////////////////////////////////
void usage(std::string progName)
{
  printf("=================================================================\n");
  printf("%s [options]\n",progName.c_str());
  printf("=================================================================\n");
  printf("Options:\n");
  printf("-h        Print this help\n");
  printf("-n        Number of events to be processed (default: -1)\n");
  printf("-f        Input file as *.root, list of *.root in a *.txt,\n"); 
  printf("          or a DIR/ containing *.root (default: none)\n");
  printf("=================================================================\n");
}

///////////////////////////////////////////////////////////////////////
// Print event information 
///////////////////////////////////////////////////////////////////////
void printEventInformation(Superlink* sl) {
  // event
  printf("==============================================\n");
  sl->nt->evt()->print();
  // pre-obj
  printf("==============================================\n");
  printf("Pre-objects: \n");
  for(auto &obj : *(sl->preElectrons))  { obj->print(); }
  printf("\n");
  for(auto &obj : *(sl->preMuons))      { obj->print(); }
  printf("\n");
  for(auto &obj : *(sl->preJets))       { obj->print(); }
  // base-obj
  printf("==============================================\n");
  printf("Base-objects: \n");
  for(auto &obj : *(sl->baseElectrons)) { obj->print(); }
  printf("\n");
  for(auto &obj : *(sl->baseMuons))     { obj->print(); }
  printf("\n");
  for(auto &obj : *(sl->baseJets))      { obj->print(); }
  // signal-obj
  printf("==============================================\n");
  printf("Signal-objects: \n");
  for(auto &obj : *(sl->electrons))     { obj->print(); }
  printf("\n");
  for(auto &obj : *(sl->muons))         { obj->print(); }
  printf("\n");
  for(auto &obj : *(sl->jets))          { obj->print(); }
  printf("==============================================\n");
  return;
}

///////////////////////////////////////////////////////////////////////
// Main function
///////////////////////////////////////////////////////////////////////
int main(int argc, char* argv[])
{
  ///////////////////////////////////////////////////////////////////////
  // Read user inputs - NOT super safe so be careful :)
  unsigned int n_events  = -1;
  unsigned int n_skip_events  = 0;
  char *input_file  = nullptr;
  char *name_suffix = nullptr;
  SuperflowRunMode run_mode = SuperflowRunMode::nominal; // SuperflowRunMode::all_syst; //SuperflowRunMode::nominal;
  int c;

  opterr = 0;
  while ((c = getopt (argc, argv, "f:s:n:h")) != -1)
    switch (c)
      {
      case 'f':
        input_file = optarg;
        break;
      case 's':
        name_suffix = optarg;
        break;
      case 'n':
        n_events = atoi(optarg);
        break;
      case 'h':
        usage("makeMiniNtuple");
        return 1;
      case '?':
        if (optopt == 'f')
          fprintf (stderr, "makeMiniNtuple\t Option -%c requires an argument.\n", optopt);
        else if (optopt == 'n')
          fprintf (stderr, "makeMiniNtuple\t Option -%c requires an argument.\n", optopt);
        else if (isprint (optopt))
          fprintf (stderr, "makeMiniNtuple\t Unknown option `-%c'.\n", optopt);
        else
          fprintf (stderr,
                   "makeMiniNtuple\t Unknown option character `\\x%x'.\n",
                   optopt);
        return 1;
      default:
        abort ();
      }

  // Catch problems or cast
  for (int index = optind; index < argc; index++)
    printf ("makeMiniNtuple\t Non-option argument %s\n", argv[index]);
  if (input_file==nullptr) {
    printf("makeMiniNtuple\t An input file must be provided with option -f (a list, a DIR or single file)\n");
    return 0;  
  }

  // Print information
  printf("makeMiniNtuple\t =================================================================\n");
  printf("makeMiniNtuple\t Running MyAnalysis/makeMiniNtuple\n");
  printf("makeMiniNtuple\t =================================================================\n");
  printf("makeMiniNtuple\t   Flags:\n");
  printf("makeMiniNtuple\t     Input file (-f)         : %s\n",input_file);
  printf("makeMiniNtuple\t     Number of events (-n)   : %i\n",n_events );
  printf("makeMiniNtuple\t =================================================================\n");
  ///////////////////////////////////////////////////////////////////////

  ///////////////////////////////////////////////////////////////////////
  // Setup Superflow 
  TChain* chain = new TChain("susyNt");
  chain->SetDirectory(0);

  bool inputIsFile = Susy::utils::endswith(input_file, ".root");
  bool inputIsList = Susy::utils::endswith(input_file, ".txt");
  bool inputIsDir  = Susy::utils::endswith(input_file, "/");

  if(inputIsFile) {
    ChainHelper::addFile(chain, input_file);
  } else if (inputIsList) {
    // If a list of ROOT files
    ChainHelper::addFileList(chain, input_file);
  } else if (inputIsDir) {
    ChainHelper::addFileDir(chain, input_file);
  } else {
    printf("makeMiniNtuple\t Cannot understand input %s",input_file);
    return 0;  
  }
  
  Superflow* cutflow = new Superflow(); // initialize the cutflow
  cutflow->setAnaName("SuperflowAna");                // arbitrary
  cutflow->setAnaType(AnalysisType::Ana_2Lep);        // analysis type, passed to SusyNt
  cutflow->setLumi(1.0);                              // set the MC normalized to X pb-1
  cutflow->setSampleName(input_file);                 // sample name, check to make sure it's set OK
  cutflow->setRunMode(run_mode);                      // make configurable via run_mode
  cutflow->setCountWeights(true);                     // print the weighted cutflows
  if(name_suffix != nullptr) cutflow->setFileSuffix(name_suffix);
  cutflow->setChain(chain);
  cutflow->nttools().initTriggerTool(ChainHelper::firstFile(input_file,0.)); 

  printf("makeMiniNtuple\t Total events available : %lli\n",chain->GetEntries());

  ///////////////////////////////////////////////////////////////////////
  // Superflow methods begin here
  ///////////////////////////////////////////////////////////////////////

  *cutflow << CutName("read in") << [](Superlink* /*sl*/) -> bool { return true; };

  //  Cleaning Cuts
  int cutflags = 0;
  
  *cutflow << CutName("Pass GRL") << [&](Superlink* sl) -> bool {
      cutflags = sl->nt->evt()->cutFlags[NtSys::NOM];
      return (sl->tools->passGRL(cutflags));
  };

  *cutflow << CutName("LAr error") << [&](Superlink* sl) -> bool {
      return (sl->tools->passLarErr(cutflags));
  };
  
  *cutflow << CutName("Tile error") << [&](Superlink* sl) -> bool {
      return (sl->tools->passTileErr(cutflags));
  };
  
  *cutflow << CutName("TTC veto") << [&](Superlink* sl) -> bool {
      return (sl->tools->passTTC(cutflags));
  };

  *cutflow << CutName("SCT seu") << [&](Superlink* sl) -> bool {
      return (sl->tools->passSCTErr(cutflags));
  };
 
  *cutflow << CutName("pass good vertex") << [&](Superlink* sl) -> bool {
      return (sl->tools->passGoodVtx(cutflags));
  };

  *cutflow << CutName("bad muon veto") << [&](Superlink* sl) -> bool {
      return (sl->tools->passBadMuon(sl->preMuons));
  };
  
  *cutflow << CutName("pass cosmic veto") << [&](Superlink* sl) -> bool {
      return (sl->tools->passCosmicMuon(sl->baseMuons));
  };

  *cutflow << CutName("jet cleaning") << [&](Superlink* sl) -> bool {
      return (sl->tools->passJetCleaning(sl->baseJets));
  };
   
  *cutflow << CutName("exactly two baseline leptons") << [](Superlink* sl) -> bool {
      return (sl->baseLeptons->size() == 2);
  };

  *cutflow << CutName("exactly two signal leptons") << [](Superlink* sl) -> bool {
      return (sl->leptons->size() == 2);
  };

//  *cutflow << CutName("opposite sign muon and electron") << [&](Superlink* sl) -> bool {
//      return ((sl->leptons->at(0)->isEle() && sl->leptons->at(1)->isMu() && sl->leptons->at(0)->q!=sl->leptons->at(1)->q) ||
//              (sl->leptons->at(1)->isEle() && sl->leptons->at(0)->isMu() && sl->leptons->at(0)->q!=sl->leptons->at(1)->q));
//  };
  *cutflow << CutName("leading lepton pt >= 20GeV") << [](Superlink* sl) -> bool {
      return (sl->leptons->at(0)->pt>=20);
  };
  *cutflow << CutName("sub-leading lepton pt >= 12GeV") << [](Superlink* sl) -> bool {
      return (sl->leptons->at(1)->pt>=12);
  };
  *cutflow << CutName("leading lepton eta <= 2.4") << [](Superlink* sl) -> bool {
      return (fabs(sl->leptons->at(0)->eta)<=2.4);
  };
  *cutflow << CutName("sub-leading lepton eta <= 2.4") << [](Superlink* sl) -> bool {
      return (fabs(sl->leptons->at(1)->eta)<=2.4);
  };
 

  //  Output Ntuple Setup
  //      > Ntuple variables

  // Storing a bunch of numbers...
  *cutflow << NewVar("Event run number"); {
    *cutflow << HFTname("runNumber");
    *cutflow << [](Superlink* sl, var_int*) -> int { return sl->nt->evt()->run; };
    *cutflow << SaveVar();
  }

  *cutflow << NewVar("Event number"); {
    *cutflow << HFTname("eventNumber");
    *cutflow << [](Superlink* sl, var_int*) -> int { return sl->nt->evt()->eventNumber; };
    *cutflow << SaveVar();
  }

  *cutflow << NewVar("is Monte Carlo"); {
    *cutflow << HFTname("isMC");
    *cutflow << [](Superlink* sl, var_bool*) -> bool { return sl->nt->evt()->isMC ? true : false; };
    *cutflow << SaveVar();
  }

  *cutflow << NewVar("event weight"); { 
    *cutflow << HFTname("eventweight"); 
    *cutflow << [](Superlink* sl, var_double*) -> double { 
        return sl->weights->product() * sl->nt->evt()->wPileup; 
        //return sl->weights->product(); 
    }; 
    *cutflow << SaveVar(); 
  }

  *cutflow << NewVar("HLT_mu18_mu8noL1 trigger bit"); {
      *cutflow << HFTname("pass_HLT_mu18_mu8noL1");
      *cutflow << [](Superlink* sl, var_bool*) -> bool { return sl->tools->triggerTool().passTrigger(sl->nt->evt()->trigBits, "HLT_mu18_mu8noL1"); };
      *cutflow << SaveVar();
  }  

  *cutflow << NewVar("HLT_2e12_lhloose_L12EM10VH trigger bit"); {
      *cutflow << HFTname("pass_HLT_2e12_lhloose_L12EM10VH");
      *cutflow << [](Superlink* sl, var_bool*) -> bool { return sl->tools->triggerTool().passTrigger(sl->nt->evt()->trigBits, "HLT_2e12_lhloose_L12EM10VH"); };
      *cutflow << SaveVar();
  }  

  *cutflow << NewVar("HLT_e17_lhloose_mu14 trigger bit"); {
      *cutflow << HFTname("pass_HLT_e17_lhloose_mu14");
      *cutflow << [](Superlink* sl, var_bool*) -> bool { return sl->tools->triggerTool().passTrigger(sl->nt->evt()->trigBits, "HLT_e17_lhloose_mu14"); };
      *cutflow << SaveVar();
  }  

  *cutflow << NewVar("HLT_mu20_mu8noL1 trigger bit"); {
      *cutflow << HFTname("pass_HLT_mu20_mu8noL1");
      *cutflow << [](Superlink* sl, var_bool*) -> bool { return sl->tools->triggerTool().passTrigger(sl->nt->evt()->trigBits, "HLT_mu20_mu8noL1"); };
      *cutflow << SaveVar();
  }  

  *cutflow << NewVar("HLT_2e15_lhvloose_L12EM13VH trigger bit"); {
      *cutflow << HFTname("pass_HLT_2e15_lhvloose_L12EM13VH");
      *cutflow << [](Superlink* sl, var_bool*) -> bool { return sl->tools->triggerTool().passTrigger(sl->nt->evt()->trigBits, "HLT_2e15_lhvloose_L12EM13VH"); };
      *cutflow << SaveVar();
  } 

  *cutflow << NewVar("HLT_2e17_lhvloose_nod0 trigger bit"); {
      *cutflow << HFTname("pass_HLT_2e17_lhvloose_nod0");
      *cutflow << [](Superlink* sl, var_bool*) -> bool { return sl->tools->triggerTool().passTrigger(sl->nt->evt()->trigBits, "HLT_2e17_lhvloose_nod0"); };
      *cutflow << SaveVar();
  } 

  *cutflow << NewVar("HLT_mu22_mu8noL1 trigger bit"); {
      *cutflow << HFTname("pass_HLT_mu22_mu8noL1");
      *cutflow << [](Superlink* sl, var_bool*) -> bool { return sl->tools->triggerTool().passTrigger(sl->nt->evt()->trigBits, "HLT_mu22_mu8noL1"); };
      *cutflow << SaveVar();
  } 

  *cutflow << NewVar("HLT_e17_lhloose_nod0_mu14 trigger bit"); {
      *cutflow << HFTname("pass_HLT_e17_lhloose_nod0_mu14");
      *cutflow << [](Superlink* sl, var_bool*) -> bool { return sl->tools->triggerTool().passTrigger(sl->nt->evt()->trigBits, "HLT_e17_lhloose_nod0_mu14"); };
      *cutflow << SaveVar();
  } 

  *cutflow << NewVar("treatAsYear"); { 
      *cutflow << HFTname("treatAsYear");
      *cutflow << [](Superlink* sl, var_double*) -> int { 
          return sl->nt->evt()->treatAsYear;
      };
      *cutflow << SaveVar();
  }


  // Accesing objects through superlink and assigning them to internal variables 
  LeptonVector baseLeptons, signalLeptons;
  Susy::Met met;
  *cutflow << [&](Superlink* sl, var_void*) { 
    baseLeptons   = *sl->baseLeptons; 
    signalLeptons = *sl->leptons; 
    met = *sl->met;
  };

  *cutflow << NewVar("number of baseline leptons"); {
    *cutflow << HFTname("nBaseLeptons");
    *cutflow << [&](Superlink* /*sl*/, var_int*) -> int { return baseLeptons.size(); };
    *cutflow << SaveVar();
  }

  *cutflow << NewVar("number of signal leptons"); {
    *cutflow << HFTname("nSignalLeptons");
    *cutflow << [&](Superlink* /*sl*/, var_int*) -> int { return signalLeptons.size(); };
    *cutflow << SaveVar();
  }

  *cutflow << NewVar("number of baseline taus"); {
    *cutflow << HFTname("nBaseTaus");
    *cutflow << [&](Superlink* sl, var_int*) -> int { return sl->baseTaus->size(); };
    *cutflow << SaveVar();
  }

  *cutflow << NewVar("number of signal taus"); {
    *cutflow << HFTname("nSignalTaus");
    *cutflow << [&](Superlink* sl, var_int*) -> int { return sl->taus->size(); };
    *cutflow << SaveVar();
  }

  // Storing a bunch of vectors
  *cutflow << NewVar("lepton pt"); {
    *cutflow << HFTname("l_pt");
    *cutflow << [&](Superlink* /*sl*/, var_float_array*) -> vector<double> {
      vector<double> out;
      for(auto& lepton : signalLeptons) {
        out.push_back(lepton->Pt());
      }
      return out;
    };
    *cutflow << SaveVar();
  }

  *cutflow << NewVar("lepton eta"); {
    *cutflow << HFTname("l_eta");
    *cutflow << [&](Superlink* /*sl*/, var_float_array*) -> vector<double> {
      vector<double> out;
      for(auto& lepton : signalLeptons) {
        out.push_back(lepton->Eta());
      }
      return out;
    };
    *cutflow << SaveVar();
  }

  *cutflow << NewVar("lepton phi"); {
    *cutflow << HFTname("l_phi");
    *cutflow << [&](Superlink* /*sl*/, var_float_array*) -> vector<double> {
      vector<double> out;
      for(auto& lepton : signalLeptons) {
        out.push_back(lepton->Phi());
      }
      return out;
    };
    *cutflow << SaveVar();
  }

  *cutflow << NewVar("lepton flavor (0: e, 1: m)"); {
    *cutflow << HFTname("l_flav");
    *cutflow << [&](Superlink* /*sl*/, var_float_array*) -> vector<double> {
      vector<double> out;
      for(auto& lepton : signalLeptons) {
        out.push_back(lepton->isEle() ? 0 : 1);
      }
      return out;
    };
    *cutflow << SaveVar();
  }

  *cutflow << NewVar("lepton type"); {
    *cutflow << HFTname("l_type");
    *cutflow << [&](Superlink* /*sl*/, var_float_array*) -> vector<double> {
      vector<double> out;
      for(auto& lepton : signalLeptons) {
        out.push_back(lepton->mcType);
      }
      return out;
    };
    *cutflow << SaveVar();
  }

  *cutflow << NewVar("lepton origin"); {
    *cutflow << HFTname("l_origin");
    *cutflow << [&](Superlink* /*sl*/, var_float_array*) -> vector<double> {
      vector<double> out;
      for(auto& lepton : signalLeptons) {
        out.push_back(lepton->mcOrigin);
      }
      return out;
    };
    *cutflow << SaveVar();
  }

  *cutflow << NewVar("lepton charge"); {
    *cutflow << HFTname("l_q");
    *cutflow << [&](Superlink* /*sl*/, var_float_array*) -> vector<double> {
      vector<double> out;
      for(auto& lepton : signalLeptons) {
          out.push_back(lepton->q);
      }
      return out;
      };
    *cutflow << SaveVar();
  }

  // MET
  TLorentzVector MET;
  *cutflow << NewVar("transverse missing energy (Et)"); {
    *cutflow << HFTname("met");
    *cutflow << [&](Superlink* sl, var_float*) -> double { 
      MET.SetPxPyPzE(sl->met->Et*cos(sl->met->phi),
                     sl->met->Et*sin(sl->met->phi),
                     0.,
                     sl->met->Et);
      return MET.Pt();
    };
    *cutflow << SaveVar();
  }

  *cutflow << NewVar("transverse missing energy (Phi)"); {
    *cutflow << HFTname("metPhi");
    *cutflow << [&](Superlink* /*sl*/, var_float*) -> double { return MET.Phi(); };
    *cutflow << SaveVar();
  }

  // Forming more detailed variables 
  TLorentzVector lepton0 ; 
  TLorentzVector lepton1 ; 
  TLorentzVector dileptonP4 ;
  *cutflow << [&](Superlink* /*sl*/, var_void*) {
    lepton0 = *signalLeptons.at(0); 
    lepton1 = *signalLeptons.at(1); 
    dileptonP4 = lepton0 + lepton1;
  };

  *cutflow << NewVar("dilepton flavor"); {
    *cutflow << HFTname("dilep_flav");
    *cutflow << [&](Superlink* /*sl*/, var_int*) -> int {
	    if(signalLeptons.at(0)->isEle() && signalLeptons.at(1)->isMu()){return 0;}       // e mu  case
        else if(signalLeptons.at(0)->isMu() && signalLeptons.at(1)->isEle()){return 1;}  // mu e  case
        else if(signalLeptons.at(0)->isEle() && signalLeptons.at(1)->isEle()){return 2;} // e e   case
        else if(signalLeptons.at(0)->isMu() && signalLeptons.at(1)->isMu()){return 3;}   // mu mu case
	    else{return 4;}
        };
    *cutflow << SaveVar();
    }

  *cutflow << NewVar("collinear mass, M_coll"); {
    *cutflow << HFTname("m_coll");
    *cutflow << [&](Superlink* /*sl*/, var_float*) -> double { 
	double deta = fabs(lepton0.Eta()-lepton1.Eta());
	double dphi = lepton0.DeltaPhi(lepton1);
	return sqrt(2*lepton0.Pt()*(lepton1.Pt()+met.Et)*(cosh(deta)-cos(dphi)));
    };
    *cutflow << SaveVar();
  }

  *cutflow << NewVar("mass of di-lepton system, M_ll"); {
    *cutflow << HFTname("mll");
    *cutflow << [&](Superlink* /*sl*/, var_float*) -> double { return dileptonP4.M(); };
    *cutflow << SaveVar();
  }

  *cutflow << NewVar("Pt of di-lepton system, Pt_ll"); {
    *cutflow << HFTname("ptll");
    *cutflow << [&](Superlink* /*sl*/, var_float*) -> double { return dileptonP4.Pt(); };
    *cutflow << SaveVar();
  }

  *cutflow << NewVar("delta R of di-lepton system"); {
    *cutflow << HFTname("drll");
    *cutflow << [&](Superlink* /*sl*/, var_float*) -> double { return lepton0.DeltaR(lepton1); };
    *cutflow << SaveVar();
  }

  *cutflow << NewVar("dphi between sub-leading lepton and MET"); {
    *cutflow << HFTname("dphi_l1_met");
    *cutflow << [&](Superlink* /*sl*/, var_float*) -> double {
        return (met.lv()).DeltaPhi(lepton1);
    };
    *cutflow << SaveVar();     
 }

  *cutflow << NewVar("dphi between leading and sub-leading lepton"); {
    *cutflow << HFTname("dphi_ll");
    *cutflow << [&](Superlink* /*sl*/, var_float*) -> double {
        return lepton0.DeltaPhi(lepton1);
    };
    *cutflow << SaveVar();     
 }

  *cutflow << NewVar("dphi between leading lepton and MET"); {
    *cutflow << HFTname("dphi_l0_met");
    *cutflow << [&](Superlink* /*sl*/, var_float*) -> double {
        return (met.lv()).DeltaPhi(lepton0);
    };
    *cutflow << SaveVar();     
 }

  *cutflow << NewVar("diff_pt between leading and sub-leading lepton"); {
    *cutflow << HFTname("dpt_ll");
    *cutflow << [&](Superlink* /*sl*/, var_float*) -> double {
        return lepton0.Pt() - lepton1.Pt();
    };
    *cutflow << SaveVar();     
 }

// Jet Variables
  JetVector baseJets, signalJets, centralLightJets, centralBJets, forwardJets;
  *cutflow << [&](Superlink* sl, var_void*) { 
    baseJets = *sl->baseJets; 
    signalJets = *sl->jets; 
    for(auto& jet : baseJets) {
      if(sl->tools->m_jetSelector->isCentralLight(jet))  { centralLightJets.push_back(jet); } 
      else if(sl->tools->m_jetSelector->isCentralB(jet)) { centralBJets.push_back(jet);     } 
      else if(sl->tools->m_jetSelector->isForward(jet))  { forwardJets.push_back(jet);      } 
    }
    std::sort(centralLightJets.begin()  , centralLightJets.end()  , comparePt);
    std::sort(centralBJets.begin()      , centralBJets.end()      , comparePt);
    std::sort(forwardJets.begin()       , forwardJets.end()       , comparePt);
  };


  *cutflow << NewVar("number of baseline jets"); {
    *cutflow << HFTname("nBaseJets");
    *cutflow << [&](Superlink* /*sl*/, var_int*) -> int { return baseJets.size(); };
    *cutflow << SaveVar();
  }

  *cutflow << NewVar("number of central light jets"); {
    *cutflow << HFTname("nCentralLJets");
    *cutflow << [](Superlink* sl, var_int*) -> int { return sl->tools->numberOfCLJets(*sl->baseJets)/*(*baseJets)*/; };
    *cutflow << SaveVar();
  }

  *cutflow << NewVar("number of central b jets"); {
    *cutflow << HFTname("nCentralBJets");
    *cutflow << [](Superlink* sl, var_int*) -> int { return sl->tools->numberOfCBJets(*sl->baseJets)/*(*baseJets)*/; };
    *cutflow << SaveVar();
  }

  *cutflow << NewVar("number of forward jets"); {
    *cutflow << HFTname("nForwardJets");
    *cutflow << [](Superlink* sl, var_int*) -> int { return sl->tools->numberOfFJets(*sl->baseJets)/*(*baseJets)*/; };
    *cutflow << SaveVar();
  }

  *cutflow << NewVar("jet pt"); {
    *cutflow << HFTname("j_pt");
    *cutflow << [&](Superlink* /*sl*/, var_float_array*) -> vector<double> {
      vector<double> out;
      for(auto& jet : baseJets) {
        out.push_back(jet->Pt());
      }
      return out;
    };
    *cutflow << SaveVar();
  }

  *cutflow << NewVar("jet eta"); {
    *cutflow << HFTname("j_eta");
    *cutflow << [&](Superlink* /*sl*/, var_float_array*) -> vector<double> {
      vector<double> out;
      for(auto& jet : baseJets) {
        out.push_back(jet->Eta());
      }
      return out;
    };
    *cutflow << SaveVar();
  }

  *cutflow << NewVar("jet JVT"); {
    *cutflow << HFTname("j_jvt");
    *cutflow << [&](Superlink* /*sl*/, var_float_array*) -> vector<double> {
      vector<double> out;
      for(auto& jet : baseJets) {
        out.push_back(jet->jvt);
      }
      return out;
    };
    *cutflow << SaveVar();
  }

  *cutflow << NewVar("jet JVF"); {
    *cutflow << HFTname("j_jvf");
    *cutflow << [&](Superlink* /*sl*/, var_float_array*) -> vector<double> {
      vector<double> out;
      for(auto& jet : baseJets) {
        out.push_back(jet->jvf);
      }
      return out;
    };
    *cutflow << SaveVar();
  }

  *cutflow << NewVar("jet phi"); {
    *cutflow << HFTname("j_phi");
    *cutflow << [&](Superlink* /*sl*/, var_float_array*) -> vector<double> {
      vector<double> out;
      for(auto& jet : baseJets) {
        out.push_back(jet->Phi());
      }
      return out;
    };
    *cutflow << SaveVar();
  }

  *cutflow << NewVar("jet flavor (0: NA, 1: CL, 2: CB, 3: F)"); {
    *cutflow << HFTname("j_flav");
    *cutflow << [&](Superlink* sl, var_float_array*) -> vector<double> {
      vector<double> out; int flav = 0;
      for(auto& jet : baseJets) {
        if(sl->tools->m_jetSelector->isCentralLight(jet))  { flav = 1; } 
        else if(sl->tools->m_jetSelector->isCentralB(jet)) { flav = 2; } 
        else if(sl->tools->m_jetSelector->isForward(jet))  { flav = 3; } 
        out.push_back(flav);
        flav=0;
      }
      return out;
    };
    *cutflow << SaveVar();
  }


  // Clear internal variables  
  *cutflow << [&](Superlink* /*sl*/, var_void*) { 
    baseLeptons.clear();signalLeptons.clear();
    baseJets.clear();signalJets.clear();
    centralLightJets.clear();centralBJets.clear();forwardJets.clear();
     
  };

  ///////////////////////////////////////////////////////////////////////
  // Systematics
  ///////////////////////////////////////////////////////////////////////

  // Here comes the systematics...

  ///////////////////////////////////////////////////////////////////////
  // Superflow methods end here
  ///////////////////////////////////////////////////////////////////////

  // Initialize the cutflow and start the event loop.
  chain->Process(cutflow, input_file, n_events, n_skip_events);

  delete cutflow;
  delete chain;

  // Print information
  printf("makeMiniNtuple\t =================================================================\n");
  printf("makeMiniNtuple\t All done!\n");
  printf("makeMiniNtuple\t =================================================================\n");
  return 0; 
}
