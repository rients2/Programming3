"""assignment6.py: this file gets pubmed ids and authors and saves them as pickles"""
import glob
import pickle
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
                            # Mostly when it is a company author.
                            try:
                                firstname = second_child[k2][1].text
                            except:
                                firstname = ''
                            # Create a full name and append it to a list
                            try:
                                name = str(firstname) + ' ' + str(lastname)
                            except:
                                name = 'None'

                            full_name.append(name)

    # Turn both lists created into a dataframe.                                                   
    db = pd.DataFrame((pubmed_id, full_name)).T

    return db

# Currently not used when running the file.
def citation_graph(myroot):

    #Function that creates a dataframe with all papers and their references.
    # Can be used to create a citation graph/network.

    # Currently only obtains papers if they cite another paper not those without.
    
    references = []
    pubmed_id = []
    # First loop over every article in the xml file.
    for k in range(0, len(myroot)):
        # Then get the references which is in the reference list tag.
        for ref_child in myroot[k][1]:
            if ref_child.tag ==  'ReferenceList':
                # Then add the reference and the corresponing pubmed id to lists.
                for ref_child2 in ref_child:
                    reference = ref_child2[1][0].text
                    pubmed_id.append(myroot[k][0][0].text)

                    references.append(reference)
    # combine the lists into a dataframe
    db = pd.DataFrame((pubmed_id, references)).T

    return db

# Currently not used when running the file.
def keyword_collector(myroot):
    # Function that creates a dataframe with all the pubmedids and their keywords. 
    # Known issue: Only obtains pubmedIDs if they have keywords. If they dont they get left out.

    keyword_list = []
    pubmed_id = []
    # Looping over all the articles.
    for k in range(0, len(myroot)):
        # Finding the location of keywords.
        for keyword_child in myroot[k][0]:
            if keyword_child.tag == 'MeshHeadingList':
                # Creating a list to store keywords per article.
                indv_list = []
                # Getting the individual keywords per article
                for keyword_child2 in keyword_child:
                    indv_list.append(keyword_child2[0].text)
                # Adding the keywords to a larger list.
                keyword_list.append(indv_list)
                # Adding the pubmedid they belong to.
                pubmed_id.append(myroot[k][0][0].text)
    db = pd.DataFrame((pubmed_id, keyword_list)).T
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
    cpus = 16
    with mp.Pool(cpus) as pool:
        results = pool.map(databaser, files)

if __name__ == "__main__":
    path = '/data/dataprocessing/NCBI/PubMed/'
    # Obtaining a list of all the stored xml files.
    files = glob.glob(path + '*.xml')
    runner(files)