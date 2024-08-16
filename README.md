# Local Webbased LLM for Audit

## Description
**Local Webbased LLM for Audit** is a Streamlit-based web application designed to facilitate the auditing of telemarketing conversation transcripts. The application leverages a locally hosted Large Language Model (LLM) to evaluate conversations against predefined criteria and generate detailed audit reports.

## Key Features
- **Telemarketing Conversation Audit**: Automatically audits conversations against specific compliance criteria.
- **Real-Time Feedback**: Provides real-time progress updates during the auditing process.
- **Manual Stop Functionality**: Users can stop the audit process at any time.
- **Detailed Results**: Generates a detailed audit summary, including pass/fail status for each criterion.

## Tech Stack

### Frontend
- **Streamlit**: For creating the web interface and managing user interactions.

### Backend
- **FastAPI**: For handling API requests and integrating with the LLM.
- **LangChain**: Utilized for managing the LLM and handling callback mechanisms.
- **LlamaCpp**: The LLM model used for generating audit responses.
- **Torch**: For managing device allocation (CUDA support).

## Hardware Requirements
- **GPU**: CUDA-enabled GPU is recommended for faster processing.
- **CPU**: Multi-core processor (12 threads or more recommended).
- **Memory**: 16 GB RAM or more.
- **Storage**: SSD recommended for faster I/O operations.
- **OS**: Windows/Linux/MacOS.

# Installation Guide

### Prerequisites:
Ensure you have the following installed on your system:

- **Python 3.8+**
- **pip** (Python package installer)
- **Git** (for version control, optional but recommended)
- **CUDA** (if you plan to run the model on a GPU)

## Step 1: Set Up the Virtual Environment
Download and Extract the Virtual Environement Zip File into the same folder as server.py:

- Virutal Environment Files on
[Google Drive](https://drive.google.com/file/d/1ZW_Zg2HyZE0tMPClJtuTZJCZ4MKBm-4Z/view?usp=sharing)

## Step 2: Install LLMs

To install the LLMs, download them from Hugging Face:

- Visit the following link: [Hugging Face - CapybaraHermes-2.5-Mistral-7B-GGUF](https://huggingface.co/TheBloke/CapybaraHermes-2.5-Mistral-7B-GGUF)
- The recommended models are:
  - `capybarahermes-2.5-mistral-7b.Q5_K_M.gguf`
  - `capybarahermes-2.5-mistral-7b.Q6_K.gguf`

Make sure the files are in the same folder as server.py



## Step 3: Install Dependencies
Install the required Python packages using pip. Make sure you're in the root directory of your project.

```bash
pip install fastapi pydantic langchain-community torch uvicorn streamlit aiohttp requests
```

For Llama.cpp
```bash
$env:CMAKE_ARGS="-DGGML_CUDA=on"
$env:CUDACXX="C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.5\bin\nvcc.exe"
pip install llama-cpp-python[server] --upgrade --force-reinstall --no-cache-dir
```

## Step 4: Configure the Model Path
Make sure the path to your LlamaCpp model is correctly set in `server.py`:

```python
model_path = "C:/scoo/sem5/FYP/VSC/capybarahermes-2.5-mistral-7b.Q5_K_M.gguf"
```

Update this path according to where your model file is located on your system.

# Running the Application

1. **Start the FastAPI server:**
   - The Streamlit app will automatically start the FastAPI server, so this step is usually not necessary unless troubleshooting.
   - To start manually:
   ```bash
   uvicorn server:app --host 127.0.0.1 --port 8001
   ```

2. **Run the Streamlit app:**
   - From the root directory:
   ```bash
   streamlit run app.py
   ```

3. **Upload a JSON file:**
   - Use the file uploader in the app to upload the JSON file containing the conversation transcript.

4. **Run the Audit:**
   - Click the "Run Audit" button to start the audit process.
   - Optionally, click "Stop Audit" if you want to terminate the process early.

5. **View Results:**
   - The audit results, along with a summary, will be displayed in the app once the process is complete.

# Acknowledgements
- **Streamlit**: For providing an easy-to-use framework for building web applications.
- **FastAPI**: For enabling fast and asynchronous web services.
- **LangChain**: For offering tools to manage LLMs effectively.
- **Torch**: For providing GPU acceleration.

# Credits for Other Libraries and Dependencies
This project leverages several open-source libraries and tools that have been essential in its development. We would like to acknowledge and thank the contributors of these libraries:

1. **FastAPI**
   - **Website**: [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)
   - **Description**: FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.
   - **License**: MIT License

2. **Pydantic**
   - **Website**: [https://pydantic-docs.helpmanual.io/](https://pydantic-docs.helpmanual.io/)
   - **Description**: Pydantic is a data validation and settings management library using Python type annotations.
   - **License**: MIT License

3. **LangChain Community**
   - **GitHub**: [https://github.com/hwchase17/langchain](https://github.com/hwchase17/langchain)
   - **Description**: LangChain is a framework for developing applications powered by language models.
   - **License**: MIT License

4. **Torch (PyTorch)**
   - **Website**: [https://pytorch.org/](https://pytorch.org/)
   - **Description**: PyTorch is an open-source machine learning framework that accelerates the path from research prototyping to production deployment.
   - **License**: BSD-Style License

5. **Uvicorn**
   - **Website**: [https://www.uvicorn.org/](https://www.uvicorn.org/)
   - **Description**: Uvicorn is a lightning-fast ASGI server implementation, using `uvloop` and `httptools`.
   - **License**: BSD-3-Clause License

6. **Streamlit**
   - **Website**: [https://streamlit.io/](https://streamlit.io/)
   - **Description**: Streamlit is an open-source app framework for Machine Learning and Data Science teams to create beautiful, custom web apps in minutes.
   - **License**: Apache 2.0 License

7. **Aiohttp**
   - **Website**: [https://docs.aiohttp.org/](https://docs.aiohttp.org/)
   - **Description**: Aiohttp is an asynchronous HTTP client/server framework for Python.
   - **License**: Apache 2.0 License

8. **Requests**
   - **Website**: [https://docs.python-requests.org/](https://docs.python-requests.org/)
   - **Description**: Requests is a simple, yet elegant, HTTP library for Python, built for human beings.
   - **License**: Apache 2.0 License

9. **JSON**
   - **Website**: [https://www.json.org/](https://www.json.org/)
   - **Description**: JSON (JavaScript Object Notation) is a lightweight data-interchange format that is easy for humans to read and write and easy for machines to parse and generate.
   - **License**: Public Domain

10. **Subprocess**
    - **Documentation**: [https://docs.python.org/3/library/subprocess.html](https://docs.python.org/3/library/subprocess.html)
    - **Description**: Subprocess is a built-in Python library that allows you to spawn new processes, connect to their input/output/error pipes, and obtain their return codes.
    - **License**: Python Software Foundation License

11. **Socket**
    - **Documentation**: [https://docs.python.org/3/library/socket.html](https://docs.python.org/3/library/socket.html)
    - **Description**: Socket is a low-level networking interface that provides access to the BSD socket interface.
    - **License**: Python Software Foundation License

12. **Signal**
    - **Documentation**: [https://docs.python.org/3/library/signal.html](https://docs.python.org/3/library/signal.html)
    - **Description**: Signal is a built-in Python module that provides mechanisms to handle asynchronous events.
    - **License**: Python Software Foundation License

13. **Atexit**
    - **Documentation**: [https://docs.python.org/3/library/atexit.html](https://docs.python.org/3/library/atexit.html)
    - **Description**: Atexit is a built-in Python module that allows you to register functions to be executed upon normal program termination.
    - **License**: Python Software Foundation License

14. **Re (Regular Expressions)**
    - **Documentation**: [https://docs.python.org/3/library/re.html](https://docs.python.org/3/library/re.html)
    - **Description**: The `re` module provides support for regular expressions in Python.
    - **License**: Python Software Foundation License

