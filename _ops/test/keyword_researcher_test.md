# Keyword Researcher — Test Prompt

## Instructions
Run this prompt against the `keyword-researcher` skill. Save the full output to `test/workflow_runs/YYYY-MM-DD-keyword-test.md`.

---

## Prompt

Follow your keyword-researcher workflow. Today's date is 2026-04-21.

Published articles (for deduplication):

| slug | title | tags |
|------|-------|------|
| 2026-03-26-build-ai-agent | Build Your First Multi-Step AI Agent with Claude 4.6 API | AI Agent, Claude 4.6, AI Tutorial, Python, LLM |
| 2026-03-30-ai-54628f | Best AI Image Generators in 2026: 8 Tools Compared | AI Image Generator, AI Art Tools, AI Tools, Midjourney V7, Free AI |
| 2026-03-31-ai-09f249 | The Complete Guide to AI Prompt Engineering (2026) | AI Prompts, Prompt Engineering, AI Tutorial, AI Tools, ChatGPT, DeepSeek |
| 2026-03-31-ai-5cb8b5 | Best AI Coding Assistants in 2026: 6 Tools Compared | AI Coding, Cursor, Copilot, AI Tools, Developer Tools |
| 2026-03-31-ai-dfb482 | The Ultimate AI Learning Guide (2026): From Zero to LLM Applications | AI Tutorial, AI for Beginners, AI Tools, LLM, ChatGPT |
| 2026-03-31-claude-vs-chatgpt | Claude vs ChatGPT 2026: Which AI Assistant Is Right for You? | Claude, ChatGPT, AI Comparison, AI Assistant, AI Tools |
| 2026-03-31-midjourney | Midjourney Tutorial 2026: Complete Beginner's Guide | Midjourney, AI Art, Image Generation, AI Tools, AI Tutorial |
| 2026-03-31-openai-122b-agentic-workflows | OpenAI's $122B Funding: Agentic Workflows & Enterprise AI 2026 | OpenAI, AI Funding, Agentic AI, Enterprise AI |
| 2026-04-03-generative-ai-chip-design | Generative AI for Chip Design: How Machine Learning Cuts Costs 75% | AI Chips, Semiconductor, Generative AI, Machine Learning |
| 2026-04-07-ai-startup-funding-trends-2026 | AI Startup Funding Trends 2026: $131.5B Invested in AI | AI Startups, AI Funding, Venture Capital, AI Investment |
| 2026-04-08-cursor | Cursor Tutorial for Beginners: Complete Guide (2026) | Cursor Tutorial, AI Coding Tools |
| 2026-04-08-how-to-evaluate-ai-companies | How to Evaluate AI Companies: Complete Framework for Investors | AI Investment, AI Valuation, Enterprise AI, AI Startups |
| 2026-04-09-ai-company-revenue | AI Company Revenue Comparison 2026: Complete Financial Breakdown | AI Revenue, OpenAI, Anthropic, AI Investment, Enterprise AI |
| 2026-04-10-ai-2027-scenario-realistic | Is the AI 2027 Scenario Realistic? Infrastructure vs Impact | AI 2027, AI Infrastructure, AI Industry, AI Investment |
| 2026-04-10-ai-agent-market-consolidation | AI Agent Market Consolidation 2026: Framework Survival Guide | AI Agents, AI Frameworks, LangChain, AI Investment |
| 2026-04-10-ai-regulations-compliance | AI Regulations Compliance Trends 2026: Investor & Business Guide | AI Regulations, EU AI Act, AI Compliance, Enterprise AI, AI Investment |
| 2026-04-10-ai-unicorn-bubble | AI Unicorn Bubble Reality Check 2026: Startups Will Fail | AI Unicorns, AI Startups, AI Investment, Startup Failure |
| 2026-04-10-ai-venture-capital-trends-2026 | AI Venture Capital Trends 2026: Where the Money Is | Venture Capital, AI Investment, AI Funding, AI Startups |
| 2026-04-10-ai-agent-frameworks | AI Agent Frameworks Comparison 2026 | AI Agents, AI Frameworks, AI Investment |
| 2026-04-16-google-gemini | 2026 AI Office Tools: 15 Productivity Boosters | AI productivity tools, AI office tools |
| 2026-04-17-deepseek | How to Use DeepSeek? A Complete Beginner's Guide for 2026 | DeepSeek tutorial, AI tools, beginner guide |
| 2026-04-20-ai-e20c44 | Best Completely Free AI Tools in 2026 | free AI tools, AI productivity, AI tools 2026 |

---

## What to verify in the output

- [ ] Step 1: reads `D:/ai-verse/_ops/data/keyword_matrix.json` via `read_file`
- [ ] Step 1: selects topic with lowest coverage count (not random)
- [ ] Step 1: if AI in Verticals selected, picks least-covered vertical
- [ ] Step 2: uses `keywords[]` from matrix as seed starting point
- [ ] Step 7: reads then writes `D:/ai-verse/_ops/data/keyword_history.json`
- [ ] Output contains `KEYWORD_RESEARCH_JSON` marker
- [ ] `target_audience` uses new values: watcher / investor / professional / all
- [ ] `suggested_angles` keys match `target_audience` entries
