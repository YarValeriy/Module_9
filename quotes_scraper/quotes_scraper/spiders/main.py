import scrapy
import json


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ["http://quotes.toscrape.com/"]
    quotes = []
    authors = []

    def parse(self, response):
        for quote in response.css("div.quote"):
            quote_item = {
                "quote": quote.css("span.text::text")
                .get()
                .strip("“”"),  
                "author": quote.css("small.author::text").get(),
                "tags": quote.css("div.tags a.tag::text").getall(),
            }
            self.quotes.append(quote_item)

            author_item = {
                "fullname": quote_item["author"],
                "born_date": "",
                "born_location": "",
                "description": "",
            }
            self.authors.append(author_item)

        # Follow pagination links
        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def closed(self, reason):
        # Save quotes to qoutes.json
        with open("qoutes.json", "w") as f:
            json.dump(self.quotes, f, indent=2)

        # Save authors to authors.json
        with open("authors.json", "w") as f:
            json.dump(self.authors, f, indent=2)


# Main function to execute the spider
def main():
    from scrapy.crawler import CrawlerProcess

    # Start the crawler process
    process = CrawlerProcess()
    process.crawl(QuotesSpider)
    process.start()


if __name__ == "__main__":
    main()
