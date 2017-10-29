import os
import settings
import unittest
import random
from File import File
from CountGramData import CountGramData, generate_one_hot_group_csv_string
from PrintProgress import print_progress


def make_directory(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


def main():
    # set the output path
    output_path = settings.output_path
    if not output_path.endswith("/"):
        output_path += "/"

    # Make train fragments

    # 1. Read files for each type for train data
    if settings.num_train_fragments_per_type != 0:
        files = []
        num_fragments_left = [settings.num_train_fragments_per_type] * len(settings.file_types)
        for file_type in settings.file_types.keys():
            files.append(File(file_type, settings.train_directory_path[file_type], settings.fragment_size_in_bytes))

        # 2. Prepare train output file
        train_file_index = 1
        train_output_path = output_path + "train_data/"
        make_directory(train_output_path)
        train_output_file_base_name = train_output_path + "train_data_"
        output_file = open(train_output_file_base_name + str(train_file_index) + ".csv", "w")

        # 3. Generate train output file
        CountGramData.load_frequent_separators()

        num_fragments_in_csv = 0
        print("Generating Train Data...")
        total_train_fragments = settings.num_train_fragments_per_type * len(settings.file_types)
        total_train_fragments_done = 0
        while len(files) != 0:
            print_progress(total_train_fragments_done, total_train_fragments)

            if num_fragments_in_csv >= settings.num_fragments_per_csv:
                num_fragments_in_csv = 0
                output_file.close()
                train_file_index += 1
                output_file = open(train_output_file_base_name + str(train_file_index) + ".csv", "w")

            index = random.randrange(len(files))
            read_data = files[index].read(settings.fragment_size_in_bytes)
            file_type = files[index].file_type
            num_fragments_left[index] -= 1

            if num_fragments_left[index] == 0:
                del files[index]
                del num_fragments_left[index]

            count_result = CountGramData.count_gram_data_and_get_result_csv_string(read_data)
            one_hot_encoding = generate_one_hot_group_csv_string(settings.file_types[file_type], settings.num_groups)
            output_file.write(count_result + "," + one_hot_encoding + "\n")

            num_fragments_in_csv += 1
            total_train_fragments_done += 1
        print_progress(total_train_fragments_done, total_train_fragments)
        output_file.close()

    # 4. Generate validation output file
    if settings.num_validation_fragments_per_type != 0:
        print("\n\nGenerating Validation Data...")
        total_validation_fragments = settings.num_validation_fragments_per_type * len(settings.file_types)
        total_validation_fragments_done = 0
        num_fragments_in_csv = 0
        validation_file_index = 1
        validation_output_path = output_path + "validation_data/"
        make_directory(validation_output_path)
        validation_output_file_base_name = validation_output_path + "validation_data_"
        output_file = open(validation_output_file_base_name + str(validation_file_index) + ".csv", "w")
        for file_type in settings.file_types.keys():
            file = File(file_type, settings.validation_directory_path[file_type], settings.fragment_size_in_bytes)

            for _ in range(settings.num_validation_fragments_per_type):
                print_progress(total_validation_fragments_done, total_validation_fragments)

                if num_fragments_in_csv >= settings.num_fragments_per_csv:
                    num_fragments_in_csv = 0
                    output_file.close()
                    validation_file_index += 1
                    output_file = open(validation_output_file_base_name + str(validation_file_index) + ".csv", "w")

                read_data = file.read(settings.fragment_size_in_bytes)
                count_result = CountGramData.count_gram_data_and_get_result_csv_string(read_data)
                one_hot_encoding = generate_one_hot_group_csv_string(settings.file_types[file_type], settings.num_groups)
                output_file.write(count_result + "," + one_hot_encoding + "\n")

                num_fragments_in_csv += 1
                total_validation_fragments_done += 1
        print_progress(total_validation_fragments_done, total_validation_fragments)
        output_file.close()

    # 5. Generate test output file
    if settings.num_test_fragments_per_type != 0:
        print("\n\nGenerating Test Data...")
        total_test_fragments = settings.num_test_fragments_per_type * len(settings.file_types)
        total_test_fragments_done = 0
        num_fragments_in_csv = 0
        test_file_index = 1
        test_output_path = output_path + "test_data/"
        make_directory(test_output_path)
        test_output_file_base_name = test_output_path + "test_data_"
        output_file = open(test_output_file_base_name + str(test_file_index) + ".csv", "w")
        for file_type in settings.file_types.keys():
            file = File(file_type, settings.test_directory_path[file_type], settings.fragment_size_in_bytes)

            for _ in range(settings.num_test_fragments_per_type):
                print_progress(total_test_fragments_done, total_test_fragments)
                if num_fragments_in_csv >= settings.num_fragments_per_csv:
                    num_fragments_in_csv = 0
                    output_file.close()
                    test_file_index += 1
                    output_file = open(test_output_file_base_name + str(test_file_index) + ".csv", "w")

                read_data = file.read(settings.fragment_size_in_bytes)
                count_result = CountGramData.count_gram_data_and_get_result_csv_string(read_data)
                one_hot_encoding = generate_one_hot_group_csv_string(settings.file_types[file_type], settings.num_groups)
                output_file.write(count_result + "," + one_hot_encoding + "\n")

                num_fragments_in_csv += 1
                total_test_fragments_done += 1
        print_progress(total_test_fragments_done, total_test_fragments)
        output_file.close()

if __name__ == "__main__":
    main()


class GramFragmentGeneratorUnitTest(unittest.TestCase):
    def test_sample(self):
        pass
