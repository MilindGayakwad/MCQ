#  Online MCQ Exam System (Student + Teacher Separation, Fixed Dashboard)

This system has **two apps**:

1. `student_app.py` → Students attempt exam (MCQs, 60-min auto-submit, results saved).
2. `teacher_dashboard.py` → Teachers log in (password protected, fixed logic) to view results, leaderboard, analytics.

##  Run Locally
```bash
pip install -r requirements.txt
python -m streamlit run student_app.py
python -m streamlit run teacher_dashboard.py
```

##  Deploy on Streamlit Cloud
Upload both apps to GitHub and deploy them separately:
- Student app → public exam link
- Teacher app → password-protected dashboard
