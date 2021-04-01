"""
Fichier contenant main

@author: Sarah CE-OUGNA
"""

from dataFunctions import Data
from Interface import MyApplication
import sys

if __name__ == "__main__":
    if ("--download" in sys.argv):
        theData = Data(download=True)
    else:
        theData = Data()
            
    app = MyApplication(theData)
    app.mainloop()