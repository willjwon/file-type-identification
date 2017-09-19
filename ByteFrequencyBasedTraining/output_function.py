from setup import *


def print_accuracy_table(accuracy_table):
    """
    prints 2d accuracy table to the console
    :param accuracy_table: 2d accuracy table to print
    """

    # print the head
    print("{:<5} | ".format(" t\\p "), end="")
    for i in range(FLAGS.num_of_groups):
        print("{:<5}\t\t".format(FLAGS.group_name[i]), end="")
    print("")
    print("----------" * (FLAGS.num_of_groups + 1))

    # print the data
    for i in range(FLAGS.num_of_groups):
        print("{:<5} | ".format(FLAGS.group_name[i]), end="")
        for j in range(FLAGS.num_of_groups):
            file_accuracy = \
                accuracy_table[i][j] / (FLAGS.num_of_test_files_per_type * FLAGS.num_of_fragments_per_csv) * 100
            print("{:2.2f}%\t\t".format(file_accuracy), end="")
        print("")
    print("----------" * (FLAGS.num_of_groups + 1))


def print_progress(current_level, max_level, bar_size=50):
    """
    prints progress bar.
    :param current_level: current progress level to show
    :param max_level: the job's maximum level to finish a job
    :param bar_size: default bar size.
    """
    progress_percentage = current_level / max_level
    num_of_bars_to_show = int(progress_percentage * bar_size)
    num_of_tabs_left = bar_size - num_of_bars_to_show
    progress_bar = "\r" + ("=" * num_of_bars_to_show) + ">" \
                   + (" " * num_of_tabs_left) \
                   + "| {:2.1f}%".format(progress_percentage * 100)
    print(progress_bar, end="")

