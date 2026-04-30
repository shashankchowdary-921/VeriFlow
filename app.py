import streamlit as st
import subprocess
import tempfile

st.set_page_config(page_title="VeriFlow", layout="wide", page_icon="⚡")

# ─── GLOBAL STYLES ────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,700;0,9..144,800;1,9..144,400&family=DM+Sans:wght@400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

.stApp {
    background: #FAF4EC;
    font-family: 'DM Sans', sans-serif;
}

/* ── Remove default padding ── */
.block-container { padding-top: 0 !important; max-width: 1200px; }
.stMainBlockContainer { padding: 0 2rem 2rem !important; }

/* ── HEADER ── */
.vf-hero {
    text-align: center;
    padding: 3rem 1rem 2rem;
    position: relative;
}
.vf-eyebrow {
    display: inline-block;
    background: #F5D6B0;
    color: #92501E;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 5px 16px;
    border-radius: 20px;
    margin-bottom: 16px;
}
.vf-title {
    font-family: 'Fraunces', serif;
    font-size: 3.8rem;
    font-weight: 800;
    color: #2A1505;
    line-height: 1.05;
    letter-spacing: -1.5px;
    margin-bottom: 12px;
}
.vf-title em {
    font-style: italic;
    color: #D4631A;
}
.vf-subtitle {
    color: #9B7B5A;
    font-size: 1rem;
    font-weight: 400;
    max-width: 480px;
    margin: 0 auto;
    line-height: 1.6;
}
.vf-divider {
    border: none;
    border-top: 1.5px solid #ECD9C4;
    margin: 1.5rem 0 2rem;
}

/* ── INPUT AREA ── */
.input-wrapper {
    background: #FFFFFF;
    border: 1.5px solid #E8D4BC;
    border-radius: 20px;
    padding: 24px 24px 20px;
    box-shadow: 0 4px 24px rgba(160, 90, 20, 0.07);
    margin-bottom: 6px;
}
.input-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #C07840;
    margin-bottom: 10px;
}
.input-title {
    font-family: 'Fraunces', serif;
    font-size: 1.15rem;
    font-weight: 700;
    color: #2A1505;
    margin-bottom: 14px;
}

/* Override Streamlit textarea */
textarea {
    background: #FFFBF6 !important;
    border: 1.5px solid #E0C9AE !important;
    border-radius: 14px !important;
    color: #2A1505 !important;
    font-family: 'Courier New', monospace !important;
    font-size: 13px !important;
    line-height: 1.7 !important;
}
textarea:focus {
    border-color: #D4631A !important;
    box-shadow: 0 0 0 3px rgba(212, 99, 26, 0.12) !important;
}

/* ── Info sidebar card ── */
.info-card {
    background: linear-gradient(145deg, #FFF3E2, #FFE8CB);
    border: 1.5px solid #F5C890;
    border-radius: 18px;
    padding: 20px;
    margin-bottom: 14px;
}
.info-card-title {
    font-family: 'Fraunces', serif;
    font-size: 1rem;
    font-weight: 700;
    color: #2A1505;
    margin-bottom: 10px;
}
.info-step {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 12px;
    color: #7A4D25;
    padding: 5px 0;
    border-bottom: 1px solid rgba(200, 130, 60, 0.15);
    font-weight: 500;
}
.info-step:last-child { border-bottom: none; }
.step-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #D4631A;
    flex-shrink: 0;
}

/* ── RUN BUTTON ── */
div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #E8732A 0%, #C4501A 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 0.7rem 0 !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    font-family: 'DM Sans', sans-serif !important;
    letter-spacing: 0.3px !important;
    width: 100% !important;
    box-shadow: 0 6px 20px rgba(212, 99, 26, 0.35) !important;
    transition: all 0.2s ease !important;
}
div[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 28px rgba(212, 99, 26, 0.45) !important;
}

/* ── PIPELINE SECTION HEADER ── */
.pipeline-title {
    font-family: 'Fraunces', serif;
    font-size: 1.7rem;
    font-weight: 800;
    color: #2A1505;
    margin: 2rem 0 1.2rem;
    letter-spacing: -0.5px;
}
.pipeline-title span {
    color: #D4631A;
}

/* ── BENTO GRID ── */
.bento-grid {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr 1fr;
    grid-template-rows: auto auto;
    gap: 14px;
    margin-bottom: 14px;
}
.bc-lexer     { grid-column: 1;   grid-row: 1; }
.bc-parser    { grid-column: 2;   grid-row: 1; }
.bc-ir        { grid-column: 3/5; grid-row: 1/3; }
.bc-optimizer { grid-column: 1/3; grid-row: 2; }

/* ── BENTO CARD BASE ── */
.bcard {
    border-radius: 20px;
    padding: 22px;
    display: flex;
    flex-direction: column;
    min-height: 200px;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.bcard:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 32px rgba(160, 90, 20, 0.14) !important;
}
.bcard-tall { min-height: 420px; }
.bcard-wide { min-height: 200px; }

/* Card color themes */
.bcard-cream {
    background: #FFFFFF;
    border: 1.5px solid #EAD8C4;
    box-shadow: 0 3px 16px rgba(160, 90, 20, 0.08);
}
.bcard-warm {
    background: linear-gradient(145deg, #FFF5EA, #FFECD4);
    border: 1.5px solid #F0C898;
    box-shadow: 0 3px 16px rgba(200, 120, 40, 0.1);
}
.bcard-amber {
    background: linear-gradient(145deg, #FFFBF0, #FFF2D4);
    border: 1.5px solid #E8CC98;
    box-shadow: 0 3px 16px rgba(180, 130, 30, 0.09);
}
.bcard-terracotta {
    background: linear-gradient(145deg, #FFF2EA, #FFE4D0);
    border: 1.5px solid #F0B898;
    box-shadow: 0 3px 16px rgba(200, 100, 40, 0.1);
}
.bcard-sage {
    background: linear-gradient(145deg, #F2F8F0, #E6F4E2);
    border: 1.5px solid #B8D8B0;
    box-shadow: 0 3px 16px rgba(80, 140, 70, 0.09);
}

/* Card internals */
.bcard-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #C07840;
    margin-bottom: 6px;
}
.bcard-badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 10px;
    font-weight: 600;
    margin-bottom: 10px;
    width: fit-content;
}
.badge-ready {
    background: #DCFCE7;
    color: #166534;
}
.badge-wait {
    background: #FEF3C7;
    color: #92400E;
}
.bcard-title {
    font-family: 'Fraunces', serif;
    font-size: 1.15rem;
    font-weight: 700;
    color: #2A1505;
    margin-bottom: 12px;
    letter-spacing: -0.3px;
}
.bcard-output {
    flex: 1;
    background: rgba(255, 255, 255, 0.65);
    border: 1px solid rgba(180, 120, 60, 0.15);
    border-radius: 12px;
    padding: 12px 14px;
    font-family: 'Courier New', monospace;
    font-size: 11.5px;
    color: #4A3020;
    line-height: 1.7;
    overflow-y: auto;
    white-space: pre-wrap;
    word-break: break-word;
    max-height: 280px;
}
.bcard-tall .bcard-output { max-height: 320px; }
.bcard-empty-text {
    font-style: italic;
    color: #C0A080;
    font-size: 12px;
    font-family: 'DM Sans', sans-serif;
}

/* ── SIMULATION FULL-WIDTH CARD ── */
.sim-card {
    background: linear-gradient(135deg, #F5F0FF, #EDE8FF);
    border: 1.5px solid #C8B8F0;
    border-radius: 20px;
    padding: 24px;
    box-shadow: 0 3px 16px rgba(120, 80, 180, 0.09);
    margin-bottom: 2rem;
    transition: transform 0.2s ease;
}
.sim-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 28px rgba(120, 80, 180, 0.14);
}
.sim-card .bcard-label { color: #7B52C0; }
.sim-card .bcard-output {
    background: rgba(255, 255, 255, 0.7);
    border-color: rgba(160, 120, 220, 0.2);
    max-height: 160px;
}

/* ── FOOTER ── */
.vf-footer {
    text-align: center;
    color: #C0A080;
    font-size: 11px;
    padding-bottom: 1.5rem;
    letter-spacing: 0.5px;
}
</style>
""", unsafe_allow_html=True)

# ─── HERO HEADER ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="vf-hero">
    <div class="vf-eyebrow">Hardware Description Language Toolchain</div>
    <div class="vf-title">⚡ Veri<em>Flow</em></div>
    <div class="vf-subtitle">
        A full Verilog compiler &amp; simulator pipeline — from source to simulation,
        in one elegant workspace.
    </div>
</div>
<hr class="vf-divider">
""", unsafe_allow_html=True)

# ─── INPUT SECTION ────────────────────────────────────────────────────────────
left_col, right_col = st.columns([3, 1], gap="large")

with left_col:
    st.markdown('<div class="input-label">✦ Verilog Source</div>', unsafe_allow_html=True)
    st.markdown('<div class="input-title">Enter your Verilog code</div>', unsafe_allow_html=True)
    code = st.text_area(
        label="verilog_input",
        height=200,
        value="""module test;
reg a, b;
assign c = a + b;
endmodule""",
        label_visibility="collapsed"
    )

with right_col:
    st.markdown('<div style="height: 2px;"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-card">
        <div class="info-card-title">Pipeline Stages</div>
        <div class="info-step"><div class="step-dot"></div>🔤 Lexer — Tokenisation</div>
        <div class="info-step"><div class="step-dot"></div>🌳 Parser — AST Build</div>
        <div class="info-step"><div class="step-dot"></div>🧠 IR — Intermediate Rep.</div>
        <div class="info-step"><div class="step-dot"></div>⚙️ Optimizer — Code Opt.</div>
        <div class="info-step"><div class="step-dot"></div>▶️ Simulation — Run</div>
    </div>
    """, unsafe_allow_html=True)
    run = st.button("Run Pipeline 🚀")

st.markdown('<hr class="vf-divider">', unsafe_allow_html=True)

# ─── PIPELINE LOGIC ───────────────────────────────────────────────────────────
sections = {"Lexer": "", "Parser": "", "IR": "", "Optimizer": "", "Simulation": ""}

if run:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".v") as tmp:
        tmp.write(code.encode())
        file_path = tmp.name

    try:
        result = subprocess.run(
            ["tclsh", "test.tcl", file_path],
            capture_output=True,
            text=True
        )
        output = result.stdout
    except Exception as e:
        st.error(f"Pipeline error: {e}")
        st.stop()

    current = None
    for line in output.splitlines():
        if "Lexer Output"             in line: current = "Lexer"
        elif "AST"                    in line: current = "Parser"
        elif "Intermediate Representation" in line: current = "IR"
        elif "Optimized Code"         in line: current = "Optimizer"
        elif "Simulation"             in line: current = "Simulation"
        if current:
            sections[current] += line + "\n"


# ─── BENTO CARD BUILDER ───────────────────────────────────────────────────────
def bcard(section_key, label, icon, theme, extra_classes=""):
    text     = sections[section_key]
    has_data = bool(text.strip())
    badge    = (
        '<span class="bcard-badge badge-ready">✓ Output ready</span>'
        if has_data else
        '<span class="bcard-badge badge-wait">⧖ Awaiting run</span>'
    )
    body = (
        f'<div class="bcard-output">{text.strip()}</div>'
        if has_data else
        '<div class="bcard-output"><span class="bcard-empty-text">Run the pipeline to see output here.</span></div>'
    )
    return f"""
    <div class="bcard {theme} {extra_classes}">
        <div class="bcard-label">{icon}  {label}</div>
        {badge}
        <div class="bcard-title">{label}</div>
        {body}
    </div>"""


# ─── BENTO GRID ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="pipeline-title">🧩 Pipeline <span>View</span></div>
""", unsafe_allow_html=True)

bento_html = f"""
<div class="bento-grid">
    <div class="bc-lexer">
        {bcard("Lexer",     "Lexer",          "🔤", "bcard-cream")}
    </div>
    <div class="bc-parser">
        {bcard("Parser",    "Parser (AST)",    "🌳", "bcard-warm")}
    </div>
    <div class="bc-ir">
        {bcard("IR",        "Intermediate Rep.", "🧠", "bcard-amber", "bcard-tall")}
    </div>
    <div class="bc-optimizer">
        {bcard("Optimizer", "Optimizer",       "⚙️", "bcard-terracotta", "bcard-wide")}
    </div>
</div>
"""
st.markdown(bento_html, unsafe_allow_html=True)

# ─── SIMULATION FULL-WIDTH CARD ───────────────────────────────────────────────
sim_text     = sections["Simulation"]
sim_has_data = bool(sim_text.strip())
sim_badge    = (
    '<span class="bcard-badge badge-ready">✓ Output ready</span>'
    if sim_has_data else
    '<span class="bcard-badge badge-wait">⧖ Awaiting run</span>'
)
sim_body = (
    f'<div class="bcard-output">{sim_text.strip()}</div>'
    if sim_has_data else
    '<div class="bcard-output"><span class="bcard-empty-text">Run the pipeline to see simulation output here.</span></div>'
)

st.markdown(f"""
<div class="sim-card">
    <div class="bcard-label">▶️  Simulation</div>
    {sim_badge}
    <div class="bcard-title">Simulation Output</div>
    {sim_body}
</div>
""", unsafe_allow_html=True)

# ─── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="vf-footer">
    VeriFlow · Verilog Compiler Pipeline · Built with Streamlit
</div>
""", unsafe_allow_html=True)
