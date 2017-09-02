import FileManager
import FragmentManager
import IOManager


def main():
    while True:
        print("(1) - Compute Bit Frequency\n(2) - Quit")
        if IOManager.IOManager.ask_int("--- ") != 1:
            break

        # Compute Bit Frequency
        print("Please type fragments' input directory path.")
        fragment_input_directory_path = IOManager.IOManager.ask_string("--- ")

        print("Please type fragments' output csv path.")
        output_csv_path = IOManager.IOManager.ask_string("--- ")

        print("Please type fragments' base name.")
        fragment_base_name = IOManager.IOManager.ask_string("--- ")

        file_manager = FileManager.FileManager(fragment_input_directory_path)
        fragment_manager = FragmentManager.FragmentManager()

        print("Please type which n-gram to be used.")
        gram = IOManager.IOManager.ask_int("--- ")

        print("Please type file type identification number.")
        file_type_number = IOManager.IOManager.ask_int("--- ")

        file_existence_flag = False
        for fragment_name in file_manager.fragment_list():
            if not fragment_name.startswith(fragment_base_name):
                continue
            file_existence_flag = True
            fragment_path = file_manager.fragment_path(fragment_name)
            print("Processing '{}' ...".format(fragment_path))
            fragment_manager.set_fragment(fragment_path, gram)
            fragment_manager.compute_bit_frequency_data(output_csv_path, file_type_number)

        if file_existence_flag:
            print("Computing bit frequency for directory '{}' is complete.\n".format(file_manager.input_directory_path))


if __name__ == "__main__":
    main()
