import ROOT

df = ROOT.RDataFrame("DecayTree", "/SSD3/MasterClassTuples/MasterClassAllCuts.root")

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

cut_base_Xic_BDT = "lab1_DIRA_OWNPV > 0.999995 && lab2_ProbNNp > 0.5 && lab3_ProbNNk > 0.4 && lab1_IPCHI2_OWNPV < 9. && lab1_CHI2NDOF_DTF_PV > 0. && lab1_IPCHI2_OWNPV > 0. && lab1_DTF_CTAU_PV > 0. && lab0_CHI2NDOF_DTF_Xic > 0."
cut_Xic_mass = "lab1_M_DTF_PV > 2456 && lab1_M_DTF_PV < 2480 &&"

cut_Xic_side = "((lab1_M_DTF_PV > 2420 && lab1_M_DTF_PV<2444)||(lab1_M_DTF_PV > 2492 && lab1_M_DTF_PV < 2515))"

cut_base_XicK = cut_base_Xic_BDT + \
    " && lab0_PT > 5000 && lab0_CHI2NDOF_DTF_Xic > 0 && lab0_CHI2NDOF_DTF_Xic < 5. && lab5_IPCHI2_OWNPV < 9 && lab5_PT > 250."

cut_base_XicK_final_2015 = cut_base_XicK + \
    " && lab5_MC12TuneV2_ProbNNk > 0.5 && lab1_Hlt2CharmHadXicpToPpKmPipDecision_TOS == 1 &&"
cut_base_XicK_final_RUNI = cut_base_XicK + " && lab5_ProbNNk > 0.5 "

cut_Omegac_mass = "  && lab0_M_DTF_Xic < 3200"

df = df.Filter(cut_base_XicK_final_RUNI)

df.Range(80_000_000).Snapshot("DecayTree", "data/Masterclass_small_2.root")