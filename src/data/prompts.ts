export interface Prompt {
  id: string;
  title: string;
  titleZh: string;
  category: string;
  categoryZh: string;
  description: string;
  descriptionZh: string;
  prompt: string;
  promptZh: string;
  tags: string[];
  tagsZh: string[];
}

export const PROMPT_CATEGORIES = [
  { id: 'all',        en: 'All',        zh: '全部' },
  { id: 'writing',    en: 'Writing',    zh: '写作' },
  { id: 'coding',     en: 'Coding',     zh: '编程' },
  { id: 'marketing',  en: 'Marketing',  zh: '营销' },
  { id: 'analysis',   en: 'Analysis',   zh: '分析' },
  { id: 'creative',   en: 'Creative',   zh: '创意' },
  { id: 'learning',   en: 'Learning',   zh: '学习' },
];

export const PROMPTS: Prompt[] = [
  // Writing
  {
    id: 'blog-post',
    title: 'Blog Post Writer',
    titleZh: '博客文章写作',
    category: 'writing',
    categoryZh: '写作',
    description: 'Write an engaging, SEO-friendly blog post on any topic.',
    descriptionZh: '撰写引人入胜、SEO 友好的博客文章。',
    prompt: `You are an expert content writer. Write a comprehensive blog post about [TOPIC].

Structure:
- Compelling headline
- Hook introduction (2-3 sentences)
- 4-5 main sections with subheadings
- Practical examples or data points
- Clear conclusion with a call to action

Tone: [TONE — e.g. professional, conversational, educational]
Target audience: [AUDIENCE]
Word count: approximately [LENGTH] words`,
    promptZh: `你是一位专业内容写作专家。请围绕【主题】撰写一篇完整的博客文章。

结构要求：
- 吸引人的标题
- 开篇钩子（2-3句话）
- 4-5个带小标题的主要章节
- 实际案例或数据支撑
- 清晰的结尾与行动号召

语气：【语气，如：专业、对话式、教育性】
目标读者：【受众】
字数：约【字数】字`,
    tags: ['blog', 'SEO', 'content'],
    tagsZh: ['博客', 'SEO', '内容'],
  },
  {
    id: 'email-writer',
    title: 'Professional Email',
    titleZh: '专业邮件写作',
    category: 'writing',
    categoryZh: '写作',
    description: 'Draft clear, professional emails for any business situation.',
    descriptionZh: '为各种商务场景起草清晰专业的邮件。',
    prompt: `You are a professional business writer. Write a [TYPE — e.g. follow-up, proposal, complaint] email.

Context: [SITUATION]
Recipient: [WHO — e.g. client, manager, vendor]
Goal: [WHAT YOU WANT TO ACHIEVE]
Tone: professional and concise

Include:
- Clear subject line
- Brief opening
- Main message (2-3 short paragraphs)
- Specific call to action
- Professional sign-off`,
    promptZh: `你是一位专业商务写作专家。请撰写一封【类型，如：跟进、提案、投诉】邮件。

背景：【情况描述】
收件人：【对象，如：客户、上级、供应商】
目标：【希望达成的结果】
语气：专业简洁

包含：
- 清晰的主题行
- 简短开场
- 正文（2-3段）
- 明确的行动号召
- 专业结尾`,
    tags: ['email', 'business', 'communication'],
    tagsZh: ['邮件', '商务', '沟通'],
  },
  {
    id: 'resume-bullet',
    title: 'Resume Bullet Points',
    titleZh: '简历要点优化',
    category: 'writing',
    categoryZh: '写作',
    description: 'Transform job duties into powerful, quantified resume bullets.',
    descriptionZh: '将工作职责转化为有力的量化简历要点。',
    prompt: `You are a professional resume writer. Transform the following job duties into strong resume bullet points.

Job title: [TITLE]
Raw duties: [LIST YOUR DUTIES]

Rules:
- Start each bullet with a strong action verb
- Quantify results where possible (%, $, time saved)
- Focus on impact, not just tasks
- Keep each bullet under 2 lines
- Write 5-7 bullets total`,
    promptZh: `你是一位专业简历写作专家。将以下工作职责转化为有力的简历要点。

职位：【职位名称】
原始职责：【列出你的职责】

要求：
- 每条以强有力的动词开头
- 尽量量化成果（百分比、金额、节省时间）
- 聚焦影响力，而非仅描述任务
- 每条不超过两行
- 共写 5-7 条`,
    tags: ['resume', 'career', 'job'],
    tagsZh: ['简历', '求职', '职业'],
  },
  // Coding
  {
    id: 'code-review',
    title: 'Code Review',
    titleZh: '代码审查',
    category: 'coding',
    categoryZh: '编程',
    description: 'Get a thorough code review with actionable feedback.',
    descriptionZh: '获得全面的代码审查和可操作的改进建议。',
    prompt: `You are a senior software engineer. Review the following code and provide detailed feedback.

Language/Framework: [LANGUAGE]
Code:
\`\`\`
[PASTE YOUR CODE HERE]
\`\`\`

Review for:
1. Bugs and potential errors
2. Performance issues
3. Security vulnerabilities
4. Code readability and maintainability
5. Best practices and conventions

For each issue: explain the problem, why it matters, and provide a corrected code snippet.`,
    promptZh: `你是一位资深软件工程师。请审查以下代码并提供详细反馈。

语言/框架：【语言】
代码：
\`\`\`
【粘贴你的代码】
\`\`\`

审查维度：
1. Bug 和潜在错误
2. 性能问题
3. 安全漏洞
4. 代码可读性和可维护性
5. 最佳实践和规范

每个问题请说明：问题描述、重要性、修正后的代码片段。`,
    tags: ['code review', 'debugging', 'best practices'],
    tagsZh: ['代码审查', '调试', '最佳实践'],
  },
  {
    id: 'explain-code',
    title: 'Explain Code',
    titleZh: '代码解释',
    category: 'coding',
    categoryZh: '编程',
    description: 'Get a clear explanation of complex code in plain language.',
    descriptionZh: '用通俗语言清晰解释复杂代码。',
    prompt: `You are a patient programming teacher. Explain the following code to someone with [LEVEL — beginner/intermediate/advanced] knowledge.

\`\`\`[LANGUAGE]
[PASTE CODE HERE]
\`\`\`

Your explanation should:
- Describe what the code does overall (1-2 sentences)
- Walk through each key section step by step
- Explain any non-obvious logic or patterns
- Use analogies where helpful
- Highlight potential gotchas`,
    promptZh: `你是一位耐心的编程老师。请向一位【水平：初级/中级/高级】开发者解释以下代码。

\`\`\`【语言】
【粘贴代码】
\`\`\`

解释要求：
- 整体描述代码功能（1-2句）
- 逐步讲解每个关键部分
- 解释不直观的逻辑或模式
- 适当使用类比
- 指出潜在的坑`,
    tags: ['learning', 'explanation', 'documentation'],
    tagsZh: ['学习', '解释', '文档'],
  },
  {
    id: 'write-tests',
    title: 'Write Unit Tests',
    titleZh: '编写单元测试',
    category: 'coding',
    categoryZh: '编程',
    description: 'Generate comprehensive unit tests for your functions.',
    descriptionZh: '为你的函数生成全面的单元测试。',
    prompt: `You are a test-driven development expert. Write comprehensive unit tests for the following code.

Framework: [TEST FRAMEWORK — e.g. Jest, pytest, JUnit]
Code to test:
\`\`\`
[PASTE YOUR CODE]
\`\`\`

Cover:
- Happy path (normal expected inputs)
- Edge cases (empty, null, boundary values)
- Error cases (invalid inputs, exceptions)
- At least [N] test cases total

Use descriptive test names that explain what is being tested.`,
    promptZh: `你是一位测试驱动开发专家。为以下代码编写全面的单元测试。

测试框架：【框架，如：Jest、pytest、JUnit】
待测代码：
\`\`\`
【粘贴代码】
\`\`\`

覆盖范围：
- 正常路径（预期输入）
- 边界情况（空值、null、边界值）
- 错误情况（无效输入、异常）
- 至少【N】个测试用例

使用描述性测试名称，清晰说明测试内容。`,
    tags: ['testing', 'TDD', 'quality'],
    tagsZh: ['测试', 'TDD', '质量'],
  },
  // Marketing
  {
    id: 'ad-copy',
    title: 'Ad Copy Writer',
    titleZh: '广告文案写作',
    category: 'marketing',
    categoryZh: '营销',
    description: 'Create compelling ad copy that converts.',
    descriptionZh: '创作高转化率的广告文案。',
    prompt: `You are a direct-response copywriter with 10+ years of experience. Write ad copy for the following product/service.

Product/Service: [DESCRIPTION]
Target audience: [WHO THEY ARE, their pain points]
Platform: [WHERE THE AD WILL RUN — Google, Facebook, LinkedIn, etc.]
Goal: [CLICKS / SIGN-UPS / PURCHASES]

Deliver:
- 3 headline variations (under 30 characters each)
- 2 body copy variations (under 90 characters each)
- 1 strong CTA

Focus on benefits, not features. Speak directly to the pain point.`,
    promptZh: `你是一位拥有10年以上经验的直接响应文案专家。为以下产品/服务撰写广告文案。

产品/服务：【描述】
目标受众：【人群特征及痛点】
投放平台：【平台，如：Google、Facebook、LinkedIn】
目标：【点击/注册/购买】

输出：
- 3个标题变体（每个不超过15字）
- 2个正文变体（每个不超过45字）
- 1个强有力的行动号召

聚焦利益而非功能，直击痛点。`,
    tags: ['advertising', 'copywriting', 'conversion'],
    tagsZh: ['广告', '文案', '转化'],
  },
  {
    id: 'social-post',
    title: 'Social Media Post',
    titleZh: '社交媒体内容',
    category: 'marketing',
    categoryZh: '营销',
    description: 'Create engaging social media posts for any platform.',
    descriptionZh: '为任意平台创作吸引人的社交媒体内容。',
    prompt: `You are a social media strategist. Create engaging posts for [PLATFORM — Twitter/X, LinkedIn, Instagram, etc.].

Topic/Product: [WHAT YOU'RE POSTING ABOUT]
Goal: [AWARENESS / ENGAGEMENT / TRAFFIC / LEADS]
Brand voice: [TONE — e.g. professional, witty, inspirational]

Deliver 3 post variations:
- Variation 1: Question-based (drives comments)
- Variation 2: Value/tip format
- Variation 3: Story or insight

Include relevant hashtags for each. Respect platform character limits.`,
    promptZh: `你是一位社交媒体策略专家。为【平台，如：微博、小红书、LinkedIn】创作吸引人的内容。

主题/产品：【发布内容】
目标：【品牌曝光/互动/引流/获客】
品牌语气：【语气，如：专业、幽默、励志】

输出3个变体：
- 变体1：提问式（引发评论）
- 变体2：价值/技巧型
- 变体3：故事或洞察

每个变体附上相关话题标签，遵守平台字数限制。`,
    tags: ['social media', 'engagement', 'content'],
    tagsZh: ['社交媒体', '互动', '内容'],
  },
  {
    id: 'product-description',
    title: 'Product Description',
    titleZh: '产品描述',
    category: 'marketing',
    categoryZh: '营销',
    description: 'Write persuasive product descriptions that sell.',
    descriptionZh: '撰写有说服力的产品描述，促进销售。',
    prompt: `You are an e-commerce copywriter. Write a compelling product description.

Product name: [NAME]
Key features: [LIST 3-5 FEATURES]
Target customer: [WHO BUYS THIS AND WHY]
Price point: [BUDGET / MID-RANGE / PREMIUM]

Write:
1. A punchy headline (under 10 words)
2. A 2-sentence hook that leads with the main benefit
3. 4-5 bullet points highlighting key features as benefits
4. A closing sentence with urgency or social proof`,
    promptZh: `你是一位电商文案专家。撰写有说服力的产品描述。

产品名称：【名称】
核心功能：【列出3-5个功能】
目标客户：【谁会购买及原因】
价格定位：【经济/中端/高端】

输出：
1. 简洁有力的标题（不超过10字）
2. 以核心利益开头的2句钩子文案
3. 4-5条将功能转化为利益的要点
4. 带紧迫感或社会证明的结尾`,
    tags: ['e-commerce', 'product', 'sales'],
    tagsZh: ['电商', '产品', '销售'],
  },
  // Analysis
  {
    id: 'swot-analysis',
    title: 'SWOT Analysis',
    titleZh: 'SWOT 分析',
    category: 'analysis',
    categoryZh: '分析',
    description: 'Conduct a thorough SWOT analysis for any business or idea.',
    descriptionZh: '对任何业务或想法进行全面的 SWOT 分析。',
    prompt: `You are a strategic business consultant. Conduct a thorough SWOT analysis.

Subject: [COMPANY / PRODUCT / IDEA / DECISION]
Industry/Context: [RELEVANT BACKGROUND]

For each quadrant, provide 4-6 specific, actionable points (not generic):
- Strengths: internal advantages
- Weaknesses: internal limitations
- Opportunities: external factors to exploit
- Threats: external risks to mitigate

End with 3 strategic recommendations based on the analysis.`,
    promptZh: `你是一位战略商业顾问。请进行全面的 SWOT 分析。

分析对象：【公司/产品/想法/决策】
行业/背景：【相关背景信息】

每个象限提供4-6个具体可操作的要点（避免泛泛而谈）：
- 优势：内部竞争优势
- 劣势：内部局限性
- 机会：可利用的外部因素
- 威胁：需应对的外部风险

最后基于分析给出3条战略建议。`,
    tags: ['strategy', 'business', 'planning'],
    tagsZh: ['战略', '商业', '规划'],
  },
  {
    id: 'data-insights',
    title: 'Data Analysis & Insights',
    titleZh: '数据分析与洞察',
    category: 'analysis',
    categoryZh: '分析',
    description: 'Extract meaningful insights from data and metrics.',
    descriptionZh: '从数据和指标中提取有意义的洞察。',
    prompt: `You are a data analyst. Analyze the following data and extract actionable insights.

Data/Metrics:
[PASTE YOUR DATA OR DESCRIBE THE METRICS]

Context: [WHAT THIS DATA IS ABOUT, WHAT DECISIONS IT INFORMS]

Provide:
1. Key findings (top 3-5 patterns or anomalies)
2. What the data suggests about [SPECIFIC QUESTION]
3. Potential causes for notable trends
4. Recommended actions based on the data
5. What additional data would strengthen the analysis`,
    promptZh: `你是一位数据分析师。分析以下数据并提取可操作的洞察。

数据/指标：
【粘贴数据或描述指标】

背景：【数据含义及决策用途】

输出：
1. 关键发现（3-5个主要规律或异常）
2. 数据对【具体问题】的启示
3. 显著趋势的潜在原因
4. 基于数据的行动建议
5. 哪些额外数据能强化分析`,
    tags: ['data', 'metrics', 'insights'],
    tagsZh: ['数据', '指标', '洞察'],
  },
  // Creative
  {
    id: 'story-starter',
    title: 'Story Starter',
    titleZh: '故事开篇',
    category: 'creative',
    categoryZh: '创意',
    description: 'Generate compelling story openings and plot outlines.',
    descriptionZh: '生成引人入胜的故事开篇和情节大纲。',
    prompt: `You are a creative writing coach. Generate a compelling story starter.

Genre: [GENRE — sci-fi, thriller, romance, fantasy, literary fiction, etc.]
Setting: [TIME AND PLACE]
Main character: [BRIEF DESCRIPTION]
Central conflict or theme: [WHAT THE STORY IS ABOUT]

Deliver:
1. An opening paragraph (150-200 words) that hooks the reader immediately
2. A brief plot outline (5 key story beats)
3. 3 possible directions the story could take`,
    promptZh: `你是一位创意写作教练。生成引人入胜的故事开篇。

类型：【类型，如：科幻、悬疑、言情、奇幻、文学小说】
背景：【时间与地点】
主角：【简要描述】
核心冲突或主题：【故事主旨】

输出：
1. 开篇段落（300-400字），立即抓住读者
2. 简要情节大纲（5个关键故事节点）
3. 故事可能走向的3个方向`,
    tags: ['fiction', 'creative writing', 'storytelling'],
    tagsZh: ['小说', '创意写作', '叙事'],
  },
  {
    id: 'brainstorm',
    title: 'Brainstorm Ideas',
    titleZh: '头脑风暴',
    category: 'creative',
    categoryZh: '创意',
    description: 'Generate diverse, creative ideas for any challenge.',
    descriptionZh: '为任何挑战生成多样化的创意想法。',
    prompt: `You are a creative strategist. Brainstorm ideas for the following challenge.

Challenge/Goal: [DESCRIBE WHAT YOU'RE TRYING TO ACHIEVE]
Constraints: [BUDGET, TIME, RESOURCES, OR OTHER LIMITS]
Context: [RELEVANT BACKGROUND]

Generate 15 ideas across 3 categories:
- 5 conventional ideas (safe, proven approaches)
- 5 creative ideas (unexpected but feasible)
- 5 wild ideas (unconventional, push boundaries)

For each idea: one sentence description + one sentence on why it could work.`,
    promptZh: `你是一位创意策略师。为以下挑战进行头脑风暴。

挑战/目标：【描述你想实现的目标】
限制条件：【预算、时间、资源或其他限制】
背景：【相关背景信息】

生成3类共15个想法：
- 5个常规想法（安全、经过验证的方法）
- 5个创意想法（出乎意料但可行）
- 5个大胆想法（非常规、突破边界）

每个想法：一句描述 + 一句说明可行性。`,
    tags: ['ideation', 'creativity', 'problem-solving'],
    tagsZh: ['创意', '头脑风暴', '解决问题'],
  },
  // Learning
  {
    id: 'explain-concept',
    title: 'Explain Any Concept',
    titleZh: '概念解释',
    category: 'learning',
    categoryZh: '学习',
    description: 'Get a clear, layered explanation of any complex topic.',
    descriptionZh: '获得任何复杂主题的清晰分层解释。',
    prompt: `You are an expert teacher who excels at making complex topics accessible.

Concept to explain: [TOPIC]
My background: [YOUR CURRENT KNOWLEDGE LEVEL]
Why I need to understand this: [YOUR GOAL OR USE CASE]

Explain it in 3 layers:
1. The simple version (explain like I'm 12)
2. The practical version (how it actually works, with a real-world example)
3. The nuanced version (edge cases, common misconceptions, deeper implications)

End with 3 questions I should be able to answer if I've understood this correctly.`,
    promptZh: `你是一位擅长将复杂主题变得易懂的专家教师。

需要解释的概念：【主题】
我的背景：【你当前的知识水平】
为什么需要理解这个：【你的目标或使用场景】

分3个层次解释：
1. 简单版本（像给12岁孩子解释一样）
2. 实用版本（实际工作原理，配真实案例）
3. 深入版本（边界情况、常见误解、深层含义）

最后给出3个问题，如果我真正理解了应该能回答。`,
    tags: ['learning', 'education', 'understanding'],
    tagsZh: ['学习', '教育', '理解'],
  },
  {
    id: 'study-plan',
    title: 'Study Plan Creator',
    titleZh: '学习计划制定',
    category: 'learning',
    categoryZh: '学习',
    description: 'Build a structured study plan to master any skill.',
    descriptionZh: '制定结构化学习计划，掌握任何技能。',
    prompt: `You are a learning coach and curriculum designer. Create a structured study plan.

Skill/Subject to learn: [WHAT YOU WANT TO MASTER]
Current level: [COMPLETE BEGINNER / SOME BASICS / INTERMEDIATE]
Available time: [HOURS PER WEEK]
Timeline: [HOW MANY WEEKS/MONTHS]
Goal: [WHAT YOU WANT TO BE ABLE TO DO AT THE END]

Deliver:
1. Week-by-week breakdown with specific topics
2. Recommended resources for each phase (free + paid options)
3. Practice exercises or projects to reinforce learning
4. Milestones to measure progress
5. Common pitfalls to avoid`,
    promptZh: `你是一位学习教练和课程设计师。制定结构化学习计划。

要学习的技能/科目：【你想掌握的内容】
当前水平：【完全零基础/有一些基础/中级】
可用时间：【每周小时数】
时间线：【几周/几个月】
目标：【最终希望能做到什么】

输出：
1. 按周分解的具体学习主题
2. 每个阶段的推荐资源（免费+付费）
3. 强化学习的练习或项目
4. 衡量进度的里程碑
5. 需要避免的常见误区`,
    tags: ['learning', 'productivity', 'skills'],
    tagsZh: ['学习', '效率', '技能'],
  },
  // Writing — additional
  {
    id: 'meeting-notes',
    title: 'Meeting Notes & Action Items',
    titleZh: '会议纪要与行动项',
    category: 'writing',
    categoryZh: '写作',
    description: 'Turn raw meeting notes into a clean, actionable summary.',
    descriptionZh: '将零散的会议记录整理成清晰的纪要和行动项。',
    prompt: `Clean up and structure the following raw meeting notes into a professional summary.

Raw notes:
[PASTE YOUR NOTES HERE]

Output format:
**Meeting Summary** (2-3 sentences)

**Key Decisions**
- [decision 1]
- [decision 2]

**Action Items**
| Owner | Task | Due Date |
|-------|------|----------|
| [name] | [task] | [date] |

**Next Steps / Follow-up**
- [item]`,
    promptZh: `将以下零散的会议记录整理成专业的会议纪要。

原始记录：
【粘贴你的记录】

输出格式：
**会议摘要**（2-3句话）

**关键决策**
- 【决策1】
- 【决策2】

**行动项**
| 负责人 | 任务 | 截止日期 |
|--------|------|----------|
| 【姓名】 | 【任务】 | 【日期】 |

**后续跟进**
- 【事项】`,
    tags: ['meeting', 'notes', 'productivity'],
    tagsZh: ['会议', '纪要', '效率'],
  },
  {
    id: 'cover-letter',
    title: 'Cover Letter',
    titleZh: '求职信',
    category: 'writing',
    categoryZh: '写作',
    description: 'Write a compelling, personalized cover letter for any job.',
    descriptionZh: '为任何职位撰写有说服力的个性化求职信。',
    prompt: `Write a compelling cover letter for the following job application.

Job title: [TITLE]
Company: [COMPANY NAME]
Key requirements from the job posting: [LIST 3-4 KEY REQUIREMENTS]
My relevant experience: [BRIEF SUMMARY OF YOUR BACKGROUND]
Why I want this role: [YOUR GENUINE REASON]

Guidelines:
- Open with a strong hook, not "I am writing to apply for..."
- Connect my experience directly to their specific needs
- Show genuine enthusiasm for the company (not generic praise)
- Keep it to 3 paragraphs, under 300 words
- End with a confident, specific call to action`,
    promptZh: `为以下职位申请撰写一封有说服力的求职信。

职位：【职位名称】
公司：【公司名称】
职位要求中的关键点：【列出3-4个关键要求】
我的相关经历：【简要介绍你的背景】
为什么想要这个职位：【你的真实原因】

要求：
- 开头要有吸引力，不要用"我写信申请..."
- 将我的经历与他们的具体需求直接挂钩
- 表达对公司的真实热情（不要泛泛而谈）
- 控制在3段以内，不超过300字
- 以自信、具体的行动号召结尾`,
    tags: ['job', 'career', 'application'],
    tagsZh: ['求职', '职业', '申请'],
  },
  {
    id: 'performance-review',
    title: 'Self Performance Review',
    titleZh: '自我绩效评估',
    category: 'writing',
    categoryZh: '写作',
    description: 'Write a strong self-assessment for your annual review.',
    descriptionZh: '为年度考核撰写有力的自我评估。',
    prompt: `Help me write a strong self-performance review for my annual evaluation.

My role: [JOB TITLE]
Review period: [TIME PERIOD]
Key accomplishments: [LIST YOUR TOP 3-5 ACHIEVEMENTS WITH METRICS IF POSSIBLE]
Challenges I overcame: [BRIEF DESCRIPTION]
Areas I improved: [SKILLS OR BEHAVIORS]
Goals for next period: [2-3 GOALS]

Write in first person. Quantify impact wherever possible. Be confident but not arrogant. Highlight growth and initiative.`,
    promptZh: `帮我为年度考核撰写一份有力的自我绩效评估。

我的职位：【职位名称】
考核周期：【时间段】
主要成就：【列出3-5项成就，尽量附数据】
克服的挑战：【简要描述】
提升的方面：【技能或行为】
下一阶段目标：【2-3个目标】

用第一人称写作。尽量量化影响。自信但不自大。突出成长和主动性。`,
    tags: ['career', 'HR', 'self-assessment'],
    tagsZh: ['职业', 'HR', '自我评估'],
  },
  // Coding — additional
  {
    id: 'sql-query',
    title: 'SQL Query Builder',
    titleZh: 'SQL 查询构建',
    category: 'coding',
    categoryZh: '编程',
    description: 'Write optimized SQL queries from plain-language descriptions.',
    descriptionZh: '用自然语言描述需求，生成优化的 SQL 查询。',
    prompt: `Write an optimized SQL query based on the following requirements.

Database type: [MySQL / PostgreSQL / SQLite / etc.]
Table structure:
\`\`\`
[DESCRIBE YOUR TABLES AND KEY COLUMNS]
\`\`\`
What I need: [DESCRIBE WHAT DATA YOU WANT TO RETRIEVE OR MODIFY]
Conditions/filters: [ANY WHERE CLAUSES OR CONSTRAINTS]
Expected output: [WHAT THE RESULT SHOULD LOOK LIKE]

Provide:
1. The SQL query with clear formatting
2. A brief explanation of the key clauses
3. Any indexes that would improve performance`,
    promptZh: `根据以下需求编写优化的 SQL 查询。

数据库类型：【MySQL / PostgreSQL / SQLite 等】
表结构：
\`\`\`
【描述你的表和关键字段】
\`\`\`
需求：【描述你想查询或修改的数据】
条件/过滤：【WHERE 条件或约束】
期望输出：【结果应该是什么样的】

请提供：
1. 格式清晰的 SQL 查询
2. 关键子句的简要说明
3. 能提升性能的索引建议`,
    tags: ['SQL', 'database', 'query'],
    tagsZh: ['SQL', '数据库', '查询'],
  },
  {
    id: 'refactor-code',
    title: 'Refactor Code',
    titleZh: '代码重构',
    category: 'coding',
    categoryZh: '编程',
    description: 'Refactor messy code to be cleaner, more maintainable, and efficient.',
    descriptionZh: '将混乱的代码重构为更清晰、可维护、高效的版本。',
    prompt: `Refactor the following code to improve its quality without changing its behavior.

Language: [LANGUAGE]
\`\`\`
[PASTE YOUR CODE]
\`\`\`

Focus on:
- Naming: variables, functions, and classes should be self-documenting
- Structure: break down large functions, reduce nesting
- DRY: eliminate repetition
- Readability: a new developer should understand it quickly
- Performance: flag any obvious inefficiencies

Show the refactored code and briefly explain each significant change.`,
    promptZh: `在不改变行为的前提下，重构以下代码以提升质量。

语言：【语言】
\`\`\`
【粘贴你的代码】
\`\`\`

重点关注：
- 命名：变量、函数、类名应能自我说明
- 结构：拆分大函数，减少嵌套层级
- DRY：消除重复代码
- 可读性：新开发者应能快速理解
- 性能：标注明显的低效之处

展示重构后的代码，并简要说明每处重要改动。`,
    tags: ['refactor', 'clean code', 'maintainability'],
    tagsZh: ['重构', '整洁代码', '可维护性'],
  },
  {
    id: 'api-design',
    title: 'REST API Design',
    titleZh: 'REST API 设计',
    category: 'coding',
    categoryZh: '编程',
    description: 'Design a clean, RESTful API for any feature or service.',
    descriptionZh: '为任何功能或服务设计清晰的 RESTful API。',
    prompt: `Design a RESTful API for the following feature.

Feature description: [WHAT THE API SHOULD DO]
Tech stack: [BACKEND LANGUAGE/FRAMEWORK]
Authentication: [JWT / API Key / OAuth / None]

Provide:
1. Endpoint list with HTTP methods, paths, and descriptions
2. Request/response schemas for each endpoint (JSON)
3. Error codes and their meanings
4. Any important design decisions or trade-offs`,
    promptZh: `为以下功能设计一套 RESTful API。

功能描述：【API 应该做什么】
技术栈：【后端语言/框架】
认证方式：【JWT / API Key / OAuth / 无】

请提供：
1. 端点列表（HTTP 方法、路径、描述）
2. 每个端点的请求/响应 Schema（JSON）
3. 错误码及其含义
4. 重要的设计决策或权衡说明`,
    tags: ['API', 'REST', 'backend', 'design'],
    tagsZh: ['API', 'REST', '后端', '设计'],
  },
  // Marketing — additional
  {
    id: 'landing-page',
    title: 'Landing Page Copy',
    titleZh: '落地页文案',
    category: 'marketing',
    categoryZh: '营销',
    description: 'Write high-converting landing page copy for any product.',
    descriptionZh: '为任何产品撰写高转化率的落地页文案。',
    prompt: `Write high-converting landing page copy for the following product/service.

Product/Service: [DESCRIPTION]
Target customer: [WHO THEY ARE, their biggest pain point]
Main benefit: [THE #1 THING YOUR PRODUCT DOES FOR THEM]
Key features: [3-5 FEATURES]
Social proof available: [TESTIMONIALS, NUMBERS, LOGOS — or "none yet"]
CTA goal: [SIGN UP / BUY / BOOK A DEMO / etc.]

Sections to write:
1. Hero headline + subheadline
2. Problem statement (2-3 sentences)
3. Solution intro (how your product solves it)
4. 3 feature/benefit blocks
5. Social proof section
6. FAQ (3 common objections + answers)
7. Final CTA`,
    promptZh: `为以下产品/服务撰写高转化率的落地页文案。

产品/服务：【描述】
目标客户：【人群特征及最大痛点】
核心利益：【产品为他们做的最重要的事】
主要功能：【3-5个功能】
社会证明：【用户评价、数据、品牌Logo，或"暂无"】
CTA 目标：【注册/购买/预约演示等】

需要撰写的板块：
1. 主标题 + 副标题
2. 痛点陈述（2-3句）
3. 解决方案介绍
4. 3个功能/利益模块
5. 社会证明板块
6. FAQ（3个常见顾虑 + 解答）
7. 最终行动号召`,
    tags: ['landing page', 'conversion', 'copywriting'],
    tagsZh: ['落地页', '转化', '文案'],
  },
  {
    id: 'cold-outreach',
    title: 'Cold Outreach Message',
    titleZh: '冷启动外联消息',
    category: 'marketing',
    categoryZh: '营销',
    description: 'Write personalized cold outreach that actually gets replies.',
    descriptionZh: '撰写真正能获得回复的个性化冷启动外联消息。',
    prompt: `Write a personalized cold outreach message that gets replies.

Channel: [EMAIL / LINKEDIN / OTHER]
My product/service: [WHAT YOU OFFER]
Prospect profile: [WHO YOU'RE REACHING OUT TO — role, company type, pain point]
Personalization hook: [SOMETHING SPECIFIC ABOUT THEM — recent post, company news, mutual connection]
Ask: [WHAT YOU WANT — 15-min call, demo, feedback]

Rules:
- Subject line (if email): curiosity-driven, under 8 words
- Opening: reference the personalization hook immediately
- Value prop: one sentence, focused on their outcome not your features
- Social proof: one brief credibility signal
- CTA: one specific, low-friction ask
- Total length: under 100 words`,
    promptZh: `撰写一条真正能获得回复的个性化冷启动外联消息。

渠道：【邮件 / LinkedIn / 其他】
我的产品/服务：【你提供什么】
目标对象：【对方的职位、公司类型、痛点】
个性化切入点：【关于对方的具体信息——近期文章、公司动态、共同联系人】
诉求：【你想要什么——15分钟通话、演示、反馈】

规则：
- 邮件主题行：激发好奇心，不超过10字
- 开头：立即引用个性化切入点
- 价值主张：一句话，聚焦对方的结果而非你的功能
- 社会证明：一个简短的可信度信号
- CTA：一个具体、低门槛的请求
- 总长度：不超过100字`,
    tags: ['outreach', 'sales', 'B2B'],
    tagsZh: ['外联', '销售', 'B2B'],
  },
  // Analysis — additional
  {
    id: 'competitor-analysis',
    title: 'Competitor Analysis',
    titleZh: '竞品分析',
    category: 'analysis',
    categoryZh: '分析',
    description: 'Conduct a structured competitor analysis to find your edge.',
    descriptionZh: '进行结构化竞品分析，找到你的差异化优势。',
    prompt: `Conduct a structured competitor analysis for the following context.

My product/service: [BRIEF DESCRIPTION]
Competitors to analyze: [LIST 3-5 COMPETITORS]
My target market: [WHO YOU'RE BOTH TARGETING]

For each competitor, analyze:
1. Core value proposition
2. Pricing model and positioning
3. Key strengths (what they do well)
4. Key weaknesses (where they fall short)
5. Target customer segment

Then provide:
- A comparison matrix (table format)
- 3 gaps or opportunities in the market
- Where I can realistically differentiate`,
    promptZh: `对以下背景进行结构化竞品分析。

我的产品/服务：【简要描述】
待分析竞品：【列出3-5个竞品】
目标市场：【你们共同针对的人群】

对每个竞品分析：
1. 核心价值主张
2. 定价模式和市场定位
3. 主要优势（做得好的地方）
4. 主要劣势（不足之处）
5. 目标客户细分

然后提供：
- 对比矩阵（表格形式）
- 市场中的3个空白或机会
- 我可以切实差异化的方向`,
    tags: ['competitive', 'strategy', 'market research'],
    tagsZh: ['竞品', '战略', '市场调研'],
  },
  {
    id: 'user-feedback',
    title: 'User Feedback Synthesis',
    titleZh: '用户反馈整合',
    category: 'analysis',
    categoryZh: '分析',
    description: 'Extract patterns and priorities from raw user feedback.',
    descriptionZh: '从原始用户反馈中提取规律和优先级。',
    prompt: `Analyze the following user feedback and extract actionable insights.

Product/Feature: [WHAT THE FEEDBACK IS ABOUT]
Feedback data:
[PASTE YOUR USER FEEDBACK — reviews, survey responses, support tickets, etc.]

Provide:
1. Top 3-5 themes (what users keep mentioning)
2. Sentiment breakdown (positive / neutral / negative with %)
3. Most requested features or improvements
4. Most common pain points
5. Surprising or unexpected findings
6. Recommended priorities based on frequency and severity`,
    promptZh: `分析以下用户反馈，提取可操作的洞察。

产品/功能：【反馈涉及的内容】
反馈数据：
【粘贴用户反馈——评论、问卷回复、客服工单等】

请提供：
1. 3-5个主要主题（用户反复提及的内容）
2. 情感分布（正面/中性/负面，附百分比）
3. 最常被请求的功能或改进
4. 最常见的痛点
5. 出乎意料的发现
6. 基于频率和严重程度的优先级建议`,
    tags: ['UX', 'product', 'user research'],
    tagsZh: ['用户体验', '产品', '用户研究'],
  },
  // Creative — additional
  {
    id: 'video-script',
    title: 'Video Script',
    titleZh: '视频脚本',
    category: 'creative',
    categoryZh: '创意',
    description: 'Write an engaging script for YouTube, TikTok, or any video format.',
    descriptionZh: '为 YouTube、抖音或任何视频格式撰写吸引人的脚本。',
    prompt: `Write a video script for the following content.

Platform: [YOUTUBE / TIKTOK / INSTAGRAM REELS / COURSE / etc.]
Topic: [WHAT THE VIDEO IS ABOUT]
Target audience: [WHO WILL WATCH IT]
Video length: [APPROXIMATE DURATION — e.g. 60 seconds, 5 minutes]
Goal: [EDUCATE / ENTERTAIN / SELL / BUILD BRAND]
Tone: [ENERGETIC / CALM / AUTHORITATIVE / CONVERSATIONAL]

Script format:
- Hook (first 3-5 seconds — make them stay)
- Main content with natural transitions
- B-roll suggestions in [brackets]
- CTA at the end
- Estimated speaking time per section`,
    promptZh: `为以下内容撰写视频脚本。

平台：【YouTube / 抖音 / 小红书 / 课程等】
主题：【视频内容】
目标受众：【谁会看】
视频时长：【大约时长，如60秒、5分钟】
目标：【教育/娱乐/销售/品牌建设】
语气：【活力/平静/权威/对话式】

脚本格式：
- 钩子（前3-5秒——让他们留下来）
- 带自然过渡的主体内容
- 用【括号】标注 B-roll 建议
- 结尾行动号召
- 每段预计说话时间`,
    tags: ['video', 'script', 'content creation'],
    tagsZh: ['视频', '脚本', '内容创作'],
  },
  {
    id: 'product-naming',
    title: 'Product / Brand Naming',
    titleZh: '产品/品牌命名',
    category: 'creative',
    categoryZh: '创意',
    description: 'Generate creative, memorable names for products or brands.',
    descriptionZh: '为产品或品牌生成有创意、易记忆的名称。',
    prompt: `Generate creative name options for the following product or brand.

What it is: [DESCRIBE THE PRODUCT OR BUSINESS]
Target audience: [WHO IT'S FOR]
Core values or personality: [3 ADJECTIVES — e.g. bold, trustworthy, playful]
Competitors' names (to avoid similarity): [LIST A FEW]
Any constraints: [MUST BE UNDER X CHARACTERS / MUST BE A REAL WORD / etc.]

Generate 15 name options across 3 styles:
- 5 descriptive names (clearly communicate what it does)
- 5 evocative names (suggest a feeling or idea)
- 5 invented/abstract names (unique, brandable)

For each: name + one-sentence rationale + domain availability note (just flag if it's a common word).`,
    promptZh: `为以下产品或品牌生成创意名称选项。

产品/业务描述：【描述产品或业务】
目标受众：【面向谁】
核心价值或个性：【3个形容词，如：大胆、可信、活泼】
竞品名称（避免相似）：【列举几个】
限制条件：【字数限制/必须是真实词汇等】

生成3种风格共15个名称选项：
- 5个描述性名称（清晰传达功能）
- 5个联想性名称（暗示某种感觉或理念）
- 5个创造性/抽象名称（独特、易于品牌化）

每个名称附：名称 + 一句话理由 + 域名可用性备注（仅标注是否为常见词）。`,
    tags: ['branding', 'naming', 'creative'],
    tagsZh: ['品牌', '命名', '创意'],
  },
  // Learning — additional
  {
    id: 'socratic-dialogue',
    title: 'Socratic Learning Session',
    titleZh: '苏格拉底式学习对话',
    category: 'learning',
    categoryZh: '学习',
    description: 'Learn any topic deeply through guided questions, not just answers.',
    descriptionZh: '通过引导性问题而非直接答案，深度学习任何主题。',
    prompt: `I want to learn [TOPIC] through a Socratic dialogue. Instead of just giving me answers, guide me to discover the key concepts myself through questions.

My current understanding: [WHAT YOU ALREADY KNOW OR THINK YOU KNOW]
My goal: [WHAT YOU WANT TO UNDERSTAND BY THE END]

Start by asking me a question that reveals what I already know. Then, based on my answers, ask follow-up questions that:
- Challenge my assumptions
- Help me discover gaps in my understanding
- Build toward the core insight
- Connect new ideas to things I already know

Only give direct explanations when I'm genuinely stuck. Keep each response to 1-2 questions maximum.`,
    promptZh: `我想通过苏格拉底式对话学习【主题】。不要直接给我答案，而是通过提问引导我自己发现关键概念。

我目前的理解：【你已经知道或认为自己知道的】
我的目标：【你希望最终理解什么】

从一个能揭示我已有认知的问题开始。然后根据我的回答，提出后续问题：
- 挑战我的假设
- 帮我发现理解中的空白
- 逐步引向核心洞察
- 将新想法与我已知的事物联系起来

只有当我真正卡住时才给出直接解释。每次回复最多提1-2个问题。`,
    tags: ['learning', 'critical thinking', 'Socratic'],
    tagsZh: ['学习', '批判性思维', '苏格拉底'],
  },
  {
    id: 'flashcards',
    title: 'Flashcard Generator',
    titleZh: '闪卡生成器',
    category: 'learning',
    categoryZh: '学习',
    description: 'Generate effective flashcards from any study material.',
    descriptionZh: '从任何学习材料生成高效的闪卡。',
    prompt: `Create a set of effective flashcards from the following study material.

Subject: [SUBJECT / TOPIC]
Material:
[PASTE YOUR NOTES, TEXTBOOK EXCERPT, OR TOPIC DESCRIPTION]

Number of cards: [HOW MANY — e.g. 20]
Difficulty level: [BASIC / INTERMEDIATE / ADVANCED]

Flashcard format:
**Q:** [Question — specific, unambiguous]
**A:** [Answer — concise, 1-3 sentences max]

Guidelines:
- One concept per card (no compound questions)
- Mix question types: definition, application, comparison, "why"
- Make questions specific enough that there's only one correct answer
- Include a few cards that test common misconceptions`,
    promptZh: `从以下学习材料生成一套高效的闪卡。

科目/主题：【科目/主题】
材料：
【粘贴你的笔记、教材摘录或主题描述】

卡片数量：【数量，如20张】
难度级别：【基础/中级/高级】

闪卡格式：
**问：**【问题——具体、无歧义】
**答：**【答案——简洁，最多1-3句话】

要求：
- 每张卡片只考察一个概念
- 混合问题类型：定义、应用、比较、"为什么"
- 问题要足够具体，只有一个正确答案
- 包含几张针对常见误解的卡片`,
    tags: ['flashcards', 'memorization', 'study'],
    tagsZh: ['闪卡', '记忆', '学习'],
  },
];

// Generator templates
export const GENERATOR_MODELS: Record<string, { en: string; zh: string; hint: string; hintZh: string }> = {
  chatgpt:   {
    en: 'ChatGPT (GPT-4o)',   zh: 'ChatGPT (GPT-4o)',
    hint:   'Structured, role-based prompts work best. Use numbered steps and explicit output format.',
    hintZh: '适合结构化、角色扮演式指令，明确编号步骤和输出格式效果最好。',
  },
  claude:    {
    en: 'Claude',             zh: 'Claude',
    hint:   'Prefers natural, conversational language with context and reasoning. Less rigid structure.',
    hintZh: '偏好自然对话式语言，提供背景和推理过程，不需要过于刻板的格式。',
  },
  deepseek:  {
    en: 'DeepSeek',           zh: 'DeepSeek',
    hint:   'Excels at technical tasks, code, and step-by-step reasoning. Be precise and specific.',
    hintZh: '擅长技术任务、代码和逐步推理，指令越精确越好。',
  },
  doubao:    {
    en: 'Doubao (豆包)',       zh: '豆包',
    hint:   'Good at creative Chinese content and casual conversation. Keep prompts natural.',
    hintZh: '擅长中文创意内容和日常对话，指令自然口语化效果更好。',
  },
  kimi:      {
    en: 'Kimi',               zh: 'Kimi',
    hint:   'Strong at long documents and reading comprehension. Great for summarization tasks.',
    hintZh: '擅长长文档处理和阅读理解，总结归纳类任务表现突出。',
  },
  ernie:     {
    en: 'ERNIE Bot (文心一言)', zh: '文心一言',
    hint:   'Optimized for Chinese writing and knowledge Q&A. Use clear Chinese instructions.',
    hintZh: '针对中文写作和知识问答优化，使用清晰的中文指令效果最佳。',
  },
  gemini:    {
    en: 'Gemini',             zh: 'Gemini',
    hint:   'Strong at research and factual tasks. Ask for sources or evidence where relevant.',
    hintZh: '擅长研究和事实性任务，可要求提供来源或依据。',
  },
  qwen:      {
    en: 'Qwen (通义千问)',      zh: '通义千问',
    hint:   'Alibaba model, good at Chinese business writing and structured analysis.',
    hintZh: '阿里模型，擅长中文商业写作和结构化分析。',
  },
};

export const GENERATOR_ROLES: Record<string, { en: string; zh: string }> = {
  // General / everyday
  student:        { en: 'Student',                  zh: '学生' },
  teacher:        { en: 'Teacher / Educator',       zh: '教师' },
  parent:         { en: 'Parent',                   zh: '家长' },
  job_seeker:     { en: 'Job Seeker',               zh: '求职者' },
  freelancer:     { en: 'Freelancer',               zh: '自由职业者' },
  // Business & professional
  entrepreneur:   { en: 'Entrepreneur / Founder',   zh: '创业者/创始人' },
  product_mgr:    { en: 'Product Manager',          zh: '产品经理' },
  marketer:       { en: 'Marketing Specialist',     zh: '营销专员' },
  sales:          { en: 'Sales Representative',     zh: '销售人员' },
  hr:             { en: 'HR Professional',          zh: 'HR 专员' },
  customer_svc:   { en: 'Customer Service Rep',     zh: '客服人员' },
  analyst:        { en: 'Business Analyst',         zh: '商业分析师' },
  // Creative & content
  writer:         { en: 'Professional Writer',      zh: '专业写作者' },
  designer:       { en: 'UX / Product Designer',    zh: 'UX/产品设计师' },
  journalist:     { en: 'Journalist / Reporter',    zh: '记者/媒体人' },
  // Technical
  developer:      { en: 'Software Developer',       zh: '软件开发者' },
  researcher:     { en: 'Researcher / Scientist',   zh: '研究员/科研人员' },
  // Specialized
  lawyer:         { en: 'Legal Professional',       zh: '法律从业者' },
  doctor:         { en: 'Healthcare Professional',  zh: '医疗从业者' },
  consultant:     { en: 'Consultant / Advisor',     zh: '顾问/咨询师' },
  custom:         { en: 'Custom (type below)',       zh: '自定义（下方输入）' },
};

export const GENERATOR_TONES: Record<string, { en: string; zh: string }> = {
  professional:  { en: 'Professional & Formal',   zh: '专业正式' },
  friendly:      { en: 'Friendly & Warm',         zh: '友好亲切' },
  concise:       { en: 'Concise & Direct',        zh: '简洁直接' },
  creative:      { en: 'Creative & Playful',      zh: '创意活泼' },
  academic:      { en: 'Academic & Rigorous',     zh: '学术严谨' },
  humorous:      { en: 'Humorous & Witty',        zh: '幽默风趣' },
  empathetic:    { en: 'Empathetic & Supportive', zh: '温暖共情' },
  persuasive:    { en: 'Persuasive & Compelling', zh: '有说服力' },
  technical:     { en: 'Technical & Precise',     zh: '技术精准' },
  storytelling:  { en: 'Narrative & Storytelling',zh: '叙事性' },
  inspiring:     { en: 'Inspiring & Motivational',zh: '激励人心' },
  casual:        { en: 'Casual & Conversational', zh: '随意轻松' },
  custom:        { en: 'Custom (type below)',      zh: '自定义（下方输入）' },
};
