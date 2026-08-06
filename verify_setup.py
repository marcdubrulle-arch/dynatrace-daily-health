#!/usr/bin/env python3
"""
Verification script to check if GitHub Secrets are properly configured.
This script doesn't need GitHub CLI - it just checks local environment variables.
"""

import os
import sys
from pathlib import Path

def check_secrets():
    """Check if all required secrets are configured."""
    print("=" * 70)
    print("GITHUB SECRETS VERIFICATION")
    print("=" * 70)
    print()
    
    # Load .env.local if it exists (for local testing)
    env_file = Path(".env.local")
    if env_file.exists():
        print("📄 Loading .env.local file...")
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    key, value = line.split("=", 1)
                    os.environ[key] = value
        print(f"   Loaded {env_file}")
        print()
    
    # Required secrets
    required = [
        ("DYNATRACE_BASE_URL", "Dynatrace instance URL"),
        ("DYNATRACE_API_TOKEN", "Dynatrace API token"),
    ]
    
    # Optional secrets for email
    optional = [
        ("SMTP_SERVER", "SMTP server for email"),
        ("SMTP_PORT", "SMTP port (default: 587)"),
        ("SMTP_USER", "SMTP username"),
        ("SMTP_PASSWORD", "SMTP password"),
        ("EMAIL_FROM", "Email sender address"),
        ("EMAIL_TO", "Email recipient address"),
    ]
    
    print("🔐 REQUIRED SECRETS:")
    print("-" * 70)
    missing_required = []
    for key, description in required:
        value = os.environ.get(key, "").strip()
        if not value:
            print(f"❌ {key:<30} - MISSING")
            missing_required.append(key)
        else:
            # Mask sensitive values
            if "TOKEN" in key or "PASSWORD" in key:
                masked = value[:10] + "..." + value[-10:] if len(value) > 20 else "***"
                print(f"✅ {key:<30} - OK ({len(value)} chars): {masked}")
            elif key == "DYNATRACE_BASE_URL":
                print(f"✅ {key:<30} - OK: {value}")
            else:
                print(f"✅ {key:<30} - OK")
    
    print()
    print("📧 OPTIONAL SECRETS (for email reports):")
    print("-" * 70)
    missing_optional = []
    for key, description in optional:
        value = os.environ.get(key, "").strip()
        if not value:
            print(f"⚠️  {key:<30} - NOT SET")
            missing_optional.append(key)
        else:
            # Mask sensitive values
            if "PASSWORD" in key:
                masked = "***"
            elif "TOKEN" in key or "PASSWORD" in key:
                masked = value[:5] + "..." + value[-5:] if len(value) > 10 else "***"
            else:
                masked = value
            print(f"✅ {key:<30} - OK: {masked}")
    
    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    if missing_required:
        print()
        print(f"❌ BLOCKING ISSUES: {len(missing_required)} required secret(s) missing:")
        for key in missing_required:
            print(f"   - {key}")
        print()
        print("📝 ACTION REQUIRED:")
        print("   1. Go to: https://github.com/marcdubrulle-arch/dynatrace-daily-health/settings/secrets/actions")
        print("   2. Click 'New repository secret'")
        print("   3. Add each missing secret")
        print()
        return False
    else:
        print()
        print("✅ All required secrets are configured!")
        
        if missing_optional:
            print()
            print(f"⚠️  WARNING: {len(missing_optional)} optional secret(s) not set:")
            print("   Email reports will NOT be sent without SMTP configuration")
            for key in missing_optional:
                print(f"   - {key}")
        else:
            print("✅ All optional secrets are also configured!")
            print("   Email reports will be sent with each run")
        
        print()
        print("🚀 Ready to trigger workflow!")
        print("   Go to: https://github.com/marcdubrulle-arch/dynatrace-daily-health/actions")
        print("   Click 'Daily Dynatrace Health' > 'Run workflow' > 'Run workflow'")
        return True

if __name__ == "__main__":
    success = check_secrets()
    sys.exit(0 if success else 1)
