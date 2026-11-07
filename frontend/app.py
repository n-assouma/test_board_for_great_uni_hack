"""Streamlit calculator UI. Talks to the backend API described in AGENTS.md section 5."""

import os

import requests
import streamlit as st

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:5000")
OPERATIONS = ["+", "-", "*", "/"]


def calculate(a, b, op):
    """POST /calculate. Returns (result, error) with exactly one of them set."""
    try:
        response = requests.post(
            f"{BACKEND_URL}/calculate",
            json={"a": a, "b": b, "op": op},
            timeout=10,
        )
    except requests.RequestException as exc:
        return None, f"Could not reach the backend at {BACKEND_URL} ({exc})"

    try:
        payload = response.json()
    except ValueError:
        return None, f"Backend returned a non-JSON response (HTTP {response.status_code})"

    if response.ok:
        if "result" not in payload:
            return None, f"Backend response is missing 'result': {payload}"
        return payload["result"], None

    return None, payload.get("error", f"Backend error (HTTP {response.status_code})")


st.set_page_config(page_title="Calculator", page_icon="🧮")
st.title("🧮 Calculator")
st.caption(f"Backend: {BACKEND_URL}")

col_a, col_op, col_b = st.columns([3, 2, 3])
with col_a:
    a = st.number_input("a", value=3.0, format="%g")
with col_op:
    op = st.selectbox("Operation", OPERATIONS)
with col_b:
    b = st.number_input("b", value=4.0, format="%g")

if st.button("Calculate", type="primary"):
    result, error = calculate(a, b, op)
    if error:
        st.error(error)
    else:
        st.success(f"{a:g} {op} {b:g} = {result:g}" if isinstance(result, (int, float)) else f"Result: {result}")
