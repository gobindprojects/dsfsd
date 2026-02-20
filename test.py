import requests
import time
import json

# Replace with your actual API key
API_KEY = 'MyDisctSolver_a15757975053f27db9a74e9ad0afc493fc3dd77e2cc6279d7c'  # Make sure to put your actual API key here

# Create task
print("Creating task...")
response = requests.post(
    'https://solver-api.mydisct.com/createTask',
    headers={
        'Content-Type': 'application/json',
        'apikey': API_KEY
    },
    json={
        "auth": {
            "token": API_KEY
        },
        "context": {
            "source": "api",
            "version": "1.0.0"
        },
        "captcha": {
            "type": "HCAPTCHA_ENTERPRISE_TOKEN",
            "metadata": {
                "siteUrl": "https://discord.com/register",
                "siteKey": "a9b5fb07-92ff-493f-86fe-352a2803b3df"
            },
            "payload": {
                "invisible": True,
                "rqdata": "OCNhhV7MNrEC2OEfaB3Zk5d8OCpWBVBZdYtgwjaRyLKuYBWFn90zR+esQkHIRw8vXiRQR6FwHxVcwy+AmmRYb4f589CGsKAK/656B542SK/kWH0uBSmUoSULDRkHKQQhW8VxkGQjWqrzJiG9hhHpSkzssiowQ1gU2b5r8wrH5m/MUUj06lBly859m/H7z+J7I/ZVp9tiIPMdBRN+/svcX1i/",
                "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "cookies": [
                    {
                        "name": "__cf_bm",
                        "value": "",
                        "domain": ".discord.com"
                    },
                    {
                        "name": "__dcfduid",
                        "value": "",
                        "domain": ".discord.com",
                        "path": "/"
                    },
                    {
                        "name": "__sdcfduid",
                        "value": "",
                        "domain": ".discord.com",
                        "path": "/"
                    }
                ],
                "proxy": {
                    "protocol": "http",
                    "host": "global.nullproxies.com",
                    "port": 8080,
                    "username": "zen5ix5e-session-39x8my-time-1",
                    "password": "PTbbHJkr5n5"
                }
            }
        }
    }
)

print(f"Status Code: {response.status_code}")
print(f"Response Text: {response.text}")

try:
    data = response.json()
    print(f"Parsed JSON: {json.dumps(data, indent=2)}")
except json.JSONDecodeError as e:
    print(f"JSON Decode Error: {e}")
    exit(1)

if not data.get('success'):
    print("Error creating task:", data.get('message'))
    exit(1)

task_id = data['task']['id']
print(f"\nTask ID: {task_id}")
print(f"Initial Status: {data['task']['status']}")

# Poll for result using fetchResult
print("\nPolling for result...")
max_attempts = 30
attempt = 0
while attempt < max_attempts:
    attempt += 1
    
    wait_time = min(attempt * 2, 10)
    print(f"\nWaiting {wait_time} seconds before check #{attempt}...")
    time.sleep(wait_time)
    
    # Check task status using fetchResult endpoint
    try:
        check_response = requests.post(
            'https://solver-api.mydisct.com/fetchResult',
            headers={
                'Content-Type': 'application/json',
                'apikey': API_KEY
            },
            json={
                "auth": {
                    "token": API_KEY
                },
                "taskId": task_id
            },
            timeout=30
        )
        
        print(f"Check #{attempt} - Status Code: {check_response.status_code}")
        print(f"Check #{attempt} - Raw Response: {check_response.text[:200]}...")  # Print first 200 chars
        
        if check_response.status_code != 200:
            print(f"Error: Received status code {check_response.status_code}")
            continue
            
        result = check_response.json()
        print(f"Check #{attempt} - Parsed: {json.dumps(result, indent=2)}")
        
        # Check different possible response formats
        if result.get('success'):
            if 'task' in result and result['task'].get('status') == 'completed':
                print("\n✅ Task completed successfully!")
                if 'result' in result['task']:
                    token = result['task']['result'].get('token')
                    print(f"Token: {token}")
                    print("\nCaptcha token ready to use!")
                    break
            elif 'task' in result and result['task'].get('status') == 'failed':
                print("\n❌ Task failed")
                break
            elif result.get('status') == 'completed':  # Alternative format
                print("\n✅ Task completed successfully!")
                token = result.get('token') or result.get('result', {}).get('token')
                print(f"Token: {token}")
                break
        else:
            print(f"Task still processing or error: {result.get('message', 'Unknown')}")
            
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        continue
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error in polling: {e}")
        print(f"Raw response that caused error: {check_response.text if 'check_response' in locals() else 'No response'}")
        continue
        
else:
    print("\n⚠️ Max polling attempts reached. Task still processing.")