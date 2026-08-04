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
② 图片:skill 调 x-border MCP 工具
   generateImage / generateImageFromText / analyzeProductImage
   └─ X-Border api-server → 图片 worker / 模型供应商
      服务端持有供应商凭证,skill 和客户端都不接触 key
```

- skill 发布/安装只搬 markdown,不搬凭证。
- 文本 key(`XBORDER_API_KEY`)和图片供应商凭证是**不同服务上的不同配置**。

---

## 2. 前置条件 checklist(部署侧,一次性)

在「注册到市场」之外,确认这些就位,聊天里才能真正出图:

- [ ] **lobehub-xb**:`XBORDER_MARKET_URL` 已设 → 技能商店显示 X-Border 的 skill,并出现「安装到 XBorder AI」按钮(自动开启 `xborder_market` feature flag)。
- [ ] **lobehub-xb**:用户用 SSO 登录 → X-Border MCP 自动安装(`xb-mcp-seed`)并自动启用(agentPlugins 自动加 `x-border`),图片工具才可调。
- [ ] **聊天用 xborder provider / `xb-fast`**(默认即是)。
- [ ] **X-Border api-server 图片链路就位**:`WORKER_BASE_URL` 可用,worker 已配置当前图片模型所需的供应商凭证。
- [ ] MCP 暴露 `generateImage`、`generateImageFromText`、`analyzeProductImage`;整套图由 skill 按槽位逐张调用 `generateImage`,当前没有公开批量预设工具。

> 具体值以你们的部署环境为准,上面是各项对应的开关/变量名。

---

## 3. 发布 skill 到市场

X-Border 后台:**设置 → 市场管理 → 登记 GitHub 来源**

```
repo:        X-Border/xborder-image-skill                  ← owner/name,不是完整 URL
identifier:  github.shmilyvidian.xborder-image-skill       ← 保留现有 identifier,避免已安装副本失联
path:        (留空,SKILL.md 在仓库根)
name/描述/分类/tags: 按需
```

需要 market 管理员权限(developer 角色 或在 `MARKET_ADMIN_USER_IDS` 白名单)。

---

## 4. 更新 skill(改了代码之后)

GitHub push 后需要把市场快照同步到新版本:

```
① 你 git push 到 GitHub
② X-Border 后台该 skill 点「重同步」→ 生成新版本快照
③ 非自动嵌入的安装副本需要重新安装/更新;自动嵌入副本在登录对账或刷新后更新
```

- 每次更新顺手 bump `SKILL.md` frontmatter 的 `version:`(不改会自动生成时间戳版本)。
- 重新安装是按 identifier 就地 upsert:内容变了才更新,没变则跳过,不会重复。
- 想省掉第②步,可给 X-Border 加 GitHub webhook 自动 `resync`。

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

- 图片默认逐张出;整套图先等待识图建立共享商品基线,再按槽位逐张调用,以便每张图
  使用明确构图且保持相同 SKU、数量、款式和事实约束。未经证实的数字参数不得写入图片。
- 想指定模型:「用 seedream 出图」→ 走 `seedream-4.5`。

---

## 6. 排查(Troubleshooting)

| 现象 | 可能原因 / 处理 |
|---|---|
| 技能商店里看不到这个 skill | `XBORDER_MARKET_URL` 没配;或市场里 status 不是 `published`;或没「重同步」 |
| 装了但聊天里不触发 | 描述没命中触发词 → 换更明确说法(带平台名 + "生成副图/上架图");确认对话开了 xborder provider |
| 图不生成、只回提示词 | `x-border` MCP 没连(让用户重新 SSO 登录);或图片 worker / 供应商凭证未配置 |
| 报错 "x-border-ai 出图需要参考图" | `generateImage` 是编辑模型,必须带参考图;纯文生/无产品图请改用 `generateImageFromText`,或上传产品图后再试 |
| 成图带中文水印 / 1688 文字 | 源图太脏 → 走两遍法(先出干净底图再做槽位);大水印去不干净时换干净白底原图(见 SKILL.md STEP 0「Source-image hygiene」) |
| 已安装用户拿不到更新 | 市场是快照,让用户重新安装一次 |
| 成图出现中文(非 CN 平台) | 已由净化规则约束,若仍出现是模型残留 → 重出或换模型 |

---

## 7. key / 配置速查

| 用途 | 变量 | 位置 |
|---|---|---|
| 文本大模型 | `XBORDER_API_KEY`(+ 可选 `XBORDER_PROXY_URL`) | lobehub-xb |
| 市场接入 | `XBORDER_MARKET_URL`(+ 可选 `XBORDER_MARKET_TOKEN`) | lobehub-xb |
| 图片默认模型 | `XBORDER_IMAGE_MODEL`(默认 `nano-banana-pro`) | X-Border api-server |
| 调 worker | `WORKER_BASE_URL` | X-Border api-server |
| 图片生成供应商凭证 | 以当前 worker 部署为准 | 图片 worker |
| 市场管理员 | developer 角色 或 `MARKET_ADMIN_USER_IDS` | X-Border api-server |

> 相关代码:SKILL.md(平台流程)、`references/image-backend.md`(图片后端契约)、`references/platforms/*`(各平台规范);X-Border `packages/api-server/src/mcp/server.ts` 与图片服务实现。
