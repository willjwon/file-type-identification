import pickle
from settings import Settings
from files import Files
from gram_frequency import GramFrequency
from gram_filter import GramFilter


def main():
        # Read Settings
        settings = Settings(directory="./", filename="settings.json")
        directory = settings.read("directory")
        fragment_size = settings.read("fragment", "size")
        pruning_threshold = settings.read("pruning", "threshold")
        max_gram_length = settings.read("pruning", "max_gram_length")
        num_separators_to_pick = settings.read("pruning", "num_separators_to_pick")

        print("Counting frequent n-grams...")
        # Generate 1-gram candidate
        gram_size = 1
        next_candidate = dict()
        for suffix in range(0, 256):
            next_candidate[bytes([suffix])] = 0
            
        # Make Files, GramFrequency and GramFilter instances
        files = Files(directory=directory)
        gram_frequency = GramFrequency(gram_size, next_candidate)
        gram_filter = GramFilter()
        
        # Count 1-Gram Frequency and number of fragments
        num_fragments = 0
        fragment = files.read_fragment(fragment_size)
        while fragment is not None:
            num_fragments += 1
            gram_frequency.count_fragment(fragment, fragment_size)
            fragment = files.read_fragment(fragment_size)
        files.reset()

        # Compute pruning threshold frequency
        pruning_threshold_frequency = int(pruning_threshold * num_fragments)
        print("\n{} Fragments, Threshold: {}\n".format(num_fragments, pruning_threshold_frequency))

        # Count N-Gram Frequency until end condition
        while True:
            # Print the previous result
            print("\nAt {}-Gram, {} Seperaters are freuquent.\n".format(gram_size, len(gram_frequency.frequency)))

            # When No separator is frequent, terminate the program.
            if len(gram_frequency.frequency) <= 0:
                break

            # Update Gram Filter
            gram_filter.add_frequent_grams(gram_frequency.frequency)
            
            # Check the ending condition. If not, update gram_frequency instance.
            if len(gram_frequency.frequency) <= 0:
                break

            if max_gram_length != -1 and gram_size >= max_gram_length:
                break
                
            next_candidate = gram_frequency.generate_next_candidate()
            if max_gram_length == -1 and len(gram_frequency.frequency) == len(next_candidate):
                break

            gram_size += 1
            gram_frequency = GramFrequency(gram_size, next_candidate)
            
            # Compute Frequent N-gram
            fragment = files.read_fragment(fragment_size)
            while fragment is not None:
                gram_frequency.count_fragment(fragment, fragment_size)
                fragment = files.read_fragment(fragment_size)
            files.reset()

            # Prune
            gram_frequency.get_frequent_gram_by_frequency(pruning_threshold_frequency)

        # Filter top-n Grams
        print("\nSelecting top-{} separators...".format(num_separators_to_pick))
        top_grams = gram_filter.filter_top_n_grams(num_separators_to_pick)
        num_picked_separators = 0
        for gram_len, picked_grams in top_grams.items():
            len_picked_grams = len(picked_grams)
            num_picked_separators += len_picked_grams
            print("\tAt {}-gram, picked {} separators.".format(gram_len, len_picked_grams))
        print("{} Separators are selected.".format(num_picked_separators))

        # Save
        print("\nSaving...")
        with open("./separators.pickle", "wb") as file:
            pickle.dump(top_grams, file, protocol=pickle.HIGHEST_PROTOCOL)
        print("Separators successfully saved at ./separators.pickle.")


if __name__ == '__main__':
    main()
