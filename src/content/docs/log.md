---
title: Wiki Log
description: '2026 04 14 source complete | ingest 小鹏刘先明 / 轻舟于骞两篇新材料 ingest 新来源 对话小鹏汽车刘先明：押注
  “极简模型”，我花了全公司最多的钱 。 ingest 新来源 对话轻舟智航于骞：比亚迪的想法被我们实现了 。 新增 wiki/people/刘先明.md 与 wiki/people/于骞.md
  。 新增 '
pageLabel: 更新日志
lastUpdated: 2026-04-14
---

## [2026-04-14] source-complete | ingest 小鹏刘先明 / 轻舟于骞两篇新材料

- ingest 新来源 `对话小鹏汽车刘先明：押注 “极简模型”，我花了全公司最多的钱`。
- ingest 新来源 `对话轻舟智航于骞：比亚迪的想法被我们实现了`。
- 新增 `wiki/people/刘先明.md` 与 `wiki/people/于骞.md`。
- 新增 `wiki/companies/小鹏汽车.md` 与 `wiki/companies/轻舟智航.md`。
- 更新 `wiki/themes/技术路线.md`，补入“拆掉 Language”的极简 VLA 路线，以及“云端世界模型 + 强化学习”这条训练基础设施路线。
- 更新 `wiki/themes/L2 与 L4.md`，把行业分歧从“断裂 vs 桥接”扩成“断裂 vs 桥接 vs 连续”三种立场。
- 更新 `wiki/themes/智驾芯片与生态.md` 与 `wiki/companies/地平线.md`，把单 J6M 城市 NOA 对国产芯片生态的验证补进去。
- 更新 `wiki/overview/自动驾驶牌桌.md` 与 `wiki/overview/自动驾驶行业总览.md`，把量产桌细分成量产操作系统派、生态 + 方案商派、车企自研派三类。
- 更新 `wiki/index.md` 与 `wiki/sources/来源总表.md`，把来源总数同步为 `22` 并补入新入口。

## [2026-04-09] schema | 新增 raw -> wiki 更新分流原则

- 在 `AGENTS.md` 中补充“Update routing principles”。
- 明确新资料进入 `raw/` 后，不是机械全站更新，而是按变化层级分流：
  - 对象级变化更新 `wiki/companies/` 或 `wiki/people/`
  - 问题级变化更新 `wiki/themes/`
  - 地图级变化更新 `wiki/overview/`
  - 来源登记与归档更新 `wiki/sources/`
- 明确一篇新 `raw/` 材料可以同时触发多个页面更新，但必须先判断它改变的是对象、问题、地图还是来源层。
- 明确 public site 不是主编辑面：新资料必须先更新 `raw/`，再更新 `wiki/`，最后才允许编译到站点；禁止绕过 `wiki/` 直接改站点。

## [2026-04-06] seed | 初始自动驾驶 wiki 建库

- 读取当前 `raw/` 下 15 篇自动驾驶相关文章。
- 建立 `wiki/` 目录结构与 `AGENTS.md` 维护规则。
- 创建总览页、主题页、公司页、人物页与来源总表。
- 当前 seed 的重心是行业结构、技术路线分歧、关键公司比较与 founder worldview。
- 待后续补充的重点是华为乾崑、百度一手资料、更多车企自研样本，以及新来源到来后的增量维护流程。

## [2026-04-06] schema-upgrade | 人物 / 公司页升级为判断档案

- 将人物页和公司页的写法从“摘要页”升级为“Bayesian dossier”。
- 新骨架统一为：`事实底稿`、`底层约束`、`主模型`、`替代模型`、`反证 / 竞争性解释`、`更新信号`。
- 人物页开始显式区分观察、推断、约束和更新信号，避免悬浮人设。
- 公司页开始引入组织原型、创生公式、市场误读和失效信号。
- 置信度统一采用 `高 / 中 / 低置信`，不使用伪精确概率。

## [2026-04-06] ingest | 小马智行 CFO 新材料

- ingest 新来源 `对话小马智行CFO王皓俊：自动驾驶行业最大的竞争对手是自己`。
- 更新 `wiki/companies/小马智行.md`，补入 UE 转正、Top line 优先、不打低价策略、车队扩张和城市复制逻辑。
- 更新 `wiki/sources/来源总表.md`。

## [2026-04-06] people | 补充小马智行管理层人物页

- 新增 `wiki/people/彭军.md`。
- 新增 `wiki/people/王皓俊.md`。
- 更新 `wiki/index.md` 与 `wiki/companies/小马智行.md` 的人物入口链接。

## [2026-04-06] ingest | 第二批新增文章同步

- ingest 新来源 `对谈文远知行韩旭：智驾终局论是妄想，不存在必赢的技术路线`。
- ingest 新来源 `投资人回顾小马、文远口水仗：连卖车的都不会搞得这么难看`。
- ingest 新来源 `Robotaxi 出故障，不能只会停在半路`。
- ingest 新来源 `对话卓驭沈劭劼：从大疆到百亿智驾公司 CEO 的十年之路`。
- 将 `造车下半场，不再有弯道超车` 登记进来源总表，作为鸿蒙智行 / 华为乾崑对照材料。
- 更新 `wiki/companies/文远知行.md`、`wiki/companies/百度 Apollo Go.md`、`wiki/companies/Waymo.md`、`wiki/companies/小马智行.md`。
- 更新 `wiki/themes/Robotaxi.md`、`wiki/themes/技术路线.md`、`wiki/overview/自动驾驶牌桌.md`。
- 新增 `wiki/companies/卓驭.md`、`wiki/people/韩旭.md`、`wiki/people/沈劭劼.md`。
