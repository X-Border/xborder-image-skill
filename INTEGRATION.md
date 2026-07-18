# 集成与使用指南 · xborder-image-skill

> 一句话:**注册到 X-Border 市场 = 让 skill「可被安装」,不等于「自动能用」。**
> 还需要:① 部署侧配置就位 → ② 用户在聊天里安装它 → ③ 图片后端在线。

---

## 1. 架构回顾(谁持有什么 key)

skill 本身是纯 markdown,**不持有任何 key**。真正花钱/用 key 的是两处独立调用:

```
用户在 lobehub-xb 聊天里触发 skill(上传产品图 + 卖点 + 说平台)
        │  skill(markdown,无 key)被注入模型上下文
        ▼
① 文本:xb-fast 大模型读 skill、写 listing 文案
   key = XBORDER_API_KEY(配在 lobehub-xb)──▶ OpenRouter
        │
② 图片:skill 调 x-border MCP 工具 generateImage / generateListingImageSet
   ├─ 默认 xborder-ai:WORKER_BASE_URL → n11-server /image/ecom/edit
   │                   key = REPLICATE_API_TOKEN(在 n11-server)──▶ Replicate
   └─ 或 linkfox:key = LINKFOX_*(在 X-Border api-server)──▶ LinkFox
```

- skill 发布/安装只搬 markdown,不搬凭证。
- 文本 key(`XBORDER_API_KEY`)和图片 key(`REPLICATE_API_TOKEN` / `LINKFOX_*`)是**不同服务上的不同配置**。

---

## 2. 前置条件 checklist(部署侧,一次性)

在「注册到市场」之外,确认这些就位,聊天里才能真正出图:

- [ ] **lobehub-xb**:`XBORDER_MARKET_URL` 已设 → 技能商店显示 X-Border 的 skill,并出现「安装到 XBorder AI」按钮(自动开启 `xborder_market` feature flag)。
- [ ] **lobehub-xb**:用户用 SSO 登录 → X-Border MCP 自动安装(`xb-mcp-seed`)并自动启用(agentPlugins 自动加 `x-border`),图片工具才可调。
- [ ] **聊天用 xborder provider / `xb-fast`**(默认即是)。
- [ ] **X-Border api-server 图片供应商就位**(二选一):
  - **xborder-ai(默认,推荐)**:`feat/xborder-ai-image-provider` 分支已合并并部署;`WORKER_BASE_URL` 指向 n11-server;n11-server 配了 `REPLICATE_API_TOKEN`;Replicate 上 `nano-banana-pro`/`seedream-4.5`/`qwen-edit-multiangle` 可用。
  - **linkfox**:`XBORDER_IMAGE_DRAW_PROVIDER=linkfox` 且 `LINKFOX_*` 配好。
- [ ] (批量套图工具 `generateListingImageSet` / `generateProductMarketingImages` 始终走 LinkFox,如果要用它们,`LINKFOX_*` 也要配。)

> 具体值以你们的部署环境为准,上面是各项对应的开关/变量名。

---

## 3. 发布 skill 到市场

X-Border 后台:**设置 → 市场管理 → 登记 GitHub 来源**

```
repo:        shmilyvidian/amazon-listing-generator-skill   ← owner/name,不是完整 URL
identifier:  xborder-image-skill                           ← 与 SKILL.md frontmatter 的 name 一致
path:        (留空,SKILL.md 在仓库根)
name/描述/分类/tags: 按需
```

需要 market 管理员权限(developer 角色 或在 `MARKET_ADMIN_USER_IDS` 白名单)。

---

## 4. 更新 skill(改了代码之后)

**不会自动同步**,三跳都手动:

```
① 你 git push 到 GitHub
② X-Border 后台该 skill 点「重同步」→ 生成新版本快照
③ 已安装的用户重新点一次安装/更新 → 各自副本才更新
```

- 每次更新顺手 bump `SKILL.md` frontmatter 的 `version:`(不改会自动生成时间戳版本)。
- 重新安装是按 identifier 就地 upsert:内容变了才更新,没变则跳过,不会重复。
- 想省掉第②步,可给 X-Border 加个 GitHub webhook 自动 `resync`(第③步无法自动)。

---

## 5. 在聊天里使用

1. **安装**:技能商店 → 搜 `xborder-image-skill` → 「安装到 XBorder AI」。
2. **触发**:开 xborder 对话,上传产品白底图 + 给卖点 + 说明平台。
3. **示例**:

```text
# Amazon(默认)
根据白底图和卖点生成 Amazon 副图,家庭风格、暖色
只生成 Listing 文案
完整 8 张,AS-02 到 AS-09 都要
重新生成 AS-07 对比图

# Temu
生成 Temu 上架图,含尺寸图
Temu 整套图

# Noon
生成 Noon 副图,中英双语,中东场景
Noon 整套上架图,英语阿拉伯语
```

- 图片默认逐张出(保留精细美术),说「整套/快」会走一键预设。
- 想指定模型:「用 seedream 出图」→ 走 `seedream-4.5`。

---

## 6. 排查(Troubleshooting)

| 现象 | 可能原因 / 处理 |
|---|---|
| 技能商店里看不到这个 skill | `XBORDER_MARKET_URL` 没配;或市场里 status 不是 `published`;或没「重同步」 |
| 装了但聊天里不触发 | 描述没命中触发词 → 换更明确说法(带平台名 + "生成副图/上架图");确认对话开了 xborder provider |
| 图不生成、只回提示词 | `x-border` MCP 没连(让用户重新 SSO 登录);或图片供应商没配(`WORKER_BASE_URL` + `REPLICATE_API_TOKEN`,或 `LINKFOX_*`) |
| 报错 "x-border-ai 出图需要参考图" | `generateImage` 是编辑模型必须带参考图;纯文生/无产品图请改用 `generateImageFromText`(参考图可选)。或上传产品图 URL 后再试,或临时把 `XBORDER_IMAGE_DRAW_PROVIDER=linkfox` |
| 成图带中文水印 / 1688 文字 | 源图太脏 → 走两遍法(先出干净底图再做槽位);大水印去不干净时换干净白底原图(见 SKILL.md STEP 0「Source-image hygiene」) |
| 已安装用户拿不到更新 | 市场是快照,让用户重新安装一次 |
| 成图出现中文(非 CN 平台) | 已由净化规则约束,若仍出现是模型残留 → 重出或换模型 |

---

## 7. key / 配置速查

| 用途 | 变量 | 位置 |
|---|---|---|
| 文本大模型 | `XBORDER_API_KEY`(+ 可选 `XBORDER_PROXY_URL`) | lobehub-xb |
| 市场接入 | `XBORDER_MARKET_URL`(+ 可选 `XBORDER_MARKET_TOKEN`) | lobehub-xb |
| 图片供应商选择 | `XBORDER_IMAGE_DRAW_PROVIDER`(默认 `xborder-ai`) | X-Border api-server |
| 图片默认模型 | `XBORDER_IMAGE_MODEL`(默认 `nano-banana-pro`) | X-Border api-server |
| 调 worker | `WORKER_BASE_URL` | X-Border api-server |
| 图片生成 key(xborder-ai) | `REPLICATE_API_TOKEN` | n11-server |
| 图片生成 key(linkfox / 批量套图) | `LINKFOX_APP_ID` / `LINKFOX_PRIVATE_KEY` / `LINKFOX_API_BASE` | X-Border api-server |
| 市场管理员 | developer 角色 或 `MARKET_ADMIN_USER_IDS` | X-Border api-server |

> 相关代码:SKILL.md(平台流程)、`references/image-backend.md`(图片后端契约)、`references/platforms/*`(各平台规范);X-Border `packages/api-server/src/mcp/server.ts`、`services/xborderAiImage.ts`、`services/linkfox.ts`。
