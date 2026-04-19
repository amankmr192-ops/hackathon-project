from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

def semantic_match(resume_skills, job_skills):

    matched = []
    missing = []

    if not resume_skills:
        return [], job_skills

    resume_embeddings = model.encode(resume_skills, convert_to_tensor=True)
    job_embeddings = model.encode(job_skills, convert_to_tensor=True)

    for i, job_skill in enumerate(job_skills):
        scores = util.cos_sim(job_embeddings[i], resume_embeddings)

        max_score = scores.max().item()

        if max_score > 0.5:   # threshold
            matched.append(job_skill)
        else:
            missing.append(job_skill)

    return matched, missing