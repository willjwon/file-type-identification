import settings
import os
import pickle
import numpy as np
import heapq


def main():
    count_result = dict()
    num_file_types = len(settings.file_path)

    for gram in range(settings.start_gram, settings.end_gram + 1):
        print("At {}-gram:".format(gram))
        for file_index in range(num_file_types):
            print("Counting file-index {}...".format(file_index))
            count_frequency(count_result, gram, file_index, num_file_types)
            print()
        reduce_to_max(count_result)
        largest_index = pick_top_grams(count_result)

        result = dict()
        for key in largest_index:
            result[key] = count_result[key]
            del count_result[key]
        count_result = result

    count_result = pick_top_grams(count_result)

    result = reconstruct(count_result)

    with open("./frequent_separators.pickle", "wb") as file:
        pickle.dump(result, file, protocol=pickle.HIGHEST_PROTOCOL)

    print("Picked {} separators.".format(settings.num_grams_to_pick))
    for gram in range(settings.start_gram, settings.end_gram + 1):
        print("\t- At {}-gram, {} separators are selected.".format(gram, len(result[gram])))

    print("Saving separators information...")
    with open("./separators_information.csv", "w") as file:
        for selected_grams in result.values():
            file.write(','.join(hex(i)[2:].upper() for i in selected_grams.keys()))

    print("Separator information has been saved at './separators_information.csv'.")


def count_frequency(count_result, gram_size, file_index, num_file_types):

    file_path = settings.file_path[file_index]

    if not file_path.endswith("/"):
        file_path += "/"

    fragments_done = 0
    for file_name in os.listdir(file_path):
        break_flag = False
        if file_name.startswith("."):
            continue

        if "exe" not in file_path and '.' not in file_name:
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
                fragments_done += 1

                if fragments_done % 1000 == 0:
                    print("{} fragments processed...".format(fragments_done))

                if fragments_done >= settings.num_fragments_to_compute_per_type:
                    break_flag = True
                    break

                data = file.read(settings.fragment_size_in_byte)

            if break_flag:
                break


def reduce_to_max(count_result):
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
