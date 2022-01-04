# Recursive BsaI
This is a repo for the materials needed to test the idea of recursive BsaI. 

Recursive BsaI is a method that uses methylated oligos in place of traditional GoldenGate linker sequences. This allows a user to do a GoldenGate assembly with BsaI which is then used as an input to another BsaI assembly.

The two advantages of this method are:
1. Removes the need to remove more than 1 restriction enzyme
2. Enables recursion to build out reusable composite components

Recursion is especially useful as a developer tool for building more basic genetic toolkits for new organisms. 

### Why now
Recursive BsaI enables simplicity in our cloning workflows for building from 500bp chunks. It gives us the following advantages:
1. Simplicity in workflow and in vectors: we only need 1 set of vectors and 1 enzyme for all steps in our process
2. Fewer restrictions on customer sequences
3. 3x drop in cost of enzyme, dropping the cost per clone by almost 20% ($5.22 to $4.37)
4. Ease of vendor independence - verified off patent with groups working on expression (https://www.addgene.org/165506/)
5. Experiment is entirely self contained and depends on no other process in work right now. However, `oligo_pool_3`'s design depends on results from this experiment.

Recursive BsaI would simplify our workflow as we develop it while also setting us up to massively drop clone costs.

## Materials needed
This experiment should be self-contained.

- 2 methylated linkers (($0.63 x 24 + $20 + $20+ $60) x 2 = $230.24)
- 2 control linkers (($0.63 x 24 + $20 + $20) x 2 = $110.24)
- 1 insert sequence ($89)
- 1 control insert sequence ($89)
- 1 vector backbone (1630 x 0.20 = $326)
- 1 sequencing primer ($0.18 x 20 = $3.6)
- M13for+M13rev ($0.18 x 17 x 2 = 6.12)

We cannot use `pOpen_v3` as a vector backbone in this case because we need BsaI cut sites, therefore we need to synthesize a new backbone based on Sebastian Cocioba's pIDMv5K. This kanamycin vector only needs to be 1630bp, containing both BsaI cut sites, BbsI cut sites (for insertion of ccdB later, optionally) and M13for+M13rev for amplifying additional plasmid.

We can simply use an IDT gBlock for the insert for this experiment. The sequence would be `b0057` from our previous oligo pool, since is just about the minimal size necessary for a gBlock. The control insert sequence would be the same, except it would not require linkers for insertion.

The two methylated linker sequences will be synthesized as Ultramer duplexes from IDT, synthesized with methylation and chemically phosophylated - ready exactly as is for use. These chemical modifications are the primary cost in synthesizing the duplexes.

## Sequence
The linkers are designed as such:
```
# Forward 
...GGTCmTC
...CC
# Reverse
TGAGmACC...
     TGG...

Overhangs set: TCmTC,TGAGm
Efficiency: 100% (https://goldengate.neb.com/)

Methylation side: https://doi.org/10.1021/sb500356d
```

### Risks
Unfortunately, we have no idea how the ligase will interact with the methylated overhangs. If the methylation prevents ligation, we will be very sad :(. But forunately, we should be able to see if methylation affecting ligation is the case.
