#include "time.h"
#include "TBox.h"
#include "TArrow.h"
#include "TCanvas.h"
#include "TH1D.h"
#include "TH2D.h"
#include "TTree.h"
#include "TLine.h"
#include "TMath.h"
#include "TCanvas.h"
#include "TRandom3.h"
#include "TROOT.h"
#include "TLatex.h"
#include "TFile.h"
#include "TLegend.h"
#include "TLegendEntry.h"
#include "Math/QuantFuncMathCore.h"
#include "Math/ProbFuncMathCore.h"
#include <string>
#include <vector>

#if !defined(__CINT__) && !defined(__MAKECINT__)
#include "DataFormats/FWLite/interface/Handle.h"
#include "DataFormats/FWLite/interface/Event.h"
#endif

void diffEventFinder(){

gROOT->Reset();

using namespace std;
using namespace edm;



eventDiff = fopen ("diffEvents.txt", "w"); //DR
eventSame = fopen ("sameEvents.txt", "w");
eventOneOnly = fopen ("oneOnlyEvents.txt", "w");
eventTwoOnly = fopen ("twoOnlyEvents.txt", "w");

char* rootFile1 = "test3.root";
char* rootFile2 = "DATA_8-15-15_eta20_vtxs.root";

TFile *fhist1 = new TFile(rootFile1);

TH1C *h_evts_t;
gDirectory->GetObject("h_evts_t",h_evts_t);

TFile *fhist2 = new TFile(rootFile2);

fhist2->cd("Run2015B");

TH1C *eventsGood;
gDirectory->GetObject("eventsGood",eventsGood);

Int_t nbins = h_evts_t->GetXaxis()->GetNbins();

Double_t h1BinContent = 0;
Double_t h2BinContent = 0;

for(Int_t i = 1; i< nbins -1; i++)
//for(Int_t i = 1; i< 100; i++)
{
        h1BinContent = h_evts_t->GetBinContent(i);
        h2BinContent = eventsGood->GetBinContent(i);
        if( h1BinContent == h2BinContent )
        {
                fprintf(eventSame, "%d \n", (int) h_evts_t->GetXaxis()->GetBinLowEdge(i));
        }else{
                fprintf(eventDiff, "%d \n", (int) h_evts_t->GetXaxis()->GetBinLowEdge(i));
                //cout << "diff bins for i = " << i << endl;
                //cout << h_evts_t->GetBinLowEdge(i) << endl;
        }
        if( h1BinContent == 1 && h2BinContent == 0 )
        {
                fprintf(eventOneOnly, "%d \n", (int) h_evts_t->GetXaxis()->GetBinLowEdge(i));
        }
        if( h1BinContent == 0 && h2BinContent == 1 )
        {
                fprintf(eventTwoOnly, "%d \n", (int) eventsGood->GetXaxis()->GetBinLowEdge(i));
        }

}

fclose(eventSame); //DR
fclose(eventDiff); //DR
fclose(eventOneOnly);
fclose(eventTwoOnly);

}


