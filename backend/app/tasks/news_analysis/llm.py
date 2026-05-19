from openai import OpenAI

from app.tasks.news_analysis.schemas import NewsAnalysis, NewsItem

SYSTEM_PROMPT = """
你是一个严谨的财经新闻分析助手。

你的任务是根据输入的单条新闻，分析它对市场、行业板块、相关公司的潜在影响。

要求：
1. 只基于输入新闻内容分析，不要编造新闻中不存在的事实。
2. 如果新闻没有明确提到公司，不要强行编造公司。
3. 可以根据新闻内容推断受影响板块，但必须给出原因。
4. 股票代码只有在新闻原文明确出现，或者你非常确定时才填写；不确定就返回 null。
5. 如果影响方向不明确，使用 uncertain。
6. importance 表示新闻本身的重要性，分为 low（一般）/ medium（较重要）/ high（十分重要）三档。
7. urgency 表示是否需要立即关注，分为 low（可观察）/ medium（尽早关注）/ high（需立即关注）三档。
8. reasoning 要简洁，不要写长篇文章。
9. 返回内容必须严格符合给定结构。
"""


def build_user_prompt(news: NewsItem) -> str:
    """
    构造用户提示词。
    """
    return f"""
请分析下面这条财经新闻。

新闻ID：
{news.news_id}

发布时间：
{news.publish_time}

正文：
{news.content}
"""


class NewsLLMClient:
    def __init__(self, model: str = "gpt-4o-mini", api_key: str | None = None):
        """
        初始化 LLM 客户端。如果 api_key 未提供，将默认从环境变量读取。
        """
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def analyze(self, news: NewsItem) -> NewsAnalysis:
        response = self.client.beta.chat.completions.parse(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": build_user_prompt(news),
                },
            ],
            response_format=NewsAnalysis,
        )

        result = response.choices[0].message.parsed

        if not isinstance(result, NewsAnalysis):
            raise TypeError(f"Unexpected parsed result type: {type(result)}")

        return result
