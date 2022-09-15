"""question6.py: this file answers question nr 6."""
import sys
import glob
import pickle
import pandas as pd
import dask.dataframe as dd

pickle_path_pa = '/students/2021-2022/master/Rients_DSLS/pickle_6/'
pickles_pa = glob.glob(pickle_path_pa + 'pubmed21n*.pkl')


# Creating a dataframe that has all the authors and their corresponding paper.
# Using dask
ddf2 = dd
ddf_list = []

for pickle in pickles_pa: 
    # Creating a pandas dataframe from each pickle
    df = pd.read_pickle(pickle)

    # Turning pandas df into a dask dataframe.
    ddf = dd.from_pandas(df, npartitions=8)
    ddf_list.append(ddf)   
    nr = len(ddf_list)

full_frame = dd.multi.concat(ddf_list)

# Question1.
total = len(full_frame) 
uniques = full_frame[0].nunique().compute()
average_authors = round(total / uniques,2)

sys.stdout.write(f"How large a group of co-authors does the average publication have? ,{average_authors}\n")