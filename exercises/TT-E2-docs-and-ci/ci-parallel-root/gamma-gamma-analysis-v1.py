import os
import sys
import time
import ROOT
from ROOT import TMath

# Usage:
#   python3 gamma-gamma-analysis-v1.py <ROOT_URL> [max_events]
#   # This file contains many data, its reasonable to use less events, maybe 1e3 or 5e3

# Output:
#   plots/histogram_<basename>.png
#   plots/histogram_<basename>.root

PRINTING_JUMPS=1000   # Number to print
PHOTON_CUT_MEV=15_000 # MeV, cut for photons # default we use 30k


if len(sys.argv) < 2:
    raise ValueError("No ROOT file provided. Pass the ROOT file URL as argv[1].")

root_file_url = sys.argv[1]
max_events = 0
if len(sys.argv) >= 3:
    try:
        max_events = int(sys.argv[2])
    except ValueError:
        max_events = 0

start = time.time()

f = ROOT.TFile.Open(root_file_url)
if not f or f.IsZombie(): 
    raise RuntimeError(f"Failed to open ROOT file: {root_file_url}")

# We know which file we search for
tree = f.Get("mini")
if not tree:
    raise RuntimeError("Tree 'mini' not found in file.")

# Histogram: diphoton invariant mass
# two gamma per event
hist = ROOT.TH1F(
    "h_M_Hyy",
    "Diphoton invariant-mass ; Invariant Mass m_{yy} [GeV] ; events",
    30, 105, 160
)

# Lorentz Vector
Photon_1 = ROOT.TLorentzVector()
Photon_2 = ROOT.TLorentzVector()

n = 0
for event in tree:
    n += 1
    if max_events > 0 and n > max_events:
        break

    if n % PRINTING_JUMPS == 0:
        print(f"Processed {n} events...")

    # Trigger condition
    if tree.trigP:
        goodphoton_index = [0] * 5
        goodphoton_n = 0
        photon_index = 0

        # Loop over photons
        for j in range(tree.photon_n):
            # photon_isTightID this variable its a value with some identify
            # boolean, the colaboration choose some property

                # then I do a cut, this data its all in MeV, the cut its 30_000 MeV
            if (tree.photon_isTightID[j] and tree.photon_pt[j] > PHOTON_CUT_MEV and
                (TMath.Abs(tree.photon_eta[j]) < 2.37) and
                (TMath.Abs(tree.photon_eta[j]) < 1.37 or TMath.Abs(tree.photon_eta[j]) > 1.52)):

                goodphoton_n += 1
                if photon_index < len(goodphoton_index):
                    goodphoton_index[photon_index] = j
                photon_index += 1

        # Exactly two good photons
        if goodphoton_n == 2:
            i1 = goodphoton_index[0]
            i2 = goodphoton_index[1]

            # Isolation
            if ((tree.photon_ptcone30[i1] / tree.photon_pt[i1] < 0.065) and
                (tree.photon_etcone20[i1] / tree.photon_pt[i1] < 0.065) and
                (tree.photon_ptcone30[i2] / tree.photon_pt[i2] < 0.065) and
                (tree.photon_etcone20[i2] / tree.photon_pt[i2] < 0.065)):

                Photon_1.SetPtEtaPhiE(tree.photon_pt[i1] / 1000., tree.photon_eta[i1],
                                      tree.photon_phi[i1], tree.photon_E[i1] / 1000.)
                Photon_2.SetPtEtaPhiE(tree.photon_pt[i2] / 1000., tree.photon_eta[i2],
                                      tree.photon_phi[i2], tree.photon_E[i2] / 1000.)

                # root object
                Photon_12 = Photon_1 + Photon_2
                hist.Fill(Photon_12.M()) # we can see the invariatn mass, filling the histogram 1 by 1

# Save outputs
os.makedirs("plots", exist_ok=True)

base = os.path.basename(root_file_url)
if base.endswith(".root"):
    base = base[:-5]

# creates root file and a png
output_png = f"plots/histogram_{base}.png"
output_root = f"plots/histogram_{base}.root" # this may be necesary to deliver to some one else

# just and histogram without any makeup,  hist.Fill(Photon_12.M())
canvas = ROOT.TCanvas("Canvas", "cz", 800, 600)
hist.Draw("E")
canvas.SetLogy()
canvas.SaveAs(output_png)

root_output_file = ROOT.TFile(output_root, "RECREATE") # write the output
hist.Write() # write the hist
root_output_file.Close() # close the output file

end = time.time()
duration = end - start
print(f"Finished {base} in {int(duration // 60)} min {int(duration % 60)} s")
