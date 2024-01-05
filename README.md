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
echo 'export PATH="/user_path_to/Library/Python/3.8/bin:$PATH"' >> ~/.bash_profile
source ~/.bash_profile
```