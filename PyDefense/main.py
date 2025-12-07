import sys
import os

# Add the package to the path so we can import modules from it
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pydefense.PyDefense import main

if __name__ == "__main__":
    main()
