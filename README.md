# Phylosequel
A python package to create a [phyloseq](https://joey711.github.io/phyloseq/) object. The phyloseq object typically consit of:
1. OTUs Abundance table.
2. Taxonomy table.
3. Metadata file.
4. OTU Phylogeny (optional)

## How to install

### Install Dependencies
* Install R>=4.1.2
```
sudo apt-get install build-essential
sudo apt-get install r-base-dev
sudo apt-get install libcurl4-openssl-dev
```
### To install the **Phylosequel**:
```
[Recommended]
Step1: git clone https://github.com/quadram-institute-bioscience/phylosequel.git
Step2: pip install ./phylosequel

[Optional]
Step1: git clone https://github.com/quadram-institute-bioscience/phylosequel.git
Step2: pip install --user ./phylosequel
Step3: echo 'export PATH="/user_path_to/Library/Python/3.8/bin:$PATH"' >> ~/.bash_profile
Step4: source ~/.bash_profile
```

## Test run
**To get help**
```
phylsoquel --help
usage: Construct a phyloseq object [-h] -a  -m  [-p] [-o] [-n] [-t  | -f] [--version]

optional arguments:
  -h, --help         show this help message and exit
  -a , --abundance   Abundance table (format: txt)
  -m , --metadata    Metadata table (format: csv)
  -p , --phylogeny   Phylogeny in newick format
  -o , --output      Output directory
  -n , --name        Phyloseq Object file name
  -t , --taxonomy    Taxonomy file. Should not be used with -f
  -f, --flag         Taxonomy within the abundance table [False]
  --version          Print version and exit
```
**Test run:**
The inputs are stored in `data` directory.

```
phylosequel -a data/abundance_wo_taxa.txt -m data/metadata.csv -p data/phylogeny.nwk -t data/taxonomy.txt -o test_phylo -n phyloseqObj
```

**Expect output**
On successful run the following log will be generated on the terminal. The phyloseq object will be save as `*.rds`

```
STEP: Parsing input files
   ✓ metadata.csv parsed successfully
   ✓ abundance_wo_taxa.txt parsed successfully
   ✓ taxonomy.txt parsed successfully
STEP: Checking files
   ✓ OTUs/species names matched b/w abundnace and taxonomy
   ✓ Sample matched b/w metadata and abundance tables
Directory 'test_phylo' already exists.
Directory 'test_phylo/files' already exists.
STEP: Parsing Phylogeny
   ✓ phylogeny.nwk parsed successfully
STEP: Checking files
   ✓ Samples matched b/w phylogeny & metadata
STEP: Running R-phyloseq
   ⏳ cmd: Rscript phyloseq.R -m test_phylo/files/metadata.csv -a test_phylo/files/abundance.txt -t test_phylo/files/taxonomy.txt -p test_phylo/files/phylogeny.nwk -o test_phylo/files/test_phylo
   ✔ Successfully created phyloseq object test_phylo/files/test_phylo.rds 
STEP: Checking Phyloseq Object
   ✔ All samples found in test_phylo/files/test_phylo.rds 
   ✔ All Taxon/OTUs found in test_phylo/files/test_phylo.rds 
   ✔ All tips found in test_phylo/files/test_phylo.rds 
STEP: Output files: test_phylo/files
```
