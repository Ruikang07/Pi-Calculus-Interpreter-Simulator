#From Ruslan Spivak's work 

from graphviz import Source
import sys

def main(file):
    path = "./"+file
    s = Source.from_file(path)
    s.view()

if __name__ == '__main__':
    main(sys.argv[1])

