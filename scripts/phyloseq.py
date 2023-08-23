#!/usr/bin/env python3

import argparse
import phylosequel
import sys, os, shutil
import pandas as pd
from phylosequel import checks, runner

"""
Python package to convert the standard reports to phyloseq obejct format.
Phyloseq object structure:
    1. Abudance table   (required)
    2. Taxnonomy        (required)
    3. Metadata table   (required)
    4. Phylogeny        (optoinal)

Metadata table: 1st column = Sample names, next columns will be samples' metadata
"""
def check_either_f_or_t(args):
    if not (args.flag or args.taxonomy):
        raise argparse.ArgumentTypeError("Either -f or -t must be used.")
    if args.flag and args.taxonomy:
        raise argparse.ArgumentTypeError()
    return args

def create_dir(outputdir):
    try:
        os.mkdir(outputdir)
        print(f"Directory '{outputdir}' created successfully.")
    except FileExistsError:
        print(f"Directory '{outputdir}' already exists.")
    except Exception as e:
        print(f"Error occurred while creating directory: {e}")
    

def arguments():
    parser = argparse.ArgumentParser('Construct a phyloseq object')
    parser.add_argument('-a','--abundance', type=str, required=True, help="Abundance table (format: txt)", metavar='')
    parser.add_argument('-m', '--metadata', type=str, required=True, help="Metadata table (format: csv)", metavar='')
    parser.add_argument('-p', '--phylogeny', type=str, help="Phylogeny in newick format", metavar='')
    parser.add_argument('-o', '--output', type=str, default="dir", help="Output directory", metavar='')
    parser.add_argument('-n', '--name', type=str, default="phylObj", help="Phyloseq Object file name", metavar='')

    # Add mutually exclusive arguments
    mutually_exclusive_group = parser.add_mutually_exclusive_group()
    mutually_exclusive_group.add_argument('-t', '--taxonomy', type=str, help="Taxonomy file. Should not be used with -f", metavar='')
    mutually_exclusive_group.add_argument('-f','--flag', action="store_true", help="Taxonomy within the abundance table [%(default)s]", default=False)
    
    parser.add_argument('--version', help="Print version and exit", action='version', version=phylosequel.__version__)

    args = parser.parse_args()

    try:
        args = check_either_f_or_t(args)
    except argparse.ArgumentTypeError as e:
        parser.error(str(e))
    
    return args

def main():
    """Main function for formating files for phyloseq object from input files."""
    args = arguments()
    print("S1. Parsing input files") 
    # 1) Metdata
    ## Parse metadata
    metadata = checks.parse_table(args.metadata)

    ## Initialize a taxonomy dataframe 
    taxonomy = pd.DataFrame(columns=['Name','Domain', 'Phylum', 'Class', 'Order', 'Family', 'Genus', 'Species'])
    
    # 2) Parse abundance and taxonomy accordingly
    if not args.flag:
        ## Taxonomy is parsed separately
        abundance = checks.parse_table(args.abundance) ## Parse abundance
        
        lineage = checks.parse_table(args.taxonomy) ## Parse taxonomy from file.
        c1 = checks.count_str(lineage) # dictionary c1[colname]=counts
        print("S2. Checking files")
        if len(c1) == 2:
            ## if len == 2 means taxonomy file consist of two columns
            ## Expecting one column is names/otus and another corresponding taxonomy.
            for key, value in c1.items():
                if value == 0:
                    taxonomy['Name'] = lineage[key]
                elif value >0:
                    taxonomy[['Domain', 'Phylum', 'Class', 'Order', 'Family', 'Genus', 'Species']] = lineage[key].str.split(';',expand=True)
                else:
                    print('   \u2717 Error parsing taxonomy')
                    sys.exit(1)
        elif len(c1) == 1:
            ## len == 1 means only one column
            ## The column consist of the taxonomy, hence get name from the column and pase taxonomy
            col = lineage.columns[0]
            taxonomy['Name'] = lineage[col].apply(lambda x: x.split(';')[-1] if ';' in x else x)
            taxonomy[['Domain', 'Phylum', 'Class', 'Order', 'Family', 'Genus', 'Species']] = lineage[col].str.split(';',expand=True)
        else:
            print('   \u2717 Error parsing taxonomy')
            sys.exit(1)
        
        # Check if OUTs/Species names matches in the taxonomy and abundance tables
        if checks.check_samples(set(abundance.iloc[:,0]), set(taxonomy.iloc[:,0])):
            print("   \u2713 OTUs/species names matched b/w abundnace and taxonomy")
        else:
            print("   \u2717 Error: Species names missmatch in the abundance and taxonomy")
            sys.exit(1)

    else:
        # 2) Parse abundance and taxonomy accordingly
            ## Taxonomy within in abudance file.
            ## Extract and return taxonomy
            ## Sometime names and taxonomy both are there within the abundance file.
        abundance = checks.parse_table(args.abundance)
        c1 = checks.count_str(abundance) # Count the ";" for identifying lineage columns
        print("S2. Checking files")
        if len(c1) == 1:
            for key, value in c1.items():
                if value > 0:
                    lineage = abundance.pop(key)
                    taxonomy['Name'] = lineage.apply(lambda x: x.split(';')[-1] if ';' in x else x)
                    taxonomy[['Domain', 'Phylum', 'Class', 'Order', 'Family', 'Genus', 'Species']] = lineage.str.split(';', expand=True)
                    abundance.insert(0, key, lineage)
                    abundance[key]=abundance[key].apply(lambda x: x.split(';')[-1] if ';' in x else x)
        elif len(c1) == 2:
            for key, value in c1.items():
                if value == 0:
                    target_col = abundance.pop(key)
                    abundance.insert(0,key, target_col)
                    taxonomy['Name'] = target_col
                elif value > 0:
                    lineage = abundance.pop(key)
                    taxonomy[['Domain', 'Phylum', 'Class', 'Order', 'Family', 'Genus', 'Species']] = lineage.str.split(';', expand=True)
                else:
                    print("   \u2717 Error2: Taxonomy not found")
                    sys.exit(1)
        else:
            print("   \u2717 Error1: Taxonomy not found")
            sys.exit(1)
    
    # Check all the samples were matched accross the metadata, abundance and tree.
    # first check if the sample names are the same in metadata
    # Check by transposing the metadata as well. Just in case if a transposed metadata files is given
    check = set()
    abund = set(abundance.columns[1:])
    
    for col in metadata.columns:
        meta = set(metadata[col])
        c = checks.check_samples(meta, abund)
        check.add(c)
    
    if any(check):
        print("Sample matched b/w metadata and abundance tables")
    else:
        metadata = metadata.T
        metadata.reset_index(inplace=True)
        metadata.rename(columns=metadata.iloc[0], inplace=True)
        metadata = metadata[1:]
        
        for col in metadata:
            meta = set(metadata[col])
            c = checks.check_samples(meta, abund)
            check.add(c)
         
        if any(check):
            print("   \u2713 Sample matched b/w metadata and abundance tables")
        else:
            print("   \u2717 Error: Missing samples in metadata or/and abundance table")
            sys.exit(1)
    
    # 4) Create phyloseq objects
    create_dir(args.output) ## Create output directory to write
    create_dir(f"{args.output}/files") ## Input directory

    taxonomy = taxonomy.fillna('NA') ## fill na for missing ranks

    metadata.to_csv(f"{args.output}/files/metadata.csv", header = True, index = False) ## Write metadata.csv
    abundance.to_csv(f"{args.output}/files/abundance.txt", sep="\t", header=True, index=False) ## Write Abundance.txt
    taxonomy.to_csv(f"{args.output}/files/taxonomy.txt", sep="\t", header=True, index=False) ## Write taxonomy

    tree_flag = False
    if args.phylogeny:
        print("S3. Parsing Phylogeny")
        tree_flag = True
        clade_names = checks.parse_phylogeny(args.phylogeny)
        clades = set(clade_names)
        c = checks.check_samples(clades, abundance[abundance.columns[0]])
        print("S4. Checking files")
        if c==True:
            print("   \u2713 Samples matched b/w phylogeny & metadata")
        else:
            print("   \u2717 Error: Missing samples b/w metadata & phylogeny")
            sys.exit(1)
        
        shutil.copy(args.phylogeny, f"{args.output}/files/phylogeny.nwk")
    
    print("S5. Running R-phyloseq")
    runner.run_phyloseq(f"{args.output}/files", tree_flag, args.name)
    print(f"S7. Output files: {args.output}/files")

    return

if __name__ == "__main__":
    main()