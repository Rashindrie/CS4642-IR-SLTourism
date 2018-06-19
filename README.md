# CS4642-soYAMU

A project used to retrieve information on places (Restaurants, Hotels, Bars, Charities, Attractions, Shops) in Sri Lanka from https://www.yamu.lk/ site and build a search index for that site.

## Running the project

### Prerequisites 

Scrapy ( For more information refer installation guide at https://doc.scrapy.org/en/latest/intro/install.html )

### Running the Scraper

From the root directory of the project type the following command in the terminal and the scraping would initiate.

  `scrapy crawl yamu -o data/pages.json`

The scraped data will be saved to a output file in the 'data' directory under the name 'pages.json'
