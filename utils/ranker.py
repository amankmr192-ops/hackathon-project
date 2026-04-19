def rank_resumes(results):
    ranked = sorted(results, key=lambda x: x["score"], reverse=True)

    for i, r in enumerate(ranked):
        r["rank"] = i + 1

    return ranked