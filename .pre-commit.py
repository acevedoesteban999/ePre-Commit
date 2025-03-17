import subprocess
import sys
import json
import re

"""
    use sys.exit(1) for error
    use sys.exit(0) for continue
"""

# EXAMPLE PROTECTED BRANCHES
PROTECTED_BRANCHES = [
    "main",
    "dev"
]

try:
    branch = subprocess.check_output(["git", "symbolic-ref", "--short", "HEAD"]).decode("utf-8").strip()
except subprocess.CalledProcessError:
    print("Error: E1")
    sys.exit(1)

if branch in PROTECTED_BRANCHES:
    print(f"Error: Direct commits are not allowed in the '{branch}' branch. Use a merge.")
    sys.exit(1)

sys.exit(0)