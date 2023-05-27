
SAMPLE_RATE = 44100
import sys
import math
from guitar import GuitarString


CONCERT_A = 440.0
NUM_STRINGS = 37
STEP = 1 / SAMPLE_RATE


def open_files():
    # open input data file
    in_file_name = input("Enter the name of the input file: ")
    try:
        infile = open(in_file_name, "r")
    except FileNotFoundError:
        print("Error opening input data file")
        sys.exit(1)

    # open output data file
    out_file_name = input("Enter the name of the output file: ")
    try:
        outfile = open(out_file_name, "w")
    except FileNotFoundError:
        print("Error opening output data file")
        sys.exit(1)

    return infile, outfile


def close_files(infile, outfile):
    infile.close()
    outfile.close()


def create_strings():
    strings = []
    for i in range(NUM_STRINGS):
        factor = pow(2, (i - 24) / 12.0)
        frequency = CONCERT_A * factor
        string = GuitarString(frequency)
        strings.append(string)
    return strings


def sum_samples(strings):
    sample_sum = 0
    for string in strings:
        sample_sum += string.sample()
    return sample_sum


def process_file(strings, infile, outfile):
    time_count = 0
    for line in infile:
        read_time, gtr_key = line.strip().split()
        read_time = float(read_time)
        gtr_key = int(gtr_key)

        while time_count < read_time:
            outfile.write("  " + str(time_count) + "\t" + str(sum_samples(strings)) + "\n")
            for string in strings:
                string.tic()
            time_count += STEP

        if gtr_key == -1:
            return

        strings[gtr_key].pluck()
        print(".", end="")
        sys.stdout.flush()


def main():
    strings = create_strings()
    infile, outfile = open_files()

    outfile.write("; Sample Rate " + str(SAMPLE_RATE) + "\n")
    outfile.write("; Channels 1\n")

    print("Reading the input file and generating a .dat file for sox")

    process_file(strings, infile, outfile)

    close_files(infile, outfile)

    print("Done.")


if __name__ == "__main__":
    main()