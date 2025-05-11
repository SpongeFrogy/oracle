import fileinput

fucked_file = "/usr/local/lib/python3.11/site-packages/pandas_ta/momentum/squeeze_pro.py"
fucked_line = "from numpy import NaN as npNaN"
good_line = "from numpy import nan as npNaN\n"


def patch_library():
    with fileinput.FileInput(fucked_file, inplace=True, backup=".bak") as file:
        for line in file:
            if fucked_line in line:
                print(good_line, end="")
            else:
                print(line, end="")

if __name__ == '__main__':
    patch_library()