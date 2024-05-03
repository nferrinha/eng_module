import csv

def str_to_int(s: str) -> int:
    """
    Returns an integer if the string 's' represents an integer
    """
    try:
        return int(s)
    except ValueError:
        return s

def str_to_float(s: str)-> float|str:
    """
    Returns the string 's' converted into a float if possible.
    Returns the original string, 's', otherwise.
    """
    try:
        return float(s)
    except ValueError:
        return s
    
def read_csv_file(filename:str)->list[list[str]]:
    """
    Returns a string representing the text data in the file
    at 'filename'.
    """
    csvfile_data=[]
    with open(filename,"r") as csv_file:
        csv_reader = csv.reader(csv_file)
        for line in csv_reader:
            csvfile_data.append(line)
    return csvfile_data