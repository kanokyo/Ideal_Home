# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class IdealhomeItem(scrapy.Item):
    url = scrapy.Field()
    get_time = scrapy.Field()
    # --- 基本情報 ---
    building_name = scrapy.Field()              # 建物名

    # --- 金額情報 ---
    rent_fee = scrapy.Field()                   # 賃料
    maintenance_fee = scrapy.Field()            # 管理費・共益費
    deposit = scrapy.Field()                    # 敷金
    key_money = scrapy.Field()                  # 礼金
    security_deposit = scrapy.Field()           # 保証金
    nonrefundable_fee = scrapy.Field()          # 敷引・償却

    # --- 画像 ---
    imgs = scrapy.Field()                       # 画像URLリスト

    # --- 立地・概要 ---
    address = scrapy.Field()                    # 所在地
    walk_time = scrapy.Field()                  # 駅徒歩
    layout = scrapy.Field()                     # 間取り
    m_2 = scrapy.Field()                        # 専有面積
    building_age = scrapy.Field()               # 築年数
    floor = scrapy.Field()                      # 階
    direction = scrapy.Field()                  # 向き
    building_type = scrapy.Field()              # 建物種別

    # --- 詳細情報 ---
    features_equipment = scrapy.Field()         # 部屋の特徴・設備
    layout_detail = scrapy.Field()              # 間取り詳細
    building_structure = scrapy.Field()         # 構造
    building_floors = scrapy.Field()            # 階建
    build_date = scrapy.Field()                 # 築年月
    # energy_efficiency = scrapy.Field()          # エネルギー消費性能
    # insulation_performance = scrapy.Field()     # 断熱性能
    # estimated_utility_cost = scrapy.Field()     # 目安光熱費
    insurance_required = scrapy.Field()         # 損保
    parking = scrapy.Field()                    # 駐車場
    move_in_date = scrapy.Field()               # 入居
    transaction_type = scrapy.Field()           # 取引態様
    rental_conditions = scrapy.Field()          # 条件
    agency_code = scrapy.Field()                # 取り扱い店舗物件コード
    suumo_code = scrapy.Field()                 # SUUMO物件コード
    total_units = scrapy.Field()                # 総戸数
    contract_period = scrapy.Field()            # 契約期間
    initial_costs = scrapy.Field()              # その他初期費用
