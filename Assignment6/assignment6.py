"""assignment6.py: this file gets pubmed ids and authors and saves them as pickles"""
import glob
import pickle
from tokenize import Name
import pandas as pd
import networkx as nx
import multiprocessing as mp
import xml.etree.ElementTree as ET


def article_author(myroot):
    # Behold my xml tree parser.
    # If it works it aint stupid.

    full_name = []
    pubmed_id = []

    # First loop over every article in the xml file.
    for k in range(0, len(myroot)):
        # Then get the the article tag which is in the medlinecitation
        for child in myroot[k][0]:
            if child.tag == 'Article':
                # Then we need the author list. 
                for second_child in child:
                    if second_child.tag == 'AuthorList':
                        # Then in the authorlist we need all the authors for one paper.
                        for k2 in range(0, len(second_child)):
                            # For every author append the corresponding id to a list
                            pubmed_id.append(myroot[k][0][0].text)
                            # Getting the authors last name
                            lastname = second_child[k2][0].text
                            # Not all authors have their first name listed.
                            try:
                                firstname = second_child[k2][1].text
                            except:
                                firstname = '-'
                            # Create a full name and append it to a list
                            try:
                                name = str(firstname) + ' ' + str(lastname)
                            except:
                                name = 'None'

                            full_name.append(name)

    # Turn both lists created into a dataframe.                                                   
    db = pd.DataFrame((pubmed_id, full_name)).T

    return db


def databaser(files):
    # Function that reads the xml and applies the parser
    name = files[33:-4]
    print('working on: ', files)
    mytree = ET.parse(files)
    myroot = mytree.getroot()
    df = article_author(myroot)

    df.to_pickle(f'/students/2021-2022/master/Rients_DSLS/pickle_6/{name}.pkl')


def runner(files):
    # Function that does the multiprocessing.
    cpus = 48
    with mp.Pool(cpus) as pool:
        results = pool.map(databaser, files)

if __name__ == "__main__":
    Full_df = pd.DataFrame()
    path = '/data/dataprocessing/NCBI/PubMed/'
    files = glob.glob(path + '*.xml')
    runner(files)