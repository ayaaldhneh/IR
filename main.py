import pickle
from operator import itemgetter

from scipy.sparse import vstack
from sklearn.metrics.pairwise import cosine_similarity

import Datasets
from PreProcessing import preProcess, date_processor
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

filename = r"C:\Users\aya\Desktop\antique\collection.tsv"
fName = r'C:\Users\aya\Desktop\wikIR1k\documents.csv'
QFile=r'C:\Users\aya\Desktop\antique\train\queries.TXT'
QFileWik=r'C:\Users\aya\Desktop\wikIR1k\training\queries.CSV'

def preprocessing_documents(path):
    corpus = Datasets.read_documents(path,',')
    processed_dic = {}
    doc_keys = []
    doc_values = []
    for key, value in corpus.items():

        value = date_processor(value)

        value = preProcess(value)
        print(key, value)
        processed_dic[key] = value
        doc_keys.append(key)
        doc_values.append(value)
    return processed_dic, doc_keys,doc_values
# preprocessing_documents(filename)

def preprocessing_queries(path):
    corpus = Datasets.read_queries(path)
    processed_queries_dic = {}
    qry_keys = []
    qry_values = []
    for key, value in corpus.items():
        value = preProcess(value)
        print(key,value)
        processed_queries_dic[key] = value
        qry_keys.append(key)
        qry_values.append(value)
    return processed_queries_dic,qry_keys,qry_values



def create_inverted_index(path1,path2):
    docs, doc_keys,doc_values = preprocessing_documents(path1)
    documents =[' '.join(terms) for terms in docs.values()]
    vectorizer = TfidfVectorizer()
    documents_matrix= vectorizer.fit_transform(documents)

    pickle.dump(documents_matrix, open("tfidf[docs]wikIR1k.pickle", "wb"))
    pickle.dump(doc_keys, open("tfidf[doc_key]wikIR1k.pickle", "wb"))
    pickle.dump(doc_values, open("tfidf[doc_value]wikIR1k.pickle", "wb"))
    pickle.dump(vectorizer, open("[vectorizer]wikIR1k.pickle", "wb"))

    qry, qry_keys, qry_values = preprocessing_queries(path2)
    quiries=[' '.join(terms) for terms in qry.values()]
    queries_matrix = vectorizer.fit_transform(quiries)
    pickle.dump(queries_matrix, open("tfidf[qrs]wikIR1k.pickle", "wb"))
    pickle.dump(qry_keys, open("tfidf[qry_key]wikIR1k.pickle", "wb"))
    pickle.dump(qry_values, open("tfidf[qry_value]wikIR1k.pickle", "wb"))

############ one time call #############
# create_inverted_index(filename, QFile)
create_inverted_index(fName,QFileWik)
def get_docs_matrix(path):
    return pickle.load(open(path, "rb"))

def calc_similarity(query, docs, vecpath, doc_keys, doc_values):
    vectorizer = pickle.load(open(vecpath, "rb"))
    query_vector = vectorizer.transform(preProcess(query))
    cosine_similarities = cosine_similarity(query_vector, docs).flatten()

    # Get indices of relevant documents with non-zero similarity scores
    nonzero_indices = [i for i, sim_score in enumerate(cosine_similarities) if sim_score > 0]

    # Check that there are relevant documents
    if not nonzero_indices:
        return [], []

    # Get relevant document keys and values
    top_doc_keys = [doc_keys[i] for i in nonzero_indices if i < len(doc_keys)]
    top_doc_values = [doc_values[i] for i in nonzero_indices if i < len(doc_values)]

    # Sort the results by similarity score
    results = sorted(zip(range(len(top_doc_keys)), top_doc_keys, cosine_similarities[nonzero_indices]), key=lambda x: x[2], reverse=True)
    results_to_show = sorted(zip(range(len(top_doc_values)), top_doc_values, cosine_similarities[nonzero_indices]), key=lambda x: x[2], reverse=True)

    # Return the top results as lists
    return [result[1] for result in results], [result[1] for result in results_to_show]


def calc_similarity_vectors(query_vector, docs, doc_keys, doc_values):
    docs_matrix = vstack(docs)
    cosine_similarities = cosine_similarity(query_vector, docs_matrix).flatten()

    # Get indices of relevant documents with non-zero similarity scores
    nonzero_indices = [i for i, sim_score in enumerate(cosine_similarities) if sim_score > 0]

    # Check that there are relevant documents
    if not nonzero_indices:
        return [], []

    # Get relevant document keys and values
    top_doc_keys = [doc_keys[i] for i in nonzero_indices if i < len(doc_keys)]
    top_doc_values = [doc_values[i] for i in nonzero_indices if i < len(doc_values)]

    # Sort the results by similarity score
    results = sorted(zip(range(len(top_doc_keys)), top_doc_keys, cosine_similarities[nonzero_indices]), key=lambda x: x[2], reverse=True)
    results_to_show = sorted(zip(range(len(top_doc_values)), top_doc_values, cosine_similarities[nonzero_indices]), key=lambda x: x[2], reverse=True)

    # Return the top results as lists
    return [result[1] for result in results], [result[1] for result in results_to_show]



