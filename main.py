import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Environment variables
username = os.getenv("GITHUB_USERNAME", "default_username")
access_token = os.getenv("GITHUB_TOKEN")
notion_token = os.getenv("NOTION_TOKEN")
parent_page_id = os.getenv("NOTION_PARENT_PAGE_ID")

# Validate required environment variables
if not access_token or not notion_token or not parent_page_id:
    raise ValueError("GitHub token, Notion token, and Notion parent page ID must be set as environment variables.")

# Calculate the date range (last 7 days)
end_date = datetime.now().strftime("%Y-%m-%d")
start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

# Get the week of the year
current_week = datetime.now().isocalendar()[1]
current_year = datetime.now().year

# API endpoint URLs
pull_request_url = f"https://api.github.com/search/issues?q=commenter:{username}+is:pr+is:public+updated:{start_date}..{end_date}"
issues_url = f"https://api.github.com/search/issues?q=commenter:{username}+is:issue+is:public+updated:{start_date}..{end_date}"
gists_url = f"https://api.github.com/users/{username}/gists"

# GitHub API headers
headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {access_token}",
}

# Prepare Notion content blocks
notion_blocks = []

# Add pull request activity if there are items
response = requests.get(pull_request_url, headers=headers)
if response.status_code == 200:
    data = response.json()
    items = data["items"]
    if items:  # Add section only if there are pull requests
        notion_blocks.append({
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "Pull request interactions"}}]
            }
        })
        for item in items:
            notion_blocks.append({
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [
                        {"type": "text", "text": {"content": item['title'], "link": {"url": item['html_url']}}}
                    ]
                }
            })

# Add issue activity if there are items
response = requests.get(issues_url, headers=headers)
if response.status_code == 200:
    data = response.json()
    items = data["items"]
    if items:  # Add section only if there are issues
        notion_blocks.append({
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "Issues"}}]
            }
        })
        for item in items:
            notion_blocks.append({
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [
                        {"type": "text", "text": {"content": item['title'], "link": {"url": item['html_url']}}}
                    ]
                }
            })

# Add gist activity if there are items
response = requests.get(gists_url, headers=headers)
if response.status_code == 200:
    gists = response.json()
    valid_gists = [gist for gist in gists if datetime.strptime(gist["created_at"], "%Y-%m-%dT%H:%M:%SZ") >= datetime.now() - timedelta(days=7)]
    if valid_gists:  # Add section only if there are gists
        notion_blocks.append({
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "Gists"}}]
            }
        })
        for gist in valid_gists:
            gist_name = list(gist['files'].keys())[0]
            notion_blocks.append({
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [
                        {"type": "text", "text": {"content": gist_name, "link": {"url": gist['html_url']}}}
                    ]
                }
            })

# Notion API headers
notion_headers = {
    "Authorization": f"Bearer {notion_token}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

# Create a new subpage
notion_payload = {
    "parent": {"type": "page_id", "page_id": parent_page_id},
    "properties": {
        "title": [{"type": "text", "text": {"content": f"W{current_week}/{current_year}"}}]
    },
    "children": notion_blocks
}

# Create the new page in Notion
notion_url = "https://api.notion.com/v1/pages"
response = requests.post(notion_url, headers=notion_headers, json=notion_payload)

if response.status_code == 200:
    print("Subpage created successfully in Notion!")
else:
    print("Failed to create subpage in Notion.")
    print(f"Status code: {response.status_code}")
    print(f"Error message: {response.text}")
