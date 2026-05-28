#!/usr/bin/env python3
"""
AI 内容生成器
使用 Claude/GPT/DeepSeek 等 API 生成 X 平台内容

Features:
- 技术推文生成
- Thread 长文生成
- 智能评论生成
- 内容安全检查
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any, Literal
from dataclasses import dataclass
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class GeneratedContent:
    """生成的内容"""
    content: str
    content_type: str  # tweet, thread, comment, quote
    safety_check: Dict[str, Any]
    metadata: Dict[str, Any]
    generated_at: str = ""

    def __post_init__(self):
        if not self.generated_at:
            self.generated_at = datetime.now().isoformat()


class SafetyChecker:
    """内容安全检查器"""

    # 敏感词库
    SENSITIVE_KEYWORDS = {
        "政治": [
            "选举", "政党", "总统", "首相", "政府", "民主", "专制",
            "左派", "右派", "自由派", "保守派", "制裁", "战争", "政治",
            "国会", "议会", "党派", "投票", "竞选"
        ],
        "地域": [
            "地域黑", "外地人", "排外", "歧视", "省份"
        ],
        "宗教": [
            "宗教", "信仰", "教徒", "无神论", "基督", "佛教", "伊斯兰"
        ],
        "性别": [
            "女拳", "男权", "性别对立", "田园", "直男癌", "女权"
        ],
        "争议": [
            "种族", "歧视", "仇恨", "攻击", "辱骂"
        ]
    }

    # 允许的技术关键词 (用于验证内容相关性)
    TECH_KEYWORDS = [
        "AI", "ML", "LLM", "GPT", "Claude", "大模型", "机器学习",
        "深度学习", "神经网络", "Transformer", "Python", "代码",
        "API", "开源", "GitHub", "算法", "数据", "训练", "推理",
        "RAG", "Fine-tuning", "Prompt", "Embedding", "向量"
    ]

    def check(self, text: str) -> Dict[str, Any]:
        """
        检查内容安全性

        Returns:
            {
                "safe": bool,
                "risk_level": "low" | "medium" | "high",
                "warnings": List[str],
                "blocked_keywords": List[str],
                "is_tech_related": bool
            }
        """
        text_lower = text.lower()
        warnings = []
        blocked_keywords = []

        # 检查敏感词
        for category, keywords in self.SENSITIVE_KEYWORDS.items():
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    blocked_keywords.append(f"{category}: {keyword}")

        # 检查技术相关性
        is_tech_related = any(
            kw.lower() in text_lower for kw in self.TECH_KEYWORDS
        )

        # 评估风险等级
        if blocked_keywords:
            if len(blocked_keywords) >= 3:
                risk_level = "high"
            elif len(blocked_keywords) >= 1:
                risk_level = "medium"
            else:
                risk_level = "low"
            safe = False
            warnings.append(f"发现敏感词: {', '.join(blocked_keywords)}")
        else:
            risk_level = "low"
            safe = True

        if not is_tech_related:
            warnings.append("内容可能与技术不相关")

        return {
            "safe": safe,
            "risk_level": risk_level,
            "warnings": warnings,
            "blocked_keywords": blocked_keywords,
            "is_tech_related": is_tech_related
        }


class ContentGenerator:
    """AI 内容生成器"""

    def __init__(self, config_path: str = "assets/config.json"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.safety_checker = SafetyChecker()
        self.client = None
        self._init_client()

    def _load_config(self) -> Dict:
        """加载配置"""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                return json.load(f)
        return {
            "ai_api": {
                "provider": "anthropic",
                "api_key": os.getenv("ANTHROPIC_API_KEY", ""),
                "model": "claude-3-sonnet-20240229"
            }
        }

    def _init_client(self):
        """初始化 AI 客户端"""
        provider = self.config.get("ai_api", {}).get("provider", "anthropic")
        api_key = self.config.get("ai_api", {}).get("api_key") or os.getenv("ANTHROPIC_API_KEY")

        if not api_key:
            logger.warning("未配置 API Key,使用模拟模式")
            self.client = None
            return

        try:
            if provider == "anthropic":
                from anthropic import Anthropic
                self.client = Anthropic(api_key=api_key)
                logger.info("Anthropic 客户端初始化成功")
            elif provider == "openai":
                from openai import OpenAI
                self.client = OpenAI(api_key=api_key)
                logger.info("OpenAI 客户端初始化成功")
            else:
                logger.warning(f"不支持的 provider: {provider}")
                self.client = None
        except Exception as e:
            logger.error(f"初始化 AI 客户端失败: {e}")
            self.client = None

    def _call_ai(self, prompt: str, max_tokens: int = 1024) -> str:
        """调用 AI API"""
        if not self.client:
            return f"[模拟响应] 基于提示词生成的内容: {prompt[:100]}..."

        provider = self.config.get("ai_api", {}).get("provider", "anthropic")
        model = self.config.get("ai_api", {}).get("model", "claude-3-sonnet-20240229")

        try:
            if provider == "anthropic":
                response = self.client.messages.create(
                    model=model,
                    max_tokens=max_tokens,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text
            elif provider == "openai":
                response = self.client.chat.completions.create(
                    model=model,
                    max_tokens=max_tokens,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.choices[0].message.content
            else:
                return ""
        except Exception as e:
            logger.error(f"AI API 调用失败: {e}")
            return ""

    # ==================== 推文生成 ====================

    def generate_tweet(
        self,
        topic: str,
        style: Literal["tip", "tool", "insight", "question", "announcement"] = "tip",
        max_length: int = 280
    ) -> GeneratedContent:
        """
        生成技术推文

        Args:
            topic: 推文主题
            style: 推文风格
            max_length: 最大长度

        Returns:
            GeneratedContent
        """
        style_prompts = {
            "tip": "一个实用的技术技巧,开头要有吸引力",
            "tool": "一个工具/库的推荐,说明为什么好用",
            "insight": "一个技术见解或观点,要有深度",
            "question": "一个引发讨论的技术问题",
            "announcement": "一个项目/文章的发布通知"
        }

        prompt = f"""你是一位专业的 AI/ML 技术博主。请生成一条关于"{topic}"的推文。

风格要求: {style_prompts.get(style, style_prompts["tip"])}

内容要求:
1. 开头要有吸引力 (Hook)
2. 内容要有实际价值,专业但不枯燥
3. 长度严格控制在 {max_length} 字符以内
4. 结尾可以加一个互动问题
5. 最多使用 2 个 emoji
6. 纯技术内容,不涉及任何政治、宗教、地域、性别话题

只输出推文内容,不要其他解释。"""

        content = self._call_ai(prompt)

        # 截断到最大长度
        if len(content) > max_length:
            content = content[:max_length-3] + "..."

        safety_check = self.safety_checker.check(content)

        return GeneratedContent(
            content=content,
            content_type="tweet",
            safety_check=safety_check,
            metadata={"topic": topic, "style": style}
        )

    def generate_thread(
        self,
        topic: str,
        num_tweets: int = 7,
        thread_type: Literal["tutorial", "analysis", "story", "list"] = "tutorial"
    ) -> GeneratedContent:
        """
        生成 Thread 长文

        Args:
            topic: 主题
            num_tweets: 推文数量
            thread_type: Thread 类型

        Returns:
            GeneratedContent (content 是 JSON 格式的推文列表)
        """
        type_prompts = {
            "tutorial": "教程型,包含具体步骤和代码示例",
            "analysis": "分析型,深度解读某个技术或趋势",
            "story": "故事型,分享一段技术经历或教训",
            "list": "清单型,总结多个要点或技巧"
        }

        prompt = f"""你是一位资深的 AI 技术专家和技术博主。
请为"{topic}"撰写一个 Thread (串推)。

类型: {type_prompts.get(thread_type, type_prompts["tutorial"])}

要求:
1. 共 {num_tweets} 条推文
2. 每条推文独立成段,但整体连贯
3. 第一条必须是强有力的 Hook,吸引人继续看
4. 包含具体的例子、数据或代码
5. 最后一条要有总结和互动引导
6. 每条推文约 200-280 字符
7. 技术深度适中,非专家也能理解
8. 纯技术内容,不涉及任何政治、宗教、地域、性别话题

请按以下 JSON 格式输出:
{{
  "tweets": [
    "1/{num_tweets} 第一条推文内容...",
    "2/{num_tweets} 第二条推文内容...",
    ...
  ]
}}

只输出 JSON,不要其他解释。"""

        response = self._call_ai(prompt, max_tokens=2048)

        # 解析 JSON
        try:
            # 尝试提取 JSON
            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                data = json.loads(json_match.group())
                tweets = data.get("tweets", [])
            else:
                tweets = [response]
        except json.JSONDecodeError:
            # 如果解析失败,按换行分割
            tweets = [t.strip() for t in response.split('\n\n') if t.strip()]

        # 安全检查每条推文
        all_safe = True
        all_warnings = []
        for tweet in tweets:
            check = self.safety_checker.check(tweet)
            if not check["safe"]:
                all_safe = False
                all_warnings.extend(check["warnings"])

        return GeneratedContent(
            content=json.dumps({"tweets": tweets}, ensure_ascii=False),
            content_type="thread",
            safety_check={
                "safe": all_safe,
                "risk_level": "high" if not all_safe else "low",
                "warnings": list(set(all_warnings))
            },
            metadata={"topic": topic, "thread_type": thread_type, "num_tweets": len(tweets)}
        )

    # ==================== 评论生成 ====================

    def generate_comment(
        self,
        original_tweet: str,
        author: str,
        comment_type: Literal["insight", "question", "supplement", "appreciation"] = "insight"
    ) -> GeneratedContent:
        """
        生成智能评论

        Args:
            original_tweet: 原推文内容
            author: 原作者
            comment_type: 评论类型

        Returns:
            GeneratedContent
        """
        type_prompts = {
            "insight": "分享一个相关的技术见解或独特角度",
            "question": "提出一个有深度的技术问题,引发作者回复",
            "supplement": "补充原帖未提及的相关经验或信息",
            "appreciation": "认可原帖观点并分享自己的体验"
        }

        prompt = f"""你是一位资深的 AI/ML 工程师。请为以下推文生成一条高质量评论。

原帖作者: @{author}
原帖内容: {original_tweet}

评论类型: {type_prompts.get(comment_type, type_prompts["insight"])}

要求:
1. 展示专业知识,但语气自然友好
2. 如果是提问类型,问题要具体且作者会愿意回答
3. 长度控制在 50-200 字符
4. 避免"Great post!"等模板化开头
5. 不要过度赞美,保持专业客观
6. 纯技术讨论,不涉及任何敏感话题

只输出评论内容,不要其他解释。"""

        content = self._call_ai(prompt, max_tokens=300)
        safety_check = self.safety_checker.check(content)

        return GeneratedContent(
            content=content,
            content_type="comment",
            safety_check=safety_check,
            metadata={
                "original_tweet": original_tweet[:100] + "...",
                "author": author,
                "comment_type": comment_type
            }
        )

    def generate_quote_tweet(
        self,
        original_tweet: str,
        author: str,
        angle: str = None
    ) -> GeneratedContent:
        """
        生成引用转发内容

        Args:
            original_tweet: 原推文
            author: 原作者
            angle: 你想要的角度 (可选)

        Returns:
            GeneratedContent
        """
        prompt = f"""你是一位 AI 技术博主。请为以下推文生成一条引用转发。

原帖作者: @{author}
原帖内容: {original_tweet}
{f"期望角度: {angle}" if angle else ""}

要求:
1. 加入你自己的见解或观点
2. 可以补充、延伸或提出不同看法
3. 长度约 100-200 字符
4. 要有价值,不是简单复述
5. 纯技术讨论

只输出引用转发的文字内容,不要其他解释。"""

        content = self._call_ai(prompt, max_tokens=300)
        safety_check = self.safety_checker.check(content)

        return GeneratedContent(
            content=content,
            content_type="quote",
            safety_check=safety_check,
            metadata={"original_tweet": original_tweet[:100], "author": author}
        )

    # ==================== 分析和建议 ====================

    def analyze_tweet_quality(self, tweet: str) -> Dict[str, Any]:
        """
        分析推文质量,判断是否值得互动

        Returns:
            {
                "worth_engaging": bool,
                "quality_score": float (0-1),
                "suggested_action": str,
                "reasons": List[str]
            }
        """
        prompt = f"""分析以下推文,判断是否值得作为 AI 技术博主进行互动。

推文内容: {tweet}

请评估:
1. 内容质量 (是否有价值)
2. 技术相关性 (是否与 AI/ML 相关)
3. 互动潜力 (是否容易产生有价值的回复)
4. 作者影响力暗示 (从措辞判断)
5. 是否有敏感内容

请以 JSON 格式输出:
{{
  "worth_engaging": true/false,
  "quality_score": 0-1 之间的分数,
  "suggested_action": "like" / "comment" / "retweet" / "quote" / "skip",
  "reasons": ["原因1", "原因2"]
}}"""

        response = self._call_ai(prompt, max_tokens=500)

        try:
            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass

        # 默认返回
        return {
            "worth_engaging": True,
            "quality_score": 0.5,
            "suggested_action": "like",
            "reasons": ["无法分析,建议手动判断"]
        }

    def suggest_improvements(self, draft: str) -> Dict[str, Any]:
        """
        为草稿提供改进建议

        Returns:
            {
                "improved_version": str,
                "suggestions": List[str],
                "hook_score": float,
                "clarity_score": float
            }
        """
        prompt = f"""请评估并改进以下推文草稿:

草稿: {draft}

请提供:
1. 改进版本 (更有吸引力、更专业)
2. 具体改进建议
3. 开头吸引力评分 (0-1)
4. 清晰度评分 (0-1)

以 JSON 格式输出:
{{
  "improved_version": "改进后的推文",
  "suggestions": ["建议1", "建议2"],
  "hook_score": 0-1,
  "clarity_score": 0-1
}}"""

        response = self._call_ai(prompt, max_tokens=800)

        try:
            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass

        return {
            "improved_version": draft,
            "suggestions": ["无法分析"],
            "hook_score": 0.5,
            "clarity_score": 0.5
        }


# ==================== 命令行接口 ====================

def main():
    """测试入口"""
    import argparse

    parser = argparse.ArgumentParser(description="AI 内容生成器")
    parser.add_argument("--action", choices=["tweet", "thread", "comment", "analyze"], required=True)
    parser.add_argument("--topic", help="主题或原推文内容")
    parser.add_argument("--style", default="tip", help="推文风格")
    parser.add_argument("--author", default="unknown", help="原作者 (评论时使用)")

    args = parser.parse_args()

    generator = ContentGenerator()

    if args.action == "tweet":
        result = generator.generate_tweet(args.topic or "Python 技巧", args.style)
        print("\n=== 生成的推文 ===")
        print(result.content)
        print(f"\n安全检查: {result.safety_check}")

    elif args.action == "thread":
        result = generator.generate_thread(args.topic or "RAG 最佳实践")
        print("\n=== 生成的 Thread ===")
        tweets = json.loads(result.content).get("tweets", [])
        for tweet in tweets:
            print(f"\n{tweet}")
        print(f"\n安全检查: {result.safety_check}")

    elif args.action == "comment":
        result = generator.generate_comment(
            args.topic or "Just released a new paper on LLM optimization!",
            args.author,
            "question"
        )
        print("\n=== 生成的评论 ===")
        print(result.content)
        print(f"\n安全检查: {result.safety_check}")

    elif args.action == "analyze":
        result = generator.analyze_tweet_quality(
            args.topic or "Just discovered a cool trick for fine-tuning LLMs!"
        )
        print("\n=== 推文分析 ===")
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
