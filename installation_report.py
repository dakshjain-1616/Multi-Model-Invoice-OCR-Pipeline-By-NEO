import subprocess
import sys

def check_install():
    print("Verifying Requirements Installation...")
    try:
        # Check for conflicts
        subprocess.check_call([sys.executable, "-m", "pip", "check"])
        print("[PASS] No dependency conflicts found.")
        
        # Verify core imports
        modules = ['transformers', 'torch', 'PIL', 'pytesseract', 'numpy']
        for m in modules:
            __import__(m)
            print(f"[PASS] Successfully imported {m}")
        
    except Exception as e:
        print(f"[FAIL] Validation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    check_install()