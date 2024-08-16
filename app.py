#app.py
import streamlit as st
import requests
import json
import time
import asyncio
import aiohttp
import subprocess
import os
import signal
import socket
from concurrent.futures import ThreadPoolExecutor
import atexit

st.set_page_config(layout="wide")  # Configures the layout of the Streamlit app to be wide.

# Global variable to hold the server process
server_process = None

def is_server_running(host='127.0.0.1', port=8001):
    """
    Checks if a server is running on the specified host and port.
    Returns True if the server is running, otherwise returns False.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0

def start_server():
    """
    Starts the FastAPI server if it's not already running.
    Uses subprocess to start the server and waits for it to become active.
    """
    global server_process
    if not is_server_running():
        server_process = subprocess.Popen(["uvicorn", "server:app", "--host", "127.0.0.1", "--port", "8001"])
        st.write("Starting FastAPI server on port 8001...")
        start_time = time.time()
        while not is_server_running():
            if time.time() - start_time > 40:
                st.error("Failed to start FastAPI server within the timeout period. Reload this page.")
                return
            time.sleep(0.5)
        st.success("FastAPI server started successfully!")
    else:
        st.info("FastAPI server is already running.")

def stop_server():
    """
    Stops the FastAPI server if it is running.
    Uses the server process's PID to send a SIGTERM signal and terminate it.
    """
    global server_process
    if server_process:
        os.kill(server_process.pid, signal.SIGTERM)
        server_process = None
        st.write("FastAPI server stopped.")

atexit.register(stop_server)  # Registers the stop_server function to run when the script exits.
start_server()  # Starts the FastAPI server when the app initializes.

st.title("Telemarketing Conversation Audit")
st.write("Upload the JSON file containing the conversation transcript for auditing.")

uploaded_file = st.file_uploader("Choose a JSON file", type="json")  # Allows users to upload a JSON file.

def process_json(file):
    """
    Processes the uploaded JSON file.
    Extracts conversation segments from the JSON file and formats them into a string.
    Displays the conversation in a text area on the Streamlit app.
    Returns the formatted conversation string.
    """
    data = json.load(file)
    dialog = ""
    for transcript in data["transcripts"]:
        for segment in transcript["segments"]:
            dialog += f"{segment['speaker']} : {segment['text']}\n"
    st.subheader("Conversation")
    st.text_area("dialog", dialog, height=400)
    return dialog

async def run_audit(prompt):
    """
    Sends an asynchronous POST request to the FastAPI server with the provided prompt.
    Waits for and retrieves the audit response from the server.
    Returns the server's response or an error message if the request fails.
    """
    async with aiohttp.ClientSession() as session:
        async with session.post("http://127.0.0.1:8001/generate/", json={"prompt": prompt, "max_tokens": 8000}) as response:
            if response.status == 200:
                result = await response.json()
                return result.get("response", "No response found in result.")
            else:
                return f"Error: {response.status} - {await response.text()}"

async def stop_audit():
    """
    Sends an asynchronous POST request to the FastAPI server to stop the audit process.
    """
    async with aiohttp.ClientSession() as session:
        await session.post("http://127.0.0.1:8001/stop/")

def run_audit_with_progress(prompt):
    """
    Runs the audit with a simulated progress bar.
    Updates the progress bar and status text as the audit runs.
    If the 'Stop Audit' button is pressed, the process is halted.
    Returns the audit result or a message if the audit was stopped.
    """
    if 'stop_pressed' not in st.session_state:
        st.session_state['stop_pressed'] = False

    progress_bar = st.progress(0)
    status_text = st.empty()

    if st.session_state['stop_pressed']:
        progress_bar.empty()
        status_text.empty()
        return "Audit stopped by user."
    
    # Simulate progress and run the audit
    for i in range(50):  # Simulated progress
        progress_bar.progress(i + 1)
        status_text.text(f"Processing: {i + 1}%")
        time.sleep(0.1)  # Replace with your actual process

    audit_result = asyncio.run(run_audit(prompt))

    for i in range(50, 100):  # Remaining progress
        progress_bar.progress(i + 1)
        status_text.text(f"Processing: {i + 1}%")
        time.sleep(0.1)  # Replace with your actual process

    progress_bar.empty()
    status_text.empty()

    return audit_result

def evaluate_audit(audit_result):
    """
    Evaluates and summarizes the audit results.
    Calculates the number of passed and failed criteria and generates a summary of failed criteria.
    Returns the overall result, pass percentage, total criteria, passed criteria, and a summary of failed criteria.
    """
    try:
        passed_criteria = 0
        failed_criteria = []
        total_criteria = 0
        NA_Criteria = 0

        # Split the audit result into blocks based on the JSON structure
        blocks = audit_result.split("{")

        # Iterate through each block to check for "Pass", "Fail", and "Not Applicable"
        for block in blocks:
            if '"Result": "Pass"' in block:
                passed_criteria += 1
                total_criteria += 1
            elif '"Result": "Fail"' in block:
                failed_criteria.append(block.strip())
                total_criteria += 1
            elif '"Result": "Not Applicable"' in block:
                total_criteria += 1
                NA_Criteria += 1

        # Calculate pass percentage
        pass_percentage = (passed_criteria / (total_criteria - NA_Criteria)) * 100 if total_criteria > 0 else 0
        overall_result = "Pass" if pass_percentage >= 50 else "Fail"

        # Summarize failed criteria
        failed_summary = "\n".join(failed_criteria)

        return overall_result, pass_percentage, total_criteria, passed_criteria, failed_summary
    except Exception as e:
        return "Error", 0, 0, 0, f"Unexpected Error: {str(e)}"

# Display the audit results
if uploaded_file is not None:
    dialog = process_json(uploaded_file)
    
    prompt = f"""
    Objective:
    Your task is to audit the conversation between a telemarketer from IPP or IPPFA and a customer. The audit will assess whether the telemarketer adhered to specific criteria during the dialogue. Answer all 8 criteria.

    Instructions:
    Carefully review the provided conversation transcript and evaluate the telemarketer's compliance based on the criteria outlined below.
    For each criterion, provide a detailed assessment, including reasons from the Conversation and a result status.
    All evaluation of the compliance strictly based on the conservation content. Do not create your own information.

    Conversation:
    {dialog}

    Questions for Audit Criteria:
    1. Did the telemarketer introduce themselves? (Search through the whole content, if no name found state no name mentioned).
    2. Did they mention they are calling from IPP or IPPFA?
    3. Did they state that IPPFA is a Licensed Financial Adviser providing advice on life insurance, general insurance, and Collective Investment Schemes (CIS)?
    4. Did the telemarketer specify the types of financial services offered by IPP or IPPFA?
    5. Did the telemarketer ask if the customer is interested in exploring how they could benefit from IPPFA's services?
    6. Did the customer inquire about the source of the call? If YES, check did the telemarketer confirm they are calling from IPP or IPPFA without mentioning any affiliation with insurers?
    7. Did the telemarketer mention the possibility of arranging a meeting or Zoom session with a consultant?
    8. Did the customer ask how their contact information was obtained? If Yes, Check did the telemarketer provide the name of the person who provided the customer's contact details?

    Output Format:
    For each of the 8 criteria, provide a Json Object for the following:
    *Question: State the criterion being evaluated. examples: "Did the telemarketer introduce their own name, mention they are calling from IPPFA or IPP, and state that IPPFA is a Licensed Financial Adviser providing advice on life insurance, general insurance, and CIS?", Did the telemarketer mention the possibility of arranging a meeting or Zoom session with a consultant?
    *Reason: Explain by pointing out specific reason based on the information in the conversation. examples: "The telemarketer introduced themselves with name (___) but mentioned they are calling from IPPFA, a Licensed Financial Adviser providing advice on life insurance, general insurance, and CIS.","The telemarketer didn't mention their name and where they are calling from."
    *Result: Indicate whether the criterion was met with "Pass," "Fail," or "Not Applicable.
    """

    # Create a container for the audit results
    audit_container = st.container()

    # Main app layout for Run and Stop buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Run Audit", key="main_run_button", use_container_width=True):
            st.session_state['stop_pressed'] = False  # Reset stop state
            start_time = time.time()

            # Run the audit asynchronously with progress bar
            audit_result = run_audit_with_progress(prompt)

            end_time = time.time()
            elapsed_time = end_time - start_time

            # Display the audit results in the container
            if audit_result:
                with audit_container:
                    st.subheader("Audit Results")
                    st.text_area("", audit_result, height=1000)
                    
                    # Evaluate and summarize the results
                    overall_result, pass_percentage, total_criteria, passed_criteria, failed_summary = evaluate_audit(audit_result)
                    
                    # Display the evaluation summary
                    st.subheader("Audit Summary")
                    st.write(f"Result: {overall_result}, {passed_criteria}/{total_criteria}") 
                    if failed_summary:
                        st.write("Failed Criteria:")
                        st.text(failed_summary)

                    st.write(f"Time taken: {elapsed_time:.2f} seconds")
            else:
                st.error("Failed to retrieve audit results.")
    
    with col2:
        if st.session_state.get('stop_pressed', False) == False and st.button("Stop Audit", key="main_stop_button", use_container_width=True):
            st.session_state['stop_pressed'] = True
