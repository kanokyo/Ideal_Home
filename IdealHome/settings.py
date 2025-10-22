# Scrapy settings for IdealHome project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "IdealHome"

SPIDER_MODULES = ["IdealHome.spiders"]
NEWSPIDER_MODULE = "IdealHome.spiders"

ADDONS = {}


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Concurrency and throttling settings
CONCURRENT_REQUESTS = 100
CONCURRENT_REQUESTS_PER_DOMAIN = 100
DOWNLOAD_DELAY = 1

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
   "Accept-Language": "ja",
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "IdealHome.middlewares.IdealhomeSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "IdealHome.middlewares.IdealhomeDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    "IdealHome.pipelines.IdealhomePipeline": 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 10
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = "httpcache"
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value

# HTTP と HTTPS のダウンロードハンドラーを指定する
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

# Playwright 設定を有効にする
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

# Playwright 設定（オプション）
PLAYWRIGHT_BROWSER_TYPE = 'chromium'

# PLAYWRIGHT_LAUNCH_OPTIONS = {
#     'headless': True,
# }

# ログ
LOG_LEVEL = "INFO"
LOG_STDOUT = True

FEEDS = {
    'suumo.csv': {
        'format': 'csv',
        'encoding': 'utf-8-sig',
        'store_empty': False,
        'overwrite': False,
        'append': True,
        'item_export_kwargs': {
            'include_headers_line': False
        },
        'fields': [
            "url","get_time","building_name",
            "rent_fee","maintenance_fee","deposit","key_money",
            "security_deposit","nonrefundable_fee","imgs",
            "address","walk_time","layout","m_2","building_age",
            "floor","direction","building_type",
            "features_equipment","layout_detail","building_structure",
            "building_floors","build_date","insurance_required",
            "parking","move_in_date","transaction_type","rental_conditions",
            "agency_code","suumo_code","total_units","contract_period","initial_costs",
        ],
    },
}

FEED_EXPORT_ENCODING = "utf-8-sig"

FEED_FORMAT='csv'
FEED_EXPORT_FIELDS = [
    # --- メタ情報 ---
    "url",
    "get_time",

    # --- 基本情報 ---
    "building_name",

    # --- 金額情報 ---
    "rent_fee",
    "maintenance_fee",
    "deposit",
    "key_money",
    "security_deposit",
    "nonrefundable_fee",

    # --- 画像 ---
    "imgs",

    # --- 立地・概要 ---
    "address",
    "walk_time",
    "layout",
    "m_2",
    "building_age",
    "floor",
    "direction",
    "building_type",

    # --- 詳細情報 ---
    "features_equipment",
    "layout_detail",
    "building_structure",
    "building_floors",
    "build_date",
    # "energy_efficiency",
    # "insulation_performance",
    # "estimated_utility_cost",
    "insurance_required",
    "parking",
    "move_in_date",
    "transaction_type",
    "rental_conditions",
    "agency_code",
    "suumo_code",
    "total_units",
    "contract_period",
    "initial_costs",
]