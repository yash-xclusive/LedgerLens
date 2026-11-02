import json, os, sys
import pandas as pd
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

ROOT=os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, ROOT)
from src.entity_resolution import candidate_pairs
from src.anomaly_detection import flag_duplicate_payments, flag_unusual_amounts
from src.graph_engine import build_entity_graph

st.set_page_config(page_title="LedgerLens", page_icon="🔎", layout="wide")
st.title("LedgerLens")
st.caption("Explainable financial entity resolution & payment intelligence — synthetic-data prototype")

with open(os.path.join(ROOT,"data/synthetic/business_records.json")) as f:
    records=json.load(f)
tx=pd.read_csv(os.path.join(ROOT,"data/synthetic/transactions.csv"))

st.warning("Demo only: all records are synthetic. Similarity scores are heuristic, not probabilities. No fraud determination or automatic entity merge is performed.")
c1,c2,c3=st.columns(3)
c1.metric("Business records",len(records))
c2.metric("Transactions",len(tx))
c3.metric("Candidate comparisons",len(candidate_pairs(records)))

tab1,tab2,tab3=st.tabs(["Entity matching","Payment signals","Relationship graph"])
with tab1:
    st.subheader("Evidence-based candidate matching")
    pairs=candidate_pairs(records)
    rows=[]
    for p in pairs:
        rows.append({"Record A":p["record_a"],"Record B":p["record_b"],"Score":p["score"],"Recommendation":p["recommendation"]})
    st.dataframe(pd.DataFrame(rows).sort_values("Score",ascending=False),use_container_width=True)
    selected=st.selectbox("Inspect a candidate pair",[f'{p["record_a"]} ↔ {p["record_b"]}' for p in pairs])
    p=next(p for p in pairs if f'{p["record_a"]} ↔ {p["record_b"]}'==selected)
    st.json(p)
with tab2:
    st.subheader("Transaction review signals")
    flagged=flag_duplicate_payments(tx)
    flagged=flag_unusual_amounts(flagged)
    st.dataframe(flagged,use_container_width=True)
    st.caption("A duplicate reference or unusual amount is a review signal only, not evidence of fraud.")
with tab3:
    st.subheader("Entity and transaction relationships")
    graph=build_entity_graph(records,tx.to_dict("records"))
    fig,ax=plt.subplots(figsize=(11,6))
    pos=nx.spring_layout(graph,seed=7)
    nx.draw_networkx(graph,pos,ax=ax,node_size=700,font_size=7)
    ax.axis("off")
    st.pyplot(fig)
