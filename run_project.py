import subprocess
import sys
import os

import platform

def run_command(command, description):
    print(f"\n>> {description}...")
    try:
        subprocess.check_call(command)
    except subprocess.CalledProcessError as e:
        print(f"Error during {description}: {e}")
        sys.exit(1)

def check_environment():
    print("\n--- Environment Check ---")
    os_name = platform.system()
    arch = platform.machine()
    print(f"OS: {os_name}")
    print(f"Architecture: {arch}")

    # Check Tesseract OCR
    tesseract_installed = False
    try:
        subprocess.run(['tesseract', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        tesseract_installed = True
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    if tesseract_installed:
        print("[PASS] Tesseract OCR is installed.")
    else:
        print("[FAIL] Tesseract OCR is NOT found.")
        if os_name == "Darwin":
            print("      Suggestion: Run 'brew install tesseract'")
        elif os_name == "Linux":
            print("      Suggestion: Run 'sudo apt-get install tesseract-ocr'")
        else:
            print("      Suggestion: Please install Tesseract OCR for your system.")

    # Check for macOS ARM64 binary permissions
    if os_name == "Darwin" and arch == "arm64":
        print("[INFO] macOS ARM64 detected. Ensure binaries are allowed to run (System Settings > Privacy & Security).")

    # Check Python version
    print(f"Python version: {sys.version.split()[0]}")
    if sys.version_info < (3, 8):
        print("[FAIL] Python 3.8+ is required.")
        return False
    else:
        print("[PASS] Python version is compatible.")
    
    print("-------------------------\n")
    return True

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base_dir)

    # 1. Check environment
    if not check_environment():
        sys.exit(1)

    # 2. Setup Venv and Install dependencies
    if os.name == "nt":
        pip_path = os.path.join("venv", "Scripts", "pip.exe")
        python_path = os.path.join("venv", "Scripts", "python.exe")
    else:
        pip_path = os.path.join("venv", "bin", "pip")
        python_path = os.path.join("venv", "bin", "python")

    if not os.path.exists(pip_path):
        if os.path.exists("venv"):
            print(">> Existing 'venv' folder found but incomplete. Removing to ensure clean setup...")
            import shutil
            # Using basic os.system for robustness if shutil fails
            os.system('rm -rf venv')
        run_command([sys.executable, "-m", "venv", "venv"], "Creating virtual environment")

    run_command([pip_path, "install", "--upgrade", "pip"], "Upgrading pip")
    run_command([pip_path, "install", "-r", "requirements.txt"], "Installing dependencies")

    # 3. Run Pipeline
    env = os.environ.copy()
    env["PYTHONPATH"] = os.path.join(base_dir, "src") + os.pathsep + env.get("PYTHONPATH", "")
    print(f"\n>> Executing Invoice Pipeline...")
    try:
        subprocess.check_call([python_path, "src/invoice_pipeline.py"], env=env)
    except subprocess.CalledProcessError as e:
        print(f"Error during Invoice Pipeline: {e}")
        sys.exit(1)

    print("\n[SUCCESS] Project ran end-to-end successfully.")

if __name__ == "__main__":
    main()