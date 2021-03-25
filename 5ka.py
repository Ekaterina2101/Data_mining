import time
import json
from pathlib import Path
import requests


class Parse5ka:
    params = {
        "records_per_page": 20,
    }

    def __init__(self, start_url: str, result_path: Path):
        self.start_url = start_url
        self.result_path = result_path

    def _get_response(self, url):
        while True:
            response = requests.get(url)
            if response.status_code == 200:
                return response
            time.sleep(1)

    def run(self):
        for product in self._parse(self.start_url):
            self._save(product)

    def _parse(self, url):
        while url:
            response = self._get_response(url, params=self.params)
            data = response.json()
            url = data.get("next")
            for product in data.get("results", []):
                yield product

    def _save(self, data):
        file_path = self.result_path.joinpath(f'{data["id"]}.json')
        file_path.write_text(json.dumps(data, ensure_ascii=False))


class Categories(Parse5ka):
    def __init__(self, cat_url, *args, **kwargs):
        self.cat_url = cat_url
        super().__init__(*args, **kwargs)

    def _get_categories(self):
        response = self._get_response(self.cat_url)
        data = response.json()
        return data

    def run(self):
        for category in self._get_categories():
            category["products"] = []
            params = f"?categories={category['parent_group_code']}"
            url = f"{self.start_url}{params}"

            category["products"].extend(list(self._parse(url)))
            file_name = f"{category['parent_group_code']}.json"
            cat_path = self.save_path.joinpath(file_name)
            self._save(category, cat_path)


if __name__ == "__main__":
    file_path_prod = Path(__file__).parent.joinpath("products")
    if not file_path_prod.exists():
        file_path_prod.mkdir()
    file_path_cat = Path(__file__).parent.joinpath("categories")
    if not file_path_cat.exists():
        file_path_cat.mkdir()
    url = "https://5ka.ru/api/v2/special_offers/"
    cat_url = "https://5ka.ru/api/v2/categories/"
    parser = Parse5ka(url, file_path_prod)
    cat_parser = Categories(cat_url, url, file_path_cat)
    cat_parser.run()