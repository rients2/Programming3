"""assignment6.py: this file gets pubmed ids and list of authors, keywords and references"""
import glob
import pandas as pd
import argparse as ap
import multiprocessing as mp
import xml.etree.ElementTree as ET

from sqlalchemy import true

# This file still needs a lot of reformatting
# But it works.


def dataframer(myroot):
    # Function that creates a dataframe with everything.
    # Will require some reformatting.

    full_name = []
    pubmed_id = []

    keyword_list = []
    key_pubmed_id = []

    references = []
    ref_pubmed_id = []
    
    # Looping over all the articles.
    for k in range(0, len(myroot)):
        # Finding the location of keywords.
        for child in myroot[k][0]:

            # Obtaining the authors.
            if child.tag == 'Article':
                # Then we need the author list. 
                full_name_list = []
                for second_child in child:
                    if second_child.tag == 'AuthorList':
                        # Then in the authorlist we need all the authors for one paper.
                        for k2 in range(0, len(second_child)):
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
                            full_name_list.append(name)
                # For every author append the corresponding id to a list
                pubmed_id.append(myroot[k][0][0].text)
                full_name.append(full_name_list)


            if child.tag == 'MeshHeadingList':
                # Creating a list to store keywords per article.
                indv_list = []
                # Getting the individual keywords per article
                for keyword_child2 in child:
                    indv_list.append(keyword_child2[0].text)
                # Adding the keywords to a larger list.
                keyword_list.append(indv_list)
                # Adding the pubmedid they belong to.
                key_pubmed_id.append(myroot[k][0][0].text)


        for child in myroot[k][1]:
            # Finding the references.
            if child.tag ==  'ReferenceList':
                # Then add the reference and the corresponing pubmed id to lists.
                ref_list = []
                for ref_child2 in child:
                    # NEED TO fix this:
                    # ref_child2[1][0] is in one article in one xml file out of range :(
                    try:
                        reference = ref_child2[1][0].text
                        ref_list.append(reference)
                    except:
                        ref_list.append('-')

                ref_pubmed_id.append(myroot[k][0][0].text)
                references.append(ref_list)

    # combine the lists into a dataframe                                                  
    auth_db = pd.DataFrame((pubmed_id, full_name)).T

    ref_db = pd.DataFrame((ref_pubmed_id, references)).T
                
    key_db = pd.DataFrame((key_pubmed_id, keyword_list)).T


    return ref_db, key_db, auth_db



def data_merger(myroot):
    dataframes = dataframer(myroot)
    references = dataframes[0]
    keywords = dataframes[1]
    authors = dataframes[2]

    authref = authors.merge(references, how='left', left_on=0, right_on=0)
    full_df = authref.merge(keywords, how='left', left_on=0, right_on=0)

    full_df = full_df.rename(columns={0:'pubmedID', '1_x':'Authors', '1_y':'Refs', 1:'keywords'})

    return full_df


def databaser(files):
    # Function that reads the xml and applies the parser
    name = files[33:-4]
    mytree = ET.parse(files)
    myroot = mytree.getroot()
    df = data_merger(myroot)

    df.to_pickle(f'/students/2021-2022/master/Rients_DSLS/pickle_frames/{name}.pkl')
    print('finnished with: ',name)


def runner(files):
    # Function that does the multiprocessing.
    cpus = args.cpu
    with mp.Pool(cpus) as pool:
        results = pool.map(databaser, files)

if __name__ == "__main__":

    argparser = ap.ArgumentParser(description=
                                "Script that parses the xml files to create pubmedID with keyword, author and reference lists and saves them as a pickle")
    argparser.add_argument("-cpu", action="store",
                           dest="cpu", required=True, type=int,
                           help="Number of cpus to run with multiprocessing")
    args = argparser.parse_args()
    print("Getting: ", args.cpu)

    path = '/data/dataprocessing/NCBI/PubMed/'
    # Obtaining a list of all the stored xml files.
    files = glob.glob(path + '*.xml')
    runner(files)