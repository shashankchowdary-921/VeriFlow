import streamlit as st
import subprocess
import tempfile
import os

st.title("Verilog Compiler Pipeline")

code = st.text_area("Enter Verilog Code:", height=200)

def run_tcl(script, filename):
    result = subprocess.run(
        ["tclsh", script, filename],
        capture_output=True,
        text=True
    )
    return result.stdout, result.stderr

if st.button("Run Pipeline"):

    if not code.strip():
        st.warning("Enter Verilog code")
    else:
        # Save code to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".v", mode="w") as f:
            f.write(code)
            filename = f.name

        try:
            # --- Step 1: Lexer ---
            st.subheader("Lexer Output")
            out, err = run_tcl("run_lexer.tcl", filename)
            st.code(out if out else "No output")

            # --- Step 2: Parser ---
            st.subheader("AST (Parser)")
            out, err = run_tcl("run_parser.tcl", filename)
            st.code(out if out else "No output")

            # --- Step 3: IR ---
            st.subheader("Intermediate Representation")
            out, err = run_tcl("run_ir.tcl", filename)
            st.code(out if out else "No output")

            # --- Step 4: Optimizer ---
            st.subheader("Optimized IR")
            out, err = run_tcl("run_optimizer.tcl", filename)
            st.code(out if out else "No output")

            # --- Step 5: Simulation ---
            st.subheader("Simulation Results")
            out, err = run_tcl("run_simulation.tcl", filename)
            st.code(out if out else "No output")

            if err:
                st.error(err)

        finally:
            os.remove(filename)