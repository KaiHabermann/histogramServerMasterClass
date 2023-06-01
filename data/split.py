import ROOT

df = ROOT.RDataFrame("DecayTree", "data/Masterclass.root")

df.Range(10_000_000).Snapshot("DecayTree", "data/Masterclass_small_2.root")