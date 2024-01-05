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
Step1: git clone https://github.com/quadram-institute-bioscience/phylosequel.git
Step2: pip install ./phylosequel or pip install --user ./phylosequel
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