"""
Validation script to check environment and prerequisites
"""
import sys
import subprocess
from pathlib import Path


def check_python_version():
    """Check Python version >= 3.10"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print(f"❌ Python 3.10+ required, found {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor}")
    return True


def check_required_files():
    """Check required files exist"""
    required_files = [
        "models.py",
        "environment.py",
        "client.py",
        "inference.py",
        "server/main.py",
        "tasks/graders.py",
        "requirements.txt",
        "openenv.yaml",
        "Dockerfile",
        "README.md",
    ]
    
    all_exist = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} missing")
            all_exist = False
    return all_exist


def check_dependencies():
    """Check required packages installed"""
    packages = [
        "fastapi",
        "uvicorn",
        "pydantic",
        "requests",
    ]
    
    for package in packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} not installed")
            return False
    return True


def check_environment():
    """Run sanity checks"""
    print("\n" + "=" * 60)
    print("ENVIRONMENT VALIDATION")
    print("=" * 60 + "\n")

    checks = [
        ("Python Version", check_python_version),
        ("Required Files", check_required_files),
        ("Dependencies", check_dependencies),
    ]

    results = []
    for check_name, check_func in checks:
        print(f"\n[{check_name}]")
        try:
            result = check_func()
            results.append(result)
        except Exception as e:
            print(f"❌ Error: {e}")
            results.append(False)

    print("\n" + "=" * 60)
    if all(results):
        print("✅ All checks passed!")
        print("=" * 60 + "\n")
        return True
    else:
        print("❌ Some checks failed")
        print("=" * 60 + "\n")
        return False


if __name__ == "__main__":
    success = check_environment()
    sys.exit(0 if success else 1)
