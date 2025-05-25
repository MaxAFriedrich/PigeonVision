import pigeonvision
import sys

if __name__ == "__main__":
    # get the first argument from the command line
    if len(sys.argv) > 1:
        query = sys.argv[1]
        verbose = sys.argv[2]
        level = sys.argv[3]
        short, explanation, _ = pigeonvision.main(query, verbose, level)
        print(short)
        print(explanation)
    else:
        print("Usage: python -m pigeonvision <query> <verbose> <log level>")
        print("e.g. python -m pigeonvision google.com False DEBUG")
