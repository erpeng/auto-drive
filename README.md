# auto-drive

`auto-drive` 现在使用 `Astro + Starlight` 作为静态站点框架。

这不是原始知识库本体，而是面向 `https://erpeng.github.io/auto-drive` 的发布层。原始内容仍在外部 Obsidian vault 中维护。

## Source Of Truth

- canonical 内容库在外部 Obsidian vault
- 站点 repo 只负责把 vault 编译到 `src/content/docs/`
- 正确流程是：`raw -> Obsidian wiki -> compile -> Astro build -> deploy`
- 不要直接把生成后的 docs 内容当成主版本维护

## 固化规则

- 新文章进入站点的唯一正确路径是：先更新外部 vault 原始文件，再运行 `python3 scripts/build_site.py` 编译到 `src/content/docs/`，最后再构建和发布。
- 不要直接手改 `src/content/docs/` 里的页面内容。这里是发布层产物，不是主编辑区。
- GitHub Actions 只负责把仓库里已经提交的内容构建成站点，不会读取你本地的 vault，也不会替你补跑 compile。
- 任何“新增文章没出现在站上”的问题，先检查两件事：
  1. 文章是否已经进入外部 vault 的 `raw/` 或 `wiki/`
  2. 本地是否已经重新运行 `python3 scripts/build_site.py`

## 技术栈

- Astro
- Starlight
- Python 编译脚本 `scripts/build_site.py`

## 内容来源

- 默认读取外部 vault：`../../Desktop/obsidian`
- 也可以通过环境变量 `AUTO_DRIVE_VAULT` 指定 vault 根目录
- 编译输出目录：`src/content/docs/`

## 日常工作流

1. 在 Obsidian vault 的 `raw/` 中引入或整理材料。
2. 先更新 vault 里的 `wiki/` 页面。
3. 重新编译站点内容：

```bash
python3 scripts/build_site.py
```

或者：

```bash
export AUTO_DRIVE_VAULT=../../Desktop/obsidian
python3 scripts/build_site.py
```

4. 本地预览：

```bash
npm install
npm run dev
```

5. 确认站点无误后，再提交到 GitHub 触发部署。

## 新增文章时，哪些页面会更新

当前站点的更新机制分两类：自动更新页，和需要手工维护的导览页。

### 自动更新

- 文章详情页：
  - 只要你在 vault 的 `wiki/` 或 `raw/` 新增了 markdown，并重新运行 `python3 scripts/build_site.py`，对应详情页就会生成。
- 左侧侧边栏分组：
  - `总览 / 主题 / 公司 / 人物 / 来源 / 原文` 这几个分组，都是按 `src/content/docs/` 里的目录自动生成。
  - 所以新增文章后，只要被编译进对应目录，侧边栏会自动出现。
- 站内链接：
  - 如果其他页面里已经用 wiki link 链到了这篇新文章，重新 compile 后会自动转成站内链接。
- 页面头部信息：
  - 判断页的 `更新时间 / 来源数`，原文页的 `发布时间 / 外部原文`，都来自 vault frontmatter。
  - 这些字段变了，重新 compile 后会自动反映到站点。
- 全站索引：
  - `site-index` 来自 vault 里的 `wiki/index.md`。
  - 如果你把新文章加进 `wiki/index.md`，compile 后它会自动更新。

### 不会自动更新，需要手工维护

- 首页：
  - 首页是人工策展页，不是自动索引。
  - 新增文章不会自动出现在首页的“精选入口”或“判断档案”里。
  - 如果这篇新文章值得作为入口页，需要手工修改首页生成逻辑。
- `raw` 资料库首页：
  - 这个页面也是手工挑选的起始阅读入口。
  - 新增原文不会自动出现在“从这里开始”里，但会自动出现在左侧 `原文` 目录里。

### 现在各类内容的触发条件

- 新增 `raw/` 原文：
  - 触发：外部 vault 的 `raw/` 下新增文件，并重新 compile。
  - 自动更新：对应原文详情页、左侧 `原文` 目录。
  - 不自动更新：首页、`raw` 首页推荐入口、`site-index`。
- 新增 `wiki/companies/`：
  - 触发：外部 vault 的 `wiki/companies/` 下新增文件，并重新 compile。
  - 自动更新：公司详情页、左侧 `公司` 目录。
  - 如果其他文章链接了它，这些引用也会自动转为站内链接。
  - 不自动更新：首页精选、`site-index`（除非你同步更新 `wiki/index.md`）。
- 新增 `wiki/people/`：
  - 触发：外部 vault 的 `wiki/people/` 下新增文件，并重新 compile。
  - 自动更新：人物详情页、左侧 `人物` 目录。
  - 不自动更新：首页精选、`site-index`（除非你同步更新 `wiki/index.md`）。
- 新增 `wiki/themes/`：
  - 触发：外部 vault 的 `wiki/themes/` 下新增文件，并重新 compile。
  - 自动更新：主题详情页、左侧 `主题` 目录。
  - 不自动更新：首页精选、`site-index`（除非你同步更新 `wiki/index.md`）。
- 新增 `wiki/overview/`：
  - 触发：外部 vault 的 `wiki/overview/` 下新增文件，并重新 compile。
  - 自动更新：总览详情页、左侧 `总览` 目录。
  - 不自动更新：首页入口排序、`site-index`（除非你同步更新 `wiki/index.md`）。
- 新增 `wiki/sources/`：
  - 触发：外部 vault 的 `wiki/sources/` 下新增文件，并重新 compile。
  - 自动更新：来源详情页、左侧 `来源` 目录。
  - 不自动更新：首页、`site-index`（除非你同步更新 `wiki/index.md`）。

## 本地启动

```bash
npm install
python3 scripts/build_site.py
npm run dev
```

## 构建

```bash
npm run build
```

构建产物在 `dist/`。

## GitHub Pages

- `astro.config.mjs` 预设：
  - `site: https://erpeng.github.io`
  - `base: /auto-drive`
- GitHub Actions 工作流会在远端执行 `npm ci && npm run build` 并部署 `dist/`
- 因为外部 Obsidian vault 不在仓库里，所以远端不会重新 compile；你需要先在本地运行 `python3 scripts/build_site.py`，把更新后的 `src/content/docs/` 提交上去

仓库设置需要确认一次：

1. 打开 GitHub 仓库 `erpeng/auto-drive`
2. 进入 `Settings -> Pages`
3. 把 `Source` 设为 `GitHub Actions`
