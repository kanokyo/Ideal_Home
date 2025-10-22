import json
import datetime
import re
import scrapy
from scrapy_playwright.page import PageMethod
from ..items import IdealhomeItem
import os
import csv
class SuumoSpider(scrapy.Spider):
    name = "suumo"
    allowed_domains = ["suumo.jp"]
    custom_settings = {
        "PLAYWRIGHT_LAUNCH_OPTIONS": {"headless": True},
        "LOG_FILE": f"suumo-{datetime.datetime.now()}.log",
    }

    start_urls = ["https://suumo.jp/chintai/tokyo/city/"]
    # 50件表示でも正確に取れる
    search_url = "https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ta=13&sc={}&pc=50"

    def __init__(self, *args, **kwargs):
        self.new = kwargs.pop('new', False)
        self.csv_path = "IdealHome/IdealHome/suumo.csv"
        self.seen_urls = set()

    def open_spider(self, spider):
        # 「新規実行」指定があれば既存URLを無視
        if not self.new and os.path.exists(self.csv_path):
            with open(self.csv_path, newline='', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get("url"):
                        self.seen_urls.add(row["url"])
            self.logger.info(f"Loaded {len(self.seen_urls)} existing URLs from CSV")
        else:
            # 新規実行のときは"get_time"から8日以上経過ているかを確認し、8日以上立っていたら再度データを取得する。その際、掲載終了していたらうんたらこうたら
            self.logger.info("New crawl: skipping CSV preload")

    async def start(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                callback=self.parse,
                meta={
                    "playwright": True,
                }
            )

    def parse(self, response, **kwargs):
        SCs = response.xpath('//table[@class="searchtable"]//input[@name="sc"]/@value').getall()
        for SC in SCs :
            yield scrapy.Request(
                url = self.search_url.format(SC),
                callback=self.parse_list,
                meta={
                    "playwright": True,
                }
            )

    def parse_list(self, response):
        property_paths = response.xpath('//a[contains(text(), "詳細を見る")]/@href').getall()
        # logger.info(f"部屋数: {len(property_paths)}")
        for property_path in property_paths:
            url = response.urljoin(property_path)
            # ここでcsvのurlを参照して同じものは弾く。
            if url in self.seen_urls:
                self.logger.info(f"Already Exists: {url}")
                continue
            yield scrapy.Request(
                url = url,
                callback=self.parse_property,
                meta={
                    "playwright": True,
                }
            )

        # 次ページへ
        next_path = response.xpath('//a[contains(text(), "次へ")]/@href').get()
        if next_path:
            yield scrapy.Request(
                url = response.urljoin(next_path),
                callback=self.parse_list,
                meta={
                    "playwright": True,
                }
            )

    def parse_property(self, response):
        self.seen_urls.add(response.url)
        building_name           = response.xpath('//*[@id="wrapper"]/div[3]/div[1]/h1/text()').get()
        rent_fee                = extract_price(response.xpath('//*[@id="js-view_gallery"]/div[1]/div[1]/div[1]/span[1]/text()').get()) # 賃料
        maintenance_fee         = extract_price(response.xpath('//*[@id="js-view_gallery"]/div[1]/div[1]/div[1]/span[2]/text()').get()) # 管理費・共益費
        deposit                 = extract_price(response.xpath('//*[@id="js-view_gallery"]/div[1]/div[1]/div[2]/span[1]/text()').get()) # 敷金
        key_money               = extract_price(response.xpath('//*[@id="js-view_gallery"]/div[1]/div[1]/div[2]/span[2]/text()').get()) # 礼金
        security_deposit        = extract_price(response.xpath('//*[@id="js-view_gallery"]/div[1]/div[1]/div[2]/span[3]/text()').get()) # 保証金
        nonrefundable_fee       = extract_price(response.xpath('//*[@id="js-view_gallery"]/div[1]/div[1]/div[2]/span[4]/text()').get()) # 敷引・償却

        imgs                    = response.xpath('//*[@id="js-view_gallery-navlist"]//img/@data-src').getall() # 画像

        address                 = response.xpath('//*[@id="js-view_gallery"]/div[3]/table/tbody/tr[1]/td/text()').get() # 所在地
        walk_time               =  ";".join([t.strip() for t in response.xpath('//*[@id="js-view_gallery"]/div[3]/table/tbody/tr[2]/td//text()').getall()]) # 駅徒歩
        layout                  = response.xpath('//*[@id="js-view_gallery"]/div[3]/table/tbody/tr[3]/td[1]/text()').get() # 間取り
        m_2                     = (response.xpath('//*[@id="js-view_gallery"]/div[3]/table/tbody/tr[3]/td[2]/text()').get() or "").replace("m", "") # 専有面積
        building_age            = extract_floor(response.xpath('//*[@id="js-view_gallery"]/div[3]/table/tbody/tr[4]/td[1]/text()').get()) # 築年数
        floor                   = extract_floor(response.xpath('//*[@id="js-view_gallery"]/div[3]/table/tbody/tr[4]/td[2]/text()').get()) # 階
        direction               = response.xpath('//*[@id="js-view_gallery"]/div[3]/table/tbody/tr[5]/td[1]/text()').get() # 向き
        building_type           = response.xpath('//*[@id="js-view_gallery"]/div[3]/table/tbody/tr[5]/td[2]/text()').get() # 建物種別

        features_equipment      = [t.strip() for t in response.xpath('//*[@id="bkdt-option"]/div/ul/li//text()').getall() if t.strip()] # 部屋の特徴・設備

        layout_detail           = response.xpath('//*[@id="contents"]/div[3]/table/tbody/tr[1]/td[1]/text()').get() # 間取り詳細
        building_structure      = response.xpath('//*[@id="contents"]/div[3]/table/tbody/tr[1]/td[2]/text()').get() # 構造
        building_floors         = response.xpath('//*[@id="contents"]/div[3]/table/tbody/tr[2]/td[1]/text()').get() # 階建
        build_date              = (response.xpath('//*[@id="contents"]/div[3]/table/tbody/tr[2]/td[2]/text()').get() or "").replace("年", "-").replace("月", "") # 築年月
        # energy_efficiency       = response.xpath('//*[@id="contents"]/div[3]/table/tbody/tr[3]/td[1]/text()').get() # エネルギー消費性能
        # insulation_performance  = response.xpath('//*[@id="contents"]/div[3]/table/tbody/tr[3]/td[2]/text()').get() # 断熱性能
        # estimated_utility_cost  = "".join(response.xpath('//*[@id="contents"]/div[3]/table/tbody/tr[4]/td//text()').getall()) # 目安光熱費
        insurance_required      = response.xpath('//*[@id="contents"]/div[3]/table/tbody/tr[5]/td[1]/text()').get() # 損保
        parking                 = response.xpath('//*[@id="contents"]/div[3]/table/tbody/tr[5]/td[2]/text()').get() # 駐車場
        move_in_date            = response.xpath('//*[@id="contents"]/div[3]/table/tbody/tr[6]/td[1]/text()').get() # 入居
        transaction_type        = response.xpath('//*[@id="contents"]/div[3]/table/tbody/tr[6]/td[2]/text()').get() # 取引態様
        rental_conditions       = response.xpath('//*[@id="contents"]/div[3]/table/tbody/tr[7]/td[1]/text()').get() # 条件
        agency_code             = response.xpath('//*[@id="contents"]/div[3]/table/tbody/tr[7]/td[2]/text()').get() # 取り扱い店舗物件コード
        suumo_code              = response.xpath('//*[@id="contents"]/div[3]/table/tbody/tr[8]/td[1]/text()').get() # SUUMO物件コード
        total_units             = response.xpath('//*[@id="contents"]/div[3]/table/tbody/tr[8]/td[2]/text()').get() # 総戸数
        label                   = response.xpath('//*[@id="contents"]/div[3]/table/tbody/tr[10]/th/text()').get()

        if label and "契約期間" in label:
            contract_period     =  ";".join(response.xpath('//*[@id="contents"]/div[3]/table/tbody/tr[10]/td/ul//text()').getall()) # 契約期間
        else:
            contract_period     = ""
        label                   = response.xpath('//*[@id="contents"]/div[3]/table/tbody/tr[11]/th/text()').get()
        if label and "その他初期費用" in label:
            match               = re.search(r'内訳：(.+?)）', "".join(response.xpath('//*[@id="contents"]/div[3]/table/tbody/tr[11]/td/ul//text()').getall()))
        else:
            match               = re.search(r'内訳：(.+?)）', "".join(response.xpath('//*[@id="contents"]/div[3]/table/tbody/tr[12]/td/ul//text()').getall()))
        initial_costs           = match.group(1) if match else "" # その他初期費用

        item = IdealhomeItem()

        item["url"] = response.url
        item["get_time"] = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).isoformat()
        item["building_name"] = building_name
        item["rent_fee"] = rent_fee
        item["maintenance_fee"] = maintenance_fee
        item["deposit"] = deposit
        item["key_money"] = key_money
        item["security_deposit"] = security_deposit
        item["nonrefundable_fee"] = nonrefundable_fee
        item["imgs"] = json.dumps(imgs, ensure_ascii=False)
        item["address"] = address
        item["walk_time"] = walk_time
        item["layout"] = layout
        item["m_2"] = m_2
        item["building_age"] = building_age
        item["floor"] = floor
        item["direction"] = direction
        item["building_type"] = building_type
        item["features_equipment"] = features_equipment
        item["layout_detail"] = layout_detail
        item["building_structure"] = building_structure
        item["building_floors"] = building_floors
        item["build_date"] = build_date
        # item["energy_efficiency"] = energy_efficiency
        # item["insulation_performance"] = insulation_performance
        # item["estimated_utility_cost"] = estimated_utility_cost
        item["insurance_required"] = insurance_required
        item["parking"] = parking
        item["move_in_date"] = move_in_date
        item["transaction_type"] = transaction_type
        item["rental_conditions"] = rental_conditions
        item["agency_code"] = agency_code
        item["suumo_code"] = suumo_code
        item["total_units"] = total_units
        item["contract_period"] = contract_period
        item["initial_costs"] = initial_costs

        for key, value in item.items():
            if isinstance(value, str):
                item[key] = clean_text(value)

        yield item

def extract_floor(text: str):
    if not text:
        return None

    nums = re.findall(r'\d+', text)
    if "新築" in text:
        return 0
    if not nums:
        return None

    # 地下ならマイナス化
    if "地下" in text:
        current = -int(nums[0])
    else:
        current = int(nums[0])

    return current

def extract_price(text: str):
    if not text or text.strip() == '-' or text.strip() == '―':
        return None

    # すべての数値を抽出（例: ['1.5', '2.3']）
    nums = re.findall(r'\d+(?:\.\d+)?', text)
    if not nums:
        return None

    if "万" in text:
        return int(float(nums[0]) * 10000)
    else:
        return int(float(nums[0]))

import re

def clean_text(text: str):
    """
    文字列の前後・内部の不要な空白や改行を削除して正規化する関数
    """
    if not text:
        return ""

    # 全角→半角スペース、ノーブレークスペース削除
    text = text.replace("\u3000", " ").replace("\xa0", " ")

    # 改行・タブをスペースに統一
    text = re.sub(r"[\r\n\t]+", " ", text)

    # 連続スペースを1つに
    text = re.sub(r"\s{2,}", " ", text)

    return text.strip()
