# from __future__ import unicode_literals
import scrapy

import json

import os

import scrapy

from scrapy.spiders import Spider

from scrapy.http import FormRequest

from scrapy.http import Request

from chainxy.items import ChainItem

from scrapy import signals

from scrapy.xlib.pydispatch import dispatcher

from selenium import webdriver

from lxml import etree

from lxml import html

import time

import pdb


class brickset(scrapy.Spider):

	name = 'brickset'

	domain = 'https://brickset.com'

	history = []

	output = []

	def __init__(self):

		pass

	
	def start_requests(self):

		url = "https://brickset.com/browse/sets"

		yield scrapy.Request(url, callback=self.parse) 


	def parse(self, response):

		category_list = response.xpath('//div[@role="main"]//section[@class="navrow"][2]//a/@href').extract()

		for category in category_list:

			link = self.domain + category

			yield scrapy.Request(link, callback=self.parse_product)


	def parse_product(self, response):

		product_list = response.xpath('//section[@class="setlist"]//article[@class="set"]')

		for product in product_list:

			item = ChainItem()

			item['brand'] = 'Lego'

			try:

				item['number'] = product.xpath('.//h1//a//span/text()').extract_first().replace(':','').strip()

			except:

				temp = product.xpath('.//div[@class="meta"]//div[@class="tags"]//a[1]/text()').extract_first()

				if '-1' in temp:

					item['number'] = temp.replace('-1', '').strip()

			try:

				item['title'] = product.xpath('.//h1//a/text()').extract_first().strip()

			except:
				
				pass

			yield item

		next_page = response.xpath('//div[@class="pagination"]//li[@class="next"]//a/@href').extract_first()

		if next_page:

			yield scrapy.Request(next_page, callback=self.parse_product)


	def validate(self, item):

		try:

			return item.replace('\n', '').replace('\t','').replace('\r', '').strip()

		except:

			pass


	def eliminate_space(self, items):

	    tmp = []

	    for item in items:

	        if self.validate(item) != '':

	            tmp.append(self.validate(item))

	    return tmp