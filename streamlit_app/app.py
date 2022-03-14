import pathlib
import streamlit as st
import altair as alt
import pickle
import pandas
import numpy




if __name__ == "__main__":
    print("restarting streamlit app...")
    # all_viz_data = pickle.load(open("./example_debate_1_processed.pkl",'rb'))
    all_viz_data = pickle.load(open("./example_debate_2_processed.pkl",'rb'))

    st.header("Clustered arguments from the a small example debate")

    # number_of_words = st.slider("number of words to include", min_value=5, max_value=100, value=10)
    number_of_clusters = st.slider("number of clusters to display", min_value=2, max_value=8, step=1, value=3)
    source_df = all_viz_data[number_of_clusters]
    
    # source = source_df[source_df['word_count'] > number_of_words]
  

    chart = alt.Chart(source_df).mark_circle(size=100).encode(
        x='tsne_x',
        y='tsne_y',
        color=alt.Color('cluster_id', scale=alt.Scale(scheme='category20')) ,
        tooltip=['cluster_id','sentence']
    ).configure_axis(
        grid=False
    ).configure_view(
        strokeWidth=0
    ).properties(
        width=600,
        height=400,
    ).interactive()


    st.altair_chart(chart)
