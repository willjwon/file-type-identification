# -*- coding: utf-8 -*-

# Scrapy settings for FileScraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = "FileScraper"

SPIDER_MODULES = ["FileScraper.spiders"]
NEWSPIDER_MODULE = "FileScraper.spiders"

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    "scrapy.pipelines.files.FilesPipeline": 300,
    "scrapy.pipelines.images.ImagesPipeline": 300
}
FILES_STORE = "./files"
IMAGES_STORE = "./images"

IMAGES_MIN_HEIGHT = 150
IMAGES_MIN_WIDTH = 150

MEDIA_ALLOW_REDIRECTS = True

# DEPTH_LIMIT = 2
