import pickle

from sklearn.cluster import KMeans
num_clusters = 4
kmeans_model = KMeans(n_clusters=num_clusters, random_state=42)
dicts=[]
def do_cluster(vectors, values,keys):

    # Fit the KMeans model on the document vectors
    cluster_labels=kmeans_model.fit_predict(vectors)

    for i, label in enumerate(cluster_labels):
        print(f"sentence  {i} belongs to cluster {label}")
    print("...................")
    # Convert the list of lists to a list of dictionaries

    dicts = []
    for i, value in enumerate(values):
        doc_dict = {'id': i, 'text': value, 'cluster': None,'vector':None,'key':None}
        dicts.append(doc_dict)

    # Assign the cluster labels to the 'cluster' key in each dictionary
    for i, value in enumerate(dicts):
        value['cluster'] = int(cluster_labels[i])
        value['vector'] = vectors[i]
        value['key'] = keys[i]

    return cluster_labels, dicts


def do_cluster_query(vector):

    query_cluster_labels = kmeans_model.predict(vector)
    print(f"query belongs to cluster {query_cluster_labels}")
    print("...................")

    return query_cluster_labels[0]



