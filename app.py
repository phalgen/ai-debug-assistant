import streamlit as st
import requests
import json

# Page config (must be first)
st.set_page_config(
    page_title="AI Debug Assistant",
    page_icon="🛠️",
    layout="centered"
)

# Sidebar (display only)
with st.sidebar:
    st.title("⚙️ Settings")
    st.write("AI Debug Assistant v1")

    st.markdown("---")
    st.write("### Features")
    st.write("✔ Rule-based analysis")
    st.write("✔ Semantic similarity")
    st.write("✔ Memory storage")

    st.markdown("---")
    st.write("Built by Asbaa Thakur")

# Main UI
st.title("🛠️ AI Debug Assistant")
st.write("Paste an error and (optionally) code. Get explanation + fix.")

# Inputs
error = st.text_area("Error message", height=120, key="error_input")
code = st.text_area("Code (optional)", height=180, key="code_input")

API_URL = "http://127.0.0.1:8000/analyze"

# Load memory
def load_memory():
    try:
        with open("memory.json", "r") as f:
            return json.load(f)
    except:
        return []

# Empty state message
if not error.strip():
    st.info("👆 Enter an error above and click Analyze to see results.")

# Button
analyze_clicked = st.button("🚀 Analyze Error", disabled=not error.strip())

if analyze_clicked:
    with st.spinner("Analyzing error..."):
        try:
            resp = requests.post(
                API_URL,
                json={"error": error, "code": code},
                timeout=20
            )
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            st.error(f"Backend not reachable or error occurred: {e}")
            st.stop()

    st.success("Analysis Complete ✅")

    st.subheader("🧠 Rule-Based Insight")
    st.info(data["analysis"]["rule_based"])

    st.subheader("🔍 Similar Error Found")
    st.write(data["analysis"]["similar_error"] or "No similar error found")

    st.subheader("🛠 Suggested Fix")
    st.code(data["analysis"]["fix"], language="python")

    st.subheader("📘 Explanation")
    st.write(data["analysis"]["explanation"])

    st.subheader("💡 Example Fix")
    st.code(data["analysis"]["example"], language="python")

    st.subheader("📊 Confidence")
    st.progress(data["analysis"]["confidence"])

    # ✅ FIXED LOCATION
    if data["analysis"].get("typo_detected"):
        st.subheader("⚠️ Possible Typo")
        st.warning(
            f"You wrote '{data['analysis']['typo_detected']['typo']}' "
            f"did you mean '{data['analysis']['typo_detected']['suggestion']}'?"
        )

    st.caption(f"⏱ {data['timestamp']}")

# Divider
st.markdown("---")

# Recent history
if analyze_clicked:
    st.markdown("---")
    st.subheader("📜 Recent Analyses")

    memory = load_memory()
    for item in memory[-3:][::-1]:
        with st.expander("🔹 " + item["input_error"][:60]):
            st.json(item)


    st.subheader("⚠️ Possible Typo")
    st.warning(
        f"You wrote '{data['analysis']['typo_detected']['typo']}' "
        f"did you mean '{data['analysis']['typo_detected']['suggestion']}'?"
    )