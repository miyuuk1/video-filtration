from sys import argv
from process_func import main_process


def main():
    if len(argv) < 2:
        print("error: params length < 2: ", argv)
        print("usage: ", argv[0], " <input> <output>")
        return
    input_path = argv[1]
    output = argv[2]

    main_process(input_path, output)


if __name__ == "__main__":
    main()