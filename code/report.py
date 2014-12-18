import json
import pdb
from utilities import *

def main(id_= 1, dir_ = "../subjects_data"):
    fls = get_data_files(id_, dir_)
    for fl in fls:
        data = json.load(open(dir_ + "/" + fl))
        SummaryChoiceData(data).main()

if __name__ == "__main__":
    main()

