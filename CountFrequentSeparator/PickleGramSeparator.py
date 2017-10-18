import os
import pickle
from operator import itemgetter
from collections import OrderedDict

directory_path = {
    'mp3': "/Users/barber/Data/Research/File-type-identification/scraped-data/train_data/mp3",
    'hwp': "/Users/barber/Data/Research/File-type-identification/scraped-data/train_data/hwp",
    'pdf': "/Users/barber/Data/Research/File-type-identification/scraped-data/train_data/pdf",
    'jpg': "/Users/barber/Data/Research/File-type-identification/scraped-data/train_data/jpg",
    'png': "/Users/barber/Data/Research/File-type-identification/scraped-data/train_data/png"
}

file_size_in_bytes = 4096
max_process_size_in_bytes = 10 * 1024 * 1024  # 100 MB


def compute_gram_frequency(gram, limit):
    print("Processing {}-gram...".format(gram))
    separator_frequency = dict()
    for file_type, directory in directory_path.items():

        if not os.path.exists(directory):
            exit(-1)

        if not directory.endswith("/"):
            directory += "/"

        fragments_processed = 0
        fragments_to_process = int(max_process_size_in_bytes / file_size_in_bytes)

        next_type_flag = False

        for file_name in os.listdir(directory):
            if next_type_flag:
                break

            if file_name.startswith("."):
                continue

            file_path = directory + file_name
            
            with open(file_path, "rb") as file:
                fragment = file.read(file_size_in_bytes)
                while len(fragment) == file_size_in_bytes:

                    for index in range(0, file_size_in_bytes - gram + 1):
                        separator = int.from_bytes(fragment[index:(index + gram)], byteorder='big')
                        if separator in separator_frequency:
                            separator_frequency[separator] += 1
                        else:
                            separator_frequency[separator] = 1

                    fragments_processed += 1
                    if fragments_processed >= fragments_to_process:
                        print("\t- Processed {}.".format(file_type))
                        
                        next_type_flag = True
                        break

                    if next_type_flag:
                        break

                    fragment = file.read(file_size_in_bytes)

    ordered_frequency = OrderedDict(
        sorted(separator_frequency.items(), key=itemgetter(1), reverse=True))
    separators = list(sorted(list(ordered_frequency.keys())[:limit]))
    result_dict = dict()
    index = 0
    for separator in separators:
        result_dict[separator] = index
        index += 1
    return result_dict


def main():
    result_separators = list()
    result_separators.append(compute_gram_frequency(gram=2, limit=2048))
    result_separators.append(compute_gram_frequency(gram=3, limit=1024))
    result_separators.append(compute_gram_frequency(gram=4, limit=512))
    result_separators.append(compute_gram_frequency(gram=5, limit=256))
    with open("./separators.pickle", "wb") as object_file:
        pickle.dump(result_separators, object_file)
    print("Done. Result: ")
    print(result_separators)

if __name__ == "__main__":
    main()

