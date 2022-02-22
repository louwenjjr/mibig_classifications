#!/usr/bin/env python3
"""
Script to run antismash on an input_folder with multiple gbk files as input,
creating a new folder in output_folder for every gbk file with antismash
output.
"""

import os
import sys
import time
import glob
import subprocess

if __name__ == "__main__":
    start_t = time.time()
    # show help message/incorrect usage
    usage = "\nUsage:\n\tpython run_antismash_on_gbks.py " +\
            "<gbk_input_folder> <output_folder>"
    if len(sys.argv) < 3:
        if len(sys.argv) == 1:
            print("Incorrect usage.")
        elif sys.argv[1] in ("-h", "--help"):
            print("Script to run antismash on an input_folder with multiple " +
                  "gbk files as input, creating a new folder in " +
                  "output_folder for every gbk file with antismash output")
        else:
            print("Incorrect usage.")
        print(usage)
        exit()

    print("\nStarted with command:", '\t'.join(sys.argv))
    # parse command line arguments to define in and output
    input_folder = sys.argv[1]
    output_folder = sys.argv[2]
    cs = 8

    # check if input exists
    if not os.path.isdir(input_folder):
        SystemExit("Input folder does not exist")

    # make output folder if not exists
    if not os.path.isdir(output_folder):
        os.mkdir(output_folder)
    else:
        print("\nOutput folder existed")

    # loop through gbk files, create new out dir, run antismash in out dir
    input_files = glob.glob(os.path.join(input_folder, "*.gbk*"))
    print(f"\nFound {len(input_files)} input files, running antismash...")
    succeeded = 0  # keep track how many input files pass
    for input_file in input_files:
        # check if for some reason input_file does not exist
        if os.path.exists(input_file):
            # split input name to new output dir
            base_name = os.path.split(input_file)[1].split(".gbk")[0]
            file_output_folder = os.path.join(output_folder, base_name)
            if not os.path.isdir(file_output_folder):
                # run antismash
                command = f"antismash -c {cs} --cb-general --cb-subclusters " \
                          "--cb-knownclusters --cc-mibig " \
                          "--genefinding-tool prodigal " \
                          f"--output-dir {file_output_folder} {input_file}"
                try:
                    subprocess.check_call(command, shell=True)
                except subprocess.CalledProcessError as e:
                    print(f"  skipping {input_file}, antismash failed: {e}")
                else:
                    succeeded += 1
            else:
                print(f"  output existed for {input_file}, not run again")
        else:
            # input file does not exist..
            print(f"  skipping {input_file}, did not exist")

    print(f"\nFinished. Successfully ran {succeeded} input files. " +
          f"{len(input_files) - succeeded} files failed.")
    end_t = time.time()
    print(f"Time elapse: {end_t - start_t:.2f}s")