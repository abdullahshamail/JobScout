import streamlit as st
from agents.ingest import ingest
from agents.matcher import match_jobs

st.set_page_config(page_title="AutoJobScout", page_icon="🧭", layout="wide")

st.title("🧭 AutoJobScout")
st.caption("Agentic job discovery + semantic resume matching (multi-source).")

with st.sidebar:
    st.header("Settings")
    per_source = st.slider("Jobs per source", 50, 300, 150, 25)
    top_k = st.slider("Top K results", 5, 25, 10, 1)
    run = st.button("🔎 Find matching jobs")

resume_text = st.text_area("Paste your resume text here", height=250, placeholder="Paste resume text…")

if run:
    if not resume_text.strip():
        st.error("Please paste your resume text.")
        st.stop()

    with st.spinner("Fetching jobs from multiple sources and building index…"):
        idx, raw_count, deduped_count = ingest(job_limit_per_source=per_source)

    st.success(f"Fetched {raw_count} postings, deduped to {deduped_count} unique jobs.")

    with st.spinner("Computing matches…"):
        matches = match_jobs(idx, resume_text, top_k=top_k)

    st.subheader(f"Top {top_k} matches")
    for i, (job, score) in enumerate(matches, start=1):
        with st.container(border=True):
            cols = st.columns([6, 2, 2])
            cols[0].markdown(f"### {i}. {job.title} — {job.company}")
            cols[1].metric("Score", f"{score:.3f}")
            cols[2].markdown(f"**Source:** {job.source}")

            st.write(f"**Location:** {job.location}")
            st.markdown(f"**Link:** {job.url}")
            with st.expander("Show job description"):
                st.write(job.description[:4000] if job.description else "")
