import os


def iterate_over_binary_files_in(directory, limit, func):
    if not directory.endswith("/"):
        directory += "/"

    files_done = 0
    for file_name in os.listdir(directory):
        if files_done >= limit:
            break

        if file_name.startswith("."):
            continue

        file_path = directory + file_name
        with open(file_path, "rb") as file:
            func(file)

        files_done += 1


def print_and_count(file, counter):
    print(file)
    counter.append(file)


iterate_over_binary_files_in(directory="./", limit=2, func=print_and_count)
