import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

st.title("🚀 AI Resume Analyzer")
st.caption("Smart Resume Evaluation using AI")

# -------------------------------
# UPLOAD
# -------------------------------
uploaded_files = st.file_uploader(
    "📄 Upload Resume(s)",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True
)

job_description = st.text_input(
    "📝 Enter Job Description (comma separated)",
    placeholder="python, ai, machine learning, docker"
)

# -------------------------------
# ANALYZE
# -------------------------------
if st.button("Analyze Resumes"):

    if not uploaded_files or not job_description:
        st.warning("Please upload resumes and enter job description")

    else:
        try:
            files = [("files", (f.name, f, f.type)) for f in uploaded_files]
            data = {"job_description": job_description}

            response = requests.post(
                "http://127.0.0.1:8000/analyze",
                files=files,
                data=data
            )

            result = response.json()
            st.success("✅ Analysis Complete")

            ranked = result["ranked_results"]

            # -------------------------------
            # 🏆 TOP + CHART (SIDE BY SIDE)
            # -------------------------------
            col1, col2 = st.columns([1, 2])

            # TOP CANDIDATE
            with col1:
                top = ranked[0]
                st.markdown("### 🏆 Top Candidate")
                st.success(f"{top['name']}")
                st.metric("Score", f"{top['score']}%")
                st.write(f"🎯 Role: {top.get('role', 'Not detected')}")

            # CHART
            with col2:
                st.markdown("### 📊 Score Comparison")

                names = [r["name"] for r in ranked]
                scores = [r["score"] for r in ranked]

                short_names = [
                    n[:12] + "..." if len(n) > 12 else n
                    for n in names
                ]

                df = pd.DataFrame({
                    "Candidate": short_names,
                    "Score": scores
                }).set_index("Candidate")

                st.bar_chart(df)

            # -------------------------------
            # 📋 DETAILED ANALYSIS
            # -------------------------------
            st.markdown("## 📋 Detailed Analysis")

            for i, res in enumerate(ranked):

                with st.expander(f"👤 {res['name']} (Rank #{i+1})"):

                    st.write(f"📊 Score: {res['score']}%")
                    st.write(f"🎯 Role: {res.get('role', 'Not detected')}")

                    col1, col2 = st.columns(2)

                    # MATCHED
                    with col1:
                        st.markdown("### ✅ Matched Skills")
                        if res["matched_skills"]:
                            for skill in res["matched_skills"]:
                                st.success(skill)
                        else:
                            st.warning("None")

                    # MISSING
                    with col2:
                        st.markdown("### ❌ Missing Skills")
                        if res["missing_skills"]:
                            for skill in res["missing_skills"]:
                                st.error(skill)
                        else:
                            st.success("None 🎉")

                    # -------------------
                    # RECOMMENDATIONS
                    # -------------------
                    st.markdown("### 💡 Recommendations")

                    if res["recommendations"]:
                        for rec in res["recommendations"]:

                            with st.container():
                                st.markdown(f"#### 🔹 {rec['skill']}")
                                st.write(f"📌 {rec['advice']}")

                                colA, colB = st.columns(2)

                                with colA:
                                    st.markdown("📚 Resources")
                                    for r in rec["resources"]:
                                        st.write(f"- {r}")

                                with colB:
                                    st.markdown("🛠 Projects")
                                    for p in rec["projects"]:
                                        st.write(f"- {p}")

                                st.divider()
                    else:
                        st.success("No recommendations needed 🎉")

        except Exception as e:
            st.error(f"Error: {e}")