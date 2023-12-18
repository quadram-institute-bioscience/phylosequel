# install_r_package.R
# Scripts to install the R-packages.
# Requires R>=4.1.2

# R-packages to install
packages_to_install = c("ape", "optparse", "xml2", "BiocManager", "jsonlite")

for (pkg in packages_to_install) {
  tryCatch({
    if (!requireNamespace(pkg, quietly = TRUE)) {
        install.packages(pkg, dependencies = TRUE, force = TRUE)
    }
  }, error = function(e) {
      message(paste("Error: Failed to install '", pkg, "'."))
      message("Details:", conditionMessage(e))
      q(status = 1)  # Exit the script with a non-zero status code
    })
}

# R-Bioconductor packages to install
biocmanager_to_install = c("annotate", "genefilter", "phyloseq")
for (pkg in biocmanager_to_install) {
tryCatch({
  if (!requireNamespace(pkg, quietly = TRUE)) {
    BiocManager::install(pkg, dependencies = TRUE, force = TRUE)
  }
}, error = function(e) {
  message(paste("Error: Failed to install '", pkg, "'."))
  message("Details:", conditionMessage(e))
  q(status = 1)  # Exit the script with a non-zero status code
  })
}
