import streamlit as st
import requests

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

# ---------------- TITLE ----------------
st.title("🚀 AI Resume Analyzer")
st.caption("Smart Resume Evaluation using AI")

# ---------------- INPUT ----------------
uploaded_file = st.file_uploader(
    "📄 Upload Resume",
    type=["pdf", "docx", "txt"]
)

job_description = st.text_input(
    "📝 Enter Job Description (comma separated)",
    placeholder="python, machine learning, docker, ai"
)

# ---------------- BUTTON ----------------
if st.button("Analyze Resume"):

    if uploaded_file and job_description:

        with st.spinner("Analyzing Resume..."):

            try:
                files = {
    "file": (
        uploaded_file.name,
        uploaded_file.getvalue(),
        uploaded_file.type
    )
}
                data = {"job_description": job_description}

                response = requests.post(
                    "http://127.0.0.1:8000/analyze/",
                    files=files,
                    data=data
                )

                result = response.json()

                st.success("✅ Analysis Complete")

                # -------- ROLE --------
                st.subheader("🎯 Predicted Role")
                st.write(result.get("role", "Not detected"))

                # -------- SCORE --------
                st.subheader("📊 Match Score")
                st.metric("Score", f"{result['score']}%")

                # -------- SKILLS --------
                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("✅ Matched Skills")
                    for skill in result["matched_skills"]:
                        st.success(skill)

                with col2:
                    st.subheader("❌ Missing Skills")
                    for skill in result["missing_skills"]:
                        st.error(skill)

                # -------- RECOMMENDATIONS --------
                st.subheader("💡 Recommendations")

                for rec in result["recommendations"]:
                    st.markdown(f"### 🔹 {rec['skill']}")
                    st.write(rec["recommendation"])

                    st.markdown("**📚 Resources:**")
                    for r in rec["resources"]:
                        st.markdown(f"- {r}")

                    st.divider()

                # -------- EXPLANATION --------
                st.subheader("🧠 Explanation")
                st.info(result["explanation"])

            except:
                st.error("❌ Backend server not running")

    else:
        st.warning("⚠️ Upload resume and enter job description")