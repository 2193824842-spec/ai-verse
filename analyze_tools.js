const aiverse = [
  'Cursor','GitHub Copilot','Windsurf','Trae','CodeGeeX','Claude Code',
  'Bolt.new','v0','Replit AI','Lovable','Devin','Continue','Amazon Q','Aider',
  'ChatGPT','Claude','DeepSeek','Gemini','Kimi','Wenxin','Doubao','Qwen',
  'Xunfei Spark','Grok','Llama','Mistral','Microsoft Copilot','Yi','Hunyuan',
  'Notion AI','Xiezuocat','Jasper','Copy.ai','Grammarly AI','QuillBot','Writesonic','Rytr',
  'Midjourney','DALLE 3','Stable Diffusion','Jimeng AI','Flux','Adobe Firefly',
  'Leonardo AI','Ideogram','Canva AI','Recraft','Playground AI','Freepik AI','Kolors',
  'Sora','Kling AI','Runway','Jimeng Video','Pika','Luma Dream Machine','HeyGen',
  'PixVerse','Hailuo AI','Vidu','Wanx',
  'Perplexity','Gamma','Dify','Monica','Otter.ai','Beautiful.ai','ChatPDF',
  'Google NotebookLM','Manus','Fireflies.ai',
  'Suno AI','ElevenLabs','Udio','Murf AI',
];

const seofarm = [
  'ChatGPT','Claude','Gemini','Copilot','Midjourney','DALLE 3','Stable Diffusion',
  'Leonardo AI','Sora','Runway Gen3','Pika','HeyGen','GitHub Copilot','Cursor',
  'Codeium','Tabnine','ElevenLabs','Murf AI','Suno','Perplexity','You.com',
  'Notion AI','Jasper','Copy.ai','Grammarly','Canva AI','Figma AI','Framer AI',
  'Gamma','Beautiful.ai','Otter.ai','Fireflies.ai','Descript','Synthesia','Luma AI',
  'Replicate','Hugging Face','Anthropic Console','OpenAI Platform','Zapier AI',
  'Adobe Firefly','DeepSeek','NovelAI','AI Dungeon','Jan','OpenAI Codex',
  'Visily','LogoAI','GoodBird','Image to Prompt Generator','Warp Intro Creator',
  'Free AI Video Upscaler','RabbitAI','Plotica','midReal','LightPDF','IndexFlow',
  'Sentence 3.0','CrushOn AI','Janitor AI','StoryChat','SillyTavern','Roleplay AI',
  'Xoul.ai','Chai','Layla','Talkie AI','Dreamily'
];

function norm(s) {
  return s.toLowerCase().replace(/\s/g,'').replace(/-/g,'').replace(/\./g,'').replace(/_/g,'');
}

const avMap = {};
aiverse.forEach(n => { avMap[norm(n)] = n; });
const sfMap = {};
seofarm.forEach(n => { sfMap[norm(n)] = n; });

const avKeys = new Set(Object.keys(avMap));
const sfKeys = new Set(Object.keys(sfMap));

const overlap = [...avKeys].filter(k => sfKeys.has(k));
const onlyAV = [...avKeys].filter(k => !sfKeys.has(k));
const onlySF = [...sfKeys].filter(k => !avKeys.has(k));

console.log('AI-Verse总数:', aiverse.length);
console.log('SEO-Farm总数:', seofarm.length);
console.log('重叠:', overlap.length);
console.log('仅AI-Verse:', onlyAV.length);
console.log('仅SEO-Farm:', onlySF.length);
console.log('');
console.log('=== 重叠工具 (' + overlap.length + '个) ===');
overlap.sort().forEach(k => console.log('  ' + avMap[k]));
console.log('');
console.log('=== 仅AI-Verse (' + onlyAV.length + '个) ===');
onlyAV.sort().forEach(k => console.log('  ' + avMap[k]));
console.log('');
console.log('=== 仅SEO-Farm (' + onlySF.length + '个) ===');
onlySF.sort().forEach(k => console.log('  ' + sfMap[k]));
