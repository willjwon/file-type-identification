from fragment import Fragment
from separator_checker import SeparatorChecker


def main():
    # Setup Fragment
    fragment_getter = Fragment(directory="/home/jonghoon/Desktop/ppt", fragment_size=4096)

    # Setup Separator checker
    separator_checker = SeparatorChecker()
    obvious_separators, obvious_gram_size = SeparatorChecker.obvious_separators()
    candidate_separators, gram_size = SeparatorChecker.init_candidate()
    total_frequent_separators = dict()

    # Compute
    print("At 2-gram:")
    print("\tCandidate: 65536 separators.")
    while len(candidate_separators) != 0:
        separator_checker.set_candidate_separators(candidate_separators=candidate_separators, gram_size=gram_size)
        fragment = fragment_getter.get_fragment()
        while fragment is not None:
            separator_checker.count_fragment(fragment=fragment)
            fragment = fragment_getter.get_fragment()

        # frequent_separators_list = separator_checker.get_frequent_separators_absolute(top_n=10000)
        # frequent_separators_list = SeparatorChecker.filter_by_frequency(frequent_separators_list, threshold=0.05)
        frequent_separators_list = separator_checker.get_frequent_separators_frequency(threshold=0.05)

        print("\t{} separators are frequent.".format(len(frequent_separators_list)))

        if len(frequent_separators_list) <= 0:
            break

        SeparatorChecker.print_top_5(frequent_separators_list)
        SeparatorChecker.print_bottom_5(frequent_separators_list)

        frequent_separators_set = SeparatorChecker.separators_into_set_form(frequent_separators_list)
        total_frequent_separators[gram_size] = frequent_separators_set

        candidate_separators = separator_checker.make_candidate_separators(frequent_separators_set)
        gram_size += 1

        if gram_size > 20:
            break

        print("\nAt {}-gram:".format(gram_size))
        print("\tCandidates: {} separators.".format(len(candidate_separators)))

    print()
    total_separators_count = 0
    for gram, separators in total_frequent_separators.items():
        print("At {}-gram, {} separators are selected.".format(gram, len(separators)))
        total_separators_count += len(separators)
    print("Total {} separators are selected.".format(total_separators_count))


if __name__ == "__main__":
    main()
