export interface Tool {
  name: string;
  slug: string;
  url: string;
  tag: string;
  desc: string;
  category: string;
  categorySlug: string;
}

export const TOOLS: { category: string; slug: string; items: Tool[] }[] = [
  {
    category: 'AI编程工具',
    slug: 'coding',
    items: [
      { name: 'Cursor', slug: 'cursor', desc: '基于 VS Code 的 AI 编程编辑器，内置 Claude/GPT-4', url: 'https://cursor.com', tag: '免费/付费', category: 'AI编程工具', categorySlug: 'coding' },
      { name: 'GitHub Copilot', slug: 'github-copilot', desc: 'GitHub 官方 AI 代码补全，支持所有主流 IDE', url: 'https://github.com/features/copilot', tag: '付费', category: 'AI编程工具', categorySlug: 'coding' },
      { name: 'Windsurf', slug: 'windsurf', desc: 'Codeium 出品的 AI 编程编辑器，免费额度慷慨', url: 'https://codeium.com/windsurf', tag: '免费/付费', category: 'AI编程工具', categorySlug: 'coding' },
      { name: 'Trae', slug: 'trae', desc: '字节跳动出品的 AI 编程工具，国内可直接使用', url: 'https://trae.ai', tag: '免费', category: 'AI编程工具', categorySlug: 'coding' },
      { name: 'CodeGeeX', slug: 'codegeex', desc: '清华出品的免费 AI 编程插件，支持 VS Code/JetBrains', url: 'https://codegeex.cn', tag: '免费', category: 'AI编程工具', categorySlug: 'coding' },
      { name: 'Claude Code', slug: 'claude-code', desc: 'Anthropic 官方 CLI 编程助手，终端直接使用', url: 'https://claude.ai/code', tag: '付费', category: 'AI编程工具', categorySlug: 'coding' },
      { name: 'Bolt.new', slug: 'bolt-new', desc: '浏览器内全栈 AI 开发，一句话生成可运行应用', url: 'https://bolt.new', tag: '免费/付费', category: 'AI编程工具', categorySlug: 'coding' },
      { name: 'v0', slug: 'v0', desc: 'Vercel 出品，AI 生成 React/UI 组件，前端神器', url: 'https://v0.dev', tag: '免费/付费', category: 'AI编程工具', categorySlug: 'coding' },
      { name: 'Replit AI', slug: 'replit-ai', desc: '在线 IDE + AI 助手，无需配置环境即可运行代码', url: 'https://replit.com', tag: '免费/付费', category: 'AI编程工具', categorySlug: 'coding' },
      { name: 'Lovable', slug: 'lovable', desc: 'AI 全栈 Web 应用构建，自然语言生成可部署应用', url: 'https://lovable.dev', tag: '免费/付费', category: 'AI编程工具', categorySlug: 'coding' },
      { name: 'Devin', slug: 'devin', desc: '首个自主 AI 软件工程师，可独立完成完整开发任务', url: 'https://devin.ai', tag: '付费', category: 'AI编程工具', categorySlug: 'coding' },
      { name: 'Continue', slug: 'continue', desc: '开源 AI 编程助手，支持本地模型，VS Code/JetBrains 插件', url: 'https://continue.dev', tag: '免费', category: 'AI编程工具', categorySlug: 'coding' },
      { name: 'Amazon Q', slug: 'amazon-q', desc: 'AWS 出品的 AI 编程助手，深度集成 AWS 生态', url: 'https://aws.amazon.com/q/developer/', tag: '免费/付费', category: 'AI编程工具', categorySlug: 'coding' },
      { name: 'Aider', slug: 'aider', desc: '终端 AI 结对编程工具，支持 Git 自动提交，开源免费', url: 'https://aider.chat', tag: '免费', category: 'AI编程工具', categorySlug: 'coding' },
    ],
  },
  {
    category: 'AI大模型',
    slug: 'models',
    items: [
      { name: 'ChatGPT', slug: 'chatgpt', desc: 'OpenAI 旗舰对话模型，GPT-4o 免费可用', url: 'https://chatgpt.com', tag: '免费/付费', category: 'AI大模型', categorySlug: 'models' },
      { name: 'Claude', slug: 'claude', desc: 'Anthropic 出品，长文本理解和代码能力强', url: 'https://claude.ai', tag: '免费/付费', category: 'AI大模型', categorySlug: 'models' },
      { name: 'DeepSeek', slug: 'deepseek', desc: '国产顶级大模型，免费使用，推理能力强', url: 'https://chat.deepseek.com', tag: '免费', category: 'AI大模型', categorySlug: 'models' },
      { name: 'Gemini', slug: 'gemini', desc: 'Google 出品，与 Google 生态深度集成', url: 'https://gemini.google.com', tag: '免费/付费', category: 'AI大模型', categorySlug: 'models' },
      { name: 'Kimi', slug: 'kimi', desc: '月之暗面出品，长文本处理能力突出', url: 'https://kimi.moonshot.cn', tag: '免费/付费', category: 'AI大模型', categorySlug: 'models' },
      { name: '文心一言', slug: 'wenxin', desc: '百度出品，国内访问稳定，中文理解好', url: 'https://yiyan.baidu.com', tag: '免费', category: 'AI大模型', categorySlug: 'models' },
      { name: '豆包', slug: 'doubao', desc: '字节跳动出品的大模型，免费好用，国内访问流畅', url: 'https://www.doubao.com', tag: '免费', category: 'AI大模型', categorySlug: 'models' },
      { name: '通义千问', slug: 'qwen', desc: '阿里出品，支持长文本和多模态，免费使用', url: 'https://tongyi.aliyun.com', tag: '免费/付费', category: 'AI大模型', categorySlug: 'models' },
      { name: '讯飞星火', slug: 'xunfei-spark', desc: '科大讯飞出品，中文语音和文字能力强', url: 'https://xinghuo.xfyun.cn', tag: '免费/付费', category: 'AI大模型', categorySlug: 'models' },
      { name: 'Grok', slug: 'grok', desc: 'xAI 出品，马斯克旗下大模型，实时联网', url: 'https://grok.com', tag: '免费/付费', category: 'AI大模型', categorySlug: 'models' },
      { name: 'Llama', slug: 'llama', desc: 'Meta 出品的开源大模型，可本地部署，业界最强开源模型', url: 'https://llama.meta.com', tag: '免费', category: 'AI大模型', categorySlug: 'models' },
      { name: 'Mistral', slug: 'mistral', desc: '欧洲顶级开源大模型，高效 MoE 架构，性价比极高', url: 'https://mistral.ai', tag: '免费/付费', category: 'AI大模型', categorySlug: 'models' },
      { name: 'Microsoft Copilot', slug: 'copilot', desc: '微软 AI 助手，GPT-4 驱动，实时联网，深度集成 Office', url: 'https://copilot.microsoft.com', tag: '免费/付费', category: 'AI大模型', categorySlug: 'models' },
      { name: '零一万物', slug: 'yi', desc: '李开复创立，Yi 大模型，长上下文能力强', url: 'https://www.lingyiwanwu.com', tag: '免费/付费', category: 'AI大模型', categorySlug: 'models' },
      { name: '腾讯混元', slug: 'hunyuan', desc: '腾讯出品的大模型，深度集成微信、腾讯文档等生态', url: 'https://hunyuan.tencent.com', tag: '免费/付费', category: 'AI大模型', categorySlug: 'models' },
    ],
  },
  {
    category: 'AI写作工具',
    slug: 'writing',
    items: [
      { name: 'Notion AI', slug: 'notion-ai', desc: 'Notion 内置 AI，写作、总结、翻译一体化', url: 'https://notion.so', tag: '付费', category: 'AI写作工具', categorySlug: 'writing' },
      { name: '秘塔写作猫', slug: 'xiezuocat', desc: '国产 AI 写作助手，中文润色和纠错', url: 'https://xiezuocat.com', tag: '免费/付费', category: 'AI写作工具', categorySlug: 'writing' },
      { name: 'Jasper', slug: 'jasper', desc: '营销文案专用 AI，模板丰富', url: 'https://jasper.ai', tag: '付费', category: 'AI写作工具', categorySlug: 'writing' },
      { name: 'Copy.ai', slug: 'copy-ai', desc: '广告文案和社媒内容生成', url: 'https://copy.ai', tag: '免费/付费', category: 'AI写作工具', categorySlug: 'writing' },
      { name: 'Grammarly AI', slug: 'grammarly', desc: '英文写作润色神器，AI 辅助改写和纠错', url: 'https://grammarly.com', tag: '免费/付费', category: 'AI写作工具', categorySlug: 'writing' },
      { name: 'QuillBot', slug: 'quillbot', desc: '英文改写和摘要工具，学术写作常用', url: 'https://quillbot.com', tag: '免费/付费', category: 'AI写作工具', categorySlug: 'writing' },
      { name: 'Writesonic', slug: 'writesonic', desc: 'AI 营销写作平台，100+ 模板，支持 SEO 内容生成', url: 'https://writesonic.com', tag: '免费/付费', category: 'AI写作工具', categorySlug: 'writing' },
      { name: 'Rytr', slug: 'rytr', desc: '高性价比 AI 写作工具，$9/月起，40+ 写作模板', url: 'https://rytr.me', tag: '免费/付费', category: 'AI写作工具', categorySlug: 'writing' },
    ],
  },
  {
    category: 'AI图像生成',
    slug: 'image',
    items: [
      { name: 'Midjourney', slug: 'midjourney', desc: '目前最强的 AI 绘画工具，通过 Discord 使用', url: 'https://midjourney.com', tag: '付费', category: 'AI图像生成', categorySlug: 'image' },
      { name: 'DALL·E 3', slug: 'dalle-3', desc: 'OpenAI 出品，集成在 ChatGPT Plus 中', url: 'https://openai.com/dall-e-3', tag: '付费', category: 'AI图像生成', categorySlug: 'image' },
      { name: 'Stable Diffusion', slug: 'stable-diffusion', desc: '开源图像生成模型，可本地部署', url: 'https://stability.ai', tag: '免费', category: 'AI图像生成', categorySlug: 'image' },
      { name: '即梦 AI', slug: 'jimeng', desc: '字节跳动出品，国内可用的 AI 绘画工具', url: 'https://jimeng.jianying.com', tag: '免费/付费', category: 'AI图像生成', categorySlug: 'image' },
      { name: 'Flux', slug: 'flux', desc: '新一代开源图像模型，质量媲美 Midjourney', url: 'https://blackforestlabs.ai', tag: '免费/付费', category: 'AI图像生成', categorySlug: 'image' },
      { name: 'Adobe Firefly', slug: 'adobe-firefly', desc: 'Adobe 出品，商用版权安全的 AI 图像生成', url: 'https://firefly.adobe.com', tag: '免费/付费', category: 'AI图像生成', categorySlug: 'image' },
      { name: 'Leonardo AI', slug: 'leonardo-ai', desc: '游戏/创意设计向图像生成，风格多样', url: 'https://leonardo.ai', tag: '免费/付费', category: 'AI图像生成', categorySlug: 'image' },
      { name: 'Ideogram', slug: 'ideogram', desc: '擅长文字排版的 AI 图像生成，海报设计利器', url: 'https://ideogram.ai', tag: '免费/付费', category: 'AI图像生成', categorySlug: 'image' },
      { name: 'Canva AI', slug: 'canva-ai', desc: '全球最流行设计平台，内置 AI 生图、Magic Edit 等功能', url: 'https://canva.com', tag: '免费/付费', category: 'AI图像生成', categorySlug: 'image' },
      { name: 'Recraft', slug: 'recraft', desc: 'AI 矢量图和品牌插画生成，支持 SVG 输出，设计师首选', url: 'https://recraft.ai', tag: '免费/付费', category: 'AI图像生成', categorySlug: 'image' },
      { name: 'Playground AI', slug: 'playground-ai', desc: '每天 500 张免费图，业内最高免费额度，支持多种模型', url: 'https://playground.com', tag: '免费/付费', category: 'AI图像生成', categorySlug: 'image' },
      { name: 'Freepik AI', slug: 'freepik-ai', desc: 'Freepik 出品，海量素材库 + AI 生图，设计师必备', url: 'https://freepik.com', tag: '免费/付费', category: 'AI图像生成', categorySlug: 'image' },
      { name: 'Kolors 可图', slug: 'kolors', desc: '快手出品的开源图像模型，中文提示词支持优秀', url: 'https://kolors.kuaishou.com', tag: '免费', category: 'AI图像生成', categorySlug: 'image' },
    ],
  },
  {
    category: 'AI视频工具',
    slug: 'video',
    items: [
      { name: 'Sora', slug: 'sora', desc: 'OpenAI 出品的文生视频模型', url: 'https://sora.com', tag: '付费', category: 'AI视频工具', categorySlug: 'video' },
      { name: '可灵 AI', slug: 'kling', desc: '快手出品，国内领先的 AI 视频生成工具', url: 'https://klingai.com', tag: '免费/付费', category: 'AI视频工具', categorySlug: 'video' },
      { name: 'Runway', slug: 'runway', desc: '专业级 AI 视频编辑和生成平台', url: 'https://runwayml.com', tag: '免费/付费', category: 'AI视频工具', categorySlug: 'video' },
      { name: '即梦视频', slug: 'jimeng-video', desc: '字节跳动出品，文生视频，国内可用', url: 'https://jimeng.jianying.com', tag: '免费/付费', category: 'AI视频工具', categorySlug: 'video' },
      { name: 'Pika', slug: 'pika', desc: '简单易用的 AI 视频生成，支持图生视频', url: 'https://pika.art', tag: '免费/付费', category: 'AI视频工具', categorySlug: 'video' },
      { name: 'Luma Dream Machine', slug: 'luma-dream-machine', desc: '高质量 AI 视频生成，动态自然流畅', url: 'https://lumalabs.ai/dream-machine', tag: '免费/付费', category: 'AI视频工具', categorySlug: 'video' },
      { name: 'HeyGen', slug: 'heygen', desc: 'AI 数字人视频生成，支持多语言口型同步', url: 'https://heygen.com', tag: '免费/付费', category: 'AI视频工具', categorySlug: 'video' },
      { name: 'PixVerse', slug: 'pixverse', desc: '高质量 AI 视频生成，运动效果流畅，每日有免费额度', url: 'https://pixverse.ai', tag: '免费/付费', category: 'AI视频工具', categorySlug: 'video' },
      { name: '海螺 AI', slug: 'hailuo', desc: 'MiniMax 出品，人物动作表情逼真，国内可直接访问', url: 'https://hailuoai.com', tag: '免费/付费', category: 'AI视频工具', categorySlug: 'video' },
      { name: 'Vidu', slug: 'vidu', desc: '生数科技出品，国产高质量 AI 视频生成', url: 'https://vidu.studio', tag: '免费/付费', category: 'AI视频工具', categorySlug: 'video' },
      { name: '通义万象', slug: 'wanx', desc: '阿里出品，文生视频和图像生成，国内可用', url: 'https://tongyi.aliyun.com/wanxiang/', tag: '免费/付费', category: 'AI视频工具', categorySlug: 'video' },
    ],
  },
  {
    category: 'AI效率工具',
    slug: 'productivity',
    items: [
      { name: 'Perplexity', slug: 'perplexity', desc: 'AI 搜索引擎，带引用来源的智能问答', url: 'https://perplexity.ai', tag: '免费/付费', category: 'AI效率工具', categorySlug: 'productivity' },
      { name: 'Gamma', slug: 'gamma', desc: 'AI 自动生成 PPT 和演示文稿', url: 'https://gamma.app', tag: '免费/付费', category: 'AI效率工具', categorySlug: 'productivity' },
      { name: 'Dify', slug: 'dify', desc: '开源 AI 应用开发平台，快速搭建 AI 工作流', url: 'https://dify.ai', tag: '免费/付费', category: 'AI效率工具', categorySlug: 'productivity' },
      { name: 'Monica', slug: 'monica', desc: '浏览器 AI 助手，网页总结、翻译、写作', url: 'https://monica.im', tag: '免费/付费', category: 'AI效率工具', categorySlug: 'productivity' },
      { name: 'Otter.ai', slug: 'otter-ai', desc: 'AI 会议录音转写，自动生成会议摘要', url: 'https://otter.ai', tag: '免费/付费', category: 'AI效率工具', categorySlug: 'productivity' },
      { name: 'Beautiful.ai', slug: 'beautiful-ai', desc: 'AI 辅助 PPT 设计，自动排版美化', url: 'https://beautiful.ai', tag: '付费', category: 'AI效率工具', categorySlug: 'productivity' },
      { name: 'ChatPDF', slug: 'chatpdf', desc: '上传 PDF 直接对话，快速提取文档信息', url: 'https://chatpdf.com', tag: '免费/付费', category: 'AI效率工具', categorySlug: 'productivity' },
      { name: 'Google NotebookLM', slug: 'notebooklm', desc: 'Google 出品，基于你的资料问答，可一键生成播客', url: 'https://notebooklm.google.com', tag: '免费', category: 'AI效率工具', categorySlug: 'productivity' },
      { name: 'Manus', slug: 'manus', desc: '通用 AI 智能体，可自主完成深度研究、数据分析等复杂任务', url: 'https://manus.im', tag: '免费/付费', category: 'AI效率工具', categorySlug: 'productivity' },
      { name: 'Fireflies.ai', slug: 'fireflies', desc: 'AI 会议记录助手，自动转写、摘要、搜索会议内容', url: 'https://fireflies.ai', tag: '免费/付费', category: 'AI效率工具', categorySlug: 'productivity' },
    ],
  },
  {
    category: 'AI音频工具',
    slug: 'audio',
    items: [
      { name: 'Suno AI', slug: 'suno', desc: 'AI 一键生成完整歌曲，含人声和伴奏，风格任选', url: 'https://suno.com', tag: '免费/付费', category: 'AI音频工具', categorySlug: 'audio' },
      { name: 'ElevenLabs', slug: 'elevenlabs', desc: '最逼真的 AI 语音合成，声音克隆，多语言配音', url: 'https://elevenlabs.io', tag: '免费/付费', category: 'AI音频工具', categorySlug: 'audio' },
      { name: 'Udio', slug: 'udio', desc: 'AI 音乐创作平台，高质量生成，风格覆盖广', url: 'https://udio.com', tag: '免费/付费', category: 'AI音频工具', categorySlug: 'audio' },
      { name: 'Murf AI', slug: 'murf', desc: 'AI 配音神器，120+ 种语音，适合视频和播客制作', url: 'https://murf.ai', tag: '免费/付费', category: 'AI音频工具', categorySlug: 'audio' },
    ],
  },
];

// Flat list for easy lookup
export const ALL_TOOLS: Tool[] = TOOLS.flatMap(cat => cat.items);

export function getToolBySlug(slug: string): Tool | undefined {
  return ALL_TOOLS.find(t => t.slug === slug);
}

export function getSimilarTools(tool: Tool, n = 3): Tool[] {
  return ALL_TOOLS
    .filter(t => t.categorySlug === tool.categorySlug && t.slug !== tool.slug)
    .slice(0, n);
}
