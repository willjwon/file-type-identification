import os
import pickle
import operator

def main():
    frequent_separator_result = dict()

    files = os.listdir("./frequent_separators")
    files = list(filter(lambda name: not name.startswith("."), files))
    if len(files) == 0:
        print("No separators in './frequent_separators'!")
        print("Please locate separators in './frequent_separators' directory and try again.")
        exit(-1)

    # merge frequent separators
    for file_name in files:
        file_path = "./frequent_separators/" + file_name
        with open(file_path, "rb") as file:
            frequent_separators = pickle.load(file)

        for gram, separator in frequent_separators.items():
            if gram not in frequent_separator_result:
                frequent_separator_result[gram] = separator
            else:
                if len(separator) < len(frequent_separator_result[gram]):
                    frequent_separator_result[gram] = separator

    # check the merged separator is correct
    grams = list(sorted(frequent_separator_result.keys()))
    missed_grams = []
    for i in range(len(grams) - 1):
        if grams[i + 1] - grams[i] != 1:
            missed_grams.append(grams[i] + 1)


    if len(missed_grams) != 0:
        if len(missed_grams) == 1:
            print("Frequent Separators are merged, but a gram is missing.")
            print("Missing Gram: ", end="")
        else:
            print("Frequent Separators are merged, but some grams are missing.")
            print("Missing Grams: ", end="")

        print(', '.join(str(gram) for gram in missed_grams))

        print("Please fix the issue and try again.")
        exit(-1)

    print("Saving Merged Separator...")

    frequent_separator_result = dict(sorted(frequent_separator_result.items(), key=operator.itemgetter(0)))
    with open("./frequent_separators.pickle", "wb") as file:
        pickle.dump(frequent_separator_result, file, protocol=pickle.HIGHEST_PROTOCOL)
    print("Merged separator saved at './frequent_separators.pickle'.")

    print("\n\nSaving Separator Information...")
    with open("./separators_information.csv", "w") as file:
        for data in frequent_separator_result.values():
            for gram in data.keys():
                file.write("{},".format(hex(gram)[2:].upper()))

    print("Separator information has been saved at './separators_information.csv'.")

if __name__ == "__main__":
    main()
