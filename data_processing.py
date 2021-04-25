import os
import regex
import pandas as pd


def remove_intro(directory_path, num_lines):
    """Remove the intro consistent to all episodes
    We remove this to avoid a problem with finding the most
    common phrases later. However, this is optional and use case
    will vary depending on the dataset being used."""
    files = os.listdir(directory_path)
    for file in files:
        with open(directory_path + file, 'r') as fin:
            data = fin.read().splitlines(True)
        with open(directory_path + file, 'w') as fout:
            fout.writelines(data[num_lines:])


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
        for l in regex.split('[\n\.\?]', full_text):
            if l and l != ".":
                df.append(l)
    return pd.DataFrame(data=df, columns=['phrase'])


def remove_phrases(dataframe, phrase_list):
    """Remove any rows from the dataframe that contain a
    phrase from the phrase list"""
    for phrase in phrase_list:
        dataframe = dataframe[~dataframe.phrase.str.contains(phrase)]
    return dataframe

def filter_phrases_by_length(df, phrase_column_name, lower_bound, upper_bound):
    """ Given a dataframe and the name of a column containing phrases, this function
    checks the number of words in each phrase between the lower and upper bounds.
    The phrases with lengths below the lower_bound, and above the upper_bound are
    then dropped from the dataframe."""
    unwanted_rows = df[df[phrase_column_name].str.split().str.len() < lower_bound].index
    df = df.drop(unwanted_rows, axis=0)

    unwanted_rows = df[df[phrase_column_name].str.split().str.len() > upper_bound].index
    df = df.drop(unwanted_rows, axis=0)

    return df


def remove_tokens(df, column_name, token_list):
    """Given a dataframe and a list of tokens we remove all items in the token
    list from the specified column name."""
    for token in token_list:
        df[column_name] = df[column_name].str.replace(token, '')

    return df