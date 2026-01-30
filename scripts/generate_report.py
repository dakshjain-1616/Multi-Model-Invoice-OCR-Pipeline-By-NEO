import os
import subprocess
from datetime import datetime

def generate_report():
    report_content = [
        "# Installation Validation Report",
        f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "\n## 1. Dependency Installation Status",
    ]
    
    try:
        # Dry run install
        result = subprocess.run([os.sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--dry-run"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            report_content.append("✅ `pip install -r requirements.txt --dry-run` passed successfully.")
        else:
            report_content.append(f"❌ `pip install` dry-run failed with code {result.returncode}.")
            report_content.append(f"```\n{result.stderr}\n```")
    except Exception as e:
        report_content.append(f"⚠️ Error during dry-run: {str(e)}")

    report_content.append("\n## 2. Dependency Conflict Check")
    try:
        result = subprocess.run([os.sys.executable, "-m", "pip", "check"], capture_output=True, text=True)
        if result.returncode == 0:
            report_content.append("✅ `pip check` found no broken dependencies.")
        else:
            report_content.append("❌ `pip check` reported conflicts:")
            report_content.append(f"```\n{result.stdout}\n```")
    except Exception as e:
        report_content.append(f"⚠️ Error during pip check: {str(e)}")

    report_content.append("\n## 3. Dynamic Path Verification")
    from config import BASE_DIR, NER_MODEL_PATH
    report_content.append(f"- Project Root: `{BASE_DIR}`")
    report_content.append(f"- NER Model Target: `{NER_MODEL_PATH}`")
    report_content.append(f"- Model Directory Exists: `{os.path.isdir(NER_MODEL_PATH)}`")

    with open("validation_report.md", "w") as f:
        f.write("\n".join(report_content))
    print("Report generated: validation_report.md")

if __name__ == "__main__":
    generate_report()