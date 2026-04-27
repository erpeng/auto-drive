---
title: 自动驾驶行业总览
description: 当前语料呈现出的自动驾驶行业，不是一个单一赛道，而是三条彼此勾连但评价体系完全不同的战线：Robotaxi、L2 与 L4、智驾芯片与生态。很多争论其实来自把三条战线混成一条。苏箐的新材料又补了一条横向约束：无论选择哪条技术路线，量产智驾最终都要回到计算平台集成、用户坑位和发版确定性。
pageLabel: 总览
lastUpdated: 2026-04-27
sourceCount: 19
---

## 三条主线

### 1. Robotaxi / L4

这一条追求的是在限定区域内真正做到无人化运营，核心指标不是“好不好用”，而是“能否不依赖人类接管地活下来并扩张”。在当前语料里，[Waymo](/auto-drive/companies/waymo/) 是默认标杆；中国最常被放在这一战线上的公司是 [百度 Apollo Go](/auto-drive/companies/apollo-go/)、[小马智行](/auto-drive/companies/note-fd360bc0cd/)、[文远知行](/auto-drive/companies/note-eac959b5c9/)。[特斯拉](/auto-drive/companies/note-3f426f96e0/) 处于高度关注但身份有争议的位置。

### 2. L2+ / 城市 NOA / 量产辅助驾驶

这一条是量产车上的产品竞争，关键变量是成本、覆盖车型、交付效率、客户关系与体验。这里的主要主角是 [Momenta](/auto-drive/companies/momenta/)、华为乾崑、车企自研，以及试图从芯片切入系统的 [地平线](/auto-drive/companies/note-217712ba17/)。这一战线和 L4 共用部分技术积木，但商业节奏、约束条件和评判方式完全不同。

### 3. 上游基础设施

包括 [智驾芯片与生态](/auto-drive/themes/note-30fb7c170c/) 与 [激光雷达](/auto-drive/themes/note-ab41bf10ba/)。它们既服务于 L2，也服务于 L4，但价值逻辑不同。芯片叙事更像“量价齐升的基础设施”，激光雷达叙事更像“性能确定性与制造降本的平衡”。

## 当前语料里的核心矛盾

- **L2 是否通向 L4**：[楼天城](/auto-drive/people/note-3307c75e01/) 明确认为不是，甚至可能越做越远；而 [曹旭东](/auto-drive/people/note-576d343d7f/) 则试图用“一条主线、两条腿”把量产辅助驾驶与 Robotaxi 接成同一个飞轮。
- **L2 是否最终仍能靠 scaling 走到更高阶无人能力**：[刘先明](/auto-drive/people/note-1e8ce634d4/) 明确回答“可以”，而 [于骞](/auto-drive/people/note-28f6fd5edb/) 也在用“接近 L4 的城市体验”重写量产桌的上限想象。
- **数据是不是越多越好**：Momenta 代表“狂热数据驱动”；楼天城和彭军都更强调高质量训练环境、世界模型和可探索性，而不是机械堆积人类驾驶数据。
- **世界模型是否只是新名词**：最新楼天城访谈说明，争议已经从“有没有世界模型”推进到“世界模型精度如何、能否自我诊断、能否驱动开发组织”。这让 [世界模型](/auto-drive/themes/note-3f42a3b35e/) 成为横跨 L4、量产智驾和物理 AI 的新主题。
- **激光雷达是不是必须**：特斯拉代表纯视觉路径；楼天城和李一帆都从不同角度强调激光雷达带来的测距确定性。
- **生态能否成为护城河**：[地平线](/auto-drive/companies/note-217712ba17/) 的核心命题不是单个芯片是否能打，而是能否成为中立基础设施。
- **算力是不是越大越好**：轻舟的新材料提醒，单颗 J6M 也可能做出高体验城市 NOA；真正被比拼的是工程体系和识别能力，而不只是名义 TOPS。
- **有没有“黄金子弹”**：苏箐的新材料给了地平线阵营内部的自我约束：大模型、端到端、星空芯片、舱驾一体都不是一劳永逸的答案，真正决定生死的是物理集成、填坑能力和稳定发版。([对话地平线苏箐：做产品的人，第二天一醒过来又开始焦虑了](/auto-drive/raw/note-96decd7e63/))
- **商业化优先还是终局优先**：L2 量产和 L4 终局看似共处一个行业，实际经常是两种公司、两种组织和两种 KPI。

## 当前阶段的粗略格局

- L4/Robotaxi 仍是少数玩家的长期战。
- 城市 NOA 已进入头部集中期。
- 城市 NOA 的量产桌内部也开始分叉成三类：量产操作系统派、生态 + 方案商派、车企自研派。
- 世界模型正在从“训练技术”变成新的行业分水岭：谁能用它制造高质量样本、诊断系统缺陷并缩短城市迁移时间，谁才可能把物理 AI 叙事落到运营结果上。
- 上游硬件的价值，正在从“是否有”转为“谁能以更低总成本提供更高确定性”。苏箐关于舱驾一体的判断进一步说明，硬件竞争会越来越像系统集成竞争：内存平面、带宽、资源池、器件数量和未来 OTA 空间都会进入同一张账。
- 量产智驾的评价标准正在变厚：不仅要看体验进步，还要看新范式能不能被收进两三个月一轮的稳定发版节奏里。
- 中国公司的优势更多体现在量产节奏、供应链、成本和产业协同。

## 这套语料最像什么

它不像一份标准行业报告，更像一组来自牌桌不同位置的人口述史。它的价值不在于给出单一正确答案，而在于把不同玩家的世界观并排放在一起。

## 相关页面

- [自动驾驶牌桌](/auto-drive/overview/note-767a041b9f/)
- [Robotaxi](/auto-drive/themes/robotaxi/)
- [L2 与 L4](/auto-drive/themes/l2-l4/)
- [技术路线](/auto-drive/themes/note-0ef0d64de9/)
- [世界模型](/auto-drive/themes/note-3f42a3b35e/)
- [智驾芯片与生态](/auto-drive/themes/note-30fb7c170c/)
- [激光雷达](/auto-drive/themes/note-ab41bf10ba/)
- [小鹏汽车](/auto-drive/companies/note-c86bb992e0/)
- [轻舟智航](/auto-drive/companies/note-63ddce497a/)
- [地平线](/auto-drive/companies/note-217712ba17/)
- [苏箐](/auto-drive/people/note-30cb260e4a/)

## 主要来源

- [市场不信自动驾驶了，但他们还信](/auto-drive/raw/note-24c67bb21c/)
- [Robotaxi 出行帝国，能再造特斯拉？](/auto-drive/raw/robotaxi/)
- [和楼天城聊Robotaxi：“L2越厉害，就离L4越远”](/auto-drive/raw/robotaxi-l2-l4/)
- [对话小马智行楼天城：只靠端到端无法通向 L4，模仿优秀司机令人绝望](/auto-drive/raw/l4/)
- [对话小马智行楼天城：驯服脱缰的野马，让 AI 自我进化](/auto-drive/raw/ai/)
- [对话Momenta曹旭东：智驾航海家、多发钱的CEO和“吃狗粮”的人｜远光灯](/auto-drive/raw/momenta-ceo/)
- [地平线还是想当安卓](/auto-drive/raw/note-ca24a1b923/)
- [对话禾赛李一帆：你仔细想行业的机会来自哪？是国家的、民族的机会](/auto-drive/raw/note-1c22224657/)
- [对话小鹏汽车刘先明：押注 “极简模型”，我花了全公司最多的钱](/auto-drive/raw/note-c7a96a607d/)
- [对话轻舟智航于骞：比亚迪的想法被我们实现了](/auto-drive/raw/note-79f296a152/)
- [对话地平线苏箐：做产品的人，第二天一醒过来又开始焦虑了](/auto-drive/raw/note-96decd7e63/)
