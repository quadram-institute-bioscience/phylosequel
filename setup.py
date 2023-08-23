from setuptools import setup
import os
import subprocess
import logging

def get_scripts():
    scripts = []
    for dirpath, dirnames, filenames in os.walk('scripts'):
        for filename in filenames:
            if filename.endswith('.py'):
                script_name = os.path.splitext(filename)[0]
                scripts.append(f'{script_name} = {dirpath.replace("/", ".")}.{script_name}:main')
    return scripts

def execute_installing_r_packages():
    r_script_path = "envs/R/install_r_package.R"
    if os.path.exists(r_script_path):
        logging.info("Installing R packages...")
        try:
            subprocess.run(['Rscript', r_script_path], check=True)
            logging.info("R packages installed successfully.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error installing R packages: {e}")
    else:
        logging.warning(f"R script not found at path: {r_script_path}")
    return

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    #Installing R
    execute_installing_r_packages()
    
    console_scripts = get_scripts()  
    setup(entry_points=dict(
        console_scripts=console_scripts
    ))