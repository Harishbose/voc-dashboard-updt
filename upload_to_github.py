#!/usr/bin/env python3
"""
Upload all files from current directory to GitHub repository
"""
import os
import requests
import base64
from pathlib import Path

# Configuration
GITHUB_TOKEN = "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"
GITHUB_USER = "Harishbose"
REPO_NAME = "voc-dashboard-updt"
BRANCH = "main"

# GitHub API endpoint
API_URL = f"https://api.github.com/repos/{GITHUB_USER}/{REPO_NAME}/contents"

# Headers
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def upload_file(file_path, file_name):
    """Upload a single file to GitHub"""
    try:
        # Read file content
        with open(file_path, 'rb') as f:
            content = f.read()
        
        # Encode to base64
        encoded_content = base64.b64encode(content).decode('utf-8')
        
        # GitHub API request
        url = f"{API_URL}/{file_name}"
        
        # Check if file exists
        try:
            get_response = requests.get(url, headers=headers, params={"ref": BRANCH})
            if get_response.status_code == 200:
                sha = get_response.json()['sha']
                message = f"Update {file_name}"
            else:
                sha = None
                message = f"Add {file_name}"
        except:
            sha = None
            message = f"Add {file_name}"
        
        # Prepare payload
        payload = {
            "message": message,
            "content": encoded_content,
            "branch": BRANCH
        }
        
        if sha:
            payload["sha"] = sha
        
        # Upload
        response = requests.put(url, json=payload, headers=headers)
        
        if response.status_code in [201, 200]:
            print(f"✓ Uploaded: {file_name}")
            return True
        else:
            print(f"✗ Failed: {file_name} - {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"✗ Error uploading {file_name}: {str(e)}")
        return False

def main():
    print("=" * 60)
    print("  UPLOADING FILES TO GITHUB")
    print("=" * 60)
    print(f"Repository: {GITHUB_USER}/{REPO_NAME}")
    print(f"Branch: {BRANCH}")
    print("")
    
    # Get all files in current directory
    current_dir = Path(".")
    files = list(current_dir.glob("*"))
    files = [f for f in files if f.is_file()]
    
    print(f"Found {len(files)} files to upload:")
    for f in files:
        print(f"  - {f.name}")
    print("")
    
    # Upload each file
    uploaded = 0
    failed = 0
    
    for file_path in files:
        file_name = file_path.name
        if upload_file(str(file_path), file_name):
            uploaded += 1
        else:
            failed += 1
    
    print("")
    print("=" * 60)
    print(f"Upload complete: {uploaded} uploaded, {failed} failed")
    print(f"Repository: https://github.com/{GITHUB_USER}/{REPO_NAME}")
    print("=" * 60)

if __name__ == "__main__":
    main()
