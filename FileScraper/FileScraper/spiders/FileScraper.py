import os
import scrapy
from FileScraper.hashchecker import *
from urllib.parse import urljoin
from scrapy.spiders import CrawlSpider


class FileScraper(CrawlSpider):
    name = "file-scraper"

    start_urls = ["http://cse.snu.ac.kr"]

    files_to_download = (".hwp", ".pdf", ".docx", ".xlsx", ".exe", ".mp3")
    images_to_download = (".jpg", ".png", ".gif")

    hash_checker = HashChecker()

    def parse(self, response):
        # check the given request is valid html document type.
        if "html" not in response.headers.get("Content-Type").decode():
            return

        # save response page
        html_name = response.url.strip().split("//")[1].replace("/", "#")
        html_name_split = html_name.split("#")
        if len(html_name_split) == 1 or len(html_name_split) == 2:
            url_hash_seed = html_name
        else:
            try:
                url_hash_seed = html_name_split[0] + html_name_split[1] + html_name_split[3][:3]
            except IndexError:
                # html_name_split has less than 5 characters. use the base seed.
                url_hash_seed = html_name_split[0] + html_name_split[1]

        if not self.hash_checker.duplicated(url_hash_seed):
            html_save_link = "./html/" + html_name + ".html"
            try:
                with open(html_save_link, "wb") as html_file:
                    html_file.write(response.body)
            except FileNotFoundError:
                os.makedirs("./html/")

        # download images
        image_links = list(set(response.xpath("//img/@src").extract()))  # list(set()) to remove duplicate links
        for i in range(len(image_links)):
            if not image_links[i].startswith("http"):
                # add base url of response if url doesn't start with http
                image_links[i] = urljoin(response.url, image_links[i][1:])
        image_links = list(filter(lambda link: link.endswith(self.images_to_download), image_links))
        yield {"image_urls": image_links}

        file_links = list(set(response.xpath("//a/@href").extract()))  # list(set()) to remove duplicate links
        for file_link in file_links:
            if not file_link.startswith("http"):
                # add base url of response if url doesn't start with http
                file_link = urljoin(response.url, file_link[1:])

            # download files
            if file_link.endswith(self.files_to_download):
                print("File To Download:", file_link)
                yield {"file_urls": [file_link]}
            else:
                yield scrapy.Request(file_link, callback=self.parse)
