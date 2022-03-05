import pprint
import pandas as pd
from sqlalchemy import column

# 作りたいデータ
# 1. 名称 (Not Null)
# 2. 住所・所在地 (Not Null)
# 3. 電話番号
# 4. 緯度
# 5. 経度
# 6. 種別


class 観光データを洗浄:
    def __init__(self, df):
        self.df = df

    def データを洗浄する(self):
        export_df = self.df
        export_df = self.カラム名を名称に統一する(export_df)
        export_df = self.カラム名を住所に統一する(export_df)
        export_df = self.カラム名を電話番号に統一する(export_df)
        export_df = self.カラム名を種別に統一する(export_df)
        return export_df

    def カラム名を名称に統一する(self, df):
        # 対象カラム
        # 1. 名称
        # 2. 観光スポット名称
        # 3. 店舗名
        # 4. いずれもなかったら削除
        # カラム名：名称
        export_df = df
        export_df = self.観光スポット名称を名称に統一する(df)
        export_df = self.店舗名を名称に統一する(df)
        export_df = self.データが存在しない行を削除する(df, "名称")
        return export_df

    def カラム名を住所に統一する(self, df):
        # 対象カラム
        # 1. 住所
        # 2. 所在地
        # 3. 住所（何区か不明）
        # 4. 住所（東京都品川区が都道府県名・市区町村名と分離していて、住所の頭についていない）
        # 5. 所在地（三鷹市から始まっている）
        # 6. 住所（狛江市から始まっている）
        # 7. 住所（江東区から始まっている）
        # 8. 東京都町田市所在地
        # いずれもなかったら削除
        # カラム名：住所
        export_df = df
        export_df = self.三鷹市から始まる所在地に東京都を付加して住所に統一する(df)
        export_df = self.都道府県名と市区町村名にある東京都品川区を住所の前方に結合する(df)
        export_df = self.東京都町田市所在地を住所に統一する(df)
        export_df = self.江東区から始まる住所に東京都を付加する(df)
        export_df = self.都道府県名と市区町村名が空欄のものに東京都板橋区を追加する(df)
        export_df = self.データが存在しない行を削除する(df, "住所")
        return export_df

    def カラム名を電話番号に統一する(self, df):
        # 対象カラム
        # 1. 電話番号
        # 2. 連絡先電話番号
        # 3. 連絡先電話番号(市外局番が（）で囲まれているものが一部ある)
        # 4. 電話番号（後ろに内線とか余計なものついてる）
        # カラム名: 電話番号
        export_df = df
        export_df = self.連絡先電話番号を電話番号に統一する(df)
        #export_df = self.市外局番の表記揺れを修正する(df)
        #export_df = self.電話番号の余計な内線を消す(df)
        return export_df

    def カラム名を種別に統一する(self, df):
        ## 対象カラム
        ## 1. 種別
        ## 2. カテゴリ
        ## 3. 大分類_
        ## 4. 文化財分類・種類
        ## 5. 業種
        ## カラム名：種別
        export_df = df
        export_df = self.カテゴリを種別に統一する(df)
        export_df = self.大分類_を種別に統一する(df)
        export_df = self.文化財分類を種別に統一する(df)
        export_df = self.業種を種別に統一する(df)
        return export_df

    def 観光スポット名称を名称に統一する(self, df):
        export_df = df
        export_df.loc[export_df["名称"].isnull() & export_df["観光スポット名称"].notnull(), "名称"] = export_df["観光スポット名称"]
        return export_df

    def 店舗名を名称に統一する(self, df):
        export_df = df
        export_df.loc[export_df["名称"].isnull() & export_df["店舗名"].notnull(), "名称"] = export_df["店舗名"]
        return export_df

    def データが存在しない行を削除する(self, df, column_name):
        export_df = df
        export_df = export_df[export_df[column_name].notnull()]
        return export_df

    def 三鷹市から始まる所在地に東京都を付加して住所に統一する(self, df):
        export_df = df.copy()
        replace = lambda 所在地: "東京都" + str(所在地)
        export_df.loc[
            (export_df["住所"].isnull()) &
            (export_df["所在地"].notnull()) &
            (export_df["所在地"].str.startswith("三鷹市"))
            , "住所"] = export_df["所在地"].map(replace)
        return export_df

    def 都道府県名と市区町村名にある東京都品川区を住所の前方に結合する(self, df):
        export_df = df
        replace = lambda 住所: '東京都品川区' + str(住所)
        export_df.loc[
            (export_df["住所"].notnull()) &
            (export_df["都道府県名"] == "東京都") &
            (export_df["市区町村名"] == "品川区")
            , "住所"
        ] = export_df["住所"].map(replace)
        return export_df

    def 東京都町田市所在地を住所に統一する(self, df):
        export_df = df
        export_df.loc[
            (export_df["住所"].isnull()) &
            (export_df["東京都町田市所在地"].notnull())
            ,"住所"
        ] = export_df["東京都町田市所在地"]
        return export_df

    def 江東区から始まる住所に東京都を付加する(self, df):
        export_df = df
        replace = lambda 住所: '東京都' + str(住所)
        export_df.loc[
            (export_df["住所"].notnull()) &
            (export_df["住所"].str.startswith("江東区"))
            ,"住所"
        ] = export_df["住所"].map(replace)
        return export_df

    def 都道府県名と市区町村名が空欄のものに東京都板橋区を追加する(self, df):
        export_df = df
        replace = lambda 住所: '東京都板橋区' + str(住所)
        export_df.loc[
            (export_df["住所"].notnull()) &
            (export_df["都道府県名"].isnull()) &
            (export_df["市区町村名"].isnull()) &
            ~export_df["住所"].str.startswith("東京都", na=False)
            ,"住所"
        ] = export_df["住所"].map(replace)
        return export_df

    def 連絡先電話番号を電話番号に統一する(self, df):
        export_df = df
        export_df.loc[
            (export_df["電話番号"].isnull()) &
            (export_df["連絡先電話番号"].notnull())
            ,"電話番号"
        ] = export_df["連絡先電話番号"]
        return export_df

    #def 市外局番の表記揺れを修正する(self, df):
        #export_df = df
        #return export_df

    #def 電話番号の余計な内線を消す(self, df):
        #export_df = df
        #return export_df

    def カテゴリを種別に統一する(self, df):
        export_df = df
        export_df.loc[
            (export_df["種別"].isnull()) &
            (export_df["カテゴリ"].notnull())
            ,"種別"
        ] = export_df["カテゴリ"]
        return export_df

    def 大分類_を種別に統一する(self, df):
        export_df = df
        export_df.loc[
            (export_df["種別"].isnull()) &
            (export_df["大分類__"].notnull())
            ,"種別"
        ] = export_df["大分類__"]
        return export_df

    def 文化財分類を種別に統一する(self, df):
        export_df = df
        export_df.loc[
            (export_df["種別"].isnull()) &
            (export_df["文化財分類"].notnull())
            ,"種別"
        ] = export_df["文化財分類"]
        return export_df

    def 業種を種別に統一する(self, df):
        export_df = df
        export_df.loc[
            (export_df["種別"].isnull()) &
            (export_df["業種"].notnull())
            ,"種別"
        ] = export_df["業種"]
        return export_df

def execute():
    df = pd.read_csv("downloaded_merged.csv").dropna(how='all')
    purifier = 観光データを洗浄(df)
    purified_df = purifier.データを洗浄する()
    purified_df = purified_df[["名称", "住所", "電話番号", "緯度", "経度", "種別"]]
    purified_df.to_csv("result.csv")

execute()