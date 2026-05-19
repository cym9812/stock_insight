import json

from openai import OpenAI

from app.core.config import settings
from app.tasks.news_analysis.schemas import NewsAnalysis, NewsItem

SYSTEM_PROMPT = """
你是一个严谨的财经新闻分析助手。

你的任务是根据输入的单条财经新闻，分析它对市场、行业板块、相关公司的潜在影响。

必须遵守：
1. 只基于输入新闻内容分析，不要编造新闻中不存在的事实。
2. 如果新闻没有明确提到公司，不要强行编造公司。
3. 可以根据新闻内容推断受影响板块，但必须给出原因。
4. 股票代码只有在新闻原文明确出现时才填写，否则为 null。
5. 如果影响方向不明确，使用 uncertain。
6. reasoning 要简洁，不要写长篇文章。
7. 必须只返回一个合法 JSON 对象。
8. 不要返回 Markdown。
9. 不要返回 ```json 代码块。
10. 不要输出任何解释性文字。

返回 JSON 的字段必须严格如下：

{
  "news_id": int,
  "summary": string,
  "event_type": string,
  "market_impact": string,
  "importance": string,
  "urgency": string,
  "sectors": [
    {
      "sector": string,
      "impact": string,
      "reason": string
    }
  ],
  "companies": [
    {
      "company": string,
      "stock_code": string 或 null,
      "impact": string,
      "reason": string
    }
  ],
  "reasoning": string,
  "confidence": float
}

字段说明：

- news_id：原始新闻 ID，必须和输入一致。
- summary：一句话概括新闻内容。
- event_type：只能是以下值之一：
  - 宏观政策
  - 行业政策
  - 公司事件
  - 国际事件
  - 商品价格
  - 金融市场
  - 监管执法
  - 突发事件
  - 其他

- market_impact：对整体市场的影响方向，只能是：
  - positive
  - negative
  - neutral
  - uncertain

- importance：新闻重要性，只能是：
  - low
  - medium
  - high

- urgency：是否需要立即关注，只能是：
  - low
  - medium
  - high

- sectors：受影响板块列表。
  - 如果没有明确受影响板块，返回空数组 []。
  - impact 只能是 positive / negative / neutral / uncertain。
  - reason 必须说明为什么影响该板块。

- companies：受影响公司列表。
  - 如果没有明确相关公司，返回空数组 []。
  - stock_code 只有新闻原文明确出现时填写，否则为 null。
  - impact 只能是 positive / negative / neutral / uncertain。
  - reason 必须说明为什么影响该公司。

- reasoning：简要分析逻辑。
- confidence：置信度，范围 0 到 1。
"""


def build_user_prompt(news: NewsItem) -> str:
    return f"""
请分析下面这条财经新闻，并返回 JSON。

新闻ID：
{news.news_id}

发布时间：
{news.publish_time}

正文：
{news.content}
"""


class NewsLLMClient:
    def __init__(
        self,
        model: str | None = None,
        api_key: str | None = None,
        base_url: str | None = None,
    ):
        model = model or settings.app.model_name
        if not model:
            raise ValueError("model is required.")
        api_key = api_key or settings.app.api_key
        if not api_key:
            raise ValueError("API key is required.")
        base_url = base_url or settings.app.base_url
        if not base_url:
            raise ValueError("Base URL is required.")

        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url,
        )
        self.model = model

    def analyze(self, news: NewsItem) -> NewsAnalysis:
        response = self.client.chat.completions.create(
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
            response_format={"type": "json_object"},
            reasoning_effort="high",
            extra_body={"thinking": {"type": "enabled"}},
        )

        content = response.choices[0].message.content
        if not content:
            raise ValueError("LLM returned empty content.")

        try:
            raw_data = json.loads(content)
        except json.JSONDecodeError as e:
            raise ValueError(f"LLM returned invalid JSON: {content}") from e

        try:
            result = NewsAnalysis.model_validate(raw_data)
        except Exception as e:
            raise ValueError(f"LLM returned JSON but schema validation failed: {raw_data}") from e

        return result


if __name__ == "__main__":
    n = NewsItem(
        id=2375960,
        content="财联社5月19日电，美国30年期国债收益率上升至5.195%，续创2007年以来最高水平。",
        ctime=1779201031,
        shareurl="https://api3.cls.cn/share/article/2375960?os=web&sv=8.4.6&app=CailianpressWeb",
    )
    c = NewsLLMClient()
    print(c.analyze(n))
