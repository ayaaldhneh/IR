from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))

import csv



# def read_documents(file_path, delimiter):
#     my_dict = {}
#     with open(file_path, "r") as csv_file:
#         reader = csv.reader(csv_file, delimiter=delimiter)
#         for row in reader:
#             key = row[0]
#             value = row[1]
#             my_dict[key] = value
#     return my_dict


def read_documents(file_path, delimiter):
    my_dict = {}
    with open(file_path, "r") as csv_file:
        reader = csv.reader(csv_file, delimiter=delimiter)
        count = 0
        for row in reader:
            count += 1
            if count > 10000:
                break
            key = row[0]
            value = row[1]
            my_dict[key] = value
    return my_dict

# print(read_documents(fName,','))
#print(read_documents(filename,'\t'))


def read_queries(path):

    my_dict = {}
    with open(path, "r") as csv_file:
        reader = csv.reader(csv_file, delimiter='\t')
        for row in reader:
            key = row[0]
            value = row[1]
            my_dict[key] = value

    return my_dict
# read_queries(QFile)



QFile=r'C:\Users\User 2004\Desktop\antique\qrels.TXT'
# def golden_standard(path):
#
#
#
#     my_dict = {}
#     with open(path, "r") as csv_file:
#         reader = csv.reader(csv_file, delimiter='\t')
#         for row in reader:
#             key = row[0]
#             value = row[1]
#             my_dict[key] = value
#
#     return my_dict
def golden_standard(path):

    # f = open(path)
    #
    # qrel = {}
    # with open(path, 'r') as f:
    #     for line in f:
    #         query_id, _, doc_id, relevance = line.split()
    #         if query_id not in qrel:
    #             qrel[query_id] = {}
    #         qrel[query_id][doc_id] = int(relevance)
    # return qrel

    with open(path, 'r') as f:
        qrels = {}
        for line in f:
            query_id, _, doc_id, relevance = line.strip().split()
            relevance = int(relevance)
            if query_id not in qrels:
                qrels[query_id] = {}
            qrels[query_id][doc_id] = relevance
    return qrels


# print(golden_standard(QFile))