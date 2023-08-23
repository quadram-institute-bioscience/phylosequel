# install_r_package.R

if (!requireNamespace("ape", quietly = TRUE)) {
  install.packages("ape", version = "5.7.1", dependencies = TRUE)
}

if (!requireNamespace("phyloseq", quietly = TRUE)) {
  install.packages("phyloseq", version = "1.36.0", dependencies = TRUE)
}

if (!requireNamespace("optparse", quietly = TRUE)) {
  install.packages("optparse", version = "1.7.3", dependencies = TRUE)
}