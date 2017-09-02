import urllib.request
import urllib.error
import os
import unittest

class FileDownloadManager:
    def __init__(self, download_path):
        self.urlOpener = urllib.request.URLopener()
        self.download_path = download_path

    def download_file_at_url(self, url):
        filename = url.strip().split("://")[1].replace("/", "_")

        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path)

        if self.download_path.endswith("/"):
            download_destination = self.download_path + "_" + filename
        else:
            download_destination = self.download_path + "/" + filename

        if os.path.exists(download_destination):
            print("The file '{}' is already downloaded.".format(download_destination))
            return

        try:
            download_url = urllib.request.urlopen(url).geturl()
            self.urlOpener.retrieve(download_url, download_destination)
        except:
            print("An error occurred while downloading the file. It is skipped.")


class FileDownloadManagerTest(unittest.TestCase):
    def setUp(self):
        self.fileDownloadManager = FileDownloadManager("./test")

    def test_download_file_at_url(self):
        self.fileDownloadManager.download_file_at_url("https://www.google.com/robots.txt")
