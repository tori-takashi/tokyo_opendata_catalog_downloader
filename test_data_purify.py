import pandas as pd
from pandas.testing import assert_frame_equal

from data_purify import 観光データを洗浄

def test_カラム名を名称に統一する():
    before = [
    {"名称": "test1", "観光スポット名称": None, "店舗名": None, "余計なカラム": "A"},
    {"名称": None, "観光スポット名称": "test2", "店舗名": None, "余計なカラム": "B"},
    {"名称": None, "観光スポット名称": None, "店舗名": "test3", "余計なカラム": "C"},
    {"名称": None, "観光スポット名称": None, "店舗名": None, "余計なカラム": "D"},
    ]

    expected = [
    {"名称": "test1", "観光スポット名称": None, "店舗名": None, "余計なカラム": "A"},
    {"名称": "test2", "観光スポット名称": "test2", "店舗名": None, "余計なカラム": "B"},
    {"名称": "test3", "観光スポット名称": None, "店舗名": "test3", "余計なカラム": "C"},
    ]

    before_df = pd.DataFrame(before)
    expected_df = pd.DataFrame(expected)
    purifier = 観光データを洗浄(before_df)

    result = purifier.カラム名を名称に統一する(before_df)

    assert_frame_equal(expected_df, result)


def test_観光スポット名を名称に統一する():
    before = [
    {"名称": None, "観光スポット名称": "test1"},
    {"名称": "test2", "観光スポット名称": None}]
    
    expected = [
    {"名称": "test1", "観光スポット名称": "test1"},
    {"名称": "test2", "観光スポット名称": None}]

    before_df = pd.DataFrame(before)
    expected_df = pd.DataFrame(expected)
    purifier = 観光データを洗浄(before_df)

    result = purifier.観光スポット名称を名称に統一する(before_df)

    assert_frame_equal(expected_df, result)
    
def test_店舗名を名称に統一する():
    before = [
    {"名称": None, "店舗名": "test1"},
    {"名称": "test2", "店舗名": None}]
    
    expected = [
    {"名称": "test1", "店舗名": "test1"},
    {"名称": "test2", "店舗名": None}]

    before_df = pd.DataFrame(before)
    expected = pd.DataFrame(expected)
    purifier = 観光データを洗浄(before_df)

    result = purifier.店舗名を名称に統一する(before_df)

    assert_frame_equal(result, expected)

def test_データが存在しない行を削除する():
    before = [
    {"名称": "test1", "店舗名": None, "観光スポット名称": None},
    {"名称": None, "店舗名": None, "観光スポット名称": None}
    ]

    expected = [
    {"名称": "test1", "店舗名": None, "観光スポット名称": None}]

    before_df = pd.DataFrame(before)
    expected = pd.DataFrame(expected)
    purifier = 観光データを洗浄(before_df)

    result = purifier.データが存在しない行を削除する(before_df, "名称")

    assert_frame_equal(result, expected)

def test_三鷹市から始まる所在地に東京都を付加して住所に統一する():
    before = [
    {"住所": None, "所在地": "三鷹市test1"},
    {"住所": "東京都ああああ区", "所在地": None},
    {"住所": None, "所在地": "東京都いいいい区"},
    ]

    expected = [
    {"住所": "東京都三鷹市test1", "所在地": "三鷹市test1"},
    {"住所": "東京都ああああ区", "所在地": None},
    {"住所": None, "所在地": "東京都いいいい区"},
    ]

    before_df = pd.DataFrame(before)
    expected = pd.DataFrame(expected)
    purifier = 観光データを洗浄(before_df)

    result = purifier.三鷹市から始まる所在地に東京都を付加して住所に統一する(before_df)

    assert_frame_equal(result, expected)

def test_都道府県名と市区町村名にある東京都品川区を住所の前方に結合する():
    before = [
    {"住所": "test1", "都道府県名": "東京都", "市区町村名": "品川区"},
    {"住所": "江東区test1", "都道府県名": "東京都", "市区町村名": "江東区"}
    ]

    expected = [
    {"住所": "東京都品川区test1", "都道府県名": "東京都", "市区町村名": "品川区"},
    {"住所": "江東区test1", "都道府県名": "東京都", "市区町村名": "江東区"}
    ]

    before_df = pd.DataFrame(before)
    expected = pd.DataFrame(expected)
    purifier = 観光データを洗浄(before_df)

    result = purifier.都道府県名と市区町村名にある東京都品川区を住所の前方に結合する(before_df)

    assert_frame_equal(result, expected)

def test_東京都町田市所在地を住所に統一する():
    before = [
    {"住所": None, "東京都町田市所在地": "東京都町田市test1"},
    {"住所": "test2", "東京都町田市所在地": None},
    ]

    expected = [
    {"住所": "東京都町田市test1", "東京都町田市所在地": "東京都町田市test1"},
    {"住所": "test2", "東京都町田市所在地": None},
    ]

    before_df = pd.DataFrame(before)
    expected = pd.DataFrame(expected)
    purifier = 観光データを洗浄(before_df)

    result = purifier.東京都町田市所在地を住所に統一する(before_df)

    assert_frame_equal(result, expected)

def test_江東区から始まる住所に東京都を付加する():
    before = [
    {"住所": "江東区test1"},
    {"住所": "東京都品川区test2"},
    ]

    expected = [
    {"住所": "東京都江東区test1"},
    {"住所": "東京都品川区test2"},
    ]

    before_df = pd.DataFrame(before)
    expected = pd.DataFrame(expected)
    purifier = 観光データを洗浄(before_df)

    result = purifier.江東区から始まる住所に東京都を付加する(before_df)

    assert_frame_equal(result, expected)

def test_都道府県名と市区町村名が空欄のものに東京都板橋区を追加する():
    before = [
    {"住所": "test1", "都道府県名": None, "市区町村名": None},
    {"住所": "東京都test2", "都道府県名": None, "市区町村名": None},
    ]

    expected = [
    {"住所": "東京都板橋区test1", "都道府県名": None, "市区町村名": None},
    {"住所": "東京都test2", "都道府県名": None, "市区町村名": None},
    ]

    before_df = pd.DataFrame(before)
    expected = pd.DataFrame(expected)
    purifier = 観光データを洗浄(before_df)

    result = purifier.都道府県名と市区町村名が空欄のものに東京都板橋区を追加する(before_df)

    assert_frame_equal(result, expected)

def test_連絡先電話番号を電話番号に統一する():
    before = [
    {"電話番号": None, "連絡先電話番号": "03-1111-1111"},
    {"電話番号": "03-2222-2222", "連絡先電話番号": None}
    ]

    expected = [
    {"電話番号": "03-1111-1111", "連絡先電話番号": "03-1111-1111"},
    {"電話番号": "03-2222-2222", "連絡先電話番号": None}
    ]

    before_df = pd.DataFrame(before)
    expected = pd.DataFrame(expected)
    purifier = 観光データを洗浄(before_df)

    result = purifier.連絡先電話番号を電話番号に統一する(before_df)

    assert_frame_equal(result, expected)

def test_カテゴリを種別に統一する():
    before = [
    {"種別": None, "カテゴリ": "test1"},
    {"種別": "test2", "カテゴリ": None},
    ]

    expected = [
    {"種別": "test1", "カテゴリ": "test1"},
    {"種別": "test2", "カテゴリ": None},
    ]

    before_df = pd.DataFrame(before)
    expected = pd.DataFrame(expected)
    purifier = 観光データを洗浄(before_df)

    result = purifier.カテゴリを種別に統一する(before_df)

    assert_frame_equal(result, expected)

def test_大分類_を種別に統一する():
    before = [
    {"種別": None, "大分類__": "test1"},
    {"種別": "test2", "大分類__": None},
    ]

    expected = [
    {"種別": "test1", "大分類__": "test1"},
    {"種別": "test2", "大分類__": None},
    ]

    before_df = pd.DataFrame(before)
    expected = pd.DataFrame(expected)
    purifier = 観光データを洗浄(before_df)

    result = purifier.大分類_を種別に統一する(before_df)

    assert_frame_equal(result, expected)

def test_文化財分類を種別に統一する():
    before = [
    {"種別": None, "文化財分類": "文化財1", "種類": "種類1"},
    {"種別": "test2", "文化財分類": None, "種類": None},
    ]

    expected = [
    {"種別": "文化財1", "文化財分類": "文化財1", "種類": "種類1"},
    {"種別": "test2", "文化財分類": None, "種類": None},
    ]

    before_df = pd.DataFrame(before)
    expected = pd.DataFrame(expected)
    purifier = 観光データを洗浄(before_df)

    result = purifier.文化財分類を種別に統一する(before_df)

    assert_frame_equal(result, expected)

def test_業種を種別に統一する():
    before = [
    {"種別": None, "業種": "test1"},
    {"種別": "test2", "業種": None},
    ]

    expected = [
    {"種別": "test1", "業種": "test1"},
    {"種別": "test2", "業種": None},
    ]

    before_df = pd.DataFrame(before)
    expected = pd.DataFrame(expected)
    purifier = 観光データを洗浄(before_df)

    result = purifier.業種を種別に統一する(before_df)

    assert_frame_equal(result, expected)