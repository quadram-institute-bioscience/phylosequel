#!/usr/bin/env Rscript

# Convert the multi-sample kraken report to phyloseq object
suppressPackageStartupMessages({
    library(optparse)
    library(ape)
    library(phyloseq)
    # Load any other packages here
})

option_list = list(
  make_option(c("-m", "--metadata"), default = NULL, type = "character", help = "Metadata"),
  make_option(c("-a", "--abundance"), default = NULL, type = "character", help = "Abundance"),
  make_option(c("-t", "--taxonomy"), default = NULL, type="character", help = "Taxaonomy"),
  make_option(c("-p", "--phylogeny"), default = NULL, type="character", help = "Phylogeny table"),
  make_option(c("-o", "--output"), default = NULL, type = "character", help = "Output Directory")
)
opt = parse_args(OptionParser(option_list=option_list))

# 1. Check if metadata file exists
if (is.null(opt$metadata)) {
  stop(sprintf("Missing (-m) metadata"))
} else if (file.access(opt$metadata) == -1) {
  stop(sprintf("%s file does not exist", opt$metadata))
} else {
  meta=read.table(opt$metadata, sep=",", header = TRUE, comment.char = "", quote = "", check.names = FALSE)
}
# 1.1 parse the metadata
rownames(meta) = meta[, 1]
meta = meta[-c(1)]
META = sample_data(meta)

# 2. Abundance file exits
if (is.null(opt$abundance)) {
  stop(sprintf("Missing (-m) abundance"))
} else if (file.access(opt$abundance) == -1) {
  stop(sprintf("%s file does not exist", opt$abundance))
} else {
  abund=read.table(opt$abundance, sep="\t", header = TRUE, comment.char = "", quote = "", check.names = FALSE)
}

# 2.1 Parse abundance
rownames(abund) = abund[, 1]
abund  = abund[-c(1)]
OTU = otu_table(abund, taxa_are_rows = TRUE)

# 3. taxonomy
if (is.null(opt$taxonomy)) {
  stop(sprintf("Missing (-m) taxonomy"))
} else if (file.access(opt$taxonomy) == -1) {
  stop(sprintf("%s file does not exist", opt$taxonomy))
} else {
  taxo=read.table(opt$taxonomy, sep="\t", header = TRUE, comment.char = "", quote = "", check.names = FALSE)
}

# 3.1 Parse taxonomy
taxo = as.matrix(taxo)
rownames(taxo) = taxo[, 1]
taxo = taxo[, -1]
TAX = tax_table(taxo)

PSobj = phyloseq(OTU, TAX, META)

# 4. Phylogeny
if (!is.null(opt$phylogeny)) {
    if (file.exists(opt$phylogeny)) {
      phylo <- readLines(opt$phylogeny)
      TREE = read.tree(text=phylo)
      PSobj = phyloseq(OTU, TAX, META, TREE)
    } else {
      stop(sprintf("Missing (-t) tree file"))
  }
}
file_path = file.path(paste0(opt$output,c(".rds")))
saveRDS(PSobj, file = file_path)

loadObj = readRDS(file_path) # Load the object

if (class(loadObj) == "phyloseq"){
  cat("   \u2714 Successfully created phyloseq object",file_path,"\n")
} else {
  cat("   \u2718 Failed to create the phyloseq object\n")
}
cat("S6. Checking Phyloseq Object\n")

# Compare the phyloseq object with input files.
## 1. Sample names
s1 = sort(sample_names(loadObj)) # from object
s2 = sort(colnames(abund)) # from file

if (all.equal(s1, s2)) {
  cat("   \u2714 All samples found in",file_path,"\n")
} else {
  cat("   \u2718 Missing samples",file_path,"\n")
}

## 2. Taxa/OTUs
s1 = sort(taxa_names(loadObj))
s2 = sort(rownames(taxo))

if (all.equal(s1, s2)) {
  cat("   \u2714 All Taxon/OTUs found in",file_path,"\n")
} else {
  cat("   \u2718 Missing Taxon/OTUs",file_path,"\n")
}

## 3. Phylogeny
if (!is.null(opt$phylogeny)) {
    if (file.exists(opt$phylogeny)) {
      treeObj = phy_tree(loadObj)
      s3 = sort(treeObj$tip.label)
      if (all.equal(s1,s3) && all.equal(s2,s3)){
        cat("   \u2714 All tips found in",file_path,"\n")
      } else {
        cat("   \u2718 Missing tips",file_path,"\n")
      }
    }
}