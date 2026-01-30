import sys
import subprocess
import os

def generate_pinned_requirements():
    print("Capturing currently installed packages in venv...")
    result = subprocess.run([sys.executable, "-m", "pip", "freeze"], capture_output=True, text=True)
    installed_packages = result.stdout.splitlines()
    
    # Define primary dependencies based on project imports
    primary_deps = [
        "torch", 
        "transformers", 
        "pillow", 
        "pytesseract", 
        "opencv-python-headless", 
        "pandas", 
        "numpy", 
        "accelerate", 
        "datasets", 
        "evaluate"
    ]
    
    pinned_requirements = []
    # Match primary dependencies with installed versions
    for dep in primary_deps:
        match = [p for p in installed_packages if p.lower().startswith(f"{dep}==")]
        if match:
            pinned_requirements.append(match[0])
        else:
            # Fallback for packages that might have different names in freeze
            pinned_requirements.append(dep)
            
    req_file = "/Users/dakshjain/Desktop/GitHubDemos/NEODEMO1/requirements.txt"
    with open(req_file, "w") as f:
        f.write("\n".join(sorted(list(set(pinned_requirements)))))
    
    print(f"Generated pinned requirements.txt at {req_file}")
    return req_file

def validate_requirements(file_path):
    print(f"Validating {file_path}...")
    # Dry run installation check (pip check)
    result = subprocess.run([sys.executable, "-m", "pip", "check"], capture_output=True, text=True)
    
    report_file = "/Users/dakshjain/Desktop/GitHubDemos/NEODEMO1/installation_report.md"
    with open(report_file, "w") as f:
        f.write("# Installation Validation Report\n\n")
        f.write(f"**Date:** {os.popen('date').read().strip()}\n")
        f.write(f"**Python Version:** {sys.version}\n\n")
        f.write("## Dependency Check Results\n")
        if result.returncode == 0:
            f.write("✅ No dependency conflicts detected by `pip check`.\n\n")
        else:
            f.write(f"⚠️ Dependency conflicts found:\n```\n{result.stdout}\n```\n\n")
            
        f.write("## Import Verification\n")
        modules = ["torch", "transformers", "PIL", "pytesseract", "cv2", "pandas"]
        for mod in modules:
            try:
                __import__(mod)
                f.write(f"- ✅ {mod}: Successfully imported\n")
            except ImportError:
                f.write(f"- ❌ {mod}: FAILED to import\n")
                
    print(f"Validation report generated at {report_file}")

if __name__ == "__main__":
    req_file = generate_pinned_requirements()
    validate_requirements(req_file)