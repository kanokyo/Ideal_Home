# import datetime
# import scrapy
# from scrapy_playwright.page import PageMethod
# from ..items import IdealhomeItem

# class SuumoSpider(scrapy.Spider):
#     name = "suumo"
#     allowed_domains = ["suumo.jp"]
#     custom_settings = {
#         "PLAYWRIGHT_LAUNCH_OPTIONS": {"headless": False},
#         "LOG_FILE": "debug.log",
#     }
#     # 東京都全域, 表示件数50件, 新着順
#     start_urls = ["https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ta=13&sc=13101&sc=13102&sc=13103&sc=13104&sc=13105&sc=13113&sc=13106&sc=13107&sc=13108&sc=13118&sc=13121&sc=13122&sc=13123&sc=13109&sc=13110&sc=13111&sc=13112&sc=13114&sc=13115&sc=13120&sc=13116&sc=13117&sc=13119&sc=13201&sc=13202&sc=13203&sc=13204&sc=13205&sc=13206&sc=13207&sc=13208&sc=13209&sc=13210&sc=13211&sc=13212&sc=13213&sc=13214&sc=13215&sc=13218&sc=13219&sc=13220&sc=13221&sc=13222&sc=13223&sc=13224&sc=13225&sc=13227&sc=13228&sc=13229&sc=13300&cb=0.0&ct=9999999&mb=0&mt=9999999&et=9999999&cn=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&sngz=&po1=09&pc=50"]

#     async def start(self):
#         for url in self.start_urls:
#             yield scrapy.Request(
#                 url,
#                 callback=self.parse,
#                 meta={
#                     "playwright": True,
#                     "playwright_page_methods": [
#                         PageMethod("wait_for_load_state", "networkidle"),
#                         PageMethod("wait_for_selector", "#js-bukkenList li", timeout=15000),
#                     ],
#                 }
#             )

#     def parse(self, response):
#         # 物件はul[1]/li[1]からスタートしてli[5]になったら次はul[2]/li[1]から始まる。
#         ul = 1
#         for li in range(1, 5):
#             apartment_name = response.xpath(f'//*[@id="js-bukkenList"]/ul{ul}/li{li}/div/div[1]/div[2]/div/div[2]/text()').get()
#             rooms = len(response.xpath(f'//*[@id="js-bukkenList"]/ul{ul}/li{li}/div/div[2]/table/tbody'))

#             # 物件ごとの部屋をとる(tbodyは1スタート)
#             for room in range(1, rooms+1):
#                 # 階だけ取得
#                 floor = response.xpath(f'//*[@id="js-bukkenList"]/ul{ul}/li{li}/div/div[2]/table/tbody[{room}]/tr/td[3]/text()').get()
#                 url = response.xpath(f'//*[@id="js-bukkenList"]/ul{ul}/li{li}/div/div[2]/table/tbody[{room}]/tr/td[9]/a/@href').get()
#                 yield IdealhomeItem(
#                     create_at = datetime.datetime.now(),
#                     apartment_name = apartment_name.strip(),
#                     floor = floor.strip(),
#                     url = url,
#                 )
#                 print(apartment_name, floor, url)

#                 if li == 5:
#                     li = 1
#                     ul += 1

# suumo.py
import datetime
import scrapy
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
from scrapy_playwright.page import PageMethod
from ..items import IdealhomeItem

# 単発最適化：帯域を食うリソースはブロック
BLOCK_TYPES = {"image", "media", "font", "stylesheet"}

def set_qs(url: str, **params) -> str:
    """URLのクエリ文字列を安全に上書き（既存パラメータは維持）。"""
    p = urlparse(url)
    q = dict(parse_qsl(p.query, keep_blank_values=True))
    q.update({k: str(v) for k, v in params.items() if v is not None})
    return urlunparse((p.scheme, p.netloc, p.path, p.params, urlencode(q, doseq=True), p.fragment))

class SuumoSpider(scrapy.Spider):
    name = "suumo"
    allowed_domains = ["suumo.jp"]

    # 並列の“ウィンドウ幅”。settings.py で SUUMO_PREFETCH を指定可（未指定は 4）
    prefetch_default = 4

    # scrapy-playwright==0.0.44 を想定：Middleware なし / Handler のみ
    custom_settings = {
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
        "PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT": 60000,
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        "FEED_EXPORT_ENCODING": "utf-8-sig",
        "FEED_EXPORT_FIELDS": ["create_at", "apartment_name", "floor", "url"],
        # 実際の並列数・ディレイ等は settings.py 側で調整OK
    }

    start_urls = [
        "https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ta=13&sc=13101&sc=13102&sc=13103&sc=13104&sc=13105&sc=13113&sc=13106&sc=13107&sc=13108&sc=13118&sc=13121&sc=13122&sc=13123&sc=13109&sc=13110&sc=13111&sc=13112&sc=13114&sc=13115&sc=13120&sc=13116&sc=13117&sc=13119&sc=13201&sc=13202&sc=13203&sc=13204&sc=13205&sc=13206&sc=13207&sc=13208&sc=13209&sc=13210&sc=13211&sc=13212&sc=13213&sc=13214&sc=13215&sc=13218&sc=13219&sc=13220&sc=13221&sc=13222&sc=13223&sc=13224&sc=13225&sc=13227&sc=13228&sc=13229&sc=13300&cb=0.0&ct=9999999&mb=0&mt=9999999&et=9999999&cn=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&sngz=&po1=09&pc=50&page=1"
    ]

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        spider.prefetch = int(crawler.settings.getint("SUUMO_PREFETCH", cls.prefetch_default))
        return spider

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.seen_urls: set[str] = set()
        self._stop = False
        self._next_to_schedule = 1  # 次に投入する page 番号（1 始まり）

    # ── Playwright 用 meta（単発最適化：body待ち＋リソースブロック） ──
    def _meta_for_request(self):
        return {
            "playwright": True,
            "playwright_context_kwargs": {
                "locale": "ja-JP",
                "user_agent": self.settings.get("USER_AGENT"),
            },
            "playwright_page_methods": [
                PageMethod(
                    "route", "**/*",
                    lambda route: route.abort()
                    if route.request.resource_type in BLOCK_TYPES
                    else route.continue_()
                ),
                # エラーページでも確実に返る "body" を待つ（networkidle は使わない）
                PageMethod("wait_for_selector", "body", timeout=45000),
            ],
        }

    # ── Request を作る共通関数 ──
    def _make_req(self, base_url: str, page: int):
        url = set_qs(base_url, page=page)
        return scrapy.Request(
            url,
            callback=self.parse_list,
            cb_kwargs={"page": page},
            meta=self._meta_for_request(),
            dont_filter=False,      # URLは毎回異なる
            priority=page,          # 低いページを先に
        )

    # ── 最初に prefetch 分だけ投入 ──
    async def start(self):
        base = self.start_urls[0]
        for p in range(1, self.prefetch + 1):
            yield self._make_req(base, p)
        self._next_to_schedule = self.prefetch + 1

    # ── 1ページ処理 → 次ページを“1つだけ”追加投入（スライディングウィンドウ） ──
    def parse_list(self, response: scrapy.http.Response, page: int):
        # 1) 存在しないページの判定（あなた指定の文言）
        err_text = response.xpath(
            'normalize-space(//*[@id="js-errorcontents"]/div[3]/div/div/div/div[2]/div/p[1]/text())'
        ).get()
        if err_text == "ページを表示できませんでした。":
            self._stop = True
            self.logger.info(f"[END] non-existent page reached: page={page} url={response.url}")
            return

        # 2) 通常ページの抽出（PR/広告を避け、rent系に限定）
        cards = response.xpath(
            "//*[@id='js-bukkenList']"
            "//div[contains(@class,'cassetteitem') and contains(@class,'cassetteitem--rent')]"
        )
        self.logger.info(f"[LIST] page={page} cards={len(cards)}")

        for card in cards:
            # 物件名（div/h2 両対応、normalize-space）
            name = card.xpath(
                "normalize-space((.//div[contains(@class,'cassetteitem_content-title')]"
                " | .//h2[contains(@class,'cassetteitem_content-title')])[1])"
            ).get()
            if not name:
                # apartment_name を必須扱いに（スパイダ段階で弾く）
                continue

            # 部屋：リンクがある tbody のみ
            for row in card.xpath(".//table/tbody[.//td[9]//a/@href]"):
                floor = (row.xpath("./tr/td[3]/text()").get() or "").strip()
                href  = row.xpath(".//td[9]//a[contains(@class,'js-cassette_link')]/@href").get() \
                        or row.xpath(".//td[9]//a[1]/@href").get()
                if not href:
                    continue
                detail = response.urljoin(href)

                # URL重複ガード（必要なら (detail, floor) に変更）
                if detail in self.seen_urls:
                    continue
                self.seen_urls.add(detail)

                yield IdealhomeItem(
                    create_at=datetime.datetime.utcnow().isoformat(),
                    apartment_name=name,
                    floor=floor,
                    url=detail,
                )

        # 3) 次ページを“1つだけ”追加投入（ウィンドウ幅を維持）
        if not self._stop:
            next_page = self._next_to_schedule
            self._next_to_schedule += 1
            yield self._make_req(self.start_urls[0], next_page)
