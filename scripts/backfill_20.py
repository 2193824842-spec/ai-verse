#!/usr/bin/env python3
"""临时补跑 2026-04-20 的新闻，用完可删"""
import sys
from unittest.mock import patch
from datetime import datetime, timezone

TARGET_DATE = "2026-04-20"

# 把 datetime.now 固定到目标日期，让评分逻辑认为"今天"是 4月20日
fixed_dt = datetime(2026, 4, 20, 4, 0, 0, tzinfo=timezone.utc)

with patch("fetch_news.datetime") as mock_dt:
    mock_dt.now.return_value = fixed_dt
    mock_dt.strptime = datetime.strptime
    import fetch_news
    fetch_news.main()
