# install_r_package.R
#dir.create("./packages") # Create a local directort for R pacakagesx
#Sys.setenv("PKG_CPPFLAGS"="-I/usr/include/libxml2 -I/opt/miniconda3/include/libxml2/libxml")

packages_to_install = c("httr", "ape", "optparse", "xml2", "BiocManager", "jsonlite")

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