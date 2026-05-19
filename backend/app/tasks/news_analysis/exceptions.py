class ClsScraperError(Exception):
    """财联社爬虫基类异常"""

    pass


class FetchError(ClsScraperError):
    """网络请求失败异常"""

    pass


class ParseError(ClsScraperError):
    """HTML解析或DOM结构异常"""

    pass


class DataFormatError(ClsScraperError):
    """JSON数据结构变更或提取异常"""

    pass
