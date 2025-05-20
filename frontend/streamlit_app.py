# function_manager.py
import streamlit as st
import requests

BASE_URL = "http://localhost:8000/functions"  # Adjust if your FastAPI is hosted elsewhere
EXECUTE_URL = "http://localhost:8000/functions/execute-function-runc/"  # Adjust the URL if needed
st.set_page_config(page_title="Serverless Function Manager", layout="centered")

st.title("🚀 Serverless Function Execution Platform")
st.subheader("Manage and Deploy Your Functions")

# ------------------------
# Function: List Functions
# ------------------------
def list_functions():
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        return response.json()
    st.error("Failed to fetch functions.")
    return []

# ------------------------
# Function: Create Function
# ------------------------
def create_function(name, route, language, timeout):
    data = {
        "name": name,
        "route": route,
        "language": language,
        "timeout": timeout
    }
    response = requests.post(BASE_URL, json=data)
    return response

# ------------------------
# Function: Update Function
# ------------------------
def update_function(func_id, name, route, language, timeout):
    data = {
        "name": name,
        "route": route,
        "language": language,
        "timeout": timeout
    }
    response = requests.put(f"{BASE_URL}/{func_id}", json=data)
    return response

# ------------------------
# Function: Delete Function
# ------------------------
def delete_function(func_id):
    response = requests.delete(f"{BASE_URL}/{func_id}")
    return response

# ------------------------
# Function Form (Create or Update)
# ------------------------
def function_form(is_update=False, existing_data=None):
    with st.form(key="function_form"):
        name = st.text_input("Function Name", value=existing_data["name"] if is_update else "")
        route = st.text_input("Route", value=existing_data["route"] if is_update else "")
        language = st.selectbox("Language", options=["python", "javascript", "bash"], index=0 if not is_update else ["python", "javascript", "bash"].index(existing_data["language"]))
        timeout = st.number_input("Timeout (seconds)", min_value=1.0, value=existing_data["timeout"] if is_update else 5.0, step=1.0)

        submit = st.form_submit_button("Update Function" if is_update else "Create Function")

        if submit:
            if is_update:
                response = update_function(existing_data["id"], name, route, language, timeout)
                if response.status_code == 200:
                    st.success("Function updated successfully!")
                else:
                    st.error("Failed to update function.")
            else:
                response = create_function(name, route, language, timeout)
                if response.status_code == 200:
                    st.success("Function created successfully!")
                else:
                    st.error("Failed to create function.")
# ------------------------
# Function: Get All Metrics
# ------------------------
def get_all_metrics():
    response = requests.get("http://localhost:8000/functions/metrics")  # Adjust if needed
    if response.status_code == 200:
        return response.json()
    st.error("Failed to fetch metrics.")
    return []
# ------------------------
# Function: Execute Function
# ------------------------
def execute_function(func_id, timeout=5.0, runtime="runc"):
    params = {
        "func_id": func_id,
        "timeout": timeout,
        "runtime": runtime
    }
    response = requests.post(EXECUTE_URL, params=params)  # ✅ use `params` not `json`
    if response.status_code == 200:
        return response.json()
    st.error("Failed to execute function.")
    return {}
# ------------------------
# Tabs: List / Create
# ------------------------
# tabs = st.tabs(["📝 List Functions", "➕ Create Function"])
# ------------------------
# Tabs: List / Create / Metrics
# ------------------------
tabs = st.tabs(["📝 List Functions", "➕ Create Function", "📊 View Metrics","⚡ Execute Function"])


# --- Tab 1: List Functions ---
with tabs[0]:
    functions = list_functions()
    if functions:
        for func in functions:
            with st.expander(f"{func['id']}: {func['name']}"):
                st.write(f"🔀 Route: `{func['route']}`")
                st.write(f"🧠 Language: `{func['language']}`")
                st.write(f"⏱️ Timeout: {func['timeout']} seconds")

                col1, col2 = st.columns(2)

                with col1:
                    if st.button(f"✏️ Edit Function {func['id']}", key=f"edit_{func['id']}"):
                        st.session_state[f"editing_{func['id']}"] = True

                with col2:
                    if st.button(f"🗑️ Delete Function {func['id']}", key=f"delete_{func['id']}"):
                        delete_response = delete_function(func["id"])
                        if delete_response.status_code == 200:
                            st.success("Function deleted.")
                        else:
                            st.error("Error deleting function.")
                        st.rerun()

                if st.session_state.get(f"editing_{func['id']}", False):
                    st.markdown("### Edit Function")
                    function_form(is_update=True, existing_data=func)
                    st.session_state[f"editing_{func['id']}"] = False
                    st.rerun()
    else:
        st.info("No functions available. Add one in the 'Create' tab.")

# --- Tab 2: Create Function ---
with tabs[1]:
    function_form()
#--- Tab 3: View Metrics ---
# with tabs[2]:
#     st.markdown("### 📈 Execution Metrics")

#     metrics = get_all_metrics()
#     if metrics:
#         for metric in metrics[::-1]:  # Latest first
#             st.markdown("---")
#             st.subheader(f"📝 Function ID: {metric['function_id']}")

#             st.write(f"🕒 Timestamp: `{metric['timestamp']}`")
#             st.write(f"🧪 Runtime: `{metric['runtime']}`")
#             st.write(f"⏱️ Duration: `{metric['duration']}s`")
#             st.write(f"📦 Exit Code: `{metric['exit_code']}`")

#             if metric.get("error_message"):
#                 st.error(f"❗ Error: {metric['error_message']}")

#             if metric.get("stdout"):
#                 st.markdown("**📤 Stdout:**")
#                 st.code(metric["stdout"], language="bash")

#             if metric.get("stderr"):
#                 st.markdown("**📥 Stderr:**")
#                 st.code(metric["stderr"], language="bash")

#     else:
#         st.info("No execution metrics yet. Run a function to see data here.")
# import time
# with tabs[2]:
#     st.markdown("### 📈 Execution Metrics")

#     auto_refresh = st.checkbox("🔁 Auto-refresh every 2 seconds", value=False)
#     if auto_refresh:
#         time.sleep(2)
#         st.experimental_rerun()

#     metrics = get_all_metrics()
#     if metrics:
#         for metric in metrics[::-1]:  # Show latest first
#             st.markdown("---")
#             st.subheader(f"📝 Function ID: {metric['function_id']}")

#             col1, col2, col3 = st.columns(3)
#             col1.metric("Runtime", metric["runtime"])
#             col2.metric("Duration (s)", f"{metric['duration']:.2f}")
#             col3.metric("Exit Code", metric["exit_code"])

#             st.write(f"🕒 Timestamp: `{metric['timestamp']}`")

#             if metric.get("error_message"):
#                 st.error(f"❗ Error: {metric['error_message']}")

#             if metric.get("stdout"):
#                 with st.expander("📤 Stdout"):
#                     st.code(metric["stdout"], language="bash")

#             if metric.get("stderr"):
#                 with st.expander("📥 Stderr"):
#                     st.code(metric["stderr"], language="bash")
#     else:
#         st.info("No execution metrics yet. Run a function to see data here.")
import time
import pandas as pd
import plotly.express as px

with tabs[2]:
    st.markdown("### 📈 Execution Metrics")

    auto_refresh = st.checkbox("🔁 Auto-refresh every 2 seconds", value=False)
    if auto_refresh:
        time.sleep(2)
        st.experimental_rerun()

    metrics = get_all_metrics()
    if metrics:
        for metric in metrics[::-1]:  # Show latest first
            st.markdown("---")
            st.subheader(f"📝 Function ID: {metric['function_id']}")

            col1, col2, col3 = st.columns(3)
            col1.metric("Runtime", metric["runtime"])
            col2.metric("Duration (s)", f"{metric['duration']:.2f}")
            col3.metric("Exit Code", metric["exit_code"])

            st.write(f"🕒 Timestamp: `{metric['timestamp']}`")

            if metric.get("error_message"):
                st.error(f"❗ Error: {metric['error_message']}")

            if metric.get("stdout"):
                with st.expander("📤 Stdout"):
                    st.code(metric["stdout"], language="bash")

            if metric.get("stderr"):
                with st.expander("📥 Stderr"):
                    st.code(metric["stderr"], language="bash")

        # ========================
        # 📊 Charts & Visualizations
        # ========================
        st.markdown("## 📊 Metrics Overview Charts")

        # Convert the metrics data into a DataFrame
        df = pd.DataFrame(metrics)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['status'] = df['exit_code'].apply(lambda x: "Success" if x == 0 else "Failed")

        # Duration per Function
        st.markdown("### ⏱️ Duration per Function")
        fig1 = px.bar(df, x="function_id", y="duration", color="runtime",
                      title="Execution Duration by Function",
                      labels={"duration": "Duration (s)", "function_id": "Function ID"})
        st.plotly_chart(fig1, use_container_width=True)

        # Success vs Failure
        st.markdown("### ✅ Success vs ❌ Failure")
        fig2 = px.pie(df, names="status", title="Execution Status")
        st.plotly_chart(fig2, use_container_width=True)

        # Execution Duration Over Time
        st.markdown("### 🕒 Execution Duration Over Time")
        fig3 = px.line(df.sort_values("timestamp"), x="timestamp", y="duration", color="function_id",
                       markers=True, title="Execution Trend")
        st.plotly_chart(fig3, use_container_width=True)

    else:
        st.info("No execution metrics yet. Run a function to see data here.")
with tabs[3]:
    st.markdown("### ⚡ Execute a Function")

    func_id = st.number_input("Function ID", min_value=1, step=1)
    timeout = st.number_input("Timeout (seconds)", min_value=1.0, value=5.0, step=1.0)
    runtime = st.selectbox("Select Runtime", options=["runc", "runsc"])

    execute_button = st.button("Execute Function")

    if execute_button:
        result = execute_function(func_id, timeout, runtime)

        if result:
            st.subheader(f"Execution Result for Function ID: {func_id}")
            st.write(f"⏱️ Duration: {result['result']['duration']} seconds")
            if 'stdout' in result['result']:
                st.markdown("**📤 Stdout:**")
                st.code(result['result']['stdout'], language="bash")
            if 'stderr' in result['result']:
                st.markdown("**📥 Stderr:**")
                st.code(result['result']['stderr'], language="bash")
            if 'exit_code' in result['result']:
                st.write(f"📦 Exit Code: {result['result']['exit_code']}")
        else:
            st.error("Failed to execute the function.")