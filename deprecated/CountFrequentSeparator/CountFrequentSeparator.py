import os
import matplotlib.pyplot as plt
from operator import itemgetter
from collections import OrderedDict

directory_path = "/Users/barber/Data/Research/File-type-identification/very-small-data/png"
file_size_in_bytes = 4096
# max_process_size_in_bytes = 3 * 1024 * 1024 # 3 MB
max_process_size_in_bytes = 700 * file_size_in_bytes # 700 Fragments
gram_size = 3


def main():
    directory = directory_path

    if not os.path.exists(directory):
        exit(-1)

    if not directory.endswith("/"):
        directory += "/"

    fragments_processed = 0
    fragments_to_process = int(max_process_size_in_bytes / file_size_in_bytes)

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    plt.title('png, 3-gram, 700 fragments')

    for file_name in os.listdir(directory):
        if file_name.startswith("."):
            continue

        # fragment_frequency_output = open("./fragment_frequency.csv", "w")

        file_path = directory + file_name
        with open(file_path, "rb") as file:
            fragment = file.read(file_size_in_bytes)
            while len(fragment) == file_size_in_bytes:
                separator_frequency = dict()
                for index in range(0, file_size_in_bytes - gram_size + 1):
                    separator = int.from_bytes(fragment[index:(index + gram_size)], byteorder='big')
                    if separator in separator_frequency:
                        separator_frequency[separator] += 1
                    else:
                        separator_frequency[separator] = 1

                ordered_frequency = OrderedDict(sorted(separator_frequency.items(), key=itemgetter(1), reverse=True))

                # fragment_frequency_output.write(','.join(str(x) for x in list(ordered_frequency.keys())[:4096]))
                # fragment_frequency_output.write('\n')
                # fragment_frequency_output.write(','.join(str(x) for x in list(ordered_frequency.values())[:4096]))
                # fragment_frequency_output.write('\n')

                x = list(ordered_frequency.keys())[:4096]
                y = list(ordered_frequency.values())[:4096]
                ax1.scatter(x, y, s=2)

                fragments_processed += 1
                if fragments_processed >= fragments_to_process:
                    print("Processed {} fragments.".format(fragments_processed))
                    # fragment_frequency.output.close();
                    plt.show()
                    return

                fragment = file.read(file_size_in_bytes)

if __name__ == "__main__":
    main()
