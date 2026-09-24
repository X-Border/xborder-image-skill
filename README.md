# X-Border Listing Image Skill

多平台商品 Listing 内容与图片工作流。它把产品事实整理为有证据来源的标准化数据，再按目标站点/类目生成文案、图片策划与图像资产，最后用市场范围明确的规则做发布前检查并导出 Excel。

支持 Amazon、Temu、Noon、Walmart Marketplace、eBay、Etsy、TikTok Shop、Ozon、Shopee、Mercado Libre。覆盖的是**内容准备、图片策划/生成、规范映射和预检**；不登录店铺，不上传商品，不定价/管库存，也不替代平台审核。

## 工作流程

1. **确定站点范围**：平台、国家/站点、类目、买家语言、listing 类型。市场不明时只能生成市场中立草稿，不能宣称合规。
2. **建立产品事实账本与卖点表**：分清用户提供、成功识图、官方文件与 AI 推断；按买家问题、证据强度、利益、视觉证明和宣称风险排序。推断不写成产品事实。
3. **加载类目字段**：使用当前 Seller Center/API 类目模板。缺失必填字段时标为未解析，不猜平台属性。
4. **生成平台内容与图片计划**：按照平台档案里的字段、语言和图像政策；图像生成通过 X-Border 图片工具。
5. **逐槽规划和生成**：每张图记录买家问题、证据、视觉证明、布局、精确文字和存在理由；主图约束按平台执行，副图按规则做差异化表达。
6. **运行预检与发布门**：只自动检查带市场范围的规则和 manifest 数据；再记录实物一致性、事实与宣称、SKU/包装、文字/视觉、语言、文件和 Seller Center 的人工终审。
7. **导出结构化清单与工作簿**：JSON/Excel 含事实账本、卖点表、逐图计划和生产状态，作为人工上架或后续 API 接入的交接件。

## 平台与规则范围

| 平台 | 已整理的规则范围 | 关键边界 |
|---|---|---|
| Amazon | US 标题/搜索词快照，Amazon 图片规则入口 | 类目图片数、字段及部分限制在 Seller Central 核对 |
| Temu | US 资料入口与创作建议 | 公开资料不足，图片数量/尺寸/类目字段需 Seller Center 确认 |
| Noon | AE 数值快照，SA/EG 继承后加本地检查 | A+ 与商品图库是两种资源；逐类目确认主图规则 |
| Walmart | CA 图片档案；US 商品类型 schema | CA 数值不能直接套到 US；US 按 item type/feed schema |
| eBay | US 图片数、文件、最小边长指导 | 类目 aspects、变体和商品状况规则动态 |
| Etsy | US 图片文件/像素建议，原创照片与 mockup 边界 | 商品须符合 Etsy 商品资格；披露商品本身 AI 制作与生成营销图分开处理 |
| TikTok Shop | US listing 图片/质量快照；listing 图片不得用数字渲染，图上不得加营销文字/图形 | 要用真实商品照片；AI 套图只能作为不上传的预览，副图也遵守无叠字规则 |
| Ozon | 官方 Seller API 入口 | 图片/API 字段、最大数量与必填属性随方法/版本/类目变化 |
| Shopee | 首版跨站共用图片规划/导出基线；按目标站点切换语言。新加坡官方 PDP/Ads 建议单独标注 | 1024 px 导出目标、800 px 预检下限、2 MB、3–9 张作为可配置项目默认值；通常规划 6–8 张，不代表全站强制限制 |
| Mercado Libre | Global Selling CBT 图片 API 规则 | 指定目的站点；图片数量及必填属性取决于目的站点和类目 |

所有数字约束、来源链接、站点范围和复核日期集中在 [`platform-rules.json`](references/platforms/platform-rules.json)。规则状态区分可拦截要求、官方建议和创作建议；动态 schema 与 Seller Center 检查列为人工任务。档案不会自动证明图片内容真实或平台审核通过。

## 标准数据与工具

- [`listing-manifest.schema.json`](references/platforms/listing-manifest.schema.json)：规范化输入/导出结构，覆盖平台/站点/语言、商品与变体、类目模板、事实账本、文案字段、平台专属字段及图片资产。
- [`validate_listing.py`](scripts/validate_listing.py)：读取 manifest 与规则档案，输出来源、错误、提醒、人工核对项及 `production_readiness`。状态为 `blocked`、`concept_preview`、`human_review_required` 或 `candidate_for_manual_upload`。候选状态依赖人工在最终文件上完成并记录终审，不等于平台批准。
- [`generate_excel.py`](scripts/generate_excel.py)：同一份 manifest 输出 Listing、Media、Product Facts、Selling Points、Preflight & Sources 五个工作表，方便逐张设计/合规交接。
- [`research-notes.md`](references/platforms/research-notes.md)：开源电商作图 skill 的架构借鉴记录和政策研究边界。

预检核对 manifest 中声明的像素/文件元数据，不会打开二进制图片，也无法判断白底、实物一致性、文字渲染质量、类目审核或账号资格。URL 无法读取、平台实时规则或具体图片未人工检查时，生产状态必须保留为人工复核。

运行方式：

```bash
python3 scripts/validate_listing.py listing-manifest.json
python3 scripts/validate_listing.py listing-manifest.json --json
python3 scripts/validate_listing.py listing-manifest.json --require-candidate-for-manual-upload
python3 scripts/generate_excel.py listing-manifest.json --output out/listing.xlsx
```

严格发布门会在非 `candidate_for_manual_upload` 状态时返回 exit code 3；数据/规则错误返回 1，成功达到候选状态返回 0。

Excel 导出需要 `openpyxl`。先按 JSON Schema 结构准备 `listing-manifest.json`；批量成图前应保存卖点表、逐图证明计划。完整发布门字段和数据结构见 [`INTEGRATION.md`](INTEGRATION.md)。
可从 [`Shopee SG 样例清单`](examples/shopee-sg-listing-manifest.json)开始；样例事实只用于演示，不能直接上架。

## 开源方案借鉴

参考 [motiful/product-shots](https://github.com/motiful/product-shots) 的模块化商品图工作流，以及 [Gayaya999/ecommerce-detail-page-generator](https://github.com/Gayaya999/ecommerce-detail-page-generator) 的证据账本、结构化中间数据和规则预检思路。实现采用自己的字段/代码和平台规则，没有复制仓库源文件；详见 [`research-notes.md`](references/platforms/research-notes.md)。

## 图片能力

- 逐槽生成 Listing 图、细节图、尺寸/尺码信息图或平台支持的详情页模块；亚马逊继续使用 AM/AS/AD 槽位。
- 其他平台按各自档案规划内容，槽位号是内部标识，不代表平台官方槽位。默认以真实商品图为身份锚点，生成图不能改变商品、配件、款式和数量。
- 主图是否允许合成、图上文字、背景、构图、AI/mockup 用法均以对应市场和类目规则为准。证据不全时输出待核对资产，不能标成已合规。
- 审图模式可只出问题报告，不生成替换图；按用户要求再修复指定槽位。

## 安装

```bash
git clone https://github.com/X-Border/xborder-image-skill.git
mkdir -p ~/.codex/skills
cp -R xborder-image-skill ~/.codex/skills/xborder-image-skill
```

仓库 skill 名称为 `xborder-image-skill`。图像渲染依赖 X-Border MCP；脚本可独立用于规范数据预检和 Excel 导出。
