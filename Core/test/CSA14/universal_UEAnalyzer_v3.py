#!/usr/bin/env python
import CommonFSQFramework.Core.ExampleProofReader

import sys, os, time, math
sys.path.append(os.path.dirname(__file__))

import ROOT
ROOT.gROOT.SetBatch(True)
from ROOT import edm, JetCorrectionUncertainty
from ROOT import TFile, TChain, TTree,TH1,TH2

from array import *
from array import array

import time
start = time.clock()

p1="_post"

bRec_nChg_pTLeadTrack_away = array("f",[0])
bRec_nChg_pTLeadTrack_towards = array("f",[0])
bRec_nChg_pTLeadTrack_trans = array("f",[0])
bRec_nChg_pTLeadTrack_transMin = array("f",[0])
bRec_nChg_pTLeadTrack_transMax = array("f",[0])
bRec_nChg_pTLeadTrack_transDiff = array("f",[0])
bRec_pTSum_pTLeadTrack_away = array("f",[0])
bRec_pTSum_pTLeadTrack_towards = array("f",[0])
bRec_pTSum_pTLeadTrack_trans = array("f",[0])
bRec_pTSum_pTLeadTrack_transMin = array("f",[0])
bRec_pTSum_pTLeadTrack_transMax = array("f",[0])
bRec_pTSum_pTLeadTrack_transDiff = array("f",[0])
bRec_pTLeadTrack = array("f",[0])
bRec_etaLeadTrack = array("f",[0])
bRec_phiLeadTrack = array("f",[0])

bRec_evtTrue_LeadTrack = array("f",[0]) 

bGen_nChg_pTLeadTrack_away = array("f",[0])
bGen_nChg_pTLeadTrack_towards = array("f",[0])
bGen_nChg_pTLeadTrack_trans = array("f",[0])
bGen_nChg_pTLeadTrack_transMin = array("f",[0])
bGen_nChg_pTLeadTrack_transMax = array("f",[0])
bGen_nChg_pTLeadTrack_transDiff = array("f",[0])
bGen_pTSum_pTLeadTrack_away = array("f",[0])
bGen_pTSum_pTLeadTrack_towards = array("f",[0])
bGen_pTSum_pTLeadTrack_trans = array("f",[0])
bGen_pTSum_pTLeadTrack_transMin = array("f",[0])
bGen_pTSum_pTLeadTrack_transMax = array("f",[0])
bGen_pTSum_pTLeadTrack_transDiff = array("f",[0])
bGen_pTLeadTrack = array("f",[0])
bGen_etaLeadTrack = array("f",[0])
bGen_phiLeadTrack = array("f",[0])

bGen_evtTrue_LeadTrack = array("f",[0])


class universal_UEAnalyzer_v3(CommonFSQFramework.Core.ExampleProofReader.ExampleProofReader):
    def init( self):

        self.jetMode = False #DR (if analyzing by leading jet)
        self.dataMode = False #DR (if running on Data, due to lumi and trigger check)
	self.genMode = False #DR (to only running on GEN MC)
	self.nogenMode = False #DR (to only running on RECO MC)
        self.etaCut = 0.8 #DR (set to 2. or 0.8 depending on analysis)
        self.d0Cut = 3. #DR (set to 3 for analysis; 2 or 4 for systematics)
        self.dzCut = 3. #DR (set to 3 for analysis; 2 or 4 for systematics)
        self.ndofCut = 4 #DR (set to 4 for analysis; 2 or 6 for systematics)

        #TODO: Currenty dataMode is implemented for ZeroBias data.  Needs to be modified for MinBias.



        self.tree = ROOT.TTree("tree","ueAnalysis")
        self.tree.Branch('bRec_pTLeadTrack',   bRec_pTLeadTrack,'bRec_pTLeadTrack/F')
        self.tree.Branch('bRec_etaLeadTrack',   bRec_etaLeadTrack,'bRec_etaLeadTrack/F')
        self.tree.Branch('bRec_phiLeadTrack',   bRec_phiLeadTrack,'bRec_phiLeadTrack/F')
        self.tree.Branch('bRec_evtTrue_LeadTrack',   bRec_evtTrue_LeadTrack,'bRec_evtTrue_LeadTrack/F')
        self.tree.Branch('bGen_evtTrue_LeadTrack',   bGen_evtTrue_LeadTrack,'bGen_evtTrue_LeadTrack/F')
        self.tree.Branch('bGen_pTLeadTrack',   bGen_pTLeadTrack,'bGen_pTLeadTrack/F')
        self.tree.Branch('bGen_etaLeadTrack',   bGen_etaLeadTrack,'bGen_etaLeadTrack/F')
        self.tree.Branch('bGen_phiLeadTrack',   bGen_phiLeadTrack,'bGen_phiLeadTrack/F')
        self.tree.Branch('bRec_nChg_pTLeadTrack_away',   bRec_nChg_pTLeadTrack_away,'bRec_nChg_pTLeadTrack_away/F')
        self.tree.Branch('bRec_nChg_pTLeadTrack_towards',   bRec_nChg_pTLeadTrack_towards,'bRec_nChg_pTLeadTrack_towards/F')
        self.tree.Branch('bRec_nChg_pTLeadTrack_trans',   bRec_nChg_pTLeadTrack_trans,'bRec_nChg_pTLeadTrack_trans/F')
        self.tree.Branch('bRec_nChg_pTLeadTrack_transMin',   bRec_nChg_pTLeadTrack_transMin,'bRec_nChg_pTLeadTrack_transMin/F')
        self.tree.Branch('bRec_nChg_pTLeadTrack_transMax',   bRec_nChg_pTLeadTrack_transMax,'bRec_nChg_pTLeadTrack_transMax/F')
        self.tree.Branch('bRec_nChg_pTLeadTrack_transDiff',   bRec_nChg_pTLeadTrack_transDiff,'bRec_nChg_pTLeadTrack_transDiff/F')
        self.tree.Branch('bRec_pTSum_pTLeadTrack_away',   bRec_pTSum_pTLeadTrack_away,'bRec_pTSum_pTLeadTrack_away/F')
        self.tree.Branch('bRec_pTSum_pTLeadTrack_towards',   bRec_pTSum_pTLeadTrack_towards,'bRec_pTSum_pTLeadTrack_towards/F')
        self.tree.Branch('bRec_pTSum_pTLeadTrack_trans',   bRec_pTSum_pTLeadTrack_trans,'bRec_pTSum_pTLeadTrack_trans/F')
        self.tree.Branch('bRec_pTSum_pTLeadTrack_transMin',   bRec_pTSum_pTLeadTrack_transMin,'bRec_pTSum_pTLeadTrack_transMin/F')
        self.tree.Branch('bRec_pTSum_pTLeadTrack_transMax',   bRec_pTSum_pTLeadTrack_transMax,'bRec_pTSum_pTLeadTrack_transMax/F')
        self.tree.Branch('bRec_pTSum_pTLeadTrack_transDiff',   bRec_pTSum_pTLeadTrack_transDiff,'bRec_pTSum_pTLeadTrack_transDiff/F')
        self.tree.Branch('bGen_nChg_pTLeadTrack_away',   bGen_nChg_pTLeadTrack_away,'bGen_nChg_pTLeadTrack_away/F')
        self.tree.Branch('bGen_nChg_pTLeadTrack_towards',   bGen_nChg_pTLeadTrack_towards,'bGen_nChg_pTLeadTrack_towards/F')
        self.tree.Branch('bGen_nChg_pTLeadTrack_trans',   bGen_nChg_pTLeadTrack_trans,'bGen_nChg_pTLeadTrack_trans/F')
        self.tree.Branch('bGen_nChg_pTLeadTrack_transMin',   bGen_nChg_pTLeadTrack_transMin,'bGen_nChg_pTLeadTrack_transMin/F')
        self.tree.Branch('bGen_nChg_pTLeadTrack_transMax',   bGen_nChg_pTLeadTrack_transMax,'bGen_nChg_pTLeadTrack_transMax/F')
        self.tree.Branch('bGen_nChg_pTLeadTrack_transDiff',   bGen_nChg_pTLeadTrack_transDiff,'bGen_nChg_pTLeadTrack_transDiff/F')
        self.tree.Branch('bGen_pTSum_pTLeadTrack_away',   bGen_pTSum_pTLeadTrack_away,'bGen_pTSum_pTLeadTrack_away/F')
        self.tree.Branch('bGen_pTSum_pTLeadTrack_towards',   bGen_pTSum_pTLeadTrack_towards,'bGen_pTSum_pTLeadTrack_towards/F')
        self.tree.Branch('bGen_pTSum_pTLeadTrack_trans',   bGen_pTSum_pTLeadTrack_trans,'bGen_pTSum_pTLeadTrack_trans/F')
        self.tree.Branch('bGen_pTSum_pTLeadTrack_transMin',   bGen_pTSum_pTLeadTrack_transMin,'bGen_pTSum_pTLeadTrack_transMin/F')
        self.tree.Branch('bGen_pTSum_pTLeadTrack_transMax',   bGen_pTSum_pTLeadTrack_transMax,'bGen_pTSum_pTLeadTrack_transMax/F')
        self.tree.Branch('bGen_pTSum_pTLeadTrack_transDiff',   bGen_pTSum_pTLeadTrack_transDiff,'bGen_pTSum_pTLeadTrack_transDiff/F')
        self.GetOutputList().Add(self.tree)
	self.hist = {}
        self.hist_vertex = {}
	self.hist_pre = {}
	self.hist_post = {}
	self.hist_gen = {}
        self.hist_jet = {}
	self.hist_gent = {}
	self.hist_trans = {}
	self.hist_tow = {}
	self.hist_away = {}
	self.hist_gentow = {}
        self.hist_genaway = {}
	self.hist_full_jet = {}
	self.hist_full_tracks = {}
	self.hist_full_genjet = {}
        self.hist_full_gentracks = {}
        self.Trans_SisCon5 = {}
        self.other_SisCon5 = {}

        #self.hist["eventsGood"] = ROOT.TH1C("eventsGood", "eventsGood", 100000000,100000000,200000000)

     
	self.hist_full_genjet["fgen_ptSisCone5"] =  ROOT.TH1F("fgen_pt_SisCone5",   "ptTrackJets",  200, 0, 200)
        self.hist_full_genjet["fgen_etaSisCone5"] =  ROOT.TH1F("fgen_eta_SisCone5",   "etaTrackJets",  100 , -5, 5)
        self.hist_full_genjet["fgen_phiSisCone5"] =  ROOT.TH1F("fgen_phi_SisCone5",   "phiTrackJets",  628 , -3.14, 3.14)

        self.hist_full_gentracks["fgen_trackPt"] =  ROOT.TH1F("fgen_tracksPt",   "tracksPt",  5000, 0, 500)

        self.hist_full_jet["f_ptSisCone5"] =  ROOT.TH1F("f_pt_SisCone5",   "ptTrackJets",  200, 0, 200)
        self.hist_full_jet["f_etaSisCone5"] =  ROOT.TH1F("f_eta_SisCone5",   "etaTrackJets",  100 , -5, 5)
        self.hist_full_jet["f_phiSisCone5"] =  ROOT.TH1F("f_phi_SisCone5",   "phiTrackJets",  628 , -3.14, 3.14
)

        self.hist_full_tracks["f_trackPt"] =  ROOT.TH1F("f_trackPt",   "tracksPt",  5000, 0, 500)


        #p = "_central_B" # a placeholder for different triggers ("B") and uncertainty variations
                         #  "central" means this is a central value (ie no variations were applied)
        self.hist_vertex["nVtx"] =  ROOT.TH1F("nVtx",   "nVtx",  100, 0, 100)
        self.hist_vertex["ndfVtx"] =  ROOT.TH1F("ndfVtx",   "ndfVtx",  100, 0, 100)
	self.hist_vertex["gen_nJets"] = ROOT.TH1F("gen_nJets",   "nJets",  100, 0, 100)
	self.hist_vertex["nJets"] = ROOT.TH1F("nJets",   "nJets",  100, 0, 100)
#######        
	self.hist_pre["trackD0"] =  ROOT.TH1F("tracksD0",   "tracksD0",  2000, -10, 10)
 	self.hist_pre["trackD0Err"] =  ROOT.TH1F("tracksD0Err",   "tracksD0Err",  1000, 0, 10)
        self.hist_pre["trackD0Significance"] =  ROOT.TH1F("tracksD0Significance",   "tracksD0Sig",  2000, -100, 100)
	self.hist_pre["trackDz"] =  ROOT.TH1F("tracksDz",   "tracksDz",  20000, -100 , 100)
        self.hist_pre["trackDzErr"] =  ROOT.TH1F("tracksDzErr",   "tracksDzErr",  1000, 0, 10)
        self.hist_pre["trackDzSignificance"] =  ROOT.TH1F("tracksDzSignificance",   "tracksDzSig",  2000, -100, 100)

        self.hist_pre["trackPt"] =  ROOT.TH1F("tracksPt",   "tracksPt",  5000, 0, 500) 
	self.hist_pre["trackPtErr"] =  ROOT.TH1F("tracksPtErr",   "tracksPtErr",  5000, 0, 50)	
        self.hist_pre["trackPtSigma"] =  ROOT.TH1F("tracksPtSigma",   "tracksPtSigma",  5000, 0, 50)

	self.hist_pre["trackEta"] =  ROOT.TH1F("tracksEta",   "tracksEta",  100, -5, 5)
	self.hist_pre["trackPhi"] =  ROOT.TH1F("tracksPhi",   "tracksPhi",  628, -3.14, 3.14)
        self.hist_pre["trackDeltaPhi"] =  ROOT.TH1F("tracksDeltaPhi",   "tracksDeltaPhi",  62800, -3.14, 3.14)

	self.hist_pre["purity"] =  ROOT.TH1F("purity",   "purity",  2, 0., 2)
	self.hist_pre["imp0"] =  ROOT.TH1F("imp0",   "imp0",  2, 0., 2)
	self.hist_pre["impz"] =  ROOT.TH1F("impz",   "impz",  2, 0., 2)
	self.hist_pre["dpt"] =  ROOT.TH1F("dpt",   "dpt",  2, 0., 2)
	self.hist_pre["kin"] =  ROOT.TH1F("kin",   "kin",  2, 0., 2)
######
        self.hist_post["trackD0"+p1] =  ROOT.TH1F("tracksD0"+p1,   "tracksD0",  2000, -10, 10)
        self.hist_post["trackD0Err"+p1] =  ROOT.TH1F("tracksD0Err"+p1,   "tracksD0Err",  1000, 0, 10)
        self.hist_post["trackD0Significance"+p1] =  ROOT.TH1F("tracksD0Significance"+p1,   "tracksD0Sig",  2000, -100, 100)
        self.hist_post["trackDz"+p1] =  ROOT.TH1F("tracksDz"+p1,   "tracksD0",  20000, -100 , 100)
        self.hist_post["trackDzErr"+p1] =  ROOT.TH1F("tracksDzErr"+p1,   "tracksDzErr",  1000, 0, 10)
        self.hist_post["trackDzSignificance"+p1] =  ROOT.TH1F("tracksDzSignificance"+p1,   "tracksDzSig",  2000, -100, 100)

        self.hist_post["trackPt"+p1] =  ROOT.TH1F("tracksPt"+p1,   "tracksPt",  5000, 0, 500) 
        self.hist_post["trackPtErr"+p1] =  ROOT.TH1F("tracksPtErr"+p1,   "tracksPtErr",  5000, 0, 50)      
        self.hist_post["trackPtSigma"+p1] =  ROOT.TH1F("tracksPtSigma"+p1,   "tracksPtSigma",  5000, 0, 50)

        self.hist_post["trackEta"+p1] =  ROOT.TH1F("tracksEta"+p1,   "tracksEta",  100, -5, 5)
        self.hist_post["trackPhi"+p1] =  ROOT.TH1F("tracksPhi"+p1,   "tracksPhi",  628, -3.14, 3.14)
        self.hist_post["trackDeltaPhi"+p1] =  ROOT.TH1F("tracksDeltaPhi"+p1,   "tracksDeltaPhi",  62800, -3.14, 3.14)

	self.hist_gen["gen_trackDeltaPhi"] =  ROOT.TH1F("gen_tracksDeltaPhi",   "tracksDeltaPhi",  62800, -3.14, 3.14)
        self.hist_gen["gen_trackPt"] =  ROOT.TH1F("gen_tracksPt",   "tracksPt",  5000, 0, 500)
	self.hist_gen["gen_trackEta"] =  ROOT.TH1F("gen_tracksEta",   "tracksEta",  100, -5, 5)
        self.hist_gen["gen_trackPhi"] =  ROOT.TH1F("gen_tracksPhi",   "tracksPhi",  628, -3.14, 3.14)

######
	self.hist["gen_ptSisCone5"] =  ROOT.TH1F("gen_pt_SisCone5",   "ptTrackJets",  200, 0, 200)
        self.hist["gen_etaSisCone5"] =  ROOT.TH1F("gen_eta_SisCone5",   "etaTrackJets",  100 , -5, 5)
        self.hist["gen_phiSisCone5"] =  ROOT.TH1F("gen_phi_SisCone5",   "phiTrackJets",  628 , -3.14, 3.14)

        self.hist_jet["ptSisCone5"] =  ROOT.TH1F("pt_SisCone5",   "ptTrackJets",  200, 0, 200)
	self.hist_jet["etaSisCone5"] =  ROOT.TH1F("eta_SisCone5",   "etaTrackJets",  100 , -5, 5)
	self.hist_jet["phiSisCone5"] =  ROOT.TH1F("phi_SisCone5",   "phiTrackJets",  628 , -3.14, 3.14)
	self.hist_jet["nTracksSisCone5"] =  ROOT.TH1F("nTracks_SisCone5",   "nTracks_TracksJets",  100 , 0, 100)

	self.hist["gen_nJetTracks"] =  ROOT.TH1F("gen_nJetTracks",   "nTracks_TracksJets",  100 , 0, 100)

#	self.hist["ptSisCone7"] =  ROOT.TH1F("pt_SisCone7",   "ptTrackJets",  20, 0, 20)

#        self.hist["ptak5"] =  ROOT.TH1F("pt_ak5",   "ptTrackJets",  20, 0, 20)
#        self.hist["ptak7"] =  ROOT.TH1F("pt_ak7",   "ptTrackJets",  20, 0, 20) 
  
	self.hist["gen_nTot_SisCone5"] = ROOT.TH2F("gen_nTot_SisCone5",   "n_tot",  800, -0.5,799.5,400, 0, 200)
	self.hist_gent["gen_nTrans_SisCone5"] = ROOT.TH2F("gen_nTrans_SisCone5",   "n_trans",  80,-0.5,79.5,400, 0, 200)
        self.hist_gent["gen_ptTrans_SisCone5"] = ROOT.TH2F("gen_ptTrans_SisCone5",   "n_trans",  400, 0.,40.,400, 0, 200)
	self.hist_gent["gen_nTransMax_SisCone5"] = ROOT.TH2F("gen_nTransMax_SisCone5",   "n_trans",  80, -0.5,79.5,400, 0, 200)
        self.hist_gent["gen_ptTransMax_SisCone5"] = ROOT.TH2F("gen_ptTransMax_SisCone5",   "n_trans",  400, 0.,40.,400, 0, 200)

        self.hist_gent["gen_nTransMin_SisCone5"] = ROOT.TH2F("gen_nTransMin_SisCone5",   "n_trans",  80, -0.5,79.5,400, 0, 200)
        self.hist_gent["gen_ptTransMin_SisCone5"] = ROOT.TH2F("gen_ptTransMin_SisCone5",   "n_trans",  400, 0.,40.,200, 0, 100) 

        self.hist_gent["gen_nTransDiff_SisCone5"] = ROOT.TH2F("gen_nTransDiff_SisCone5",   "n_trans",  160, -80.5,79.5,400, 0, 200)
        self.hist_gent["gen_ptTransDiff_SisCone5"] = ROOT.TH2F("gen_ptTransDiff_SisCone5",   "n_trans",  160, -80.5,79.5,200, 0, 100)


        self.hist_genaway["gen_nAway_SisCone5"] = ROOT.TH2F("gen_nAway_SisCone5",   "n_away",  80, -0.5,79.5,200, 0, 100)
        self.hist_genaway["gen_ptAway_SisCone5"] = ROOT.TH2F("gen_ptAway_SisCone5",   "pt_away",  1000, 0.,10.,200, 0, 100)

        self.hist_gentow["gen_nTow_SisCone5"] = ROOT.TH2F("gen_nTow_SisCone5",   "n_tow",  80, -0.5,79.5,200, 0, 100)
        self.hist_gentow["gen_ptTow_SisCone5"] = ROOT.TH2F("gen_ptTow_SisCone5",   "pt_tow",  80, -0.5,79.5,200, 0, 100)


        self.hist_jet["nTot_SisCone5"] = ROOT.TH2F("nTot_SisCone5",   "n_tot",  800, -0.5,799.5,400, 0, 200)

	self.hist_trans["nTrans_SisCone5"] = ROOT.TH2F("nTrans_SisCone5",   "n_trans",  80, -0.5,79.5,400, 0, 200)
        self.hist_trans["ptTrans_SisCone5"] = ROOT.TH2F("ptTrans_SisCone5",   "pt_trans",  400, 0.,40.,200, 0, 100)
	
	self.hist_trans["nTransMax_SisCone5"] = ROOT.TH2F("nTransMax_SisCone5",   "n_trans",  80, -0.5,79.5,400, 0, 200)
        self.hist_trans["ptTransMax_SisCone5"] = ROOT.TH2F("ptTransMax_SisCone5",   "pt_trans",  400, 0.,40.,200, 0, 100)
	
	self.hist_trans["nTransMin_SisCone5"] = ROOT.TH2F("nTransMin_SisCone5",   "n_trans",  80, -0.5,79.5,400, 0, 200)
        self.hist_trans["ptTransMin_SisCone5"] = ROOT.TH2F("ptTransMin_SisCone5",   "pt_trans",  400, 0.,40.,200, 0, 100)		

        self.hist_trans["nTransDiff_SisCone5"] = ROOT.TH2F("nTransDiff_SisCone5",   "n_trans",  160, -80.5,79.5,400, 0, 200)
        self.hist_trans["ptTransDiff_SisCone5"] = ROOT.TH2F("ptTransDiff_SisCone5",   "pt_trans",  160, -80.,80.,200, 0, 100)

        self.hist_away["nAway_SisCone5"] = ROOT.TH2F("nAway_SisCone5",   "n_away",  80, -0.5,79.5,200, 0, 100)
        self.hist_away["ptAway_SisCone5"] = ROOT.TH2F("ptAway_SisCone5",   "pt_away",  1000, 0.,10.,200, 0, 100)

        self.hist_tow["nTow_SisCone5"] = ROOT.TH2F("nTow_SisCone5",   "n_tow",  80, -0.5,79.5,200, 0, 100)
        self.hist_tow["ptTow_SisCone5"] = ROOT.TH2F("ptTow_SisCone5",   "pt_tow",  1000, 0.,10.,200, 0, 100)

        for h in self.hist:
            self.hist[h].Sumw2()
            self.GetOutputList().Add(self.hist[h])
	for h in self.hist_vertex:
            self.hist_vertex[h].Sumw2()
            self.GetOutputList().Add(self.hist_vertex[h])
	for h in self.hist_gen:
            self.hist_gen[h].Sumw2()
            self.GetOutputList().Add(self.hist_gen[h])
	for h in self.hist_gent:
            self.hist_gent[h].Sumw2()
            self.GetOutputList().Add(self.hist_gent[h])
	for h in self.hist_trans:
            self.hist_trans[h].Sumw2()
            self.GetOutputList().Add(self.hist_trans[h])
	for h in self.hist_pre:
            self.hist_pre[h].Sumw2()
            self.GetOutputList().Add(self.hist_pre[h])
	for h in self.hist_post:
            self.hist_post[h].Sumw2()
            self.GetOutputList().Add(self.hist_post[h])	
	for h in self.hist_jet:
            self.hist_jet[h].Sumw2()
            self.GetOutputList().Add(self.hist_jet[h])
	for h in self.hist_tow:
            self.hist_tow[h].Sumw2()
            self.GetOutputList().Add(self.hist_tow[h])
	for h in self.hist_away:
            self.hist_away[h].Sumw2()
            self.GetOutputList().Add(self.hist_away[h])
	for h in self.hist_gentow:
            self.hist_gentow[h].Sumw2()
            self.GetOutputList().Add(self.hist_gentow[h])
        for h in self.hist_genaway:
            self.hist_genaway[h].Sumw2()
            self.GetOutputList().Add(self.hist_genaway[h])
	for h in self.hist_full_genjet:
            self.hist_full_genjet[h].Sumw2()
            self.GetOutputList().Add(self.hist_full_genjet[h])	
	for h in self.hist_full_gentracks:
            self.hist_full_gentracks[h].Sumw2()
            self.GetOutputList().Add(self.hist_full_gentracks[h])
	for h in self.hist_full_jet:
            self.hist_full_jet[h].Sumw2()
            self.GetOutputList().Add(self.hist_full_jet[h])
        for h in self.hist_full_tracks:
            self.hist_full_tracks[h].Sumw2()
            self.GetOutputList().Add(self.hist_full_tracks[h])


	 	

        self.Trans_SisCon5["nTransDensity"] = ROOT.TProfile("nTransDensity_SisCon5",   "n_trans",  200, 0, 100)
        self.Trans_SisCon5["ptTransDensity"] = ROOT.TProfile("ptTransDensity_SisCon5",   "pt_trans",  200, 0, 100)
	self.Trans_SisCon5["nTow"] = ROOT.TProfile("nTow_SisCon5",   "n_tow",  200, 0, 100)
        self.Trans_SisCon5["nAway"] = ROOT.TProfile("nAway_SisCon5",   "n_away",  200, 0, 100)
        self.Trans_SisCon5["ptTow"] = ROOT.TProfile("ptTow_SisCon5",   "pt_tow",  200, 0, 100)
        self.Trans_SisCon5["ptAway"] = ROOT.TProfile("ptAway_SisCon5",   "pt_away",  200, 0, 100)
        self.Trans_SisCon5["nTot"] = ROOT.TProfile("nTot_SisCon5",   "pt_away",  200, 0, 100)
        self.Trans_SisCon5["ptTot"] = ROOT.TProfile("ptTot_SisCon5",   "pt_away",  200, 0, 100)

        self.Trans_SisCon5["gen_nTransDensity"] = ROOT.TProfile("gen_nTransDensity_SisCon5",   "n_trans",  200, 0, 100)
        self.Trans_SisCon5["gen_ptTransDensity"] = ROOT.TProfile("gen_ptTransDensity_SisCon5",   "pt_trans",  200, 0, 100)
	self.Trans_SisCon5["gen_nTow"] = ROOT.TProfile("gen_nTow_SisCon5",   "n_tow",  200, 0, 100)
        self.Trans_SisCon5["gen_nAway"] = ROOT.TProfile("gen_nAway_SisCon5",   "n_away",  200, 0, 100)
        self.Trans_SisCon5["gen_ptTow"] = ROOT.TProfile("gen_ptTow_SisCon5",   "pt_tow",  200, 0, 100)
        self.Trans_SisCon5["gen_ptAway"] = ROOT.TProfile("gen_ptAway_SisCon5",   "pt_away",  200, 0, 100)
        self.Trans_SisCon5["gen_nTot"] = ROOT.TProfile("gen_nTot_SisCon5",   "pt_away",  200, 0, 100)
        self.Trans_SisCon5["gen_ptTot"] = ROOT.TProfile("gen_ptTot_SisCon5",   "pt_away",  200, 0, 100)


	for h in self.Trans_SisCon5:
            self.Trans_SisCon5[h].Sumw2()
            self.GetOutputList().Add(self.Trans_SisCon5[h])	

        self.other_SisCon5["nTransMax"] = ROOT.TProfile("nTransMax_SisCon5",   "n_trans",  200, 0, 100)
        self.other_SisCon5["nTransMin"] = ROOT.TProfile("nTransMin_SisCon5",   "n_trans",  200, 0, 100)
	self.other_SisCon5["ptTransMax"] = ROOT.TProfile("ptTransMax_SisCon5",   "pt_trans",  200, 0, 100)
        self.other_SisCon5["ptTransMin"] = ROOT.TProfile("ptTransMin_SisCon5",   "pt_trans",  200, 0, 100)
	self.other_SisCon5["nDiff"] = ROOT.TProfile("nDiff_SisCon5",   "pt_diff",  200, 0, 100)
        self.other_SisCon5["ptDiff"] = ROOT.TProfile("ptDiff_SisCon5",   "pt_diff",  200, 0, 100)

        self.other_SisCon5["gen_nTransMax"] = ROOT.TProfile("gen_nTransMax_SisCon5",   "n_trans",  200, 0, 100)
        self.other_SisCon5["gen_nTransMin"] = ROOT.TProfile("gen_nTransMin_SisCon5",   "n_trans",  200, 0, 100)
	self.other_SisCon5["gen_ptTransMax"] = ROOT.TProfile("gen_ptTransMax_SisCon5",   "pt_trans",  200, 0, 100)
        self.other_SisCon5["gen_ptTransMin"] = ROOT.TProfile("gen_ptTransMin_SisCon5",   "pt_trans",  200, 0, 100)
	self.other_SisCon5["gen_nDiff"] = ROOT.TProfile("gen_nDiff_SisCon5",   "pt_diff",  200, 0, 100)
        self.other_SisCon5["gen_ptDiff"] = ROOT.TProfile("gen_ptDiff_SisCon5",   "pt_diff",  200, 0, 100)		

        for h in self.other_SisCon5:
            self.other_SisCon5[h].Sumw2()
            self.GetOutputList().Add(self.other_SisCon5[h])
         
        #self.eventCounter = 0

    def analyze(self):
        # note: use printTTree.py asamplename in order to learn what tries/branches are avaliable

        weight = 1 # 
        num = 0
        #self.hist["numGenTracks"].Fill(num, weight)
        #for t in self.fChain.genParticlesp4: # this collection contains four-momenta of charged genparticles
        #    self.hist["etaGenTracks"].Fill(t.eta(), weight)

        # consistency xcheck
        ''' - disabled
        sizes = set()
        sizes.add(self.fChain.dxy.size())
        sizes.add(self.fChain.dz.size())
        sizes.add(self.fChain.recoTracks.size())
        sizes.add(self.fChain.testTrkData.size())
        if len(sizes)!= 1:
            print "Wrong collection lengths:", sizes
            raise Exception("Inonsistent data")
        # '''

        #for i in xrange(0, self.fChain.dz.size()):
        #for i in xrange(0, self.fChain.testTrkData.size()):
        #for i in xrange(0, self.fChain.recoTracksp4.size()):
         #   self.hist["etaRecoTracks"].Fill(self.fChain.recoTracksp4.at(i).eta())
            
        sumpt_gen=0.
        pt_gen=-1.
        dphi_gen=999
	phi_gen=0
        eta_gen=999
        n_gen=0.
        ntracks_gen=0
        n_tow_gen=0.
        sumpt_tow_gen=0.
        n_away_gen=0.
        sumpt_away_gen=0.
	n_tot_gen=0.

        sumpt1_gen=0
        sumpt2_gen=0
        n1_gen=0
        n2_gen=0
        sumpt_max_gen=0
        sumpt_min_gen=0
        n_max_gen=0
        n_min_gen=0

        nconst=0


        weight = 1  
        num = 0

        numgoodvtx = 0
	nu=0

        vtx_x=0
        vtx_y=0
	vtx_z=0

        #SUNIL
        bGen_pTLeadTrack[0] = -999
        bGen_etaLeadTrack[0] = -999
        bGen_phiLeadTrack[0] = -999
        bGen_evtTrue_LeadTrack[0] = -100

        bGen_nChg_pTLeadTrack_away[0]         = 0
        bGen_nChg_pTLeadTrack_towards[0]      = 0
        bGen_nChg_pTLeadTrack_trans[0]        = 0
        bGen_nChg_pTLeadTrack_transMin[0]     = 0
        bGen_nChg_pTLeadTrack_transMax[0]     = 0
        bGen_nChg_pTLeadTrack_transDiff[0]    = 0
        bGen_pTSum_pTLeadTrack_away[0]        = 0
        bGen_pTSum_pTLeadTrack_towards[0]     = 0
        bGen_pTSum_pTLeadTrack_trans[0]       = 0
        bGen_pTSum_pTLeadTrack_transMin[0]    = 0
        bGen_pTSum_pTLeadTrack_transMax[0]    = 0
        bGen_pTSum_pTLeadTrack_transDiff[0]   = 0
        #/SUNIL

        #SUNIL
        bRec_pTLeadTrack[0] = -999
        bRec_etaLeadTrack[0] = -999
        bRec_phiLeadTrack[0] = -999
        bRec_evtTrue_LeadTrack[0] = -100

        bRec_nChg_pTLeadTrack_away[0]         = 0
        bRec_nChg_pTLeadTrack_towards[0]      = 0
        bRec_nChg_pTLeadTrack_trans[0]        = 0
        bRec_nChg_pTLeadTrack_transMin[0]     = 0
        bRec_nChg_pTLeadTrack_transMax[0]     = 0
        bRec_nChg_pTLeadTrack_transDiff[0]    = 0
        bRec_pTSum_pTLeadTrack_away[0]        = 0
        bRec_pTSum_pTLeadTrack_towards[0]     = 0
        bRec_pTSum_pTLeadTrack_trans[0]       = 0
        bRec_pTSum_pTLeadTrack_transMin[0]    = 0
        bRec_pTSum_pTLeadTrack_transMax[0]    = 0
        bRec_pTSum_pTLeadTrack_transDiff[0]   = 0
        #/SUNIL
















        #GEN
        #if True:  
         #self.eventCounter += 1
         #if self.eventCounter == 100: sys.exit("You have set the program to exit at 100 events!")
        
        sumpt=0.
        pt=-1.
        dphi=999
	phi=0
        eta=999
        n=0.
        ntracks=0
        n_tow=0.
        sumpt_tow=0.
        n_away=0.
        sumpt_away=0.

	sumpt1=0
	sumpt2=0
	n1=0
	n2=0
	sumpt_max=0
	sumpt_min=0
	n_max=0
	n_min=0
	
	ptLeading=0
	phiLeading=0
	etaLeading=0

	ptf=0
	phif=0
	etaf=0

        #DR DR DR: Can add a check to initialize these only if not self.jetMode, but doesn't really matter.
        l_trd0Err=[]
	l_trdzErr=[]
        l_trptErr=[]

	l_trx=[]
	l_try=[]		
	l_trz=[]

	l_trd0= []
	l_trdz=  []

        l_trHighPurity = []

        l_trGood = []


	#self.hist_vertex["nJets"].Fill(self.fChain.SisCone5CHp4.size())
        

        sumpt_gen=0.
        pt_gen=-1.
        dphi_gen=999
	phi_gen=0
        eta_gen=999
        n_gen=0.
        ntracks_gen=0
        n_tow_gen=0.
        sumpt_tow_gen=0.
        n_away_gen=0.
        sumpt_away_gen=0.
	n_tot_gen=0.

        sumpt1_gen=0
        sumpt2_gen=0
        n1_gen=0
        n2_gen=0
        sumpt_max_gen=0
        sumpt_min_gen=0
        n_max_gen=0
        n_min_gen=0

        nconst=0


        weight = 1  
        num = 0

        numgoodvtx = 0
	nu=0

        vtx_x=0
        vtx_y=0
	vtx_z=0


        #goAhead is universally used to determine if a given loop should proceed.
	goAhead = True
	if self.dataMode: goAhead = False
        if self.nogenMode: goAhead = False

	if goAhead:
            #Define leading object properties.
            #JET MODE
            if self.jetMode:
                leadObjSize = self.fChain.sisCone5ChgGenJetsp4.size()
                leadObjp4 = self.fChain.sisCone5ChgGenJetsp4
                nJetTracks = self.fChain.sisCone5ChgGenJetsnConst
                ptMin = 1
            #TRACK MODE
            else:
                leadObjSize = self.fChain.genParticlesp4.size()
                leadObjp4 = self.fChain.genParticlesp4
                nJetTracks = self.fChain.genParticlespdg #This is just an unused placeholder.
                ptMin = 0.5

	    #LEADING OBJECT LOOP
	    for i in xrange(0, leadObjSize): #DR

               #JET MODE
               if self.jetMode:
                   trackp4 = leadObjp4.at(i)
                   #find leading jet with no cuts
                   if trackp4.pt()>ptf:
                       ptf=trackp4.pt()
                       phif=trackp4.phi()
                       etaf=trackp4.eta()
                   #find leading jet with cuts
                   if trackp4.pt()>ptLeading and nJetTracks.at(i) > 1 and trackp4.pt() > ptMin and math.fabs(trackp4.eta()) < self.etaCut:
                       ptLeading=trackp4.pt()
                       phiLeading=trackp4.phi()
                       etaLeading=trackp4.eta()
                       ntracks=nJetTracks.at(i)

               #TRACK MODE
               if not self.jetMode:
                   track = leadObjp4.at(i) #DR
                   if track.pt()>ptMin and math.fabs(track.eta())<self.etaCut and not self.fChain.genParticlescharge == 0:
                       if track.pt()>ptLeading:
                           ptLeading=track.pt()
                           phiLeading=track.phi()
                           etaLeading=track.eta()

            #/LEADING OBJECT LOOP


            #Fill histograms for leading object without cuts.  These values stay as zero in leading track mode.
	    self.hist_full_genjet["fgen_ptSisCone5"].Fill(ptf)
            self.hist_full_genjet["fgen_phiSisCone5"].Fill(phif)
            self.hist_full_genjet["fgen_etaSisCone5"].Fill(etaf)


            #Proceed with particle loop only if there is a leading object.
            if not ptLeading < ptMin and math.fabs(etaLeading)<self.etaCut:
                self.hist["gen_ptSisCone5"].Fill(ptLeading)
		self.hist["gen_phiSisCone5"].Fill(phiLeading)
		self.hist["gen_etaSisCone5"].Fill(etaLeading)
		self.hist["gen_nJetTracks"].Fill(ntracks)

                #SUNIL
                bGen_pTLeadTrack[0] = ptLeading
                bGen_etaLeadTrack[0] = etaLeading
                bGen_phiLeadTrack[0] = phiLeading
                #/SUNIL

                #PARTICLE LOOP
                for i in xrange(0, self.fChain.genParticlesp4.size()):
		  track= self.fChain.genParticlesp4.at(i)

		  dphi_gen=track.phi()-phiLeading
                  while dphi_gen > math.pi:
                         dphi_gen=dphi_gen-2*math.pi
                  while dphi_gen < -math.pi:
                         dphi_gen=dphi_gen+2*math.pi

		
		  self.hist_gen["gen_trackPt"].Fill(track.pt())
		  self.hist_gen["gen_trackEta"].Fill(track.eta())
		  self.hist_gen["gen_trackPhi"].Fill(track.phi())
		  self.hist_gen["gen_trackDeltaPhi"].Fill(dphi_gen)



                  #Don't be tempted to change that 0.5 to ptMin.  Different min values are used for leading object and particles in jet mode!
		  if track.pt()>0.5 and math.fabs(track.eta())<self.etaCut:	
			if not ptLeading < ptMin and math.fabs(etaLeading)<self.etaCut:
			   
                           if (dphi_gen > math.pi/3. and dphi_gen < 2*math.pi/3.):
                            n_gen=n_gen+1.
			    sumpt_gen=sumpt_gen+track.pt()

			    n1_gen=n1_gen+1
			    sumpt1_gen=sumpt1_gen+track.pt()		    			   

			   if (dphi_gen < -math.pi/3. and dphi_gen > -2*math.pi/3.):	
			    n_gen=n_gen+1.
                            sumpt_gen=sumpt_gen+track.pt()				   
	 		
			    n2_gen=n2_gen+1
			    sumpt2_gen=sumpt2_gen+track.pt()

			   if (dphi_gen < math.pi/3. and dphi_gen > -math.pi/3):
			    n_tow_gen=n_tow_gen+1
			    sumpt_tow_gen=sumpt_tow_gen+track.pt()	

			   if (dphi_gen > 2*math.pi/3. or dphi_gen < -2*math.pi/3):
			    n_away_gen=n_away_gen+1
                            sumpt_away_gen=sumpt_away_gen+track.pt()

                #\PARTICLE LOOP

                #print "individual n", n_gen, n_tow_gen, n_away_gen
                #print "total n", n_gen+n_tow_gen+n_away_gen

                #Pretty sure this is a redundant check.
		if n_gen+n_tow_gen+n_away_gen>-1:

  	    	 self.hist["gen_nTot_SisCone5"].Fill(n_gen+n_tow_gen+n_away_gen,ptLeading)
                 self.Trans_SisCon5["gen_nTot"].Fill(ptLeading,n_gen+n_tow_gen+n_away_gen)

                 self.Trans_SisCon5["gen_ptTot"].Fill(ptLeading,sumpt_gen+sumpt_away_gen+sumpt_tow_gen)

                 self.hist_gent["gen_nTrans_SisCone5"].Fill(n_gen,ptLeading)
		 self.Trans_SisCon5["gen_nTransDensity"].Fill(ptLeading,n_gen)

                 self.Trans_SisCon5["gen_ptTransDensity"].Fill(ptLeading,sumpt_gen)
                 self.hist_gent["gen_ptTrans_SisCone5"].Fill(sumpt_gen,ptLeading)
	
		 if sumpt1_gen>sumpt2_gen:
			sumpt_max_gen=sumpt1_gen
			sumpt_min_gen=sumpt2_gen
		 else :
			sumpt_max_gen=sumpt2_gen
                        sumpt_min_gen=sumpt1_gen
		 if n1_gen>n2_gen:
                        n_max_gen=n1_gen
                        n_min_gen=n2_gen
                 else :
                        n_max_gen=n2_gen
                        n_min_gen=n1_gen
  
		 self.hist_gent["gen_nTransMax_SisCone5"].Fill(n_max_gen,ptLeading)
                 self.other_SisCon5["gen_nTransMax"].Fill(ptLeading,n_max_gen)
		  	
                 self.hist_gent["gen_ptTransMax_SisCone5"].Fill(sumpt_max_gen,ptLeading)
	         self.other_SisCon5["gen_ptTransMax"].Fill(ptLeading,sumpt_max_gen)  

                 self.hist_gent["gen_nTransMin_SisCone5"].Fill(n_min_gen,ptLeading)
		 self.other_SisCon5["gen_nTransMin"].Fill(ptLeading,n_min_gen)  
			
                 self.hist_gent["gen_ptTransMin_SisCone5"].Fill(sumpt_min_gen,ptLeading)	
		 self.other_SisCon5["gen_ptTransMin"].Fill(ptLeading,sumpt_min_gen)

		 self.hist_gent["gen_nTransDiff_SisCone5"].Fill(-n_min_gen+n_max_gen,ptLeading)
		 self.other_SisCon5["gen_nDiff"].Fill(ptLeading,-n_min_gen+n_max_gen)

                 self.hist_gent["gen_ptTransDiff_SisCone5"].Fill(-sumpt_min_gen+sumpt_max_gen,ptLeading)
		 self.other_SisCon5["gen_ptDiff"].Fill(ptLeading,-sumpt_min_gen+sumpt_max_gen)	

		 self.hist_gentow["gen_nTow_SisCone5"].Fill(n_tow_gen,ptLeading)
		 self.Trans_SisCon5["gen_nTow"].Fill(ptLeading,n_tow_gen)
			
                 self.hist_gentow["gen_ptTow_SisCone5"].Fill(sumpt_tow_gen,ptLeading)
		 self.Trans_SisCon5["gen_ptTow"].Fill(ptLeading,sumpt_tow_gen)	

		 self.hist_genaway["gen_nAway_SisCone5"].Fill(n_away_gen,ptLeading)
		 self.Trans_SisCon5["gen_nAway"].Fill(ptLeading,n_away_gen)

                 self.hist_genaway["gen_ptAway_SisCone5"].Fill(sumpt_away_gen,ptLeading)
		 self.Trans_SisCon5["gen_ptAway"].Fill(ptLeading,sumpt_away_gen)	

                 #SUNIL
                 bGen_nChg_pTLeadTrack_away[0]         = n_away_gen
                 bGen_nChg_pTLeadTrack_towards[0]      = n_tow_gen
                 bGen_nChg_pTLeadTrack_trans[0]        = n_gen
                 bGen_nChg_pTLeadTrack_transMin[0]     = n_min_gen
                 bGen_nChg_pTLeadTrack_transMax[0]     = n_max_gen
                 bGen_nChg_pTLeadTrack_transDiff[0]    = -n_min_gen + n_max_gen
                 bGen_pTSum_pTLeadTrack_away[0]        = sumpt_away_gen
                 bGen_pTSum_pTLeadTrack_towards[0]     = sumpt_tow_gen
                 bGen_pTSum_pTLeadTrack_trans[0]       = sumpt_gen
                 bGen_pTSum_pTLeadTrack_transMin[0]    = sumpt_min_gen
                 bGen_pTSum_pTLeadTrack_transMax[0]    = sumpt_max_gen
                 bGen_pTSum_pTLeadTrack_transDiff[0]   = -sumpt_min_gen + sumpt_max_gen
                 bGen_evtTrue_LeadTrack[0]             = 100

             #/GEN





























        #RECO

        goAhead = False
        if self.dataMode: 
            goAhead = self.fChain.lumi >= 90 #and self.fChain.trgZeroBias == 1
        else:
            goAhead = True
        if self.genMode: goAhead = False

        #DEBUG (this line of code is useful for analyzing and printing out stats from just one event):
        #if(self.fChain.event != 100304082 ): goAhead = False;

        if goAhead:  

         #VERTEX LOOP
         for i in xrange(0, self.fChain.vtxisFake.size()):
                    
                    vtxrho = math.sqrt(self.fChain.vtxx.at(i)*self.fChain.vtxx.at(i) + self.fChain.vtxy.at(i)*self.fChain.vtxy.at(i))

		    nu=nu+1	

                    if not self.fChain.vtxisFake.at(i) and abs(self.fChain.vtxz.at(i) - self.fChain.vtxzBS.at(i) ) <= 10 and self.fChain.vtxndof.at(i) > self.ndofCut and vtxrho <= 2: # count only good primary vertices

                        numgoodvtx+=1
			if numgoodvtx==1:
			 vtx_x=self.fChain.vtxx.at(i)
			 vtx_y=self.fChain.vtxy.at(i)
			 vtx_z=self.fChain.vtxz.at(i)

			 #These can be re-implemented if we want to calculate impact param sig using vertex error as well.
			 #vtx_x_Err=self.fChain.vtxxErr.at(i)
			 #vtx_y_Err=self.fChain.vtxyErr.at(i)
			 #vtx_z_Err=self.fChain.vtxzErr.at(i)

			self.hist_vertex["ndfVtx"].Fill(self.fChain.vtxndof.at(i))	


        #/VERTEX LOOP

        self.hist_vertex["nVtx"].Fill(numgoodvtx) 

        #print "Event", self.eventCounter
        #print "good vertex?", numgoodvtx
        sumpt=0.
        pt=-1.
        dphi=999
	phi=0
        eta=999
        n=0.
        ntracks=0
        n_tow=0.
        sumpt_tow=0.
        n_away=0.
        sumpt_away=0.

	sumpt1=0
	sumpt2=0
	n1=0
	n2=0
	sumpt_max=0
	sumpt_min=0
	n_max=0
	n_min=0
	
	ptLeading=0
	phiLeading=0
	etaLeading=0

	ptf=0
	phif=0
	etaf=0

        #DR DR DR: Can add a check to initialize these only if not self.jetMode
        l_trd0Err=[]
	l_trdzErr=[]
        l_trptErr=[]

	l_trx=[]
	l_try=[]		
	l_trz=[]

	l_trd0= []
	l_trdz=  []

        l_trHighPurity = []

        l_trGood = []


	self.hist_vertex["nJets"].Fill(self.fChain.SisCone5CHp4.size())

        #DR
        #JET MODE
        if self.jetMode:
            leadObjSize = self.fChain.SisCone5CHp4.size()
            leadObjp4 = self.fChain.SisCone5CHp4
            nJetTracks = self.fChain.SisCone5CHnConst
            ptMin = 1
        #TRACK MODE
        else:
            leadObjSize = self.fChain.recoTracksp4.size()
            leadObjp4 = self.fChain.recoTracksp4
            nJetTracks = self.fChain.recoTracksnValidHits #This is a bit of an awkward placeholder for an observable tracks don't need.
            ptMin = 0.5

	#LEADING OBJECT LOOP
        if numgoodvtx == 1:
            for i in xrange(0, leadObjSize): #DR

                    #JET MODE
                    if self.jetMode:
                        trackp4 = leadObjp4.at(i) #DR
                        #find leading jet with no cuts
                        if trackp4.pt()>ptf:
                            ptf=trackp4.pt()
                            phif=trackp4.phi()
                            etaf=trackp4.eta()
                        #find leading jet with cuts
                        if trackp4.pt()>ptLeading and nJetTracks.at(i) > 1 and trackp4.pt() > ptMin and math.fabs(trackp4.eta()) < self.etaCut:  
                            ptLeading=trackp4.pt()
                            phiLeading=trackp4.phi()
                            etaLeading=trackp4.eta()

                    #TRACK MODE
                    if not self.jetMode:
		        track = self.fChain.recoTracksp4.at(i)

			#More sophisticated error calculation if we want to use it.
			#sigma_d0_v_2= (track.py()*vtx_x_Err/track.pt())**2 + (track.px()*vtx_y_Err/track.pt())**2
                        #l_trd0Err.append( math.sqrt( (self.fChain.recoTracksd0Err.at(i))**2 +  sigma_d0_v_2) )
	                #l_trdzErr.append( math.sqrt( (self.fChain.recoTracksdzErr.at(i))**2 + vtx_z_Err**2 ) )	

                        l_trd0Err.append( self.fChain.recoTracksd0Err.at(i) )
	                l_trdzErr.append( self.fChain.recoTracksdzErr.at(i) )	
                        l_trptErr.append( self.fChain.recoTracksptErr.at(i) )

	                l_trx.append( self.fChain.recoTracksvx.at(i) )
	                l_try.append( self.fChain.recoTracksvy.at(i) )	
	                l_trz.append( self.fChain.recoTracksvz.at(i) )

		        tr_x=self.fChain.recoTracksvx.at(i)
		        tr_y=self.fChain.recoTracksvy.at(i)		
		        tr_z=self.fChain.recoTracksvz.at(i) 

	                l_trd0.append( (- (tr_x-vtx_x) * track.py() + (tr_y-vtx_y) * track.px() ) / track.pt()  )

	                l_trdz.append(  (tr_z-vtx_z) - ((tr_x-vtx_x)*track.px()+(tr_y-vtx_y)*track.py())/track.pt() * (track.pz()/track.pt())	 )

                        l_trHighPurity.append( self.fChain.recoTrackshighPurity.at(i) )

                        #Initialize to zero.  Check in next lines if the track is good, "1".
                        l_trGood.append( 0 )

		        if math.fabs(l_trd0[i]/l_trd0Err[i])<self.d0Cut:
		            if math.fabs(l_trdz[i]/l_trdzErr[i])<self.dzCut:
		                if l_trptErr[i]/track.pt()<0.05:
                                    if l_trHighPurity[i]:
		                        if track.pt()>ptMin and math.fabs(track.eta())<self.etaCut:
                                            l_trGood[i] = 1

                        if l_trGood[i]:
                            if track.pt()>ptLeading:
                                ptLeading=track.pt()
                                phiLeading=track.phi()
                                etaLeading=track.eta()

                        
                        

        #END LEADING OBJECT LOOP


        #Fill histograms for leading object without cuts.  These values stay as zero in leading track mode.
	self.hist_full_jet["f_ptSisCone5"].Fill(ptf)
        self.hist_full_jet["f_phiSisCone5"].Fill(phif)
        self.hist_full_jet["f_etaSisCone5"].Fill(etaf)

	#PARTICLE LOOP

        #Only proceed if there is exactly one good vertex.
        if numgoodvtx == 1:


            #Only proceed if there is a leading object.
            if not ptLeading < ptMin and math.fabs(etaLeading)<self.etaCut:
                self.hist_jet["ptSisCone5"].Fill(ptLeading)
		self.hist_jet["phiSisCone5"].Fill(phiLeading)
		self.hist_jet["etaSisCone5"].Fill(etaLeading)
		self.hist_jet["nTracksSisCone5"].Fill(ntracks)

                #SUNIL
                bRec_pTLeadTrack[0] = ptLeading
                bRec_etaLeadTrack[0] = etaLeading
                bRec_phiLeadTrack[0] = phiLeading
                #/SUNIL



                #PARTICLE LOOP
                for i in xrange(0, self.fChain.recoTracksd0Err.size()):
		  track= self.fChain.recoTracksp4.at(i)

                  #JET MODE
                  if self.jetMode:

		      #Optional sophisticated error calculation.
	      	      #sigma_d0_v_2= (track.py()*vtx_x_Err/track.pt())**2 + (track.px()*vtx_y_Err/track.pt())**2
		      #tr_d0Err= math.sqrt( self.fChain.recoTracksd0Err.at(i)**2 + sigma_d0_v_2 )
		      #tr_dzErr= math.sqrt( self.fChain.recoTracksdzErr.at(i)**2 + vtx_z_Err**2 ) 

		      tr_d0Err= self.fChain.recoTracksd0Err.at(i)
		      tr_dzErr= self.fChain.recoTracksdzErr.at(i)		
		      tr_ptErr= self.fChain.recoTracksptErr.at(i)	

		      tr_x=self.fChain.recoTracksvx.at(i)
		      tr_y=self.fChain.recoTracksvy.at(i)		
		      tr_z=self.fChain.recoTracksvz.at(i) 

		      tr_d0= (- (tr_x-vtx_x) * track.py() + (tr_y-vtx_y) * track.px() ) / track.pt() 

	              tr_dz=  (tr_z-vtx_z) - ((tr_x-vtx_x)*track.px()+(tr_y-vtx_y)*track.py())/track.pt() * (track.pz()/track.pt())	

                  #TRACK MODE
                  if not self.jetMode:
		      tr_d0Err=l_trd0Err[i]
		      tr_dzErr=l_trdzErr[i]	
		      tr_ptErr=l_trptErr[i]	

		      tr_x=l_trx[i]
		      tr_y=l_try[i]		
		      tr_z=l_trz[i]

		      tr_d0=l_trd0[i]

	              tr_dz=l_trdz[i]

                      #DEBUG
                      #print "event", self.fChain.event
                      #print "pTmax", ptLeading
                      #print "pT   ", track.pt()
                      #print "purity", self.fChain.recoTrackshighPurity.at(i)
                      #print "d0sig", math.fabs(tr_d0/tr_d0Err)
                      #print "dzsig", math.fabs(tr_dz/tr_dzErr)
                      #print "eta", etaLeading
                      #print "i_pTmax", i_ptMax
                      #if not(ptLeading == -1): print "ptErr", self.fChain.recoTracksptErr.at(i)/track.pt()




		  purity=0
        	  imp0= 0
        	  impz= 0
                  dpt= 0
                  kin= 0
		  dphi=track.phi()-phiLeading
                  while dphi > math.pi:
                         dphi=dphi-2*math.pi
                  while dphi < -math.pi:
                         dphi=dphi+2*math.pi

                  #print "FILL 1"	
		  self.hist_pre["trackD0"].Fill(tr_d0)
		  self.hist_pre["trackD0Err"].Fill(tr_d0Err)
		  self.hist_pre["trackD0Significance"].Fill(tr_d0/tr_d0Err)	
		  self.hist_pre["trackDz"].Fill(tr_dz)
                  self.hist_pre["trackDzErr"].Fill(tr_dzErr)
                  self.hist_pre["trackDzSignificance"].Fill(tr_dz/tr_dzErr)	
		  self.hist_pre["trackPt"].Fill(track.pt())
		  self.hist_pre["trackPtErr"].Fill(tr_ptErr)
		  self.hist_pre["trackPtSigma"].Fill(tr_ptErr/track.pt())
		  self.hist_pre["trackEta"].Fill(track.eta())
		  self.hist_pre["trackPhi"].Fill(track.phi())
		  self.hist_pre["trackDeltaPhi"].Fill(dphi)
		  if self.fChain.recoTrackshighPurity.at(i):
		   #purity=1	
		   if math.fabs(tr_d0/tr_d0Err)<self.d0Cut:
		    # imp0=1	
		     if math.fabs(tr_dz/tr_dzErr)<self.dzCut:
		     # impz=1	
		      if tr_ptErr/track.pt()<0.05:
		       #dpt=1	
                       #Again, don't change that 0.5 to ptMin!
		       if track.pt()>0.5 and math.fabs(track.eta())<self.etaCut:	
		  	kin=1
			if not ptLeading < ptMin and math.fabs(etaLeading)<self.etaCut:# and ntracks > 1:	 		
			   self.hist_post["trackD0"+p1].Fill(tr_d0)
                 	   self.hist_post["trackD0Err"+p1].Fill(tr_d0Err)
                 	   self.hist_post["trackD0Significance"+p1].Fill(tr_d0/tr_d0Err)
                 	   self.hist_post["trackDz"+p1].Fill(tr_dz)
                 	   self.hist_post["trackDzErr"+p1].Fill(tr_dzErr)
                  	   self.hist_post["trackDzSignificance"+p1].Fill(tr_dz/tr_dzErr)
                  	   self.hist_post["trackPt"+p1].Fill(track.pt())
                  	   self.hist_post["trackPtErr"+p1].Fill(tr_ptErr)
                  	   self.hist_post["trackPtSigma"+p1].Fill(tr_ptErr/track.pt())
                  	   self.hist_post["trackEta"+p1].Fill(track.eta())
                  	   self.hist_post["trackPhi"+p1].Fill(track.phi())	
                           self.hist_post["trackDeltaPhi"+p1].Fill(dphi)	
			   
                           if (dphi > math.pi/3. and dphi < 2*math.pi/3.):
                            n=n+1.
			    sumpt=sumpt+track.pt()

			    n1=n1+1
			    sumpt1=sumpt1+track.pt()		    			   

			   if (dphi < -math.pi/3. and dphi > -2*math.pi/3.):	
			    n=n+1.
                            sumpt=sumpt+track.pt()				   
	 		
			    n2=n2+1
			    sumpt2=sumpt2+track.pt()

			   if (dphi < math.pi/3. and dphi > -math.pi/3):
			    n_tow=n_tow+1
			    sumpt_tow=sumpt_tow+track.pt()	

			   if (dphi > 2*math.pi/3. or dphi < -2*math.pi/3):
			    n_away=n_away+1
                            sumpt_away=sumpt_away+track.pt()

                  self.hist_pre["purity"].Fill(purity)
        	  self.hist_pre["imp0"].Fill(imp0)
        	  self.hist_pre["impz"].Fill(impz)
                  self.hist_pre["dpt"].Fill(dpt)
                  self.hist_pre["kin"].Fill(kin)
                #print "individual n", n, n_tow, n_away
                #print "total n", n+n_tow+n_away
		if n+n_tow+n_away>-1:
                 #print "FILL 3"
  	    	 self.hist_jet["nTot_SisCone5"].Fill(n+n_tow+n_away,ptLeading)
                 self.Trans_SisCon5["nTot"].Fill(ptLeading,n+n_tow+n_away)

                 self.Trans_SisCon5["ptTot"].Fill(ptLeading,sumpt+sumpt_away+sumpt_tow)
	         #if n+n_tow+n_away>0:
                 self.hist_trans["nTrans_SisCone5"].Fill(n,ptLeading)
		 self.Trans_SisCon5["nTransDensity"].Fill(ptLeading,n)

                 self.Trans_SisCon5["ptTransDensity"].Fill(ptLeading,sumpt)
                 self.hist_trans["ptTrans_SisCone5"].Fill(sumpt,ptLeading)	
		 if sumpt1>sumpt2:
			sumpt_max=sumpt1
			sumpt_min=sumpt2
		 else :
			sumpt_max=sumpt2
                        sumpt_min=sumpt1
		 if n1>n2:
                        n_max=n1
                        n_min=n2
                 else :
                        n_max=n2
                        n_min=n1
  
		 self.hist_trans["nTransMax_SisCone5"].Fill(n_max,ptLeading)
                 self.other_SisCon5["nTransMax"].Fill(ptLeading,n_max)
		  	
                 self.hist_trans["ptTransMax_SisCone5"].Fill(sumpt_max,ptLeading)
	         self.other_SisCon5["ptTransMax"].Fill(ptLeading,sumpt_max)  

                 self.hist_trans["nTransMin_SisCone5"].Fill(n_min,ptLeading)
		 self.other_SisCon5["nTransMin"].Fill(ptLeading,n_min)  
			
                 self.hist_trans["ptTransMin_SisCone5"].Fill(sumpt_min,ptLeading)	
		 self.other_SisCon5["ptTransMin"].Fill(ptLeading,sumpt_min)

		 self.hist_trans["nTransDiff_SisCone5"].Fill(-n_min+n_max,ptLeading)
		 self.other_SisCon5["nDiff"].Fill(ptLeading,-n_min+n_max)

                 self.hist_trans["ptTransDiff_SisCone5"].Fill(-sumpt_min+sumpt_max,ptLeading)
		 self.other_SisCon5["ptDiff"].Fill(ptLeading,-sumpt_min+sumpt_max)	

		 self.hist_tow["nTow_SisCone5"].Fill(n_tow,ptLeading)
		 self.Trans_SisCon5["nTow"].Fill(ptLeading,n_tow)
			
                 self.hist_tow["ptTow_SisCone5"].Fill(sumpt_tow,ptLeading)
		 self.Trans_SisCon5["ptTow"].Fill(ptLeading,sumpt_tow)	

		 self.hist_away["nAway_SisCone5"].Fill(n_away,ptLeading)
		 self.Trans_SisCon5["nAway"].Fill(ptLeading,n_away)

                 self.hist_away["ptAway_SisCone5"].Fill(sumpt_away,ptLeading)
		 self.Trans_SisCon5["ptAway"].Fill(ptLeading,sumpt_away)	

                 #self.hist["eventsGood"].Fill(self.fChain.event)


                 #SUNIL
                 bRec_nChg_pTLeadTrack_away[0]         = n_away
                 bRec_nChg_pTLeadTrack_towards[0]      = n_tow
                 bRec_nChg_pTLeadTrack_trans[0]        = n
                 bRec_nChg_pTLeadTrack_transMin[0]     = n_min
                 bRec_nChg_pTLeadTrack_transMax[0]     = n_max
                 bRec_nChg_pTLeadTrack_transDiff[0]    = -n_min + n_max
                 bRec_pTSum_pTLeadTrack_away[0]        = sumpt_away
                 bRec_pTSum_pTLeadTrack_towards[0]     = sumpt_tow
                 bRec_pTSum_pTLeadTrack_trans[0]       = sumpt
                 bRec_pTSum_pTLeadTrack_transMin[0]    = sumpt_min
                 bRec_pTSum_pTLeadTrack_transMax[0]    = sumpt_max
                 bRec_pTSum_pTLeadTrack_transDiff[0]   = -sumpt_min + sumpt_max
                 bRec_evtTrue_LeadTrack[0]             = 100
                 #/SUNIL

                 #print "Hopefully filling tree with ptMax", ptLeading
                 

                 if (bRec_evtTrue_LeadTrack[0] == 100 or bGen_evtTrue_LeadTrack[0] == 100): 
                     self.tree.Fill()
                     #print "Filling tree because", bRec_evtTrue_LeadTrack[0], bGen_evtTrue_LeadTrack[0]
                     #print "entry for GenpTlead should be", bGen_pTLeadTrack[0]

        return 1

    def finalize(self):
        #tree.Write()
        #outfile.Write()
        #outfile.Close()      
        end = time.clock()

        print "Finalize:"
        normFactor = self.getNormalizationFactor()
        print "  applying norm", normFactor


        #DR DR DR DR commented out to test as my analysis does not scale
        
	for h in self.Trans_SisCon5:
           self.Trans_SisCon5[h].Scale(3/(2*4*math.pi))
	for h in self.other_SisCon5:
           self.other_SisCon5[h].Scale(3/(4*math.pi))

        for h in self.hist:
            self.hist[h].Scale(normFactor)
        

    def finalizeWhenMerged(self):
        #
        # you can save further histograms to the output file by calling:
        #self.GetOutputList().Add(myNewHisto)
        #
        pass

if __name__ == "__main__":
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
    ROOT.gSystem.Load("libFWCoreFWLite.so")
    ROOT.AutoLibraryLoader.enable()

    sampleList = None
    maxFilesMC = None
    maxFilesData = None
    nWorkers = 14 # Use all

    # debug config:
    #'''
    # Run printTTree.py alone to get the samples list
    #sampleList = []
    #sampleList.append("QCD_Pt-15to3000_TuneZ2star_Flat_HFshowerLibrary_7TeV_pythia6")
    #maxFilesMC = 2
    #maxFilesData = 2
    nWorkers = 5
    maxNevents = -1
    #maxFilesData = 1
    #nWorkers =1
    # '''


    slaveParams = {}
    #slaveParams["maxEta"] = 2.


    # use printTTree.py <sampleName> to see what trees are avaliable inside the skim file
    universal_UEAnalyzer_v3.runAll(treeName="UETree",
                               slaveParameters=slaveParams,
                               sampleList=sampleList,
                               maxFilesMC = maxFilesMC,
                               maxFilesData = maxFilesData,
                               maxNevents = maxNevents,
                               nWorkers=nWorkers,
			       outFile = "4-21-16a_P8M1NoPU_uniTrack_eta08_vtx1.root" )



