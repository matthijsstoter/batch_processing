from excel_interface import run
import os
import platform

def main():
    if platform.system() == "Windows":
        cmd = """
            env\Scripts\activate;
           python excel_interface.py"""
        os.system(cmd)
        
    elif platform.system() == "Darwin":
        cmd = """source env/bin/activate;
                python excel_interface.py"""
        os.system(cmd)



if __name__ == "__main__":
    main()