from setuptools import setup
import os

def get_scripts():
    #['hellllow = scripts:hellllow:main']
    scripts = []
    for dirpath, dirnames, filenames in os.walk('scripts'):
        for filename in filenames:
            if filename.endswith('.py'):
                script_name = os.path.splitext(filename)[0]
                scripts.append(f'{script_name} = {dirpath.replace("/", ".")}.{script_name}:main')
    return scripts

if __name__ == "__main__":

    console_scripts = get_scripts()    
    setup(entry_points=dict(

            console_scripts=console_scripts
    ))