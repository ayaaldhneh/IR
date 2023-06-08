antique / wikIR1k datasets:
    steps applied:
    - date processing (for documents only)
    1- lowercasing
    2- stopwords removal
    3- numbers to words
    4- removing puncs
    5- stemming
    6- lemmatization
    7- tf-idf
    8- similarity

"RESULTS":
 antique first 10.000:
    Average precision = 0.0013584209336648242
    Average recall = 0.013510728370579983
    mean average precision = 0.000979876177870463
    mean reciprocal rank = 0.011489610854069946

all antique before Clustering :
    Average precision = 0.010392884935872619
    Average recall = 0.604227638642981
    mean average precision = 0.005953113749598888
    mean reciprocal rank = 0.2915108275730294


all antique after Clustering :
   Average precision = 0.009930769057064715
   Average recall = 0.33513282898630525
   mean average precision = 0.005342707974359607
   mean reciprocal rank = 0.24644871787306985