import requests
import json
import time

# Load JSON data from a file
with open(r'C:\scoo\sem5\FYP\Testing Sprint 4\Audio 5\response_1718197859058.json', 'r') as file:
    data = json.load(file)

# Construct the dialog string
dialog = ""
for transcript in data["transcripts"]:
    for segment in transcript["segments"]:
        dialog += f"{segment['speaker']} : {segment['text']}\n"

prompt = f"""
Objective:
Your task is to audit the conversation between a telemarketer from IPP or IPPFA and a customer. The audit will assess whether the telemarketer adhered to specific criteria during the dialogue based on the 8 different Criteria.

Instructions:
Carefully review the provided conversation transcript and evaluate the telemarketer's compliance based on the criteria outlined below.
For each criterion, provide a detailed assessment, including reasons from the Conversation and a result status.
All evaluation of the compliance strictly based on the conservation content. Do not create your own information.

Conversation:
{dialog}

Audit Criteria:
1. Did the telemarketer introduce themselves? (Search through the whole content, if no name found state no name mentioned).
2. Did they mention they are calling from IPP or IPPFA?
3. Did they state that IPPFA is a Licensed Financial Adviser providing advice on life insurance, general insurance, and Collective Investment Schemes (CIS)?
4. Did the telemarketer specify the types of financial services offered by IPP or IPPFA?
5. Did the telemarketer ask if the customer is interested in exploring how they could benefit from IPPFA's services?
6. Did the customer inquired about the source of the call? If YES, check did the telemarketer confirm they are calling from IPP or IPPFA without mentioning any affiliation with insurers?
7. Did the telemarketer mention the possibility of arranging a meeting or Zoom session with a consultant?
8. Did the customer asked how their contact information was obtained? If Yes, Check did the telemarketer provide the name of the person who provided the customer's contact details?

Output Format:
For each criterion, provide Json Object for the following:
*Question: State the criterion being evaluated. examples: "Did the telemarketer introduce their own name, mention they are calling from IPPFA or IPP, and state that IPPFA is a Licensed Financial Adviser providing advice on life insurance, general insurance, and CIS?",Did the telemarketer mention the possibility of arranging a meeting or Zoom session with a consultant?
*Reason: Explain by pointing out specific reason based on the information in the conversation. examples: "The telemarketer introduced themselves with name (___)  but mentioned they are calling from IPPFA, a Licensed Financial Adviser providing advice on life insurance, general insurance, and CIS.","The telemarketer didn't mention their name and where they are calling from."
*Result: Indicate whether the criterion was met with "Pass," "Fail," or "Not Applicable.

"""


start_time = time.time()

response = requests.post("http://127.0.0.1:8000/generate/", json={"prompt": prompt, "max_tokens": 8000, "min_length": 100})

if response.status_code == 200:
    audit_report = response.json()["response"]
    print(audit_report)
    print(' ')
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Runtime: {elapsed_time:.2f} seconds")
else:
    print(f"Error: {response.status_code} - {response.text}")