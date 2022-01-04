# Recursive BsaI
This is a repo for the materials needed to test the idea of recursive BsaI. 

Recursive BsaI is a method that uses methylated oligos in place of traditional GoldenGate linker sequences. This allows a user to do a GoldenGate assembly with BsaI. The output of that reaction can then be used as an input to another BsaI assembly.

The two advantages of this method are:
1. Forces removal of 1 restriction enzyme rather than 2
2. Enables recursion to build out reusable composite components

Recursion is especially useful as a developer tool for building more basic genetic toolkits for new organisms. 

### Why now
Recursive BsaI enables simplicity in our cloning workflows for building from 500bp chunks. It gives us the following advantages:
1. Simplicity in workflow and in vectors: we only need 1 set of vectors and 1 enzyme for all steps in our process
2. Fewer restrictions on customer sequences
3. 3x drop in cost of enzyme, dropping the cost per clone by almost 20% ($5.22 to $4.37)
4. Ease of vendor independence - BsaI is verified off patent with groups working on expression (https://www.addgene.org/165506/)
5. Experiment is entirely self contained and depends on no other process in work right now. However, `oligo_pool_3`'s design depends on results from this experiment.

Recursive BsaI not only simplifies our workflow, but makes it more powerful and cheaper.

## Materials needed
This experiment should be self-contained and executed on a single robot in a single day. There are no PCRs or outside vectors required.

- 2 methylated linkers (($0.63 x 24 + $20 + $20+ $60) x 2 = $230.24)
- 2 control linkers (($0.63 x 24 + $20 + $20) x 2 = $110.24)
- 1 insert sequence ($89)
- 1 control insert sequence ($89)
- 1 vector backbone (1630 x 0.20 = $326)
- 1 sequencing primer ($0.18 x 20 = $3.6)
- M13for+M13rev ($0.18 x 17 x 2 = 6.12)

We cannot use `pOpen_v3` as a vector backbone in this case because we need BsaI cut sites. I recommend we synthesize a new backbone based on Sebastian Cocioba's pIDMv5K. This kanamycin vector only needs to be ~1630bp, containing both BsaI cut sites, BbsI cut sites (for insertion of ccdB later, optionally) and M13for+M13rev for amplifying additional backbone.

We can simply use an IDT gBlock for the insert for this experiment. The sequence would be `b0057` from our previous oligo pool, since is just about the minimal size necessary for a gBlock. There is 1 control insert that does not require linkers for insertion.

The two methylated linker sequences will be synthesized as Ultramer duplexes from IDT, synthesized with methylation and chemical phosophylation - ready for use exactly as-is. These chemical modifications are the primary cost in synthesizing the duplexes.

### Lowering costs
To save $504, we could instead PCR the control inserts and vector backbone. This shouldn't theoretically be too hard, and may be worthwhile to save money. Assuming our time is worth $100 per day, it shouldn't take >5 days to optimize a PCR. However, this does increase the risk that something goes wrong.

We could also forgo synthesis of the control linkers, since the methylation site won't be in the ligation overlap anyway.

However, I believe we should synthesize our own copy. There are a couple reasons for this:
1. Absolute de-risk. Any PCR or handling means possible setbacks.
2. Known provenance.

## Sequence
The linkers are designed as such:
```
# Methylation site definitions
B1:
G GTCTC
CmCAGAG
B2: 
GG TCTC
CCmAGAG
T1:
GGTCmTC
CCAG AG
T2:
GGTCTCm
CCAGAG

# Forward (B1)
...G GTCTC
...CmC
# Reverse (B1)
    ACCm...
ACTCTGG ...

GGTCTC

Overhangs set: TCTC,TGAG
Efficiency: 100% (https://goldengate.neb.com/)

Methylation site paper: https://doi.org/10.1021/sb500356d
Methylation site efficiency - figure S2: https://pubs.acs.org/doi/suppl/10.1021/sb500356d/suppl_file/sb500356d_si_002.pdf
```

The B1 methylation site (the first C on the bottom strand) is actually at the least efficient out of the entire set of `[B1,B2,T1,T2]`. However, this is the only position that can be made on the linker yet and have no interaction with T4 ligase. 

The denatured PAGE run shows that there is a small amount of cutting when methylated at this site. However, we can assume that rate is at some constant, which can be countered by the ligation having a higher constant rate. For example, the Yeast Toolkit has shown that a GoldenGate reaction with one set of internal BsaI sites will still return colonies, so it is likely that this will be good enough.

# Results
After this experiment is run, we should be able to tell if we can clone level 0 GoldenGate parts using methylated BsaI.

### Risks
The methylation on B1 may still have a werid interaction with the ligase that prevents ligation. The rate of BsaI cutting may also still be too high for efficient ligation and building of the DNA. 
