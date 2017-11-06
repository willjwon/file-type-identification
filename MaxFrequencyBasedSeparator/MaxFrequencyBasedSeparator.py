import settings
import os
import pickle
import numpy as np
import heapq


def main():
    count_result = dict()
    num_file_types = len(settings.file_path)

    for gram in range(settings.start_gram, settings.end_gram + 1):
        for file_index in range(num_file_types):
            count_frequency(count_result, gram, file_index, num_file_types)
        reduce_to_max(count_result, gram)

    count_result = pick_top_grams(count_result)

    result = reconstruct(count_result)

    with open("./frequent_separators.pickle", "wb") as file:
        pickle.dump(result, file, protocol=pickle.HIGHEST_PROTOCOL)

    print("Picked {} separators.".format(settings.num_grams_to_pick))
    for gram in range(settings.start_gram, settings.end_gram + 1):
        print("\t- At {}-gram, {} separators are selected.".format(gram, len(result[gram])))


def count_frequency(count_result, gram_size, file_index, num_file_types):

    file_path = settings.file_path[file_index]

    if not file_path.endswith("/"):
        file_path += "/"

    for file_name in os.listdir(file_path):
        if file_name.startswith(".") or "." not in file_name:
            continue

        with open(file_path + file_name, "rb") as file:
            data = file.read(settings.fragment_size_in_byte)
            while len(data) == settings.fragment_size_in_byte:
                for index in range(settings.fragment_size_in_byte - gram_size + 1):
                    gram_value = int.from_bytes(data[index:(index + gram_size)], byteorder='big')
                    gram_key = (gram_size, gram_value)
                    if gram_key in count_result:
                        count_result[gram_key][file_index] += 1
                    else:
                        count_result[gram_key] = [0] * num_file_types
                        count_result[gram_key][file_index] += 1
                data = file.read(settings.fragment_size_in_byte)


def reduce_to_max(count_result, gram_size):
    for key, freq in count_result.items():
        count_result[key] = np.max(freq)


def pick_top_grams(count_result):
    return heapq.nlargest(settings.num_grams_to_pick, count_result, key=count_result.get)


def reconstruct(count_result):
    result = dict()
    index = dict()
    for gram in range(settings.start_gram, settings.end_gram + 1):
        result[gram] = dict()
        index[gram] = 0

    for gram, value in count_result:
        result[gram][value] = index[gram]
        index[gram] += 1

    return result


if __name__ == "__main__":
    main()
