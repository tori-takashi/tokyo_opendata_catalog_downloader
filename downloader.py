import pandas as pd
import lxml.html
import requests
import io

class TokyoOpenDataCatalogDownloader:
    def __init__(self, urls_csv_name: str, export_file_name: str):
        self.export_file_name = export_file_name
        self.download_targets = pd.read_csv(urls_csv_name).URL.tolist()
        self.download_target_urls = set()

    def generate_csv(self):
        download_target_urls = self.generate_download_target_urls()
        df = self.download_csvs_dataframes(download_target_urls)
        print(df)
        df.to_csv(self.export_file_name)

    def download_csvs_dataframes(self, download_target_urls: set):
        df_list = []
        for csv_url in download_target_urls:
            df = self.download_df_from_csv(csv_url)
            if (df is not None):
                df_list.append(df)
                print(df)
        print(df_list)

        return pd.concat(df_list)

    def download_df_from_csv(self, csv_url):
        res = requests.get(csv_url)
        res.encoding = res.apparent_encoding
        if (res.status_code == 200):
            return pd.read_csv(io.StringIO(res.text))

    def download_html(self, url: str):
        html_text = requests.get(url).text
        return lxml.html.fromstring(html_text)

    def get_resource_items(self, html):
        resource_url_path = "//a[@class='resource-url-analytics']"
        resource_items = html.xpath(resource_url_path)
        return resource_items

    def generate_download_target_urls(self):
        download_target_urls = set()

        for download_target in self.download_targets:
            html = self.download_html(download_target)
            resource_items = self.get_resource_items(html)
            print("Loading: " + download_target)
            for resource_item in resource_items:
                target_url = resource_item.get("href")
                if (target_url[-4:] == ".csv"):
                    download_target_urls.add(target_url)

        return download_target_urls

downloader = TokyoOpenDataCatalogDownloader("target_real.csv", "downloaded_merged.csv")
downloader.generate_csv()