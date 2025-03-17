import subprocess
import sys
import json
import re


PROTECTED_BRANCHES = [
    "main",
    "dev"
]

REPLACEMENTS = {
    "DEPENDS": "",
    "IDF_VERSION":"",
}


SDK_CONFIG = 'sdkconfig'


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

    
    version_idf = "?"
    try:
        with open(SDK_CONFIG, 'r') as f:
            for linea in f:
                if "Espressif IoT Development Framework" in linea:
                    version_idf = linea.split("ESP-IDF")[1].split()[1]
    except :
        pass

    for key, value in REPLACEMENTS.items():
        if key == 'DEPENDS':
            result = subprocess.run(['git', 'submodule', 'status'], stdout=subprocess.PIPE, text=True)
            submodules = result.stdout.splitlines()
            value= ""
            for sub in submodules:
                parts = sub.split()
                component = parts[1].split("components/")[1]
                version = parts[-1]
                value += f"- {component} {version}\n"
        if key == "IDF_VERSION":
            value = version_idf
        
        content = re.sub(r'\{\{' + re.escape(key) + r'\}\}', value, content)
    
    with open("README.md", "w") as readme_file:
        readme_file.write(content)

    subprocess.run(["git", "add", "README.md"], check=True)

except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)

sys.exit(0)