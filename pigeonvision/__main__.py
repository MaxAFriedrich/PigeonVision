import pigeonvision
import sys

if __name__ == "__main__":
    # get the first argument from the command line
    if len(sys.argv) > 1:
        query = sys.argv[1]
        short, explanation = pigeonvision.main(query)
        print(short)
        print(explanation)
    else:
        print("Usage: python -m pigeonvision <query>")
