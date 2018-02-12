from __future__ import print_function
import os
import click
import glob
import subprocess
from tqdm import tqdm

@click.command()
@click.argument("input_folder",
                type=click.Path(
                    exists=True,
                    file_okay=False)
               )
@click.argument("output_folder",
                type=click.Path(
                    exists=True,
                    file_okay=False)
               )
def main(input_folder, output_folder):
    """segment all the files in the folder"""
    input_filenames = sorted(glob.glob(os.path.join(input_folder, "*.tif")))
    d = len(input_filenames)
    first_filename = input_filenames[0]
    command = "identify {0}".format(first_filename)
    print(command)
    output = subprocess.check_output(command, shell=True)
    w, h = output.split()[2].decode().split("x")
    dims_output_filename = os.path.join(
        output_folder,
        "dims.txt")
    print(w, h, d, dims_output_filename)
    with open(dims_output_filename, "w") as dims_output:
        print(w, h, d, file=dims_output)
    output_filename = os.path.join(
        output_folder,
        "dr.raw")
    command = "fiji --ij2 --headless --run distance_ridge_macro.py 'input_file=\"{}\",output_file=\"{}\"'".format(
        input_filenames[0],
        output_filename
    )
    print(command)
    subprocess.check_call(segmentation_command, shell=True)


if __name__ == "__main__":
    main()