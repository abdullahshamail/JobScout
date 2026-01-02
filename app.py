import sys
import os
from pathlib import Path

ROOT = Path(__file__).parent.absolute()
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
from agents.graph import job_graph
from utils.text import clean_html
from utils.logger import app_logger
import config

st.set_page_config(
    page_title=config.STREAMLIT_PAGE_TITLE,
    page_icon=config.STREAMLIT_PAGE_ICON,
    layout=config.STREAMLIT_LAYOUT,
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        color: #666;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🧭 AutoJobScout</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">AI-powered job discovery using LLM planners, LangGraph orchestration, and multi-source ingestion</p>',
    unsafe_allow_html=True
)

# Initialize session state
if "results" not in st.session_state:
    st.session_state.results = None
if "intent" not in st.session_state:
    st.session_state.intent = ""
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

# Sidebar
with st.sidebar:
    st.header("⚙️ Search Configuration")
    
    intent = st.text_input(
        "Job Search Intent",
        value=st.session_state.intent,
        placeholder="e.g., machine learning engineer roles, data scientist positions",
        help="Describe the type of jobs you're looking for"
    )
    st.session_state.intent = intent
    
    with st.expander("🎯 Advanced Settings", expanded=True):
        top_k = st.slider(
            "Number of results",
            min_value=5,
            max_value=50,
            value=config.DEFAULT_TOP_K,
            help="How many matching jobs to return"
        )
        
        sources = st.multiselect(
            "Job Sources",
            ["RemoteOK", "Remotive", "WeWorkRemotely", "NewGradJobs", "Indeed", "Adzuna", "Greenhouse"],
            default=["RemoteOK", "Remotive", "WeWorkRemotely"],
            help="Select which job boards to search"
        )
        
        fetch_descriptions = st.checkbox(
            "Fetch full job descriptions",
            value=False,  # Default to False for speed
            help="Slower but more accurate matching"
        )
        
        run_gap_analysis = st.checkbox(
            "Run skill gap analysis",
            value=True,
            help="Analyze missing skills for top matches"
        )
    
    st.divider()
    
    search_button = st.button("🔍 Find Matching Jobs", type="primary", use_container_width=True)
    
    if st.session_state.results:
        if st.button("🔄 Clear Results", use_container_width=True):
            st.session_state.results = None
            st.rerun()
    
    st.divider()
    
    with st.expander("ℹ️ About AutoJobScout"):
        st.markdown("""
        **AutoJobScout** uses:
        - 🤖 LangGraph for agent orchestration
        - 🔍 Multi-source job aggregation
        - 🧠 Semantic matching with embeddings
        - 📊 LLM-powered explanations
        - ✅ Self-critique for accuracy
        """)

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📄 Your Resume")
    resume_text = st.text_area(
        "Paste your resume",
        height=300,
        placeholder="Paste your complete resume here...",
        value=st.session_state.resume_text,
        label_visibility="collapsed"
    )
    st.session_state.resume_text = resume_text

with col2:
    st.subheader("💡 Tips for Best Results")
    st.info("""
    **For optimal matching:**
    
    ✓ Include complete work experience
    
    ✓ List technical skills clearly
    
    ✓ Mention specific projects
    
    ✓ Add education details
    
    ✓ Be specific in your job intent
    """)

# Execute search
if search_button:
    if not resume_text.strip():
        st.error("⚠️ Please paste your resume text before searching.")
        st.stop()
    
    if not sources:
        st.error("⚠️ Please select at least one job source.")
        st.stop()
    
    if not intent.strip():
        st.warning("💡 Tip: Add a job search intent for better results!")
    
    # ✅ FIX: Pass user settings to the graph
    initial_state = {
        "resume_text": resume_text,
        "user_intent": intent or "relevant job opportunities",
        "use_sources": sources,  # ✅ User-selected sources
        "fetch_descriptions": fetch_descriptions,  # ✅ User preference
        "top_k": top_k,  # ✅ User-selected count
        "run_gap_analysis": run_gap_analysis,  # ✅ User preference
    }
    
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        status_text.text("🤖 Planning search strategy...")
        progress_bar.progress(20)
        
        status_text.text("📥 Fetching jobs from multiple sources...")
        progress_bar.progress(40)
        
        status_text.text("🔍 Analyzing and matching jobs...")
        progress_bar.progress(60)
        
        # Execute the agent graph
        final_state = job_graph.invoke(initial_state)
        
        status_text.text("✨ Generating explanations...")
        progress_bar.progress(80)
        
        progress_bar.progress(100)
        status_text.text("✅ Analysis complete!")
        
        # Store results
        st.session_state.results = final_state
        
        app_logger.info(f"Job search completed: {len(final_state.get('matches', []))} matches found")
        
    except Exception as e:
        st.error(f"❌ Error during job search: {str(e)}")
        app_logger.error(f"Job search failed: {e}", exc_info=True)
        st.stop()
    finally:
        progress_bar.empty()
        status_text.empty()

# Display results
if st.session_state.results:
    final_state = st.session_state.results
    matches = final_state.get("matches", [])
    
    if not matches:
        st.warning("😔 No matching jobs found. Try adjusting your search criteria or resume.")
        st.stop()
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Jobs Found", len(matches))
    with col2:
        avg_score = sum(score for _, score in matches) / len(matches)
        st.metric("Avg Match Score", f"{avg_score:.3f}")
    with col3:
        sources_used = len(final_state.get("use_sources", []))
        st.metric("Sources Searched", sources_used)
    with col4:
        top_score = matches[0][1] if matches else 0
        st.metric("Top Match Score", f"{top_score:.3f}")
    
    st.divider()
    
    # Job results
    st.subheader("🎯 Top Matching Jobs")
    
    for rank, (job, score) in enumerate(matches, start=1):
        with st.container(border=True):
            cols = st.columns([8, 2])
            
            with cols[0]:
                st.markdown(f"### {rank}. {job.title}")
                st.markdown(f"**{job.company}** • {job.location}")
                
            with cols[1]:
                st.metric("Match", f"{score:.3f}", delta=None)
                st.markdown(f"*{getattr(job, 'source', 'Unknown')}*")
            
            # Job details
            job_col1, job_col2 = st.columns([3, 1])
            
            with job_col1:
                if job.description:
                    with st.expander("📄 View Job Description"):
                        clean_desc = clean_html(job.description)
                        paragraphs = [p.strip() for p in clean_desc.split("\n") if len(p.strip()) > 40]
                        for p in paragraphs[:15]:
                            st.markdown(f"- {p}")
            
            with job_col2:
                st.link_button("🔗 View Job", job.url, use_container_width=True)
                
                if job.tags:
                    st.caption("Tags:")
                    for tag in job.tags[:5]:
                        st.caption(f"• {tag}")
    
    st.divider()
    
    # Explanation section
    if final_state.get("explanation"):
        with st.container(border=True):
            st.subheader("💡 Why These Jobs Match")
            st.write(final_state["explanation"])
    
    # Gap analysis
    if final_state.get("gap_analysis"):
        with st.container(border=True):
            st.subheader("📊 Skill Gap Analysis")
            st.write(final_state["gap_analysis"])
    
    # Agent execution trace
    with st.expander("🔍 Agent Execution Trace"):
        agent_log = final_state.get("agent_log", [])
        for i, step in enumerate(agent_log, 1):
            st.text(f"{i}. {step}")
    
    # Self-critique
    if final_state.get("critique"):
        with st.expander("🤔 System Self-Critique"):
            st.info(final_state["critique"])

# Footer
st.divider()
st.caption("Built with LangGraph, Streamlit, and powered by Groq LLMs")