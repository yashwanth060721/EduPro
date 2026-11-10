import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="EduPro Analytics Dashboard", page_icon="📚", layout="wide")

st.title("🎓 EduPro Learner Demographics & Enrollment Trends")
st.markdown("Exploring online education dynamics, course popularity, and learner segmentation.")

# 2. Re-create Mock Datasets (matching your notebook pipeline)
@st.cache_data
def load_data():
    np.random.seed(42)
    n_users, n_courses, n_transactions = 1000, 20, 3500

    users = pd.DataFrame({
        "UserID": [f"USR_{1000 + i}" for i in range(n_users)],
        "UserName": [f"Learner_{i}" for i in range(n_users)],
        "Age": np.random.normal(loc=29, scale=8.5, size=n_users).clip(14, 65).astype(int),
        "Gender": np.random.choice(["Female", "Male", "Non-Binary", "Prefer not to say"], size=n_users)
    })

    courses = pd.DataFrame({
        "CourseID": [f"CRS_{100 + i}" for i in range(n_courses)],
        "CourseName": [f"Course Title {i}" for i in range(n_courses)],
        "CourseCategory": np.random.choice(["Data Science", "Software Engineering", "Business & Finance", "Healthcare", "Design & UX"], size=n_courses),
        "CourseType": np.random.choice(["Self-Paced", "Instructor-Led", "Bootcamp Short"], size=n_courses),
        "CourseLevel": np.random.choice(["Beginner", "Intermediate", "Advanced"], size=n_courses)
    })

    transactions = pd.DataFrame({
        "TransactionID": [f"TXN_{10000 + i}" for i in range(n_transactions)],
        "UserID": np.random.choice(users["UserID"], size=n_transactions),
        "CourseID": np.random.choice(courses["CourseID"], size=n_transactions)
    })

    df_merged = transactions.merge(users, on="UserID", how="inner").merge(courses, on="CourseID", how="inner")
    
    bins = [0, 17, 25, 35, 45, 100]
    labels = ["<18", "18-25", "26-35", "36-45", "45+"]
    df_merged["AgeGroup"] = pd.cut(df_merged["Age"], bins=bins, labels=labels, right=True)
    
    return df_merged

df_merged = load_data()

# 3. Sidebar Filters
st.sidebar.header("🔍 Filter Dashboard")
selected_category = st.sidebar.selectbox("Select Course Category", ["All"] + list(df_merged["CourseCategory"].unique()))

if selected_category != "All":
    filtered_df = df_merged[df_merged["CourseCategory"] == selected_category]
else:
    filtered_df = df_merged

# 4. KPI Metrics Row
st.subheader("📌 Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Enrollments", len(filtered_df))
col2.metric("Unique Learners", filtered_df["UserID"].nunique())
col3.metric("Popular Category", filtered_df["CourseCategory"].mode()[0] if not filtered_df.empty else "N/A")
col4.metric("Avg Learner Age", f"{int(filtered_df['Age'].mean())} yrs" if not filtered_df.empty else "N/A")

st.markdown("---")

# 5. Visualizations
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📊 Course Popularity by Category")
    cat_counts = filtered_df["CourseCategory"].value_counts().reset_index()
    cat_counts.columns = ["CourseCategory", "Enrollments"]
    fig_cat = px.bar(cat_counts, x="CourseCategory", y="Enrollments", color="CourseCategory", template="plotly_dark")
    st.plotly_chart(fig_cat, use_container_width=True)

with col_right:
    st.subheader("🍩 Learner Age Demographics")
    age_counts = filtered_df["AgeGroup"].value_counts().sort_index().reset_index()
    age_counts.columns = ["AgeGroup", "Count"]
    fig_age = px.pie(age_counts, names="AgeGroup", values="Count", hole=0.4, template="plotly_dark")
    st.plotly_chart(fig_age, use_container_width=True)