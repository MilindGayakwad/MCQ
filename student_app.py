import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

def load_questions(csv_path="questions.csv"):
    df = pd.read_csv(csv_path)
    data = []
    for _, row in df.iterrows():
        options = [row["option1"], row["option2"], row["option3"], row["option4"]]
        correct_answers = [a.strip() for a in str(row["answer"]).split(";")]
        data.append({
            "id": int(row["id"]),
            "q": row["q"],
            "options": options,
            "answer": correct_answers,
            "topic": row["topic"],
            "co": row["co"],
            "blooms": row["blooms"]
        })
    return pd.DataFrame(data)

st.title("🎓 Student MCQ Exam Portal")

# Student info
with st.form("student_info"):
    st.subheader("📝 Student Information")
    roll = st.text_input("Roll Number")
    prn = st.text_input("PRN")
    name = st.text_input("Full Name")
    class_name = st.text_input("Class (e.g., SE, TE, BE)")
    div = st.text_input("Division")
    start_exam = st.form_submit_button("Start Exam")

if start_exam:
    roll, prn, name, class_name, div = roll.strip(), prn.strip(), name.strip(), class_name.strip(), div.strip()
    if all([roll, prn, name, class_name, div]):
        st.success(f"Welcome {name} (Roll: {roll}, PRN: {prn}, {class_name}-{div}) 🎉")
        questions = load_questions()
        if "responses" not in st.session_state:
            st.session_state["responses"] = {}
        if "end_time" not in st.session_state:
            st.session_state["end_time"] = datetime.now() + timedelta(minutes=60)

        # Timer
        remaining = st.session_state["end_time"] - datetime.now()
        if remaining.total_seconds() > 0:
            mins, secs = divmod(int(remaining.total_seconds()), 60)
            st.warning(f"⏳ Time Remaining: {mins:02d}:{secs:02d}")
        else:
            st.error("⏰ Time is up! Auto-submitting...")
            if "auto_submitted" not in st.session_state:
                st.session_state["auto_submitted"] = True
                st.session_state["force_submit"] = True
                st.experimental_rerun()

        for _, row in questions.iterrows():
            st.subheader(f"Q{row.id}: {row.q}")
            ans = st.multiselect("Choose:", row.options, default=None, key=f"q{row.id}")
            st.session_state["responses"][row.id] = ans

        submit_pressed = st.button("Submit") or st.session_state.get("force_submit", False)
        if submit_pressed:
            correct = 0
            for _, row in questions.iterrows():
                chosen = st.session_state["responses"].get(row.id, [])
                if set(chosen) == set(row.answer):
                    correct += 1

            total_qs = len(questions)
            score_percent = (correct / total_qs) * 100
            st.success(f"✅ Your Score: {correct}/{total_qs} ({score_percent:.2f}%)")

            result_data = {
                "Roll": roll,
                "PRN": prn,
                "Name": name,
                "Class": class_name,
                "Division": div,
                "Score": correct,
                "Percent": score_percent
            }
            if os.path.exists("results.csv"):
                df_results = pd.read_csv("results.csv")
                df_results = pd.concat([df_results, pd.DataFrame([result_data])], ignore_index=True)
            else:
                df_results = pd.DataFrame([result_data])
            df_results.to_csv("results.csv", index=False)
    else:
        st.error("⚠️ Please fill all fields before starting.")
