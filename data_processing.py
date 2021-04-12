import os
import regex
import pandas as pd

def concatFiles(directory_path, output_filename):
    """Merge all files in the specified directory path
        and output a single file to output_filename.

        For example: we can create a directory with all episode
        transcriptions in .txt format and call this function
        to merge all episode text files to a single .txt"""
    files = os.listdir(directory_path)
    with open(output_filename, "w") as fo:
        for infile in files:
            with open(os.path.join(directory_path, infile)) as fin:
                for line in fin:
                    fo.write(line)


def transcript_to_dataframe(file_path):
    """Take text file and split on new lines and periods
    Returns a pandas dataframe with a column for each phrase"""
    df = []
    with open(file_path, "r") as f:
        full_text = f.read()
        for l in regex.split('[\n\.]', full_text):
            if l and l != ".":
                df.append(l)
    return pd.DataFrame(df)