import requests
from bs4 import BeautifulSoup


class YahooFinanceScraper:
    def __init__(self, stock_code):
        self.base_url = 'https://tw.stock.yahoo.com/quote/'
        self.stock_code = stock_code
        self.stock_data = {}

    def fetch_page(self):
        url = f"{self.base_url}{self.stock_code}.TW"
        response = requests.get(url)
        response.raise_for_status()  # Check that the request was successful
        return response.text

    def parse_page(self, html):
        return BeautifulSoup(html, 'html.parser')

    def get_name(self, soup):
        name_element = soup.find('h1', class_='C($c-link-text) Fw(b) Fz(24px) Mend(8px)')
        self.stock_data['名稱'] = name_element.text if name_element else 'N/A'

    def get_red_elements(self, soup):
        red_elements = soup.find_all('span', class_='Fw(600) Fz(16px)--mobile Fz(14px) D(f) Ai(c) C($c-trend-up)')
        if red_elements:
            self.stock_data['成交'] = red_elements[0].text if len(red_elements) > 0 else 'N/A'
            self.stock_data['開盤'] = red_elements[1].text if len(red_elements) > 1 else 'N/A'
            self.stock_data['最高'] = red_elements[2].text if len(red_elements) > 2 else 'N/A'
            self.stock_data['最低'] = red_elements[3].text if len(red_elements) > 3 else 'N/A'

    def get_black_elements(self, soup):
        black_elements = soup.find_all('span', class_="Fw(600) Fz(16px)--mobile Fz(14px) D(f) Ai(c)")
        if black_elements:
            self.stock_data['均價'] = black_elements[0].text if len(black_elements) > 0 else 'N/A'
            self.stock_data['昨收'] = black_elements[1].text if len(black_elements) > 1 else 'N/A'

    def get_sec_black_elements(self, soup):
        sec_black_elements = soup.find_all('span', class_="Fw(600) Fz(16px)--mobile Fz(14px)")
        if sec_black_elements:
            self.stock_data['成交值(億)'] = sec_black_elements[0].text if len(sec_black_elements) > 0 else 'N/A'
            self.stock_data['總量'] = sec_black_elements[1].text if len(sec_black_elements) > 1 else 'N/A'
            self.stock_data['昨量'] = sec_black_elements[2].text if len(sec_black_elements) > 2 else 'N/A'
            self.stock_data['振幅'] = sec_black_elements[3].text if len(sec_black_elements) > 3 else 'N/A'

    def get_price_detail_items(self, soup):
        price_detail_items = soup.find_all('li', class_='price-detail-item')
        for item in price_detail_items:
            label_span = item.find('span', class_='C(#232a31) Fz(16px)--mobile Fz(14px)')
            value_span = item.find('span', class_='Fw(600) Fz(16px)--mobile Fz(14px)')
            if label_span and value_span:
                label_text = label_span.text.strip()
                value_text = value_span.text.strip()
                if label_text == '漲跌幅':
                    self.stock_data['漲跌幅'] = value_text
                elif label_text == '漲跌':
                    self.stock_data['漲跌'] = value_text

    def get_data(self,):
        self.stock_data['代碼'] = f'{self.stock_code}.TW'
        html = self.fetch_page()
        soup = self.parse_page(html)
        self.get_name(soup)
        self.get_red_elements(soup)
        self.get_black_elements(soup)
        self.get_sec_black_elements(soup)
        self.get_price_detail_items(soup)
        return self.stock_data

    def get_vol(self):
        self.vol = {}
        left_vol = soup.find('div', class_="D(f) Jc(sb) Ai(c) Py(6px) Pstart(0px) Pend(16px)")


# Example usage
scraper = YahooFinanceScraper('2609')
data = scraper.get_data()
print(data)
