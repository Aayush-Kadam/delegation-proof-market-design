from pathlib import Path
import sys
import numpy as np
import pandas as pd
import streamlit as st

ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"src"))
from delegation_market.agents import TruthfulAgent,HedgeAgent,Exp3Agent,QLearningAgent,UCBAgent
from delegation_market.simulation import SimulationConfig,simulate

st.set_page_config(page_title="Delegation-Proof Market Design",layout="wide")
st.title("Delegation-Proof Market Design")
st.caption("A reproducible laboratory for repeated auctions with adaptive bidders — diagnostic outputs are not research claims.")

with st.sidebar:
    with st.form("market_configuration", border=False):
        mechanism=st.selectbox("Auction",["first_price","second_price","hybrid","reserve_first_price","reserve_second_price"])
        rounds=st.slider("Rounds",100,20_000,2_000,100)
        alpha=st.slider("Hybrid first-price weight α",0.0,1.0,0.5,.05)
        reserve=st.slider("Reserve",0.0,1.0,0.0,.05)
        seed=st.number_input("Seed",0,100000,0)
        names=[]
        for i in range(2): names.append(st.selectbox(f"Bidder {i+1}",["Truthful","Hedge","EXP3","Q-learning","UCB"],index=min(i,3),key=f"bidder_{i}"))
        run=st.form_submit_button("Run market",type="primary",width="stretch")

classes={"Truthful":TruthfulAgent,"Hedge":HedgeAgent,"EXP3":Exp3Agent,"Q-learning":QLearningAgent,"UCB":UCBAgent}
if run:
    grid=np.linspace(0,1,101); agents=[classes[n](v,grid,seed=int(seed)+i) for i,(n,v) in enumerate(zip(names,[1.0,.6]))]
    with st.spinner("Running seeded market…"):
        frame,metrics=simulate(agents,SimulationConfig(mechanism=mechanism,rounds=rounds,reserve=reserve,alpha=alpha,seed=int(seed),record_every=max(1,rounds//2000)))
    with st.container(horizontal=True):
        for label,key in [('Revenue','mean_revenue'),('Welfare ratio','welfare_ratio'),('Efficiency','allocative_efficiency'),('Bidder surplus','mean_bidder_surplus')]: st.metric(label,f"{metrics[key]:.3f}",border=True)
    st.subheader("Dynamics")
    bids=frame.pivot(index="round",columns="bidder",values="bid").rename(columns=lambda i:f"Bidder {i+1} bid")
    with st.container(border=True):
        st.markdown("**Bids over time**")
        st.line_chart(bids,x_label="Auction round",y_label="Bid")
    per_round=frame.groupby("round",as_index=False).agg(price=("price","first"),revenue=("payment","sum"),welfare=("value",lambda x:0.0))
    welfare=frame.assign(contribution=frame.value*frame.allocated).groupby("round").contribution.sum().to_numpy(); per_round["welfare"]=welfare
    with st.container(border=True):
        st.markdown("**Price, revenue, and welfare**")
        st.line_chart(per_round.set_index("round"),x_label="Auction round",y_label="Outcome")
    st.subheader("Reproduce")
    st.json({"mechanism":mechanism,"rounds":rounds,"reserve":reserve,"alpha":alpha,"seed":int(seed),"agents":names,"values":[1.0,.6],"config_sha256":metrics["config_sha256"]})
else:
    st.info("Choose a configuration and run the market. The default is a small development run.")
    st.markdown("### Evidence boundary\nThis interface visualizes simulations. It does not label low prices or correlated bids as collusion, and it reports revenue separately from welfare.")
