"""
Bharat Quest - Helper script to push repository to GitHub
Supports both direct git command and pure-Python dulwich push.
"""
import os
import sys
import socket

# Ensure DNS resolution for github.com works on local network
orig_getaddrinfo = socket.getaddrinfo

def custom_getaddrinfo(host, port, *args, **kwargs):
    if host == 'github.com':
        return orig_getaddrinfo('20.207.73.82', port, *args, **kwargs)
    return orig_getaddrinfo(host, port, *args, **kwargs)

socket.getaddrinfo = custom_getaddrinfo

def push_with_token(token: str, repo_url: str = "https://github.com/yodityarahi/Bharat-quest.git"):
    import dulwich.porcelain
    import dulwich.repo
    
    clean_url = repo_url.replace("https://", "").replace("http://", "")
    auth_url = f"https://oauth2:{token}@{clean_url}"
    
    print(f"Connecting and pushing to {repo_url}...")
    repo_path = os.path.dirname(os.path.abspath(__file__))
    repo = dulwich.repo.Repo(repo_path)
    
    dulwich.porcelain.push(repo, auth_url, refspecs=[b"refs/heads/main:refs/heads/main"])
    print("SUCCESS! Successfully pushed branch 'main' to GitHub repository.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        token = sys.argv[1].strip()
        push_with_token(token)
    else:
        token = os.environ.get("GITHUB_TOKEN")
        if token:
            push_with_token(token)
        else:
            print("Usage: python push_to_github.py <YOUR_GITHUB_PERSONAL_ACCESS_TOKEN>")
            print("Or set GITHUB_TOKEN environment variable.")
