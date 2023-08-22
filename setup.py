from setuptools import setup
from setuptools.command.install import install
import os
import subprocess

def get_scripts():
    #['hellllow = scripts:hellllow:main']
    scripts = []
    for dirpath, dirnames, filenames in os.walk('scripts'):
        for filename in filenames:
            if filename.endswith('.py'):
                script_name = os.path.splitext(filename)[0]
                scripts.append(f'{script_name} = {dirpath.replace("/", ".")}.{script_name}:main')
    return scripts

def execute_installing_r_packages():
    r_script_path = os.path.join("envs", "R-package", "install_r_package.R")
    if os.path.exists(r_script_path):
        print("Installing R packages...")
        subprocess.run(['Rscript', r_script_path], check=True)
        print("R packages installed successfully.")
    else:
        print(f"R script not found at path: {r_script_path}")

if __name__ == "__main__":

    console_scripts = get_scripts()  
    setup(entry_points=dict(

            console_scripts=console_scripts
    ))
    #Install R-packages
    execute_installing_r_packages()

