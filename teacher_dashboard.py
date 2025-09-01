import streamlit as st
import pandas as pd
import plotly.express as px
import os

PASSWORD = "admin123"  # change for security

st.title("👩‍🏫 Teacher Dashboard")

pwd = st.text_input("Enter Teacher Password:", type="password")

if pwd == PASSWORD:
    st.success("✅ Access granted. Welcome, Teacher!")

    if os.path.exists("results.csv"):
        df = pd.read_csv("results.csv")

        st.subheader("📊 All Student Results")
        st.dataframe(df)
        st.download_button("📥 Download Results CSV", df.to_csv(index=False), "results.csv")

        st.subheader("🏆 Top 10 Leaderboard")
        leaderboard = df.sort_values(by="Score", ascending=False).head(10)
        for i, row in leaderboard.iterrows():
            symbol = "👏" if row["Percent"] >= 70 else ("👎" if row["Percent"] < 40 else "👌")
            st.write(f"{row['Name']} ({row['Class']}-{row['Division']}) | Score: {row['Score']} | {symbol}")

        if "Class" in df.columns:
            co_summary = df.groupby("Class")["Score"].mean().reset_index()
            st.plotly_chart(px.bar(co_summary, x="Class", y="Score", title="Average Score by Class"))

    else:
        st.warning("No results found yet.")

elif pwd:  # show error only if wrong password entered
    st.error("❌ Wrong password, try again.")
