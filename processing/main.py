from sys import argv
from process_func import main_process
import common.common as commons

def main():
    if len(argv) < 2:
        print("error: params length < 2: ", argv)
        print("usage: ", argv[0], " <input> <output>")
        return
    # input_path = argv[1]
    # output = argv[2]

    input_path = commons.DEFAULT_INPUT + "static_noise_res.avi"
    output_path = commons.DEFAULT_OUTPUT + "result.avi"
    main_process(input_path, output_path)


if __name__ == "__main__":
    main()