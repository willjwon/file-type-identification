from fragment import Fragment
from separator_checker import SeparatorChecker


def main():
    # Setup Fragment
    fragment_getter = Fragment(directory="/home/jonghoon/Desktop/ppt", fragment_size=4096)

    # Setup Separator checker
    separator_checker = SeparatorChecker()
    obvious_separators, obvious_gram_size = SeparatorChecker.obvious_separators()
    candidate_separators, gram_size = SeparatorChecker.init_candidate()

    # Compute
    while len(candidate_separators) != 0:
        separator_checker.set_candidate_separators(candidate_separators=candidate_separators, gram_size=gram_size)
        fragment = fragment_getter.get_fragment()
        while fragment is not None:
            separator_checker.count_fragment(fragment=fragment)
            fragment = fragment_getter.get_fragment()

        frequent_separators = separator_checker.get_frequent_separators(proportion=0.01)
        print("At {}-gram, {} separators are frequent.".format(gram_size, len(frequent_separators)))

        candidate_separators = separator_checker.make_candidate_separators(frequent_separators)
        gram_size += 1
        print("{}-gram candidates: {} separators.".format(gram_size, len(candidate_separators)))
        print()


if __name__ == "__main__":
    main()