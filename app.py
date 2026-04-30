import streamlit as st
import subprocess
import tempfile

st.set_page_config(page_title="VeriFlow", layout="wide")

# --------- HEADER ----------
st.markdown("""
    <h1 style='text-align: center;'>⚡ VeriFlow</h1>
    <p style='text-align: center; color: gray;'>Verilog Compiler + Simulator Pipeline</p>
    <hr>
""", unsafe_allow_html=True)


# --------- INPUT ----------
code = st.text_area("Enter Verilog Code", height=200, value="""
module test;
reg a, b;
assign c = a + b;
endmodule
""")

run = st.button("Run Pipeline 🚀")

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
        st.error(str(e))
        st.stop()


    # --------- PARSE OUTPUT INTO SECTIONS ----------
    sections = {
        "Lexer": "",
        "Parser": "",
        "IR": "",
        "Optimizer": "",
        "Simulation": ""
    }

    current = None

    for line in output.splitlines():
        if "Lexer Output" in line:
            current = "Lexer"
        elif "AST" in line:
            current = "Parser"
        elif "Intermediate Representation" in line:
            current = "IR"
        elif "Optimized Code" in line:
            current = "Optimizer"
        elif "Simulation" in line:
            current = "Simulation"

        if current:
            sections[current] += line + "\n"


    # --------- BENTO GRID ----------
    st.markdown("## 🧩 Pipeline View")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 🔤 Lexer")
        st.code(sections["Lexer"] or "No output")

    with col2:
        st.markdown("### 🌳 Parser (AST)")
        st.code(sections["Parser"] or "No output")

    with col3:
        st.markdown("### 🧠 IR")
        st.code(sections["IR"] or "No output")

    col4, col5 = st.columns(2)

    with col4:
        st.markdown("### ⚙️ Optimizer")
        st.code(sections["Optimizer"] or "No output")

    with col5:
        st.markdown("### ▶️ Simulation")
        st.code(sections["Simulation"] or "No output")
