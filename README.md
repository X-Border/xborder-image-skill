# X-Border Listing Image Skill

多平台电商 Listing 资产生成 skill。基于产品白底图 + 卖点,生成 Listing 文案、图片规划与提示词、**真实渲染的上架/营销图**,以及 Excel 汇总表;支持带风格参考图出图、多角度商品图,以及对已有套图**只审不生成**的诊断模式。

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

## 执行模式

| 模式 | 触发示例 | 产出 |
|---|---|---|
| 全套 Full kit | "帮我做listing" | 文案 + 副图集 + Excel |
| 仅图片集 | "生成副图" | 推荐 5-7 张(按价值定量,不凑数) |
| 仅文案 | "只生成Listing文案" | 标题 / 五点 / 描述 / 后台词 |
| 单槽位 | "重新生成AS-07对比图" | 指定槽位 1 张 |
| 详情页 / A+ | "生成A+页面" | AD-01~07 模块集 |
| 预览批 | "先来4张" | 1-4 张预览 |
| 诊断 / 审图 | "诊断一下我这套副图" | 逐张 + 整套问题报告与修复路由,不出图 |

**品类感知**:识别产品品类后加载 `references/categories/` 对应档案(买家关注点优先级、轮播图式、场景/人设语言);无匹配档案时按品类常识推导,禁止跨品类移植道具与人设。

**卖点提取**:用户没给或给得薄时,按三级证据构建卖点表——用户事实 > 识图事实 > AI 推断(必须标注,不得上图为数字断言),整套图前软性邀请确认一次,可跳过。

## 图片后端(X-Border)

`references/image-backend.md` 定义了如何把图片 brief 变成真实图片:

- **逐张出图(默认)**:`generateImage`(`prompt`=槽位 brief,`referenceImageUrl`=产品图 URL,可选 `model`:`nano-banana-pro` 默认 / `seedream-4.5` / `qwen-edit-multiangle`)。
- **整套图片**:先识图建立一份共享商品基线,再按平台槽位逐张调用
  `generateImage`;每张复用相同参考图、商品数量/款式和事实约束。
- **一致性校验(防偏移)**:整套图与数量/款式编辑默认在出图后用 `analyzeProductImage`
  对照共享基线做漂移审计(形状/颜色/Logo/部件位置/配件/数量);发现偏移只针对受影响
  单张点名偏移属性、加强约束重出(限一次)。≥5 张整套先出 2 张样张,审计通过再补齐
  其余槽位;审计通过前所有结果按"待复核预览"表述。
- **数量编辑**:识别个/件/只/顶/台/pcs 等数量表达;用户已明确总数和每款数量时
  直接按原值写入提示词,例如“深灰色 1 台、白色 2 台、共 3 台”。
- **输入组合**:仅商品图(默认)/ 商品图+参考图(商品图占 `referenceImageUrl` 身份锚位,
  参考图以风格 DNA 进提示词;用户要求强贴风格时改走 `generateImageFromText` 双参考
  `[商品图, 参考图]`,并强制漂移审计)/ 仅参考图(只出概念方向图,不算 listing 资产)/
  多角度商品图(识图用全部,出图按槽位选最合适角度)。
- **无参考图**:`generateImageFromText`;识图分析:`analyzeProductImage`。
- 无 MCP 工具时降级为只输出提示词。上传图以 URL 传入,非 base64。

## 质量与一致性保障

SKILL.md 开头是一份**不可协商执行契约**,与细则冲突时契约优先。核心保障:

- **证据锁定**:数字参数、认证、性能与对比断言必须来自用户或识图结果;定性词不授权
  数字("安静" ≠ "28 dB")。
- **防偏移闭环**:商品图永占 `referenceImageUrl` 身份锚位(风格参考图不得顶替)+
  共享商品基线逐张复用 + 出图后漂移审计 + ≥5 张整套样张先行。
- **修复路由**:坏在哪层修哪层——文案错只改文案、产品漂移点名偏移属性重出单张
  (限一次)、多张同病才动共享基线,绝不默认整套重出。
- **计划锁定**:shot plan 定稿后写提示词不得重新规划、不得改动图上文字口径;槽位号
  (AS-04 / AD-03)等内部词汇不得渲染上图。
- **软门哲学**:歧义确认与样张检查点都是可跳过的提醒("直接出完"即生效),绝不循环
  追问。
- **诚实汇报**:未调工具不声称出图;未过审计的结果一律按"待复核预览"表述,不虚报
  检查结论。

## 文件结构

```text
xborder-image-skill/
├── SKILL.md                      # 平台感知的编排 + Amazon 详细流程
├── agents/
│   └── openai.yaml
├── references/
│   ├── image-backend.md          # X-Border 图片工具契约(可复用)
│   ├── amazon-image-strategy.md  # Amazon 副图深度策略(品类无关)
│   ├── categories/
│   │   ├── README.md             # 品类档案复用模型 + 加品类 checklist
│   │   └── fitness-equipment.md  # 健身器材品类档案
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
参考这张竞品图的风格,按我们的产品出场景图
诊断一下我这套副图有什么问题

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

先理解产品与买家关注点,再安排每张图表达什么;卖点按证据分级提取:用户事实 > 识图事实 > AI 推断,推断必须标注且不得上图为数字断言;每张图只讲一个核心观点;先做版式决策;标题需有画面证明,无标题时产品/人物/细节/标注也要把卖点讲清;主色随产品/品牌/类目灵活选;不重复出图、不凑数;参考图只做策略参考不照抄(吉祥物/人设等风格 DNA 做抽象迁移,不复制品牌与身份);副图缩略图可读、层次强;详情页/A+ 由首屏 2-4 个 claim seed 牵引整页叙事,各模块文案角色与句式不重复。各平台合规(Amazon 白底主图、Temu 主图纯净、Noon 中东文化+双语)见各自档案。

## Excel 输出

```bash
python3 scripts/generate_excel.py \
  --product "Product Name" --title "Title" \
  --b1 "..." --b2 "..." --b3 "..." --b4 "..." --b5 "..." \
  --description "..." --backend "backend terms" \
  --output "Listing_Product.xlsx"
```
