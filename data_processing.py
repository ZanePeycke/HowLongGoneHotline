import os

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