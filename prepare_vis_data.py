from sentence_transformers import SentenceTransformer
from sentence_transformers import util

from sklearn.cluster import KMeans
from sklearn.manifold import TSNE 

import argument_embed_vis.example_debates as example_debates

import pickle
import pandas as pd

print(pd.__version__)
e_corpus = example_debates.EXAMPLE_DEBATE_1.split(".")
# e_corpus = example_debates.EXAMPLE_DEBATE_2.split(".")


model = SentenceTransformer('all-MiniLM-L6-v2')
corpus_embeddings = model.encode(e_corpus) 

all_viz_data ={}
for num_clusters in [2,3,4,5,6,7,8]:
    print(num_clusters)
    clustering_model = KMeans(n_clusters=num_clusters)
    clustering_model.fit(corpus_embeddings)
    cluster_assignment = clustering_model.labels_
    clustered_sentences = [[] for i in range(num_clusters)]

    tsne_dims = TSNE(n_components=2, 
                        learning_rate='auto', 
                        init='random',
                        random_state=42).fit_transform(corpus_embeddings)

    df = pd.DataFrame(columns=['cluster_id','sentence',
    # 'sentence_embedding',
    'tsne_x','tsne_y'])

    df["cluster_id"] = cluster_assignment
    df["sentence"] = e_corpus
    # df["sentence_embedding"] = corpus_embeddings[:,:]
    df["tsne_x"] = tsne_dims[:,0]
    df["tsne_y"] = tsne_dims[:,1]

    all_viz_data[num_clusters] = df


pickle.dump(all_viz_data, open("example_debate_1_processed.pkl",'wb'))
# pickle.dump(all_viz_data, open("example_debate_2_processed.pkl",'wb'))