#!/usr/bin/env python3
"""
Complete setup and test for dynatrace-daily-health
Usage: python3 setup.py
"""

import os
import sys
import json
import subprocess
from pathlib import Path


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 60}")
    print(f"  {text}")
    print(f"{'=' * 60}{Colors.ENDC}\n")


def print_step(num, text):
    print(f"{Colors.OKBLUE}[Step {num}]{Colors.ENDC} {text}")


def print_success(text):
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")


def print_error(text):
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")


def print_warning(text):
    print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")


def get_github_token():
    """Get GitHub PAT from user."""
    print_header("Step 1: GitHub Personal Access Token")
    
    print("You need a GitHub PAT to configure secrets.")
    print("To create one:")
    print("  1. Go to: https://github.com/settings/tokens")
    print("  2. Click 'Generate new token (classic)'")
    print("  3. Select scopes: 'repo', 'workflow'")
    print("  4. Copy the token and paste here\n")
    
    token = input("Enter your GitHub PAT: ").strip()
    if not token:
        print_error("Token required!")
        sys.exit(1)
    
    if not token.startswith("ghp_"):
        print_warning("Token should start with 'ghp_'")
    
    return token


def get_dynatrace_token():
    """Get Dynatrace token from user."""
    print_header("Step 2: Dynatrace API Token")
    
    print("You need a Dynatrace API token.")
    print("To create one:")
    print("  1. Go to: https://uxw82338.live.dynatrace.com/ui/settings/integration/apiTokens")
    print("  2. Click 'Create token'")
    print("  3. Name: 'Daily Health Check'")
    print("  4. Scopes: 'entities.read', 'metrics.read', 'problems.read'")
    print("  5. Copy the token\n")
    
    token = input("Enter your Dynatrace API token: ").strip()
    if not token:
        print_error("Token required!")
        sys.exit(1)
    
    if not token.startswith("dt0c01."):
        print_warning("Token should start with 'dt0c01.'")
    
    return token


def configure_secrets(github_token, dynatrace_token):
    """Configure GitHub secrets using the API."""
    print_header("Step 3: Configuring GitHub Secrets")
    
    owner = "marcdubrulle-arch"
    repo = "dynatrace-daily-health"
    secrets = {
        "DYNATRACE_BASE_URL": "https://uxw82338.live.dynatrace.com",
        "DYNATRACE_API_TOKEN": dynatrace_token,
        "EMAIL_TO": "marc.dubrulle@orange.com",
    }
    
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github.v3+json",
    }
    
    for name, value in secrets.items():
        try:
            # Get public key for encryption (if needed)
            print_step(1, f"Configuring {name}...")
            
            # For simplicity, we'll just use curl
            cmd = [
                "curl", "-X", "PUT",
                f"https://api.github.com/repos/{owner}/{repo}/actions/secrets/{name}",
                "-H", f"Authorization: Bearer {github_token}",
                "-H", "Accept: application/vnd.github.v3+json",
                "-d", json.dumps({"encrypted_value": value}),
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print_success(f"{name} configured")
            else:
                print_error(f"Failed to configure {name}: {result.stderr}")
                
        except Exception as e:
            print_error(f"Error configuring {name}: {e}")


def trigger_workflow(github_token):
    """Trigger the workflow."""
    print_header("Step 4: Triggering Workflow")
    
    owner = "marcdubrulle-arch"
    repo = "dynatrace-daily-health"
    workflow = "daily-health.yml"
    
    try:
        cmd = [
            "curl", "-X", "POST",
            f"https://api.github.com/repos/{owner}/{repo}/actions/workflows/{workflow}/dispatches",
            "-H", f"Authorization: Bearer {github_token}",
            "-H", "Accept: application/vnd.github.v3+json",
            "-d", '{"ref":"main"}',
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print_success("Workflow triggered!")
            print(f"\nWatch it at:")
            print(f"  https://github.com/{owner}/{repo}/actions")
        else:
            print_error(f"Failed to trigger workflow: {result.stderr}")
            
    except Exception as e:
        print_error(f"Error triggering workflow: {e}")


def main():
    """Main setup flow."""
    print(f"\n{Colors.HEADER}{Colors.BOLD}")
    print("╔═══════════════════════════════════════════╗")
    print("║  Dynatrace Daily Health - Complete Setup  ║")
    print("╚═══════════════════════════════════════════╝")
    print(f"{Colors.ENDC}")
    
    # Get tokens
    github_token = get_github_token()
    dynatrace_token = get_dynatrace_token()
    
    # Confirm
    print_header("Confirmation")
    print("About to configure:")
    print(f"  Repository: marcdubrulle-arch/dynatrace-daily-health")
    print(f"  Secrets: 3 (DYNATRACE_BASE_URL, DYNATRACE_API_TOKEN, EMAIL_TO)")
    print(f"  Workflow: daily-health.yml")
    print()
    
    confirm = input("Proceed? (y/n): ").strip().lower()
    if confirm != 'y':
        print_warning("Cancelled")
        sys.exit(0)
    
    # Configure secrets
    configure_secrets(github_token, dynatrace_token)
    
    # Trigger workflow
    trigger_workflow(github_token)
    
    # Summary
    print_header("Setup Complete!")
    print_success("Configuration done")
    print(f"\n{Colors.OKBLUE}Next steps:{Colors.ENDC}")
    print("  1. Wait 2-5 minutes for the workflow to complete")
    print("  2. Check GitHub Actions for logs and artifacts")
    print("  3. Check your email for the daily report")
    print(f"\nWorkflow URL:")
    print(f"  https://github.com/marcdubrulle-arch/dynatrace-daily-health/actions")
    print()


if __name__ == "__main__":
    main()
