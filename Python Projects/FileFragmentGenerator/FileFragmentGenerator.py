import DirectoryManager
import FileManager
import IOManager


def main():
    while True:
        print("(1) Do Fragmentation\n(2) Quit")
        if IOManager.IOManager.ask_int("1 or 2 --- ") != 1:
            break

        # Do Fragmentation
        print("Please type input files' directory path.")
        input_directory_path = IOManager.IOManager.ask_string("--- ")
        print("Please type output files' directory path.")
        output_directory_path = IOManager.IOManager.ask_string("--- ")
        print("Please type target files' extension.")
        file_extension = IOManager.IOManager.ask_string("--- .")

        directory_manager = DirectoryManager.DirectoryManager(input_directory_path, output_directory_path)
        file_manager = FileManager.FileManager()

        print("Please type resulting fragments' base filename. They will be named as (base_filename)_0, ...")
        base_filename = IOManager.IOManager.ask_string("--- ")
        print("Please type resulting fragments' extension. Leave empty if not needed.")
        fragment_extension = IOManager.IOManager.ask_string("--- .")

        while True:
            print("Please type fragmentation type.")
            print("(1) Sequential Cut\n(2) Random Cut")
            fragmentation_type = IOManager.IOManager.ask_int("--- ")
            if fragmentation_type == 1 or fragmentation_type == 2:
                break
            print("Wrong type. Only (1) or (2) is available. Please try again.")

        fragment_count = None
        if fragmentation_type == 2:
            print("How many fragments are needed for each file?")
            fragment_count = IOManager.IOManager.ask_int("--- ")

        print("Please type each fragment's byte length.")
        fragment_length = IOManager.IOManager.ask_int("--- ")

        print("Please type fragment's starting number..")
        fragment_starting_number = IOManager.IOManager.ask_int("--- ")

        directory_not_exist_flag = True
        fragment_number = fragment_starting_number
        for filename in directory_manager.file_list():
            directory_not_exist_flag = False
            if not filename.endswith(file_extension) or filename.startswith("~$"):
                continue

            print("Processing", filename, "...")
            file_path = directory_manager.get_input_path(filename)
            file_manager.set_file(file_path, fragment_length)

            if fragmentation_type == 1:
                for fragment in file_manager.sequential_fragment():
                    filename = base_filename + "_" + str(fragment_number)
                    if len(fragment_extension) != 0:
                        filename += "." + fragment_extension
                    directory_manager.write_into_file(filename, fragment)
                    fragment_number += 1
            else:
                for fragment in file_manager.random_fragment(fragment_count):
                    filename = base_filename + "_" + str(fragment_number)
                    if len(fragment_extension) != 0:
                        filename += "." + fragment_extension
                    directory_manager.write_into_file(filename, fragment)
                    fragment_number += 1

        if not directory_not_exist_flag:
            print("Fragmentation for directory '{}' is complete.\n".format(directory_manager.input_directory_path))


if __name__ == "__main__":
    main()
