import json
from typing import Any

import httpx
from bs4 import BeautifulSoup
from pydantic import ValidationError

from backend.core.logger import logger
from backend.tasks.news_analysis.exceptions import ClsScraperError, DataFormatError, FetchError, ParseError
from backend.tasks.news_analysis.schemas import NewsItem

CLS_URL = "https://www.cls.cn/telegraph"


# ==========================================
# 2. 核心抓取器封装
# ==========================================
class ClsTelegraphScraper:
    def __init__(self, url: str = CLS_URL, timeout: int = 10):
        self.url = url
        self.timeout = timeout
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0 Safari/537.36"
            )
        }

    def _fetch_html(self) -> str:
        """获取网页源码"""
        logger.info(f"Fetching CLS telegraph page: {self.url}")
        try:
            with httpx.Client(timeout=self.timeout, follow_redirects=True, headers=self.headers) as client:
                resp = client.get(self.url)
                resp.raise_for_status()
        except httpx.HTTPError as exc:
            error_msg = f"Failed to fetch CLS telegraph page HTTP Error: {self.url}"
            logger.exception(error_msg)
            # 直接抛出自定义网络异常
            raise FetchError(error_msg) from exc

        logger.info(f"Fetch success: status_code={resp.status_code}, bytes={len(resp.text)}")
        return resp.text

    def _extract_raw_data(self, html: str) -> dict[str, Any]:
        """解析 HTML 并提取注入的 JSON 数据"""
        soup = BeautifulSoup(html, "html.parser")
        script_tag = soup.find("script", id="__NEXT_DATA__", type="application/json")

        if not script_tag:
            raise ParseError("Missing targeted script tag: 未找到 id 为 __NEXT_DATA__ 的 script 标签")

        json_string = script_tag.string
        if not json_string:
            raise ParseError("Empty JSON content: script 标签内没有内容")

        try:
            return json.loads(json_string)
        except json.JSONDecodeError as exc:
            raise ParseError("Invalid JSON format: 无法解析 script 标签内的 JSON 字符串") from exc

    def _extract_news(self, data: dict[str, Any]) -> list[NewsItem]:
        """从 JSON 字典中提取新闻列表并验证"""
        try:
            telegraph_list = data["props"]["initialState"]["telegraph"]["telegraphList"]
        except KeyError as exc:
            raise DataFormatError("JSON structure changed: 无法按原有路径提取 telegraphList") from exc

        if not isinstance(telegraph_list, list):
            raise DataFormatError(f"Expected telegraphList to be a list, got {type(telegraph_list)}")

        try:
            news_list = [NewsItem(**telegraph) for telegraph in telegraph_list]
            return news_list
        except ValidationError as exc:
            logger.exception("Pydantic validation failed for one or more news items")
            raise DataFormatError("Data validation failed: 提取的数据字段不满足 NewsItem 定义") from exc

    def get_latest_news(self) -> list[NewsItem]:
        html = self._fetch_html()
        raw_data = self._extract_raw_data(html)
        return self._extract_news(raw_data)


# ==========================================
# 测试入口
# ==========================================
if __name__ == "__main__":
    scraper = ClsTelegraphScraper()

    try:
        news = scraper.get_latest_news()
        print(f"成功获取 {len(news)} 条新闻数据！")

    except ClsScraperError as e:
        print(f"抓取过程发生异常: {e}")
    except Exception as e:
        print(f"发生未知错误: {e}")
