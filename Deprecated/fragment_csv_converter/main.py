from directories import Directories
from settings import Settings
from separator_counter import SeparatorCounter
from frequency_writer import FrequencyWriter


def main():
    # Read Settings file
    settings = Settings(directory="./", filename="settings.json")

    train_directories_dict = settings.read("data", "train")
    validation_directories_dict = settings.read("data", "validation")
    test_directories_dict = settings.read("data", "test")

    csv_directories = settings.read("csv", "directory")
    csv_file_names = settings.read("csv", "filename")
    num_csv_fragments = settings.read("csv", "num_fragments")

    fragment_size = settings.read("fragment_size")
    separator_path = settings.read("separator")

    num_validation_fragments_per_type = settings.read("fragments", "num_validation_fragments_per_type")
    num_test_fragments_per_type = settings.read("fragments", "num_test_fragments_per_type")

    # Instantiate Directories class
    train_directories = Directories(directories=train_directories_dict)
    validation_directories = Directories(directories=validation_directories_dict)
    test_directories = Directories(directories=test_directories_dict)

    # Instantiate FrequencyWriter class
    train_writer = FrequencyWriter(directory=csv_directories["train"],
                                   filename=csv_file_names["train"],
                                   directories=train_directories_dict,
                                   num_max_row=num_csv_fragments)
    validation_writer = FrequencyWriter(directory=csv_directories["validation"],
                                        filename=csv_file_names["validation"],
                                        directories=validation_directories_dict,
                                        num_max_row=num_csv_fragments)
    test_writer = FrequencyWriter(directory=csv_directories["test"],
                                  filename=csv_file_names["test"],
                                  directories=test_directories_dict,
                                  num_max_row=num_csv_fragments)

    # Instantiate SeparatorCounter class
    separator_counter = SeparatorCounter(separator_path=separator_path)

    # Generate Train Fragments
    print("Generating Train Fragments...")
    train_writer.start_csv()
    type_index, train_directory = train_directories.random_directory()
    while train_directory is not None:
        fragment = train_directory.read_fragment(size=fragment_size)
        if fragment is None:
            train_directories.remove_directory(type_index)
            type_index, train_directory = train_directories.random_directory()
            continue
        separator_frequency = separator_counter.count_frequency(fragment)
        train_writer.write(frequency=separator_frequency, index=type_index)
        type_index, train_directory = train_directories.random_directory()

    print("\nGenerating Validation Fragments...")
    validation_writer.start_csv()
    type_index, validation_directory = validation_directories.sequential_directory()
    fragments_processed = 0
    while validation_directory is not None:
        fragment = validation_directory.read_fragment(size=fragment_size)
        if fragment is None or fragments_processed >= num_validation_fragments_per_type:
            validation_directories.remove_directory(type_index)
            type_index, validation_directory = validation_directories.sequential_directory()
            print("\n{} Types Left.".format(len(validation_directories.files)))
            fragments_processed = 0
            continue
        separator_frequency = separator_counter.count_frequency(fragment)
        validation_writer.write(frequency=separator_frequency, index=type_index)
        fragments_processed += 1
    
    print("\nGenerating Test Fragments...")
    test_writer.start_csv()
    type_index, test_directory = test_directories.sequential_directory()
    fragments_processed = 0
    while test_directory is not None:
        fragment = test_directory.read_fragment(size=fragment_size)
        if fragment is None or fragments_processed >= num_test_fragments_per_type:
            test_directories.remove_directory(type_index)
            type_index, test_directory = test_directories.sequential_directory()
            print("\n{} Types Left.".format(len(validation_directories.files)))
            fragments_processed = 0
            continue
        separator_frequency = separator_counter.count_frequency(fragment)
        test_writer.write(frequency=separator_frequency, index=type_index)
        fragments_processed += 1


if __name__ == '__main__':
    main()