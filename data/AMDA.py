import ROOT
# from lcdstk.PlottingTools import plotroothist
filesr1 = [
    #"root://eoslhcb.cern.ch//eos/lhcb/wg/Charm/LHCb-PAPER-2017-002/Omegac2XicK/Data/2011/Omegacst_XicK_2011_MD.root",
    "/SSD3/MasterClassTuples/MasterClassAllCuts.root"
    # "root://eoslhcb.cern.ch//eos/lhcb/wg/Charm/LHCb-PAPER-2017-002/Omegac2XicK/Data/2011/Omegacst_XicK_2011_MU.root",
    # "root://eoslhcb.cern.ch//eos/lhcb/wg/Charm/LHCb-PAPER-2017-002/Omegac2XicK/Data/2012/Omegacst_XicK_2012_MD.root",
    # "root://eoslhcb.cern.ch//eos/lhcb/wg/Charm/LHCb-PAPER-2017-002/Omegac2XicK/Data/2012/Omegacst_XicK_2012_MU.root",
]

filesr2 = [
    "root://eoslhcb.cern.ch//eos/lhcb/wg/Charm/LHCb-PAPER-2017-002/Omegac2XicK/Data/2015/Omegacst_XicK_2015_MD.root",
    "root://eoslhcb.cern.ch//eos/lhcb/wg/Charm/LHCb-PAPER-2017-002/Omegac2XicK/Data/2015/Omegacst_XicK_2015_MU.root",
]

chainr1 = ROOT.TChain("DecayTree")
# chainr2 = ROOT.TChain("Omegacst2XicKTree/DecayTree")

# chainr1ws = ROOT.TChain("Omegacst2XicKTreeWS/DecayTree")
# chainr2ws = ROOT.TChain("Omegacst2XicKTreeWS/DecayTree")

for file in filesr1:
    chainr1.Add(file)

# for file in filesr2:
#     chainr2.Add(file)

# for file in filesr1:
#     chainr1ws.Add(file)

# for file in filesr2:
#     chainr2ws.Add(file)    

dfrun1 = ROOT.RDataFrame(chainr1)
# dfrun2 = ROOT.RDataFrame(chainr2) 
# dfrun1ws = ROOT.RDataFrame(chainr1ws)
# dfrun2ws = ROOT.RDataFrame(chainr2ws) 

labcuts = "lab0_PT               > 5000   && \n" \
          "lab0_CHI2NDOF_DTF_Xic > 0      && \n" \
          "lab0_CHI2NDOF_DTF_Xic < 5      && \n" \
          "lab1_IPCHI2_OWNPV     < 9      && \n" \
          "lab1_PT               > 1000   && \n" \
          "lab1_FDCHI2_OWNPV     > 90     && \n" \
          "lab1_ENDVERTEX_CHI2   < 25     && \n" \
          "lab1_TAU              > 0.0003 && \n" \
          "lab1_M                > 2420   && \n" \
          "lab1_M                < 2510   && \n" \
          "lab2_ProbNNp          > 0.4    && \n" \
          "lab2_P                > 10000  && \n" \
          "lab2_IPCHI2_OWNPV     > 9      && \n" \
          "lab2_PT               > 250    && \n" \
          "lab3_ProbNNk          > 0.4    && \n" \
          "lab3_IPCHI2_OWNPV     > 9      && \n" \
          "lab3_P                > 3200   && \n" \
          "lab3_PT               > 250    && \n" \
          "lab4_ProbNNpi         > 0.2    && \n" \
          "lab4_IPCHI2_OWNPV     > 9      && \n" \
          "lab4_PT               > 250    && \n" \
          "lab4_P                > 3200   && \n" \
          "lab5_OWNPV_CHI2       < 9      && \n" \
          "lab5_TRACK_GhostProb  < 0.3    && \n" \
          "lab5_ProbNNk          > 0.5    && \n" \
          "lab5_PT               > 250         "

cut_base_Xic_BDT = "lab1_DIRA_OWNPV > 0.999995 && lab2_ProbNNp > 0.5 && lab3_ProbNNk > 0.4 && lab1_IPCHI2_OWNPV < 9 && lab1_CHI2NDOF_DTF_PV > 0. && lab1_IPCHI2_OWNPV > 0. && lab1_DTF_CTAU_PV > 0. && lab0_CHI2NDOF_DTF_Xic > 0."
cut_Xic_mass = "&& lab1_M_PV > 2456 && lab1_M_PV < 2480 && "
cut_Xic_mass = ""
cut_Xic_side = "((lab1_M_PV > 2420 && lab1_M_PV<2444)||(lab1_M_PV > 2492 && lab1_M_PV < 2515))"

cut_base_XicK = cut_base_Xic_BDT + "&& lab0_PT > 5000 && lab0_CHI2NDOF_DTF_Xic > 0 && lab0_CHI2NDOF_DTF_Xic < 5 && lab5_IPCHI2_OWNPV < 9 && lab5_PT > 250"

cut_base_XicK_final_2015 = cut_base_XicK + \
    " && lab5_MC12TuneV2_ProbNNk > 0.5 && lab1_Hlt2CharmHadXicpToPpKmPipDecision_TOS == 1 &&"
cut_base_XicK_final_RUNI = cut_base_XicK + " && lab5_ProbNNk > 0.5"

cut_Omegac_mass = "lab0_M_Xic < 3200"
cut_Omegac_mass  =""
dfcutr1 = dfrun1.Filter(cut_base_XicK_final_RUNI + cut_Xic_mass + cut_Omegac_mass) 

print(dfcutr1.Count().GetValue())
# plotroothist(df=dfcutr1, branch1="lab0_M_Xic", filename="Omega_c.pdf")
# dfcutr2 = dfrun2.Filter(cut_base_XicK_final_2015 + cut_Omegac_mass + cut_Xic_mass)

# dfcutr1ws = dfrun1ws.Filter(cut_base_XicK_final_RUNI + cut_Xic_mass + cut_Omegac_mass) 
# dfcutr2ws = dfrun2ws.Filter(cut_base_XicK_final_2015 + cut_Xic_mass + cut_Omegac_mass)

dfcutr1.Snapshot("DecayTree", "/SSD3/MasterClassTuples/mclass1.root", {"lab0_M_Xic"})

# dfcutr2.Snapshot("DecayTree", "mclass2.root", {"lab0_M_Xic"})

# opts = ROOT.RDF.RSnapshotOptions()
# opts.fMode = "UPDATE"

# dfcutr1ws.Snapshot("DecayTreeWS", "selrun1.root", {"lab0_M_Xic"}, opts)
# dfcutr2ws.Snapshot("DecayTreeWS", "selrun2.root", {"lab0_M_Xic"}, opts)