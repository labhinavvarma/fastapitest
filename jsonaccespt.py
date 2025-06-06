import httpx
import argparse
import json
import os

def load_json_file(path: str):
    if not os.path.isfile(path):
        raise FileNotFoundError(f"❌ File not found: {path}")
    with open(path, 'r') as f:
        return json.load(f)

def main(file_path):
    try:
        # Load the JSON dashboard file
        dashboard_data = load_json_file(file_path)
        schema = json.dumps(dashboard_data)
    except Exception as e:
        print(f"❌ Failed to load JSON schema: {e}")
        return

    # 📌 Updated Query for complex dashboards
    query = """You will receive a complex JSON array containing dashboard and chart components.

Convert it to an array of objects in the exact format:
[{"metric_name": "name", "value": 123}]

Rules:
1. Extract ALL numeric fields from each `data` object in the `components` array (including nested arrays or objects).
2. Create descriptive metric names using the `title` and `code` from each component to make it clear where the value came from.
3. Ignore all non-numeric values.
4. Return ONLY the JSON array — no extra text, no explanations, no markdown formatting.
5. Start with [ and end with ].

Example output:
[
  {"metric_name": "In Network Inpatient Admissions (IN_NETWORK_INPATIENT_ADMISSIONS)", "value": 825.0},
  {"metric_name": "Out of Network Inpatient Admissions (OUT_OF_NETWORK_INPATIENT_ADMISSIONS)", "value": 46.0}
]
"""

    # Final Prompt
    prompt = f"""
You are a JSON summarization expert.

You will be given a dashboard-style JSON structure with nested chart and KPI components.
Extract numeric metrics following the instructions.

data:
{schema}

data-query:
{query}
"""

    # Cortex API call
    url = 'https://sfassist.edagenaidev.awsdns.internal.das/api/cortex/complete'
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    body = {
        "query": {
            "aplctn_cd": "edagnai",
            "app_id": "edadip",
            "api_key": "78a799ea-a0f6-11ef-a0ce-15a449f7a8b0",
            "method": "cortex",
            "model": "llama3.1-70b",
            "sys_msg": "You are powerful AI assistant in providing accurate answers always. Be concise in providing answers based on context.",
            "limit_convs": "0",
            "prompt": {
              "messages": [
                {
                  "role": "user",
                  "content": prompt
                }
              ]
            },
            "session_id": "0947b240-9447-4af7-8367-65e6cc8fa5d9"
        }
    }

    try:
        response = httpx.post(url=url, headers=headers, json=body, timeout=None)
        if response.status_code == 200:
            print("✅ Response from LLM:")
            print(response.text)
        else:
            print(f"❌ Request failed: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Error during HTTP request: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Extract numeric metrics from dashboard JSON using LLM.")
    parser.add_argument("file", nargs="?", help="Path to the JSON file")
    args = parser.parse_args()

    if args.file:
        main(args.file)
    else:
        file_path = input("Please enter the path to your JSON file: ").strip()
        if file_path:
            main(file_path)
        else:
            print("❌ No file path provided. Exiting.")
