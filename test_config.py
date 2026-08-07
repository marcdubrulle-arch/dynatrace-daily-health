#!/usr/bin/env python3
"""Diagnostic script to test Dynatrace API token and configuration"""
import os
import sys

def test_config():
    """Test if all required environment variables are set"""
    print("=" * 60)
    print("CONFIGURATION DIAGNOSTIC TOOL")
    print("=" * 60)
    
    required_vars = {
        "DYNATRACE_BASE_URL": "Dynatrace environment URL",
        "DYNATRACE_API_TOKEN": "Dynatrace API token",
    }
    
    optional_vars = {
        "EMAIL_TO": "Email recipient",
        "SMTP_SERVER": "SMTP server",
    }
    
    print("\n[REQUIRED VARIABLES]")
    all_required_set = True
    for var, desc in required_vars.items():
        value = os.environ.get(var, "")
        status = "✓ SET" if value else "✗ MISSING"
        if var == "DYNATRACE_API_TOKEN" and value:
            print(f"{status:10} | {var:30} | prefix: {value[:20]}... | length: {len(value)}")
        else:
            print(f"{status:10} | {var:30} | value: {value[:50] if value else 'EMPTY'}")
        
        if not value:
            all_required_set = False
    
    print("\n[OPTIONAL VARIABLES]")
    for var, desc in optional_vars.items():
        value = os.environ.get(var, "")
        status = "✓ SET" if value else "○ NOT SET"
        print(f"{status:10} | {var:30} | value: {value[:50] if value else 'EMPTY'}")
    
    print("\n" + "=" * 60)
    if all_required_set:
        print("✓ All required variables are set!")
    else:
        print("✗ Some required variables are missing!")
        print("\nTo configure GitHub Secrets:")
        print("1. Go to Settings -> Secrets and variables -> Actions")
        print("2. Create new secrets:")
        print("   - DYNATRACE_BASE_URL: https://uxw82338.live.dynatrace.com")
        print("   - DYNATRACE_API_TOKEN: <your-token>")
        sys.exit(1)
    
    print("=" * 60)

if __name__ == "__main__":
    test_config()
