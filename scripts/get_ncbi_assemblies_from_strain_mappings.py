#!usr/bin/env python3
"""
Author: Joris Louwen

Script that takes in a csv with assembly accessions from the PoDP strain
mappings, and tries to download the assemblies from the ncbi ftp.
"""

import argparse
from glob import glob
import os
import subprocess
import time


def get_commands():
    parser = argparse.ArgumentParser(description="Script that takes in a csv\
        with assembly accessions, after which those assemblies are downloaded\
        from ncbi. If assemblies cannot be found in GenBank\
        RefSeq will also be checked and vice versa.")
    parser.add_argument("-i", "--in_file", help="Input csv containing ncbi\
        assembly accessions as one of the fields, can be multiple",
                        required=True, nargs='+')
    parser.add_argument("-o", "--out_dir", dest="out_dir",
                        required=True, help="Output dir")
    return parser.parse_args()


def read_csv(infile, no_head=True):
    """Reads csv and extracts [assembly_acc], starting with GCA/GCF

    infile: str, filepath to csv
    no_head: bool, is there no header in the file
    """
    result = []
    with open(infile, 'r') as inf:
        if not no_head:
            inf.readline()
        for line in inf:
            line = line.strip().split(',')
            for elem in line:
                if elem.startswith("GCF_") or elem.startswith("GCA_"):
                    # elem = elem.rpartition(".")[0]
                    if elem not in result:
                        result.append(elem)
    return result


def get_assemblies_wrapper(assembly_acc, outdir, keep_ass=True):
    """
    Takes [assembly_acc], downloads acc

    outdir: str, location of assemblies
    keep_ass: bool, delete assembly after extraction
    """
    print("\nDownloading assemblies and extracting {} accessions from input"
          .format(len(assembly_acc)))
    ass_files = []
    for acc in assembly_acc:
        ass_file = download_unzip_acc(acc, outdir)
        if not ass_file:
            # try again - other database: RefSeq or GenBank, switch GCF and GCA
            # subprocess.check_call('rm {}'.format(ass_file), shell=True)
            if acc.startswith('GCA'):
                new_acc = 'GCF' + acc[3:]
                print('  search again in RefSeq with accession: ' + new_acc)
            else:
                new_acc = 'GCA' + acc[3:]
                print('  search again in GenBank with accession: ' + new_acc)
            ass_file = download_unzip_acc(new_acc, outdir, True)
        if not keep_ass:
            if ass_file:
                subprocess.check_call('rm -r {}'.format(ass_file), shell=True)

        ass_files.append(ass_file)
    print("\nSuccessfully downloaded {}/{} accessions in {}".format(
        len([ass_f for ass_f in ass_files if ass_f]), len(assembly_acc),
        outdir))


def download_unzip_acc(acc, out_folder='./', second=False):
    """Downloads and unzips assembly genbank

    acc: str, assembly accession
    out: str, path to downloaded assembly
    second: bool, is this a second try or not? - will alter print message
    """
    # will be empty list if file not there
    out = glob(os.path.join(out_folder, '*' + acc + '*.gbk'))
    # print(out)
    # print(acc)
    if not out:
        ftp_url = 'ftp://ftp.ncbi.nlm.nih.gov/genomes/all/{}/{}/{}/{}/' \
            .format(acc[:3], acc[4:7], acc[7:10], acc[10:13])
        download_command = (
                'wget -q --recursive -e robots=off --reject "index.html"' +
                ' --no-host-directories --cut-dirs=6 {}'.format(ftp_url) +
                ' -P {}'.format(out_folder))
        try:
            subprocess.check_call(download_command, shell=True)
        except subprocess.CalledProcessError:
            # print("test")
            if second:
                pr = '  accession {} does not exist at {}'.format(acc, ftp_url)
            else:
                pr = ' Accession {} does not exist at {}'.format(acc, ftp_url)
            # print(pr)
            return
        # if multiple assembly versions exist, take newest
        # print(os.path.join(out_folder, acc + '*/'))
        out_dir = sorted(glob(os.path.join(out_folder, acc + '*/')))
        # print(out_dir)
        try:
            gzip_genome = glob(os.path.join(out_dir[-1],
                                            acc + '*genomic.gbff.gz'))[0]
            # print(gzip_genome)
        except IndexError:
            # print("test2")
            if second:
                pr = '  accession {} does not exist at {}'.format(acc, ftp_url)
            else:
                pr = ' Accession {} does not exist at {}'.format(acc, ftp_url)
            # print(pr)
            return
        out_genome = os.path.join(out_folder,
                                  os.path.split(gzip_genome)[1].split('.gbff')[
                                      0] + '.gbk')
        # print(out_genome)
        subprocess.check_call(
            'gunzip -c {} > {}'.format(gzip_genome, out_genome), \
            shell=True)
        for out_d in out_dir:  # remove all assembly version directories
            subprocess.check_call('rm -r {}'.format(out_d), shell=True)
    else:
        out_genome = out[0]
        print(" Existing accession: {}".format(out_genome))
    # print(out_genome)
    return out_genome


if __name__ == "__main__":
    print("Start")
    start = time.time()
    cmd = get_commands()

    accessions = []
    for in_file in cmd.in_file:
        file_content = read_csv(in_file)
        accessions += file_content

    get_assemblies_wrapper(accessions, cmd.out_dir, True)

    # succeeded jobs
    len_success = len(glob(os.path.join(cmd.out_dir, "*.gbk")))
    print(f"\n{len_success} assemblies downloaded in gbk format")

    end = time.time()
    t = end - start
    t_str = '{}h{}m{}s'.format(int(t / 3600), int(t % 3600 / 60),
                               int(t % 3600 % 60))
    print('\nScript completed in {}'.format(t_str))
