import sqlite3
import os
import pickle
import heapq
import settings
import Database as db
from PrintProgress import print_progress


def main():
    connection = sqlite3.connect('./frequency.db')
    print("Do you want to use existing database?")
    print("Use this option only if you have proper database at './frequency.db' set.")
    selected_option = input("[Y/n]: ")
    if selected_option.lower() == "n":
        db.remove_database(connection)
        db.create_database(connection)

        for gram in range(settings.end_gram, settings.start_gram - 1, -1):
            print("Computing {}-gram:".format(gram))
            finished_file_type_count = 0
            for file_type in settings.file_path.keys():
                count_frequency(connection, gram, file_type, finished_file_type_count)
                finished_file_type_count += 1
            reduce_to_max(connection, gram)

    # Pick largest grams after DB construction
    result = dict()
    for gram in range(settings.start_gram, settings.end_gram + 1):
        result[gram] = dict()

    db.pick_by_maximum(connection, result_dict=result, limit=settings.num_grams_to_pick)

    print("\n\nSaving Separators...")
    with open("./frequent_separators.pickle", "wb") as file:
        pickle.dump(result, file, protocol=pickle.HIGHEST_PROTOCOL)
    print("Separators are saved at './frequent_separators.pickle'.")

    print("\n\nPicked {} separators.".format(settings.num_grams_to_pick))
    for gram in range(settings.start_gram, settings.end_gram + 1):
        print("\t- At {}-gram, {} separators are selected.".format(gram, len(result[gram])))

    print("\n\nSaving separators information...")
    with open("./separators_information.csv", "w") as file:
        for selected_grams in result.values():
            file.write(','.join(hex(i)[2:].upper() for i in selected_grams.keys()))

    print("Separator information has been saved at './separators_information.csv'.")


def count_frequency(connection, gram_size, file_type, finished_file_type_count):
    file_path = settings.file_path[file_type]
    finished_fragments = settings.num_fragments_to_compute_per_type * finished_file_type_count

    if not file_path.endswith("/"):
        file_path += "/"

    fragments_done = 0
    result_dict = dict()
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
                    if gram_key in result_dict:
                        result_dict[gram_key] += 1
                    else:
                        result_dict[gram_key] = 1

                fragments_done += 1
                finished_fragments += 1

                print_progress(current_level=finished_fragments, max_level=_max_level)

                if fragments_done % 500 == 0:
                    db.update_by_dict(connection, gram_dict=result_dict, file_type=file_type)
                    result_dict.clear()

                if fragments_done >= settings.num_fragments_to_compute_per_type:
                    db.update_by_dict(connection, gram_dict=result_dict, file_type=file_type)
                    result_dict.clear()
                    break_flag = True
                    break

                data = file.read(settings.fragment_size_in_byte)

            print_progress(current_level=finished_fragments, max_level=_max_level)
            if break_flag:
                break


_max_level = len(settings.file_path) * settings.num_fragments_to_compute_per_type


def reduce_to_max(connection, gram):
    iterate_cursor = connection.cursor()
    update_cursor = connection.cursor()
    iterate_cursor.execute("SELECT * FROM frequency WHERE gram = {}".format(gram))
    for data in iterate_cursor:
        max_value = max(data[4:])
        query_string = "UPDATE frequency SET maximum = {} WHERE gram = {} AND gram_value = {}"\
            .format(max_value, data[0], data[1])
        update_cursor.execute(query_string)


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
