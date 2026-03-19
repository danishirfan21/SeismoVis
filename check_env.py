import sys
import os
import subprocess

print(f"Python Path: {sys.executable}")
print(f"Python Version: {sys.version}")
print(f"Current Working Directory: {os.getcwd()}")
print("\nEnvironment Variables:")
for k, v in os.environ.items():
    if "PYTHON" in k.upper():
        print(f"{k}: {v}")

print("\nInstalled Packages (Filtered):")
try:
    result = subprocess.run([sys.executable, "-m", "pip", "list"], capture_output=True, text=True)
    for line in result.stdout.splitlines():
        if any(pkg in line.lower() for pkg in ["pandas", "numpy", "vtk", "requests"]):
            print(line)
except Exception as e:
    print(f"Could not list packages: {e}")
