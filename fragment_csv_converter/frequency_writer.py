import os


class FrequencyWriter:
    def __init__(self, directory, filename, directories, num_max_row):
        if not os.path.exists(directory):
            os.makedirs(directory)

        self.current_csv_number = 1
        self.file_path = os.path.join(directory, filename)
        self.csv_file = None
        self.num_files = int(max(directories.keys())) + 1
        self.num_max_row = num_max_row
        self.num_current_csv_row = 0

    def __del__(self):
        self.csv_file.close()

    def start_csv(self):
        self.csv_file = open(self.file_path.format(self.current_csv_number), "w")

    def set_to_next_csv(self):
        self.csv_file.close()
        self.current_csv_number += 1
        self.csv_file = open(self.file_path.format(self.current_csv_number), "w")

    def write(self, frequency, index):
        one_hot = [0 for _ in range(self.num_files)]
        one_hot[index] = 1

        data_to_write = frequency + one_hot
        data_in_string = [str(data) for data in data_to_write]
        data_in_csv_format = ",".join(data_in_string)

        self.num_current_csv_row += 1
        if self.num_current_csv_row < self.num_max_row:
            self.csv_file.write(data_in_csv_format + "\n")
        elif self.num_current_csv_row == self.num_max_row:
            self.csv_file.write(data_in_csv_format)
        else:
            self.num_current_csv_row = 1
            self.set_to_next_csv()
            self.csv_file.write(data_in_csv_format + "\n")
