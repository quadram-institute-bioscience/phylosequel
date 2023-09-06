import subprocess
import os

def run_phyloseq(file_path, tree_flag, fname):
    
    # Get the full path to the "phyloseq.R" script
    path_to_rscript = os.path.join(os.path.dirname(__file__), 'phyloseq.R')
    
    # Rscript command
    rscript = ['Rscript', path_to_rscript]

    if tree_flag:
        parameters = ['-m', f"{file_path}/metadata.csv",'-a', f"{file_path}/abundance.txt", '-t', f"{file_path}/taxonomy.txt", '-p', f"{file_path}/phylogeny.nwk", '-o', f"{file_path}/{fname}"]
        command = rscript + parameters
        command = ' '.join(command)
    else:
        parameters = ['-m', f"{file_path}/metadata.csv",'-a', f"{file_path}/abundance.txt", '-t', f"{file_path}/taxonomy.txt", '-o', f"{file_path}/{fname}"]
        command = rscript + parameters
        command = ' '.join(command)
    
    # Try running the Rscript
    try:
        print("   \u23F3 cmd:", command)
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print("   \u2717 Error: Running Phyloseq", e)
    return