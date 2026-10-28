"""
FlowMedic Demo Repository Setup Script
Automates Step 1 to Step 5 of the Demo Repository Kit:
1. Creates the GitHub repository 'flowmedic-demo-source' (if not already existing)
2. Pushes the initial commit from the local git repository
3. Creates all 6 synthetic issues with exact titles, bodies, and labels
4. Sets Issue #4 to 'closed' state
5. Prepares .env.local configuration for FlowMedic
"""

import os
import re
import sys
import json
import subprocess
import urllib.request
import urllib.error

DEFAULT_REPO_NAME = "flowmedic-demo-source"
DEFAULT_OWNER = "Anshita-18H"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ISSUES_DIR = os.path.join(SCRIPT_DIR, "issues")
SOURCE_REPO_LOCAL_DIR = r"d:\saboot\flowmedic-demo-source"
FLOWMEDIC_DIR = r"d:\saboot\FlowMedic"

def parse_issue_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    title_match = re.search(r"^#\s*Issue\s*\d+\s*[—–-]\s*(.+)$", content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else ""

    state_match = re.search(r"\*\*Suggested state:\*\*\s*(.+)$", content, re.MULTILINE)
    state = state_match.group(1).strip().lower() if state_match else "open"

    labels_match = re.search(r"\*\*Suggested labels:\*\*\s*(.+)$", content, re.MULTILINE)
    labels = []
    if labels_match:
        labels = [l.strip(" `") for l in labels_match.group(1).split(",")]

    body = ""
    if "## Body" in content:
        body = content.split("## Body", 1)[1].strip()

    return {
        "title": title,
        "state": state,
        "labels": labels,
        "body": body
    }

def github_api_request(url, method="GET", token=None, payload=None):
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "FlowMedic-Demo-Setup"
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    data = json.dumps(payload).encode("utf-8") if payload else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req) as response:
            res_body = response.read().decode("utf-8")
            return response.status, json.loads(res_body) if res_body else {}
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8")
        try:
            err_json = json.loads(err_body)
        except Exception:
            err_json = {"message": err_body}
        return e.code, err_json
    except Exception as e:
        return 500, {"message": str(e)}

def run(token=None, owner=DEFAULT_OWNER, repo_name=DEFAULT_REPO_NAME, is_private=False):
    token = token or os.environ.get("GITHUB_TOKEN")
    if not token:
        print("\n[!] Error: GITHUB_TOKEN is required.")
        print("Please provide a GitHub Personal Access Token (PAT) with repo/issues permissions.")
        print("Usage: python setup_github_repo_and_issues.py <token>")
        sys.exit(1)

    print(f"[*] Target Owner: {owner}")
    print(f"[*] Target Repository: {repo_name}")

    # 1. Verify or create repository
    print(f"\n[1/4] Checking repository '{owner}/{repo_name}' on GitHub...")
    status, res = github_api_request(f"https://api.github.com/repos/{owner}/{repo_name}", token=token)

    if status == 200:
        print(f"      Repository '{owner}/{repo_name}' already exists.")
    elif status == 404:
        print(f"      Repository does not exist. Creating '{owner}/{repo_name}'...")
        create_payload = {
            "name": repo_name,
            "description": "Synthetic issue source repository for FlowMedic live demo (Phase 01–04)",
            "private": is_private,
            "has_issues": True,
            "auto_init": False
        }
        c_status, c_res = github_api_request("https://api.github.com/user/repos", method="POST", token=token, payload=create_payload)
        if c_status in (200, 201):
            print(f"      Repository created successfully! URL: {c_res.get('html_url')}")
        else:
            print(f"      Failed to create repository: {c_res.get('message')}")
            sys.exit(1)
    else:
        print(f"      Unexpected error checking repo: {status} - {res.get('message')}")
        sys.exit(1)

    # 2. Push local repository README
    print(f"\n[2/4] Pushing local commit to remote origin...")
    try:
        subprocess.run(
            ["git", "-C", SOURCE_REPO_LOCAL_DIR, "push", "-u", f"https://{token}@github.com/{owner}/{repo_name}.git", "main"],
            check=True,
            capture_output=True,
            text=True
        )
        print("      Local branch 'main' pushed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"      Note on git push: {e.stderr.strip() or 'Remote might already contain branch.'}")

    # 3. Create Issues
    print(f"\n[3/4] Creating 6 synthetic issues from demo-repo-kit/issues/...")
    issue_files = sorted([f for f in os.listdir(ISSUES_DIR) if f.startswith("issue-") and f.endswith(".md")])
    created_issues = []

    for idx, f in enumerate(issue_files, 1):
        parsed = parse_issue_file(os.path.join(ISSUES_DIR, f))
        print(f"      [{idx}/6] Creating: \"{parsed['title']}\" (Target state: {parsed['state']})")
        
        issue_payload = {
            "title": parsed["title"],
            "body": parsed["body"],
            "labels": parsed["labels"]
        }
        
        i_status, i_res = github_api_request(
            f"https://api.github.com/repos/{owner}/{repo_name}/issues",
            method="POST",
            token=token,
            payload=issue_payload
        )
        
        if i_status in (200, 201):
            issue_num = i_res.get("number")
            issue_url = i_res.get("html_url")
            print(f"            Created Issue #{issue_num}: {issue_url}")
            
            # If state should be closed, update it
            if parsed["state"] == "closed":
                print(f"            Updating Issue #{issue_num} state to 'closed'...")
                p_status, p_res = github_api_request(
                    f"https://api.github.com/repos/{owner}/{repo_name}/issues/{issue_num}",
                    method="PATCH",
                    token=token,
                    payload={"state": "closed"}
                )
                if p_status == 200:
                    print(f"            Issue #{issue_num} closed successfully.")
                else:
                    print(f"            Warning: Failed to close issue: {p_res.get('message')}")
            
            created_issues.append((issue_num, parsed["title"], parsed["state"]))
        else:
            print(f"            Error creating issue: {i_res.get('message')}")

    # 4. Generate .env.local
    print(f"\n[4/4] Writing configuration to FlowMedic/.env.local...")
    env_local_path = os.path.join(FLOWMEDIC_DIR, ".env.local")
    env_content = f"""# FlowMedic Local Environment Configuration
# Generated for demo repository: {owner}/{repo_name}

GITHUB_OWNER={owner}
GITHUB_REPOSITORY={repo_name}
GITHUB_TOKEN={token}
DATABASE_URL=
LLM_API_KEY=
FLOWMEDIC_RUN_TOKEN=flowmedic-demo-token-secure-preview-2026
AUTH_SECRET=flowmedic-auth-secret-demo-32char-string
"""
    with open(env_local_path, "w", encoding="utf-8") as f:
        f.write(env_content)
    print(f"      Configured {env_local_path} successfully!")

    print("\n" + "="*60)
    print("SUCCESS: Demo Repository Kit Task Completed!")
    print("="*60)
    print(f"Repository: https://github.com/{owner}/{repo_name}")
    print(f"Issues created: {len(created_issues)}")
    print(f"FlowMedic Config: {env_local_path}")

if __name__ == "__main__":
    cli_token = sys.argv[1] if len(sys.argv) > 1 else None
    run(token=cli_token)

