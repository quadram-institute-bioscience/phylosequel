import rpy2.robjects as robjects

# Run R code to load the package and retrieve session information
r_code = """
library(optparse)
packageVersion("optparse")
"""
r_version = robjects.r(r_code)

print("Installed version of examplePackage:", r_version)
