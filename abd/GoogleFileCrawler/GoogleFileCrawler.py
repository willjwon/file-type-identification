import GoogleSearchManager
import FileDownloadManager
import IOManager
import pickle
import os


def main():
    while True:
        print("(1) - Crawl File on Google\n(2) - End")
        if IOManager.IOManager.ask_int("1 or 2 --- ") != 1:
            break

        if os.path.exists("./last_input.log"):
            print("Last input settings without crawling completed is found! Those data were used.")
            with open("./last_input.log", "rb") as file:
                load_data = pickle.load(file)
                file_type = load_data["file_type"]
                query_msg = load_data["query_msg"]
                num_files_to_download = load_data["num_files_to_download"]
                destination_directory = load_data["destination_directory"]
                print("File Type: {}".format(file_type))
                print("Query Message: {}".format(query_msg))
                print("Number of Files to Download: {}".format(num_files_to_download))
                print("Destination Directory: {}".format(destination_directory))
                print()

        else:
            print("Please type file type to search")
            file_type = IOManager.IOManager.ask_string("--- .")

            print("Please type query message to search")
            query_msg = IOManager.IOManager.ask_string("--- ")

            print("Please type number of files to download (resulting file number may be different)")
            num_files_to_download = IOManager.IOManager.ask_int("--- ")

            print("Please type file download destination directory")
            destination_directory = IOManager.IOManager.ask_string("--- ")

        with open("./last_input.log", "wb") as file:
            saving_data = {"file_type": file_type,
                           "query_msg": query_msg,
                           "num_files_to_download": num_files_to_download,
                           "destination_directory": destination_directory}
            pickle.dump(saving_data, file)

        google_search_manager = GoogleSearchManager.GoogleSearchManager()
        file_download_manager = FileDownloadManager.FileDownloadManager(destination_directory)

        num_downloaded_files = 0
        search_result_links = []

        while num_downloaded_files < num_files_to_download and google_search_manager.start_num < 101:
            used_log, search_result_segment = google_search_manager.search_file_on_google(query_msg, file_type)
            search_result_links += search_result_segment
            num_downloaded_files += len(search_result_segment)

            if num_downloaded_files <= 1:
                print("Now crawled {} file...".format(num_downloaded_files))
            else:
                print("Now crawled {} files...".format(num_downloaded_files))

            if used_log:
                break

        with open("./last_search_result.log", "wb") as file:
            pickle.dump(search_result_links, file)
        print("Crawling complete!\n")

        download_counter = 1
        num_searched_files_to_download = len(search_result_links)
        for link in search_result_links:
            print("({} / {}) Downloading '{}'".format(download_counter, num_searched_files_to_download, link))
            file_download_manager.download_file_at_url(link)
            download_counter += 1

        os.remove("./last_input.log")
        os.remove("./last_search_result.log")
        print("Download complete!\n")

if __name__ == "__main__":
    main()
