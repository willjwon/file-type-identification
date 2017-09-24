import os
import scrapy
from urllib.parse import urljoin
from scrapy.spiders import CrawlSpider


class FileScraper(CrawlSpider):
    name = "file-scraper"

    start_urls = ["http://admission.kaist.ac.kr/undergraduate/"]
    allowed_domains = ["admission.kaist.ac.kr"]

    files_to_download = (".hwp", ".pdf", ".docx", ".xlsx", ".exe", ".mp3")
    images_to_download = (".jpg", ".png", ".gif")

    def parse(self, response):
        # check the given request is valid html document type.
        if "html" not in response.headers.get("Content-Type").decode():
            return

        # save response page
        html_save_link = "./html/" + \
                         response.url.strip().split("//")[1].replace("/", "#") + \
                         ".html"
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
