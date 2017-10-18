import os
import matplotlib.pyplot as plt
from operator import itemgetter
from collections import OrderedDict

directory_path = {
    'mp3': "/Users/barber/Data/Research/File-type-identification/very-small-data/mp3",
    'hwp': "/Users/barber/Data/Research/File-type-identification/very-small-data/hwp",
    'pdf': "/Users/barber/Data/Research/File-type-identification/very-small-data/pdf",
    'jpg': "/Users/barber/Data/Research/File-type-identification/very-small-data/jpg",
    'png': "/Users/barber/Data/Research/File-type-identification/very-small-data/png"
}

file_size_in_bytes = 4096
max_process_size_in_bytes = 3 * 1024 * 1024 # 3 MB
# max_process_size_in_bytes = 700 * file_size_in_bytes # 700 Fragments
gram_size = 50


def main():
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    plt.title('all, 50-gram, 3 MB')

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
            separator_frequency = dict()
            with open(file_path, "rb") as file:
                fragment = file.read(file_size_in_bytes)
                while len(fragment) == file_size_in_bytes:

                    for index in range(0, file_size_in_bytes - gram_size + 1):
                        separator = int.from_bytes(fragment[index:(index + gram_size)], byteorder='big')
                        if separator in separator_frequency:
                            separator_frequency[separator] += 1
                        else:
                            separator_frequency[separator] = 1

                    fragments_processed += 1
                    if fragments_processed >= fragments_to_process:
                        print("Processed {}.".format(file_type))
                        ordered_frequency = OrderedDict(
                            sorted(separator_frequency.items(), key=itemgetter(1), reverse=True))
                        x = list(ordered_frequency.keys())[:4096]
                        y = list(ordered_frequency.values())[:4096]
                        ax1.scatter(x, y, s=2, label=file_type)
                        # fragment_frequency.output.close();
                        next_type_flag = True
                        break

                    if next_type_flag:
                        break

                    fragment = file.read(file_size_in_bytes)

    box = ax1.get_position()
    ax1.set_position([box.x0, box.y0 + box.height * 0.1,
                     box.width, box.height * 0.9])

    # Put a legend below current axis
    ax1.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=5)
    plt.show()

if __name__ == "__main__":
    main()
