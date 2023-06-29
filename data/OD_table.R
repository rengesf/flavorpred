library(rlang)
library(tidyverse)

CAS_to_odorants <- read.table("~/Bioinformatik_20.21/Bachelorarbeit/CAS_to_mol.txt", sep = "\t", header = FALSE)
OD_to_mol <- read.table("~/Bioinformatik_20.21/Bachelorarbeit/OD_mol.txt", sep = "\t", header = FALSE)

OD_to_mol_sep <- OD_to_mol %>%
  separate_rows(V2, sep = ";\\s*") %>%
  mutate(V2 = trimws(V2))
OD_to_mol_final <- OD_to_mol_sep[, c("V2","V1")]
colnames(OD_to_mol_final) <- c("molecule", "OD")

CAS_to_odorants_sep <- CAS_to_odorants %>%
  separate_rows(V3, sep = ";\\s*") %>%
  mutate(V3 = trimws(V3))
colnames(CAS_to_odorants_sep) <- c("CAS","Mol Wt", "molecule")


merged_df <- merge(CAS_to_odorants_sep, OD_to_mol_final, by = "molecule")
