import unittest


def print_progress(current_level, max_level, bar_length=50):
    num_bar_to_print = int(current_level / max_level * bar_length)
    string_to_print = "|" + \
                      ("=" * num_bar_to_print) + \
                      ">" + \
                      " " * (bar_length - num_bar_to_print) \
                      + "| {:2.2f}%".format(current_level / max_level * 100) + \
                      " ({} / {})".format(current_level, max_level)
    print("\r{}".format(string_to_print), end="")


class PrintProgressTest(unittest.TestCase):
    def test_print_progress(self):
        print_progress(1, 17, 50)
