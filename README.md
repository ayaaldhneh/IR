# IR

antique / wikIR1k datasets:
    steps applied:
    - date processing (for documents only)
    1- lowercasing
    2- stopwords removal
    3- removing puncs
    4- remove Acronomies
    5- stemming
    6- lemmatization
    7- tf-idf
    8- similarity

"RESULTS":

all antique before Clustering :

   Average precision = 0.010313353157731426
   Average recall = 0.603940418656183
   mean average precision = 0.005771237612059775
   mean reciprocal rank = 0.2906820772831279


all antique after Clustering :
   Average precision = 0.010377518827150413
   Average recall = 0.36500308856597463
   mean average precision = 0.005417219711696655
   mean reciprocal rank = 0.2521504435214747


all wikIR1k before Clustering :
   Average precision = 0.04123925496074963
   Average recall = 0.6982175691535768
   mean average precision = 0.048215173271309725
   mean reciprocal rank = 0.5872882355770691


all wikIR1k after Clustering :
   Average precision = 0.04219949766642758
   Average recall = 0.5139970823574279
   mean average precision = 0.040603968804809126
   mean reciprocal rank = 0.5428220063861247
