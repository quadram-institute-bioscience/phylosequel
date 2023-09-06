#!/usr/bin/env python3
import argparse
import sys


def main():
    #print("Hellllllll World!")
    #amp = AmplikrakenCore(['a', 'b', 'c'])
    #print(amp.process_data())
    #print("Kraken: ",amplikraken.fastq.has_kraken())
    #print("NF: ",amplikraken.utils.has_nextflow())

    args = argparse.ArgumentParser(description='List samples from a directory')
    args.add_argument('path', type=str, nargs='+', help='Path to fastq files')
    args.add_argument('-a',  action="store_true", help='Print absolute path')
    args.add_argument('-b',  action="store_true", help='Print basename')
    argz = args.parse_args()
    

    for path in argz.path:
        print(path)
        datasets = amplikraken.fastq.pairedend_samples_from_path(path)
        datasets.displayBasename() if argz.b else datasets.displayAbsolute()
        print(datasets)
if __name__ == '__main__':
    main()