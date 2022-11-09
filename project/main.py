from src.WikiData import *

if __name__ == "__main__":
    reader = WikiDataReader("data/original.txt")
    for x in reader.data:
        print(x)
    for x in reader.exceptions:
        print(x)
