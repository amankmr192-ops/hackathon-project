import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

st.title("🚀 AI Resume Analyzer")
st.caption("Smart Resume Evaluation using AI")

# Upload multiple resumes
uploaded_files = st.file_uploader(
    "📄 Upload Resume(s)",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True
)

# Job description input
job_description = st.text_input(
    "📝 Enter Job Description (comma separated)",
    placeholder="python, ai, machine learning, communication"
)

# Analyze button
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

            # -------------------------------
            # 🏆 TOP CANDIDATE
            # -------------------------------
            top = result["ranked_results"][0]

            st.subheader("🏆 Top Candidate")
            st.success(f"{top['name']} — {top['score']}%")

            st.write(f"🎯 Role: {top.get('role', 'Not detected')}")

            # -------------------------------
            # 📊 SCORE COMPARISON (FIXED)
            # -------------------------------
            st.subheader("📊 Score Comparison")

            names = [r["name"] for r in result["ranked_results"]]
            scores = [r["score"] for r in result["ranked_results"]]

            # shorten long names
            short_names = [
                n[:15] + "..." if len(n) > 15 else n
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
            st.subheader("📋 Detailed Analysis")

            for i, res in enumerate(result["ranked_results"]):

                with st.expander(f"👤 {res['name']} (Rank #{i+1})"):

                    st.write(f"📊 Score: {res['score']}%")
                    st.write(f"🎯 Role: {res.get('role', 'Not detected')}")

                    st.markdown("### ✅ Matched Skills")
                    if res["matched_skills"]:
                        for skill in res["matched_skills"]:
                            st.success(skill)
                    else:
                        st.warning("No matched skills")

                    st.markdown("### ❌ Missing Skills")
                    for skill in res["missing_skills"]:
                        st.error(skill)

                    st.markdown("### 💡 Recommendations")
                    for rec in res["recommendations"]:
                        st.info(rec)

        except Exception as e:
            st.error(f"Error: {e}")