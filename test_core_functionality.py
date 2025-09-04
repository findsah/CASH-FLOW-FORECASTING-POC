import sys

def test_imports():
    print("🐍 Python Version:", sys.version.split('\n')[0])
    print("\n🔍 Testing core functionality...\n")
    
    tests = {
        'Flask': lambda: __import__('flask').__version__,
        'Flask-CORS': lambda: __import__('flask_cors').__version__,
        'Pandas': lambda: __import__('pandas').__version__,
        'NumPy': lambda: __import__('numpy').__version__,
        'Matplotlib': lambda: __import__('matplotlib').__version__,
        'PyPDF2': lambda: __import__('PyPDF2').__version__,
        'scikit-learn': lambda: __import__('sklearn').__version__,
        'Plotly': lambda: __import__('plotly').__version__,
        'yfinance': lambda: __import__('yfinance').__version__
    }
    
    all_ok = True
    for name, test in tests.items():
        try:
            version = test()
            print(f"✅ {name} ({version}) is working")
        except Exception as e:
            print(f"❌ {name} failed: {str(e)}")
            all_ok = False
    
    if all_ok:
        print("\n🎉 All core functionality is working!")
    else:
        print("\n❌ Some tests failed. Please check the output above.")

if __name__ == "__main__":
    test_imports()
