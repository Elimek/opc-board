"""OPC Board Engine — Topic router.
Analyzes user input, classifies domain, selects which advisors to call."""

from __future__ import annotations
import re
from engine.models import Domain, AgentDef, BOARD, TOPIC_VOTERS, DEFAULT_DOMAINS

# Chinese keywords per domain
CN_DOMAIN_KEYWORDS: dict[Domain, list[str]] = {
    Domain.FINANCE:    ["投资", "理财", "股票", "基金", "定投", "买房", "攒钱",
                        "钱", "资产", "仓位", "ETF", "回报", "风险", "杠杆",
                        "收入", "工资", "被动收入", "财务自由", "退休", "FIRE"],
    Domain.BRAND:      ["品牌", "内容", "营销", "粉丝", "自媒体", "短视频",
                        "写作", "产品", "转化", "流量", "IP", "人设", "曝光",
                        "涨粉", "变现", "个人品牌", "solopreneur"],
    Domain.HEALTH:     ["健康", "睡眠", "睡", "运动", "饮食", "压力", "焦虑",
                        "身体", "体检", "长寿", "精力", "养生", "protocol",
                        "神经", "激素", "皮质醇", "多巴胺", "生物", "年龄"],
    Domain.STRATEGY:   ["战略", "方向", "选择", "规划", "职业", "转行",
                        "跳槽", "学习", "教育", "移民", "执行", "效率",
                        "时间管理", "ROI", "目标", "创业", "决策"],
    Domain.INNOVATION: ["创新", "技术", "AI", "第一性原理", "成本",
                        "效率", "颠覆", "未来", "科技", "趋势", "工程",
                        "产品设计", "自动化", "制造", "极限", "物理"],
}

# English keywords per domain
EN_DOMAIN_KEYWORDS: dict[Domain, list[str]] = {
    Domain.FINANCE:    ["invest", "stock", "portfolio", "index", "asset",
                        "retire", "passive income", "money", "wealth", "FIRE",
                        "compound", "dividend", "ETF", "leverage", "risk"],
    Domain.BRAND:      ["brand", "content", "marketing", "audience", "follower",
                        "social media", "write", "productize", "solopreneur",
                        "personal brand", "monetize", "growth", "build in public"],
    Domain.HEALTH:     ["health", "sleep", "exercise", "diet", "stress",
                        "longevity", "energy", "protocol", "neuroscience",
                        "wellness", "biohack", "hormone", "cortisol", "dopamine"],
    Domain.STRATEGY:   ["strategy", "career", "choice", "direction", "learn",
                        "education", "plan", "goal", "execute", "ROI",
                        "transition", "decision", "immigrate", "startup"],
    Domain.INNOVATION: ["innovate", "technology", "AI", "first principle",
                        "cost", "efficiency", "science", "engineering",
                        "product", "disrupt", "physics", "automation", "scale"],
}


def classify(text: str) -> list[Domain]:
    """Classify user input into relevant domains.
    Returns ordered list of domains by relevance score."""
    text_lower = text.lower()
    scores: dict[Domain, int] = {d: 0 for d in Domain}

    # Check predefined topic keys first
    for topic_key, domains in TOPIC_VOTERS.items():
        if topic_key in text_lower:
            return domains  # exact match shortcut

    # Score by keyword matches
    for domain, keywords in CN_DOMAIN_KEYWORDS.items():
        for kw in keywords:
            if kw in text_lower:
                scores[domain] += 1

    for domain, keywords in EN_DOMAIN_KEYWORDS.items():
        for kw in keywords:
            if kw in text_lower:
                scores[domain] += 1

    # Return domains with score > 0, sorted by relevance
    relevant = [(d, s) for d, s in scores.items() if s > 0]
    relevant.sort(key=lambda x: -x[1])

    if not relevant:
        return list(DEFAULT_DOMAINS)  # fallback: call everyone

    return [d for d, _ in relevant]


def get_voters(domains: list[Domain]) -> list[AgentDef]:
    """Given a list of domains, return the agents who vote.
    Returns all matching agents, CFOs get double weight context."""
    voters = [a for a in BOARD if a.domain in domains]
    return voters


def get_reference(domains: list[Domain]) -> list[AgentDef]:
    """Agents not in the voting team — give reference opinions only."""
    voting_ids = {a.id for a in get_voters(domains)}
    return [a for a in BOARD if a.id not in voting_ids]


def format_summary(text: str, max_len: int = 60) -> str:
    """Short summary for display."""
    text = re.sub(r'\s+', ' ', text).strip()
    if len(text) <= max_len:
        return text
    return text[:max_len].rstrip() + "…"