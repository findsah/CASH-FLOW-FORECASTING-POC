import sys
import importlib.metadata

def check_package(package_name, version=None):
    try:
        installed_version = importlib.metadata.version(package_name)
        if version and installed_version != version:
            print(f"⚠️  {package_name}: Version mismatch! Installed: {installed_version}, Expected: {version}")
            return False
        print(f"✅ {package_name} ({installed_version}) is installed and working")
        return True
    except importlib.metadata.PackageNotFoundError:
        print(f"❌ {package_name} is not installed")
        return False

def main():
    print("\n🐍 Python Version:", sys.version.split('\n')[0])
    print("\n🔍 Checking dependencies...\n")
    
    # Core dependencies
    dependencies = {
        'flask': '2.3.3',
        'flask-cors': '4.0.0',
        'pandas': '2.0.3',
        'numpy': '1.24.4',
        'matplotlib': '3.7.2',
        'python-dateutil': '2.8.2',
        'PyPDF2': '3.0.1',
        'scikit-learn': '1.3.0',
        'plotly': '5.15.0',
        'plotly-express': '0.4.1',
        'yfinance': '0.2.18'
    }
    
    all_ok = True
    for package, version in dependencies.items():
        if not check_package(package, version):
            all_ok = False
    
    if all_ok:
        print("\n🎉 All dependencies are installed and working correctly!")
    else:
        print("\n❌ Some dependencies have issues. Please check the output above.")

if __name__ == "__main__":
    main()
