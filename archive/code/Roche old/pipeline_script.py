import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz
import csv

def dict_to_matrix(dictionary):
    '''
    Does convert a pandas dataframe into a matrix where 
    Parameters
    ----------
    dictionary : dict,
        keys = row name
        values = col name
    data : int, either 0 or 1 
    '''
    unique_values = set(val for sublist in dictionary.values() for val in sublist)
    data_dict = {key: {val: 1 if val in values else 0 for val in unique_values} for key, values in dictionary.items()}
    df = pd.DataFrame(data_dict).T
    return(df)


def overlapping_elements(list1, list2, threshold=70):
    '''
    Find overlapp between to lists with a threshold (=70)
    
    Parameters
    ----------
    list1: list
    list2: list
    threshold: int, fixed to 70
    '''
    overlap = []
    for elem1 in list1:
        for elem2 in list2:
            ratio = fuzz.ratio(elem1, elem2)
            if ratio >= threshold:
                overlap.append(elem1)
    return overlap


def dataframe_to_dict(df):
    '''
    Convert DataFrame to dictionary

    Parameters
    ----------
    df: dataframe
    '''
    result_dict = {}
    for index, row in df.iterrows():
        if row[0] in result_dict:
            result_dict[row[0]].append(row[1])
        else:
            result_dict[row[0]] = [row[1]]
    return result_dict     


def find_matching_entries(dictionary,df):
    '''
    Find match between dictionary entries and the rows of a dataframe
    
    Parameters:
    -----------
    dictionary: dict
    df: dataframe
    '''
    threshold = 50
    found_match = []
    found_match_per_entry = {}
    for key, value in dictionary.items():
        all_matches = set()
        for index, row in df.iterrows():
            for keyword in value:
                if fuzz.ratio(keyword, str(index).lower()) >= threshold:
                    if index not in all_matches:
                        all_matches.add(index)
                        found_match.append(row)
        found_match_per_entry[key] = all_matches
    found_match = pd.DataFrame(found_match)
    return(found_match, found_match_per_entry)


def create_matrix_from_dict(dictionary,df):
    '''
    Create a new matrix by finding matches and filtering right columns
    
    Parameters:
    -----------
    dictionary: dict
    df: dataframe
    '''
    matrix = pd.DataFrame(columns=list(df), index=ms_cas)
    final_dict = {}
    for key, value in dictionary.items():
        current_val = []
        for v in value:
            for index, row in df.iterrows():
                if index == v:
                    current_val.append(','.join(row.loc[row.eq(1)].index.tolist()))
                    # todo: maybe exception -> do change if two ones in a row
                    matrix.loc[key][row.loc[row.eq(1)].index.tolist()] = 1
        final_dict[key] = set(current_val)
    matrix = matrix.fillna(0)
    matrix = matrix.loc[:, (matrix != 0).any(axis=0)]
    return(final_dict, matrix)


def read_massspec_data(file_path, replicate, sample_key, n):
    ''''
    Get a dataframe with cas numbers and largest intensities (n times)
    
    Parameters:
    ----------
    file_path: string, path to file
    replicate: int, 1 2 or 3
    sample_key: str
    n: int, nlargest
    '''
    data = pd.read_csv(file_path, delimiter=',')
    data = data[data["sample_key"]== sample_key]
    data = data[data["replicate"] == replicate]
    # filter columns that are 0 
    data = data.loc[:, (data != 0).any(axis=0)]
    data = data.drop(columns=['sample_key', 'replicate'])
    largest_entries = data.iloc[0].nlargest(n)
    data_top_entries = pd.DataFrame({'Intensities':largest_entries})
    return data_top_entries

def flavornet_dataframe():
    '''
    read flavornet data and save it in mol_to_OD
    '''
    mol_to_OD = {}
    descriptors = []
    CAS_numbers= []
    with open('./data/CAS_mol_OD.csv', 'r',encoding='utf-8') as tabfile:
        reader = csv.reader(tabfile, delimiter=',')
        for row in reader: 
            molecule = row[0]
            CAS = row[1]
            OD = row[3]
            CAS_numbers.append(CAS)
            descriptors.append(OD)
            if CAS in mol_to_OD:
                mol_to_OD[CAS].add(OD)
            else:
                mol_to_OD[CAS]  = set([OD])
    CAS_numbers = list(set(CAS_numbers))
    descriptors = list(set(descriptors))
    D = pd.DataFrame(index=CAS_numbers, columns=descriptors)
    for col in D.columns:
        for index, row in D.iterrows():
            # Check if value in  current row matches any entry in the dictionary
            if index in mol_to_OD.keys() and col in mol_to_OD[index]:
                # Set to 1
                D.at[index, col] = 1
    D = D.fillna(0)
    return (D,mol_to_OD)

def get_ms_cas(sample_key, n):
    replicate = 1
    file_path = 'data/cas_intensities.csv'
    top_cas = read_massspec_data(file_path, replicate, sample_key,n)
    ms_cas = list(top_cas.index)
    return(ms_cas)

def main(sample_key,n):
    # always the same from flavornet
    D, mol_to_OD = flavornet_dataframe()
    sample = get_ms_cas(sample_key,n)
    
    #


if __name__ == "__main__":
    n = 50
    main('000920',n)
    


