import configparser
import importlib
import importlib.metadata as metadata
import re, sys
from packaging import version as packaging_version

def test_check_packages(required_packages):
    missing_packages = []

    for package in required_packages:
        if package !='':
            package_name = re.split(r">=",package)
            if package_name[0] == "importlib-resources":
                package = "importlib_resources"
            elif package_name[0] == "more-itertools":
                package = "more_itertools"
            elif package_name[0] == "biopython":
                package = "Bio"
            else:
                package = package_name[0]

            try:
                required_version = package_name[1]
                module = importlib.import_module(package)
                installed_version = metadata.version(module.__name__)
                print(installed_version)
                if packaging_version.parse(installed_version) >= packaging_version.parse(required_version):
                    print(f"Package '{package}' successfully imported.")
                    print(f"{package}\tinstalled-version: {installed_version} >= required-version: {required_version}")
                else:
                    print(f"Warning: Package '{package}' successfully imported. But lower version than required-version")
                    print(f"{package}\tinstalled-version: {installed_version} < required-version: {required_version}")
            
            except ImportError:
                print(f"ERROR: Package '{package}'")
                sys.exit(1)




# Read package list and required versions from setup.cfg
config = configparser.ConfigParser()
config.read("setup.cfg")
required_packages = config["options"]["install_requires"].splitlines()
print(required_packages)
test_check_packages(required_packages)

