# 2025_OASIS_CircadianRhythm
Repository to analyse the Cell Painting assay with co-administration of chemical perturbations and dexamethasone. 

The hypothesis is that synchronizing the circadian rhythm of the cells will make compound mode-of-actions more detectable. We test this by adding dexamethasone (a GR agonist) along with the compounds of interest in full dose-response series. We measure the same perturbations but without dexamethasone. We check two things:

1) Do samples cluster much more strongly by compound in UMAPs when co-treated with dexamethasone? -> visually examine UMAPs
2) Is there more phenotypic activity when co-treating with dexamethasone? -> compute mAP vs. neg controls separately for Dex co-treated samples and compare % active and p-values.

After analysing multiple versions of the data (diff normalisation, filtering, batch correction, etc) we cannot detect any significant differences in phenotypic activity / mode-of-action clustering between the regular samples and dexamethasone co-treated samples. We don't even see differences in the DMSO negative controls. Therefore, I wonder if either the dexamethasone concentration wasn't high enough, or if the normalisation methods should be adjusted further. 
