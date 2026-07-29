import streamlit as st
import time
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Meridian · AI Research Agent",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@300;400;500;600&family=Inter:ital,wght@0,300;0,400;0,500;1,300&display=swap');

/* ── Reset & base ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: #dce8e5;
}

.stApp {
    background: #05070a;
    background-image:
        radial-gradient(ellipse 70% 45% at 15% -8%, rgba(45,212,191,0.10) 0%, transparent 60%),
        radial-gradient(ellipse 55% 35% at 90% 105%, rgba(74,222,128,0.06) 0%, transparent 55%);
}

/* ── Hide default streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem; max-width: 1200px; }

/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 3.5rem 0 2.5rem;
    position: relative;
}
.hero-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #2dd4bf;
    margin-bottom: 1rem;
    opacity: 0.9;
}
.hero h1 {
    font-family: 'Space Grotesk', sans-serif;
    font-size: clamp(2.8rem, 6vw, 5rem);
    font-weight: 700;
    line-height: 1.0;
    letter-spacing: -0.03em;
    color: #eef4f2;
    margin: 0 0 1rem;
}
.hero h1 span {
    color: #2dd4bf;
}
.hero-sub {
    font-size: 1.05rem;
    font-weight: 300;
    color: #8fa39e;
    max-width: 520px;
    margin: 0 auto;
    line-height: 1.65;
}

/* ── Divider ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(45,212,191,0.3), transparent);
    margin: 2rem 0;
}

/* ── Input card ── */
.input-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(45,212,191,0.15);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 2rem;
    backdrop-filter: blur(8px);
}

/* ── Streamlit input overrides ── */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(45,212,191,0.25) !important;
    border-radius: 10px !important;
    color: #eef4f2 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.75rem 1rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stTextInput > div > div > input:focus {
    border-color: #2dd4bf !important;
    box-shadow: 0 0 0 3px rgba(45,212,191,0.12) !important;
}
.stTextInput > label {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    color: #2dd4bf !important;
    font-weight: 500 !important;
}

/* ── Button ── */
.stButton > button {
    background: linear-gradient(135deg, #2dd4bf 0%, #22a58f 100%) !important;
    color: #05070a !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.04em !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.7rem 2.2rem !important;
    cursor: pointer !important;
    transition: transform 0.15s, box-shadow 0.15s, opacity 0.15s !important;
    box-shadow: 0 4px 20px rgba(45,212,191,0.25) !important;
    width: 100%;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(45,212,191,0.35) !important;
    opacity: 0.95 !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Signal rail (pipeline visual) ── */
.rail {
    position: relative;
    padding-left: 2.6rem;
}
.rail-item {
    position: relative;
    padding-bottom: 2.1rem;
}
.rail-item:last-child { padding-bottom: 0; }
.rail-node {
    position: absolute;
    left: -2.6rem;
    top: 0.15rem;
    width: 1.3rem;
    height: 1.3rem;
    border-radius: 50%;
    background: #0c1210;
    border: 2px solid rgba(255,255,255,0.15);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 2;
    transition: border-color 0.3s, box-shadow 0.3s;
}
.rail-node::after {
    content: '';
    width: 0.4rem;
    height: 0.4rem;
    border-radius: 50%;
    background: rgba(255,255,255,0.2);
}
.rail-node.running {
    border-color: #2dd4bf;
    box-shadow: 0 0 0 4px rgba(45,212,191,0.15), 0 0 14px rgba(45,212,191,0.5);
    animation: pulse-node 1.4s ease-in-out infinite;
}
.rail-node.running::after { background: #2dd4bf; }
.rail-node.done {
    border-color: #4ade80;
    box-shadow: 0 0 0 4px rgba(74,222,128,0.12);
}
.rail-node.done::after { background: #4ade80; }
@keyframes pulse-node {
    0%, 100% { box-shadow: 0 0 0 4px rgba(45,212,191,0.15), 0 0 14px rgba(45,212,191,0.5); }
    50% { box-shadow: 0 0 0 7px rgba(45,212,191,0.06), 0 0 20px rgba(45,212,191,0.7); }
}
.rail-item:not(:last-child)::before {
    content: '';
    position: absolute;
    left: -2rem;
    top: 1.45rem;
    width: 2px;
    height: calc(100% - 0.3rem);
    background: rgba(255,255,255,0.08);
}
.rail-item.line-done:not(:last-child)::before {
    background: linear-gradient(180deg, #4ade80, rgba(74,222,128,0.2));
}

.rail-card {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px;
    padding: 1rem 1.3rem;
    transition: border-color 0.3s, background 0.3s;
}
.rail-card.running {
    border-color: rgba(45,212,191,0.35);
    background: rgba(45,212,191,0.04);
}
.rail-card.done {
    border-color: rgba(74,222,128,0.25);
    background: rgba(74,222,128,0.03);
}
.rail-head {
    display: flex;
    align-items: baseline;
    gap: 0.7rem;
}
.rail-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.95rem;
    font-weight: 600;
    color: #eef4f2;
}
.rail-status {
    margin-left: auto;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.66rem;
    letter-spacing: 0.1em;
}
.status-waiting  { color: #4a5550; }
.status-running  { color: #2dd4bf; }
.status-done     { color: #4ade80; }
.rail-desc {
    font-size: 0.8rem;
    color: #6b7975;
    margin-top: 0.25rem;
}

/* ── Result panels ── */
.result-panel {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 1.8rem 2rem;
    margin-top: 1rem;
    margin-bottom: 1.5rem;
}
.result-panel-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #2dd4bf;
    margin-bottom: 1rem;
    padding-bottom: 0.7rem;
    border-bottom: 1px solid rgba(45,212,191,0.15);
}
.result-content {
    font-size: 0.92rem;
    line-height: 1.8;
    color: #cdd8d4;
    white-space: pre-wrap;
    font-family: 'Inter', sans-serif;
}

/* ── Report & feedback panels ── */
.report-panel {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(45,212,191,0.2);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-top: 1rem;
}
.feedback-panel {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(74,222,128,0.2);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-top: 1rem;
}
.panel-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
    padding-bottom: 0.7rem;
}
.panel-label.teal {
    color: #2dd4bf;
    border-bottom: 1px solid rgba(45,212,191,0.15);
}
.panel-label.green {
    color: #4ade80;
    border-bottom: 1px solid rgba(74,222,128,0.15);
}

/* ── Progress text ── */
.stSpinner > div { color: #2dd4bf !important; }

/* ── Expander ── */
details summary {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.75rem !important;
    color: #8fa39e !important;
    letter-spacing: 0.1em !important;
    cursor: pointer;
}

/* ── Section heading ── */
.section-heading {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: #eef4f2;
    margin: 2rem 0 1rem;
}

/* ── Example chips ── */
.chip {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 6px;
    padding: 0.25rem 0.7rem;
    font-size: 0.75rem;
    color: #8fa39e;
    font-family: 'Inter', sans-serif;
}

/* ── Toast-style notice ── */
.notice {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: #4a5550;
    text-align: center;
    margin-top: 3rem;
    letter-spacing: 0.08em;
}
</style>
""", unsafe_allow_html=True)


# ── Session state init ────────────────────────────────────────────────────────
for key in ("results", "running", "done"):
    if key not in st.session_state:
        st.session_state[key] = {} if key == "results" else False


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Multi-Agent AI System</div>
    <h1>Meridian</h1>
    <p class="hero-sub">
        Four specialized AI agents collaborate — searching, scraping, writing,
        and critiquing — to deliver a polished research report on any topic.
    </p>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)


# ── Layout: input left, pipeline right ───────────────────────────────────────
col_input, col_spacer, col_pipeline = st.columns([5, 0.5, 4])

with col_input:
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    topic = st.text_input(
        "Research Topic",
        placeholder="e.g. Quantum computing breakthroughs in 2025",
        key="topic_input",
        label_visibility="visible",
    )
    run_btn = st.button("⚡  Run Research Pipeline", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Example chips
    chips_html = '<div style="display:flex;gap:0.5rem;flex-wrap:wrap;margin-bottom:1.5rem;align-items:center;">'
    chips_html += '<span style="font-family:\'JetBrains Mono\',monospace;font-size:0.68rem;color:#4a5550;letter-spacing:0.1em;">TRY →</span>'
    for ex in ["LLM agents 2025", "CRISPR gene editing", "Fusion energy progress"]:
        chips_html += f'<span class="chip">{ex}</span>'
    chips_html += '</div>'
    st.markdown(chips_html, unsafe_allow_html=True)

with col_pipeline:
    st.markdown('<div class="section-heading">Pipeline</div>', unsafe_allow_html=True)

    r = st.session_state.results
    steps = [
        ("search", "Search Agent", "Gathers recent web information"),
        ("reader", "Reader Agent", "Scrapes & extracts deep content"),
        ("writer", "Writer Chain", "Drafts the full research report"),
        ("critic", "Critic Chain", "Reviews & scores the report"),
    ]

    def step_state(key):
        if key in r:
            return "done"
        if st.session_state.running:
            for k, _, _ in steps:
                if k not in r:
                    return "running" if k == key else "waiting"
        return "waiting"

    status_labels = {"waiting": "WAITING", "running": "● RUNNING", "done": "✓ DONE"}

    rail_html = '<div class="rail">'
    for key, title, desc in steps:
        state = step_state(key)
        line_cls = "line-done" if state == "done" else ""
        node_cls = state if state != "waiting" else ""
        card_cls = state if state != "waiting" else ""
        rail_html += (
            f'<div class="rail-item {line_cls}">'
            f'<div class="rail-node {node_cls}"></div>'
            f'<div class="rail-card {card_cls}">'
            f'<div class="rail-head">'
            f'<span class="rail-title">{title}</span>'
            f'<span class="rail-status status-{state}">{status_labels[state]}</span>'
            f'</div>'
            f'<div class="rail-desc">{desc}</div>'
            f'</div>'
            f'</div>'
        )
    rail_html += '</div>'
    st.markdown(rail_html, unsafe_allow_html=True)


# ── Run pipeline ──────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False
        st.rerun()

if st.session_state.running and not st.session_state.done:
    results = {}
    topic_val = st.session_state.topic_input

    # ── Step 1: Search ──
    with st.spinner("🔍  Search Agent is working…"):
        search_agent = build_search_agent()
        sr = search_agent.invoke({
            "messages": [("user", f"Find recent, reliable and detailed information about: {topic_val}")]
        })
        results["search"] = sr["messages"][-1].content
        st.session_state.results = dict(results)

    # ── Step 2: Reader ──
    with st.spinner("📄  Reader Agent is scraping top resources…"):
        reader_agent = build_reader_agent()
        rr = reader_agent.invoke({
            "messages": [("user",
                f"Based on the following search results about '{topic_val}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{results['search'][:800]}"
            )]
        })
        results["reader"] = rr["messages"][-1].content
        st.session_state.results = dict(results)

    # ── Step 3: Writer ──
    with st.spinner("✍️  Writer is drafting the report…"):
        research_combined = (
            f"SEARCH RESULTS:\n{results['search']}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{results['reader']}"
        )
        results["writer"] = writer_chain.invoke({
            "topic": topic_val,
            "research": research_combined
        })
        st.session_state.results = dict(results)

    # ── Step 4: Critic ──
    with st.spinner("🧐  Critic is reviewing the report…"):
        results["critic"] = critic_chain.invoke({
            "report": results["writer"]
        })
        st.session_state.results = dict(results)

    st.session_state.running = False
    st.session_state.done = True
    st.rerun()


# ── Results display ───────────────────────────────────────────────────────────
r = st.session_state.results

if r:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Results</div>', unsafe_allow_html=True)

    # Raw outputs in expanders
    if "search" in r:
        with st.expander("🔍 Search Results (raw)", expanded=False):
            st.markdown(f'<div class="result-panel"><div class="result-panel-title">Search Agent Output</div>'
                        f'<div class="result-content">{r["search"]}</div></div>', unsafe_allow_html=True)

    if "reader" in r:
        with st.expander("📄 Scraped Content (raw)", expanded=False):
            st.markdown(f'<div class="result-panel"><div class="result-panel-title">Reader Agent Output</div>'
                        f'<div class="result-content">{r["reader"]}</div></div>', unsafe_allow_html=True)

    # Final report
    if "writer" in r:
        st.markdown("""
        <div class="report-panel">
            <div class="panel-label teal">📝 Final Research Report</div>
        """, unsafe_allow_html=True)
        st.markdown(r["writer"])   # render markdown natively
        st.markdown("</div>", unsafe_allow_html=True)

        # Download
        st.download_button(
            label="⬇  Download Report (.md)",
            data=r["writer"],
            file_name=f"research_report_{int(time.time())}.md",
            mime="text/markdown",
        )

    # Critic feedback
    if "critic" in r:
        st.markdown("""
        <div class="feedback-panel">
            <div class="panel-label green">🧐 Critic Feedback</div>
        """, unsafe_allow_html=True)
        st.markdown(r["critic"])
        st.markdown("</div>", unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="notice">
    Meridian · Powered by LangChain multi-agent pipeline · Built with Streamlit
</div>
""", unsafe_allow_html=True)
