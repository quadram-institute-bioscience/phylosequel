import subprocess

def run_phyloseq(file_path, tree_flag, fname):
    # Rscripts
    rscript = ['Rscript', './phylosequel/phyloseq.R']

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