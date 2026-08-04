# X-Border Listing Image Skill

多平台电商 Listing 资产生成 skill。基于产品白底图 + 卖点,生成 Listing 文案、图片规划与提示词、**真实渲染的上架/营销图**,以及 Excel 汇总表。

支持 **Amazon(参考实现,最完整)/ Temu / Noon(中东)**。图片通过 **X-Border 图片工具**(MCP)渲染 —— 本 skill **不持有任何图片 key**,凭证在 X-Border 服务端。

> skill 标识(frontmatter `name`)、本地目录与 GitHub 仓库均为
> `xborder-image-skill`。市场迁移仓库时保留既有 identifier,避免已安装副本失联。

## 多平台支持

| 平台 | 文案规范 | 图片槽位 | 档案 |
|---|---|---|---|
| **Amazon** | 标题≤150 / 5×(150-200)五点 / 1500-2000 描述 / 250B 后台词 | AM-01 主图, AS-02~09 副图, AD-01~07 A+ | 本文件 STEP 1/3/3B + `references/platforms/amazon.md` |
| **Temu** | 精简标题 / 3-6 卖点 / 短描述 / 属性驱动 | TM-01 主图, TS-02~07 | `references/platforms/temu.md` |
| **Noon** | 双语 EN/AR 标题 / 3-5 亮点 / 类目属性 | NM-01 主图, NS-02~07 | `references/platforms/noon.md` |

共享部分(执行模式、产品解析、图片后端、图片工艺原则、Excel)所有平台复用;每个平台只写自己的**文案规则 + 槽位 + 合规**。加新平台见 `references/platforms/README.md`。

## 图片后端(X-Border)

`references/image-backend.md` 定义了如何把图片 brief 变成真实图片:

- **逐张出图(默认)**:`generateImage`(`prompt`=槽位 brief,`referenceImageUrl`=产品图 URL,可选 `model`:`nano-banana-pro` 默认 / `seedream-4.5` / `qwen-edit-multiangle`)。
- **整套图片**:先识图建立一份共享商品基线,再按平台槽位逐张调用
  `generateImage`;每张复用相同参考图、商品数量/款式和事实约束。
- **数量编辑**:识别个/件/只/顶/台/pcs 等数量表达;用户已明确总数和每款数量时
  直接按原值写入提示词,例如“深灰色 1 台、白色 2 台、共 3 台”。
- **无参考图**:`generateImageFromText`;识图分析:`analyzeProductImage`。
- 无 MCP 工具时降级为只输出提示词。上传图以 URL 传入,非 base64。

## 文件结构

```text
xborder-image-skill/
├── SKILL.md                      # 平台感知的编排 + Amazon 详细流程
├── agents/
│   └── openai.yaml
├── references/
│   ├── image-backend.md          # X-Border 图片工具契约(可复用)
│   ├── amazon-image-strategy.md  # Amazon 副图深度策略
│   └── platforms/
│       ├── README.md             # 复用模型 + 加平台 checklist
│       ├── amazon.md
│       ├── temu.md
│       └── noon.md
├── scripts/
│   └── generate_excel.py
└── README.md
```

## 安装 / 使用

**主路径 —— X-Border AI(lobehub-xb 聊天):** 通过 X-Border 市场发布(登记 GitHub 来源 `owner/repo`),用户在技能商店一键安装,聊天里上传产品图 + 卖点即可触发,图片自动走 X-Border。

**Codex(兼容):**

```bash
git clone https://github.com/X-Border/xborder-image-skill.git
mkdir -p ~/.codex/skills
cp -R xborder-image-skill ~/.codex/skills/xborder-image-skill
```

## 基础用法(示例)

```text
# Amazon(默认)
根据白底图和卖点生成Amazon副图,家庭风格、暖色
只生成Listing文案
完整8张,AS-02到AS-09都要
重新生成AS-07对比图

# Temu
生成Temu上架图,含尺寸图
Temu整套图,marketplace_basic

# Noon
生成Noon副图,中英双语,中东场景
Noon整套上架图,英语阿拉伯语
```

## Slot 对照表

**Amazon 副图:** AS-02 核心卖点 / AS-03 功能拆解 / AS-04 尺寸 / AS-05 场景 / AS-06 细节 / AS-07 对比 / AS-08 步骤 / AS-09 包装。
**Amazon A+:** AD-01 品牌主视觉 / AD-02 痛点解决 / AD-03 卖点详情 / AD-04 结构细节 / AD-05 场景扩展 / AD-06 尺寸适配 / AD-07 安装维护。
**Temu:** TM-01 主图 / TS-02 卖点 / TS-03 场景 / TS-04 细节材质 / TS-05 尺寸规格(服饰鞋类需尺码表) / TS-06 白底多角度 / TS-07 包装配件。
**Noon:** NM-01 主图 / NS-02 卖点 / NS-03 场景(中东文化合规) / NS-04 细节材质 / NS-05 白底多角度 / NS-06 尺寸规格(双语尺码表) / NS-07 包装配件。

## 设计原则

先理解产品与买家关注点,再安排每张图表达什么;每张图只讲一个核心观点;先做版式决策;标题需有画面证明,无标题时产品/人物/细节/标注也要把卖点讲清;主色随产品/品牌/类目灵活选;不重复出图、不凑数;参考图只做策略参考不照抄;副图缩略图可读、层次强;详情页/A+ 更完整讲故事。各平台合规(Amazon 白底主图、Temu 主图纯净、Noon 中东文化+双语)见各自档案。

## Excel 输出

```bash
python3 scripts/generate_excel.py \
  --product "Product Name" --title "Title" \
  --b1 "..." --b2 "..." --b3 "..." --b4 "..." --b5 "..." \
  --description "..." --backend "backend terms" \
  --output "Listing_Product.xlsx"
```
