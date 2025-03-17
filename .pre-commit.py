import subprocess
import sys
import json
import re


PROTECTED_BRANCHES = [
    "main",
    "dev"
]

REPLACEMENTS = {
    "TEST": "ASD",
}

#PROTECTES BRANCHES
try:
    branch = subprocess.check_output(["git", "symbolic-ref", "--short", "HEAD"]).decode("utf-8").strip()
except subprocess.CalledProcessError:
    print("Error: No se pudo obtener la rama actual.")
    sys.exit(1)

if branch in PROTECTED_BRANCHES:
    print(f"Error: Direct commits are not allowed in the '{branch}' branch. Use a merge.")
    sys.exit(1)


#README
try:
    with open(".PRE-README.md", "r") as pre_readme_file:
        content = pre_readme_file.read()

    for var, value in REPLACEMENTS.items():
        content = re.sub(r'\{\{' + re.escape(var) + r'\}\}', value, content)

    with open("README.md", "w") as readme_file:
        readme_file.write(content)

    subprocess.run(["git", "add", "README.md"], check=True)

except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)

sys.exit(0)