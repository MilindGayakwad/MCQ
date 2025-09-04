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
if "student_verified" not in st.session_state:
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
            st.session_state["student_verified"] = True
            st.session_state["roll"] = roll
            st.session_state["prn"] = prn
            st.session_state["name"] = name
            st.session_state["class"] = class_name
            st.session_state["div"] = div
            st.session_state["responses"] = {}
            st.session_state["q_index"] = 0
            st.session_state["end_time"] = datetime.now() + timedelta(minutes=60)
            st.experimental_rerun()
        else:
            st.error("⚠️ Please fill all fields before starting.")

if "student_verified" in st.session_state:
    questions = load_questions()
    q_index = st.session_state.get("q_index", 0)
    question = questions.iloc[q_index]

    # Timer
    remaining = st.session_state["end_time"] - datetime.now()
    if remaining.total_seconds() > 0:
        mins, secs = divmod(int(remaining.total_seconds()), 60)
        st.warning(f"⏳ Time Remaining: {mins:02d}:{secs:02d}")
    else:
        st.error("⏰ Time is up! Auto-submitting...")
        st.session_state["auto_submit"] = True

    # Display question
    st.subheader(f"Q{question.id}: {question.q}")
    ans = st.multiselect("Choose:", question.options,
                         default=st.session_state["responses"].get(question.id, []))
    st.session_state["responses"][question.id] = ans

    # Navigation
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("⬅ Previous") and q_index > 0:
            st.session_state["q_index"] -= 1
            st.experimental_rerun()
    with col2:
        if st.button("➡ Next") and q_index < len(questions) - 1:
            st.session_state["q_index"] += 1
            st.experimental_rerun()
    with col3:
        if st.button("✅ Submit Exam") or st.session_state.get("auto_submit", False):
            correct = 0
            for _, row in questions.iterrows():
                chosen = st.session_state["responses"].get(row.id, [])
                if set(chosen) == set(row.answer):
                    correct += 1
            total_qs = len(questions)
            score_percent = (correct / total_qs) * 100
            st.success(f"✅ Your Score: {correct}/{total_qs} ({score_percent:.2f}%)")

            result_data = {
                "Roll": st.session_state["roll"],
                "PRN": st.session_state["prn"],
                "Name": st.session_state["name"],
                "Class": st.session_state["class"],
                "Division": st.session_state["div"],
                "Score": correct,
                "Percent": score_percent
            }
            if os.path.exists("results.csv"):
                df_results = pd.read_csv("results.csv")
                df_results = pd.concat([df_results, pd.DataFrame([result_data])], ignore_index=True)
            else:
                df_results = pd.DataFrame([result_data])
            df_results.to_csv("results.csv", index=False)
            st.stop()
