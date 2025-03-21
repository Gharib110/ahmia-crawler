# -*- coding: utf-8 -*-
""" Settings """
import warnings
import datetime
import requests
from decouple import config

BOT_NAME = 'ahmia'

SPIDER_MODULES = ['ahmia.spiders']
NEWSPIDER_MODULE = 'ahmia.spiders'

# Log level and ignore useless warnings
LOG_LEVEL = 'INFO'
warnings.filterwarnings("ignore", category=RuntimeWarning,
                        module='scrapy.spidermiddlewares.referer',
                        message="Could not load referrer policy")

# Elasticsearch settings using environment variables for sensitive information
ELASTICSEARCH_SERVER = config('ES_URL', default="http://localhost:9200/")
ELASTICSEARCH_INDEX = datetime.datetime.now().strftime("tor-%Y-%m")
ELASTICSEARCH_USERNAME = config('ES_USERNAME', default='elastic')
ELASTICSEARCH_PASSWORD = config('ES_PASSWORD', default='password12345')
ELASTICSEARCH_CA_CERTS = config('ES_CA_CERTS',
                                default='/etc/elasticsearch/certs/http_ca.crt')

# Identify as normal Tor Browser
#USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0"
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"

# Main settings for crawling speed and performance
DOWNLOAD_TIMEOUT = 60  # seconds
DOWNLOAD_DELAY = 1
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 60
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0  # Adjust based on performance

# Crawl in breadth-first order (BFO)
DEPTH_PRIORITY = 1
SCHEDULER_DISK_QUEUE = "scrapy.squeues.PickleFifoDiskQueue"
SCHEDULER_MEMORY_QUEUE = "scrapy.squeues.FifoMemoryQueue"
DOMAIN_MAX_REQUESTS = 1000 # Spider does not over-focus on large websites, set 0 for unlimited

# Broad Crawls
# https://docs.scrapy.org/en/latest/topics/broad-crawls.html
SCHEDULER_PRIORITY_QUEUE = "scrapy.pqueues.DownloaderAwarePriorityQueue"
CONCURRENT_REQUESTS = 100
REACTOR_THREADPOOL_MAXSIZE = 100
DOWNLOAD_MAXSIZE = 1048576 # Max-limit in bytes, 1 MB, 2^20 = 1,048,576 bytes
COOKIES_ENABLED = False
RETRY_ENABLED = False
REDIRECT_MAX_TIMES = 3
AJAXCRAWL_ENABLED = True
DEPTH_LIMIT = 25  # Crawling depth, default is 25
ROBOTSTXT_OBEY = False

ITEM_PIPELINES = {
    'ahmia.pipelines.CustomElasticSearchPipeline': 900,
}

DOWNLOADER_MIDDLEWARES = {
    'ahmia.middlewares.ProxyMiddleware': 100,
    'ahmia.middlewares.FilterBannedDomains': 200,
    'ahmia.middlewares.DomainLimitMiddleware': 300,
    'ahmia.middlewares.SubDomainLimit': 400,
    'ahmia.middlewares.FilterResponses': 500, # Finally, filter non-text responses
}

SEEDLIST = [
    'http://torlinkv7cft5zhegrokjrxj2st4hcimgidaxdmcmdpcrnwfxrr2zxqd.onion/',
    'http://oniondirsl37g3uwoesuwvg6nufnsnibpfo7x7ukbydtdsgdpanjxjqd.onion/',
    'http://3bbad7fauom4d6sgppalyqddsqbf5u5p56b5k5uk2zxsy3d6ey2jobad.onion/discover',
    'http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion/address/',
    'http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion/add/onionsadded/',
    'http://darkeyepxw7cuu2cppnjlgqaav6j42gyt43clcn4vjjf7llfyly5cxid.onion/',
    'http://3bbad7fauom4d6sgppalyqddsqbf5u5p56b5k5uk2zxsy3d6ey2jobad.onion/discover',
    'http://tor66sewebgixwhcqfnp5inzp5x5uohhdy3kvtnyfxc2e5mxiuh34iid.onion/fresh',
    'https://crt.sh/?q=.onion&exclude=expired&deduplicate=Y',
    'http://darkeyepxw7cuu2cppnjlgqaav6j42gyt43clcn4vjjf7llfyly5cxid.onion/',
    'http://raptora2y6r3bxmjcd3xglr3tcakc6ezq3omyzbnvwahhpi27l3w4yad.onion/'
]

for _i in range(2, 11):
    SEEDLIST.append(f"http://3bbad7fauom4d6sgppalyqddsqbf5u5p56b5k5uk2zxsy3d6ey2jobad.onion/discover?p={_i}")

BANNED_DOMAINS = []
try:
    response = requests.get('https://ahmia.fi/banned/?987654321', timeout=120)
    for md5 in response.text.split("\n"):
        md5 = md5.strip().replace(" ", "")
        if len(md5) == 32:
            BANNED_DOMAINS.append(md5)
except requests.exceptions.Timeout:
    print("\nsettings.py: Timed out fetching BANNED_DOMAINS\n")

# Tor proxy settings: http://localhost:15000 - http://localhost:15099
HTTP_PROXY_TOR_PROXIES = ["http://localhost:9055", "http://localhost:9056"]
