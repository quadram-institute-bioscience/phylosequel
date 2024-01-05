import csv
import pandas as pd
import sys
from Bio import Phylo
import re

def detect_separators(filename):
    with open(filename,'r', newline='') as file:
        sample_data = ''.join([file.readline() for _ in range(5)]) # first 20 lines
    sep = csv.Sniffer().sniff(sample_data).delimiter
    return sep 
                  
def parse_table(table):
    try:
        delimiter = detect_separators(table) # check for delimiter
        df = pd.read_csv(table, sep=delimiter, header = 0) # reads metadata
        print(f"   \u2713 {table} parsed successfully")
        return df
    except pd.errors.ParserError as e:
        raise ValueError(f"Error parsing table '{table}': {e}")

def parse_phylogeny(phylogeny):    
    try:
        #with open(phylogeny, "r") as f:
        #    print(newick_tree)
        #    newick_tree = f.read()
    
        #for _, row in df.iterrows():
        #    original = f"{row['Original']}:"
        #    modified = f"{row['Modified']}:"
        #    newick_tree = newick_tree.replace(original,modified)
        
        #tree = Phylo.read(StringIO(newick_tree), 'newick')
        tree = Phylo.read(phylogeny, 'newick')
        terms_names = [term for term in tree.get_terminals()]
        clade_names = [clade.name for clade in terms_names]
        print(f"   \u2713 {phylogeny} parsed successfully")
    
    except Exception as e:
        print(f"   \u2717 Error: Unable to parse '{phylogeny}': {e}")
        sys.exit(1)
    
    return clade_names

def check_samples(setA, setB):
    # Common column names
    common_col_names = setA.intersection(setB)
    if len(common_col_names) == len(setB):
        check = True
    else:
        check = False
    return check

def count_str(df):
    count={}
    for col in df:
        if df[col].dtype == 'object':
            count[col] = df[col].str.count(';').sum()
    return count

def remove_special_chars(df):
    mapping_df = pd.DataFrame(columns=['Original', 'Modified'])
    mapping_df['Original'] = df[df.columns[0]]
    df[df.columns[0]] = df[df.columns[0]].apply(lambda x: re.sub(r'\W+','',x))
    mapping_df['Modified'] = df[df.columns[0]]
    return df, mapping_df


    

        

        





