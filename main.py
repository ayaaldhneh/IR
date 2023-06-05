import pickle
from operator import itemgetter

from sklearn.metrics.pairwise import cosine_similarity

import Datasets
from PreProcessing import preProcess, date_processor
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

filename = r"C:\Users\aya\Desktop\antique\collection.tsv"
fName = r'C:\Users\aya\Desktop\wikIR1k\documents.csv'
QFile=r'C:\Users\aya\Desktop\antique\train\queries.TXT'

# def preprocessing_documents(path):
#     corpus = Datasets.read_documents(path,'\t')
#     processed_dic = {}
#     for key, value in corpus.items():
#         value = date_processor(value)
#         value = preProcess(value)
#         print(key,value)
#         processed_dic[key] = value
#     return processed_dic
def preprocessing_documents(path):
    corpus = Datasets.read_documents(path,'\t')
    processed_dic = {}
    doc_keys = []
    doc_values = []
    for key, value in corpus.items():
        value = date_processor(value)
        value = preProcess(value)
        processed_dic[key] = value
        doc_keys.append(key)
        doc_values.append(value)
    return processed_dic, doc_keys,doc_values
# cleaned_term=preprocessing_documents(filename)

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
    docs, doc_keys,doc_values = preprocessing_documents(filename)
    documents =[' '.join(terms) for terms in docs.values()]
    vectorizer = TfidfVectorizer()
    documents_matrix= vectorizer.fit_transform(documents)

    pickle.dump(documents_matrix, open("tfidf[docs]" + path1[27:34] + ".pickle", "wb"))
    pickle.dump(doc_keys, open("tfidf[doc_key]" + path1[27:34] + ".pickle", "wb"))
    pickle.dump(doc_values, open("tfidf[doc_value]" + path1[27:34] + ".pickle", "wb"))
    pickle.dump(vectorizer, open("[vectorizer]" + path1[27:34] + ".pickle", "wb"))

    qry, qry_keys, qry_values = preprocessing_queries(QFile)
    quiries=[' '.join(terms) for terms in qry.values()]
    queries_matrix = vectorizer.transform(quiries)
    pickle.dump(queries_matrix, open("tfidf[qrs]" + path1[27:34] + ".pickle", "wb"))
    pickle.dump(qry_keys, open("tfidf[qry_key]" + path1[27:34] + ".pickle", "wb"))
    pickle.dump(qry_values, open("tfidf[qry_value]" + path1[27:34] + ".pickle", "wb"))

    # df = pd.DataFrame(documents_matrix.toarray(), columns=vectorizer.get_feature_names_out(), index=corpus.keys())
    # df = df.div(df.sum(axis=1), axis=0)
    # pd.set_option('display.max_columns', None)
    # print('Number of documents:', len(corpus))
    # print('Number of unique terms:', df.shape[1])
    # print(df)



############ one time call #############
# create_inverted_index(filename, QFile)
# create_inverted_indexf(fName,....)

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





# create_inverted_index(cleaned_term)
#
# res=calc_similarity('why do fish died with open eyes?',get_docs_matrix("tfidf[docs]antique.pickle"),'[vectorizer]antique.pickle')
# print(res)
# docs, doc_keys = preprocessing_documents(filename)
# matrix = get_docs_matrix("tfidf[docs]antique.pickle")
# res = calc_similarity('why do fish died with open eyes?', get_docs_matrix("tfidf[docs]antique.pickle"), '[vectorizer]antique.pickle', get_docs_matrix("tfidf[doc_key]antique.pickle"))
# print(res)