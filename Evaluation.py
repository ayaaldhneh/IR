import pickle
import numpy as np
from Clustering import do_cluster, do_cluster_query
from Datasets import golden_standard
from main import calc_similarity_vectors, calc_similarity

# qry_vectors = pickle.load(open("tfidf[qrs]antique.pickle", "rb"))
# doc_vectors = pickle.load(open("tfidf[docs]antique.pickle", "rb"))
# doc_keys = pickle.load(open("tfidf[doc_key]antique.pickle", "rb"))
# doc_values = pickle.load(open("tfidf[doc_value]antique.pickle", "rb"))
# qrels = golden_standard(r'C:\Users\aya\Desktop\antique\qrels.TXT')
# qry_key = pickle.load(open("tfidf[qry_key]antique.pickle", "rb"))
# qry_values = pickle.load(open("tfidf[qry_value]antique.pickle", "rb"))

qry_vectors = pickle.load(open("tfidf[qrs]wikIR1k.pickle", "rb"))
doc_vectors = pickle.load(open("tfidf[docs]wikIR1k.pickle", "rb"))
doc_keys = pickle.load(open("tfidf[doc_key]wikIR1k.pickle", "rb"))
doc_values = pickle.load(open("tfidf[doc_value]wikIR1k.pickle", "rb"))
qrels = golden_standard(r'C:\Users\aya\Desktop\wikIR1k\training\qrels.TXT')
qry_key = pickle.load(open("tfidf[qry_key]wikIR1k.pickle", "rb"))
qry_value = pickle.load(open("tfidf[qry_value]wikIR1k.pickle", "rb"))


precision_all = 0.0
recall_all = 0.0
mean_avg_precision = 0.0
mean_reciprocal_rank = 0.0
clustering=False


def calculate_precision(output, matching_output):
    return float(matching_output) / float(output)


def calculate_recall(matching_output, golden_standard):
    relevant_docs = golden_standard.get(query_key, {})
    return float(matching_output) / float(len(relevant_docs))


def calculate_average_precision(relevant_docs, top_doc_key, qid):
    # Sort documents by decreasing order of similarity
    # if(clustering is True):
    #  sorted_docs = sorted(zip(top_doc_key, doc_values), key=lambda x: x[1]['similarity'], reverse=True)
    # else:

    sorted_docs = sorted(zip(top_doc_key, doc_values), key=lambda x: x[1], reverse=True)
    # Compute precision and recall values at each ranked position
    precisions, recalls = [], []
    num_relevant_docs_seen = 0
    for i, (doc_key, doc_value) in enumerate(sorted_docs, start=1):
        relevance = relevant_docs.get(doc_key, None)
        if relevance is not None:
            num_relevant_docs_seen += 1
        precision_i = num_relevant_docs_seen / i
        recall_i = num_relevant_docs_seen / len(relevant_docs)
        precisions.append(precision_i)
        recalls.append(recall_i)

    # Compute average precision by integrating the precision-recall curve
    ap = 0.0
    for i in range(len(precisions)):
        if i == 0:
            delta_recall = recalls[i]
        else:
            delta_recall = recalls[i] - recalls[i - 1]
        ap += precisions[i] * delta_recall

    return ap


def calculate_reciprocal_rank(relevant_docs, top_doc_key):
    for i, doc_key in enumerate(top_doc_key):
        if doc_key in relevant_docs:
            return 1.0 / float(i + 1)
    return 0.0


############## if we want to do clustering##############

# cluster_labels, doc_dicts = do_cluster(doc_vectors, doc_values,doc_keys)
doc_dicts=[]
clustering=False

#######################################################


# Compare each query vector with all document vectors
for i, query_key in enumerate(qry_key):
    counter = 0
    query_vector = qry_vectors[i]
    vectors=[]
    keys=[]
    values=[]
    if(clustering is True):
        qrycluster = do_cluster_query(query_vector)

        print("***********************")
        print(qrycluster)
        print("***********************")

        for doc in doc_dicts:
            if (doc['cluster'] == qrycluster):
                vectors.append(doc['vector'])
                keys.append(doc['key'])
                values.append(doc['text'])

        top_doc_key, top_doc_value = calc_similarity_vectors(query_vector,vectors,keys,values)
    else:
        top_doc_key, top_doc_value = calc_similarity_vectors(query_vector, doc_vectors, doc_keys, doc_values)

    print(f"Query {query_key}")
    print(f"Top document: {len(top_doc_key)}")
    print(f"Top document value: {len(top_doc_value)}")
    print("////////////////////////////////////////////////")
    relevant_docs = qrels.get(query_key, {})
    for doc_key, doc_value in zip(top_doc_key, top_doc_value):
        relevance = relevant_docs.get(doc_key, None)
        if relevance is not None:
            counter += 1
            print(f"Document {doc_key}, relevance={relevance}, similarity={doc_value}")
    print(f"Query {query_key} has {counter} relevant documents")
    if counter != 0:
        precision = calculate_precision(len(top_doc_key), counter)
        recall = calculate_recall(counter, qrels)
        average_precision_query = calculate_average_precision(relevant_docs, top_doc_key, query_key)
        reciprocal_rank = calculate_reciprocal_rank(relevant_docs, top_doc_key)
        print(f"Precision: {precision}")
        print(f"Recall: {recall}")
        print("avg_precision: " + str(average_precision_query))
        print("reciprocal_rank: " + str(reciprocal_rank))

        precision_all += precision
        recall_all += recall
        mean_avg_precision += (average_precision_query / float(len(qry_key)))
        mean_reciprocal_rank += (reciprocal_rank / float(len(qry_key)))

num_queries = len(qry_key)
avg_precision = precision_all / float(num_queries) if num_queries > 0 else 0.0
avg_recall = recall_all / float(num_queries) if num_queries > 0 else 0.0
print("------------------------------------------------------------")
print(f"Average precision = {avg_precision}")
print(f"Average recall = {avg_recall}")
print("mean average precision = " + str(mean_avg_precision))
print("mean reciprocal rank = " + str(mean_reciprocal_rank))
print("------------------------------------------------------------")
