# 第三方来源与声明

本仓库是个人维护的技能集合，其中包含原创内容、改编内容和受公开资料启发的内容。下表依据技能中已有的来源说明及与上游文件的对照整理，不把改编内容重新声明为独立原创。

本仓库的 MIT 许可证适用于原创内容与新增改动。上游内容保留原有版权和适用许可证；下列文本在 2026-10-12 从来源仓库取得。未打包上游项目的完整代码或技能集合。

| 本仓库位置 | 来源 | 关系与声明 |
| --- | --- | --- |
| `skills/think/` | [Tw93 / Waza · think](https://github.com/tw93/Waza/tree/main/skills/think) | 方案判断、规划流程及参考资料的改编 |
| `skills/check/` | [Tw93 / Waza · check](https://github.com/tw93/Waza/tree/main/skills/check) | 发布与交付流程、发布面检查及 `release_gate.py` 的改编与复用 |
| `skills/code-review/` | [Tw93 / Waza · check](https://github.com/tw93/Waza/tree/main/skills/check) | 当前通用版本复用 `audit_signals.py` 并改编审查资料；与 Claude Code 官方同名插件命令分别维护，此项说明这些文件的来源 |
| `skills/hunt/` | [Tw93 / Waza · hunt](https://github.com/tw93/Waza/tree/main/skills/hunt) | 故障排查流程和参考资料的改编与复用 |
| `skills/health/` | [Tw93 / Waza · health](https://github.com/tw93/Waza/tree/main/skills/health) | 代理配置检查、采集脚本、检查脚本和参考资料的改编与复用 |
| `skills/read/` | [Tw93 / Waza · read](https://github.com/tw93/Waza/tree/main/skills/read) | 内容读取流程与抓取脚本的改编与复用；同时保留其对乔木项目的致谢 |
| `skills/write/` | [Tw93 / Waza · write](https://github.com/tw93/Waza/tree/main/skills/write) | 中英文写作说明、参考资料和检查脚本的改编与复用 |
| `skills/learn/` | [Tw93 / Waza · learn](https://github.com/tw93/Waza/tree/main/skills/learn) | 参考上游研究工作流，重新编写本地研究入口 |
| `skills/ui/` | [Tw93 / Waza · ui](https://github.com/tw93/Waza/tree/main/skills/ui) | 界面工作流和设计参考资料的改编；保留其他设计来源 |
| `skills/adversarial-review/` | [poteto/noodle](https://github.com/poteto/noodle) | 原说明标注为改编；保留 [MIT 许可证](licenses/poteto-noodle-LICENSE.txt) |
| `skills/how/` | [poteto/how](https://github.com/poteto/how) | 原说明标注为改编；保留 [MIT 许可证](licenses/poteto-how-LICENSE.txt) |
| `skills/read/scripts/fetch.sh`、`fetch_feishu.py`、`fetch_weixin.py` | [joeseesun/qiaomu-markdown-proxy](https://github.com/joeseesun/qiaomu-markdown-proxy) | 原脚本标注为受其实现思路启发；保留致谢及 [MIT 许可证](licenses/joeseesun-qiaomu-markdown-proxy-LICENSE.txt) |
| `skills/ui/references/design-reference.md` | [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | 部分检查来源；本地资料为整理与改写，保留 [Apache 2.0 许可证](licenses/pbakaus-impeccable-LICENSE.txt) 和 [上游声明](licenses/impeccable-NOTICE.md) |
| `skills/ui/references/design-reference.md` | [getdesign.md](https://getdesign.md)、[VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md) | 设计资料来源；保留 [MIT 许可证](licenses/getdesign-LICENSE.txt) |
| `skills/ui/references/design-reference.md` | [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) | 部分检查来源；保留 [MIT 许可证](licenses/Leonxlnx-taste-skill-LICENSE.txt) |
| `skills/write/references/write-technical.md` | [danyuchn/asd-ste100-skill](https://github.com/danyuchn/asd-ste100-skill) | 原说明标注为参考部分清晰表达原则的独立改写；保留 [MIT 许可证](licenses/danyuchn-asd-ste100-skill-LICENSE.txt) |

## 工程方法参考

2026-10-14 新增的以下内容为独立整理，以公开技术资料核对机制；未复制来源教程、代码或图像，不因此改变上述改编技能的署名与许可证。

| 本仓库位置 | 核对来源 | 用途 |
| --- | --- | --- |
| `skills/think/references/system-design.md` | [Kotlin 协程文档](https://kotlinlang.org/docs/coroutines-basics.html)、[AWS 事务发件箱](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html) | 结构化并发的生命周期、事务与重复事件边界 |
| `skills/think/references/product-experiments.md` | [Microsoft Research 在线实验](https://www.microsoft.com/en-us/research/publication/online-experimentation-at-microsoft/)、[随机单位与租户实验](https://www.microsoft.com/en-us/research/articles/why-tenant-randomized-a-b-test-is-challenging-and-tenant-pairing-may-not-work/) | 随机化与因果证据、组间干扰和实验限制 |
| `skills/hunt/references/performance-diagnosis.md` | [OpenTelemetry Traces](https://opentelemetry.io/docs/concepts/signals/traces/)、[Google SRE 服务目标](https://sre.google/sre-book/service-level-objectives/)、[错误预算策略](https://sre.google/workbook/error-budget-policy/) | 链路关联、服务质量指标、目标与错误预算 |

2026-10-15 新增的维护方法参考如下。内容为独立整理，未复制博客全文、原始提示词、代码或图像；保留既有技能的上游声明。

| 本仓库位置 | 核对来源 | 用途 |
| --- | --- | --- |
| `skills/prune/references/retirement-evidence.md`、`skills/hunt/references/ci-maintenance.md`、`skills/health/references/instruction-replay.md` 及对应入口、`skills/test-audit/SKILL.md` | Rodrigo Roim / OpenAI，[Maintaining software with the GPT-6 family](https://developers.openai.com/blog/maintaining-software-with-the-gpt-6-family)（2026-10-14） | 跨来源删除证据、废弃开关与间接依赖审计、按历史量化 CI 收益、偶发失败修复及单条指令对照重放 |

## Tw93 / Waza

特别感谢 [Tw93](https://github.com/tw93)，也是 [Mole](https://github.com/tw93/Mole) 的作者。本仓库上表中的 9 项技能参考或改编自他的 [Waza](https://github.com/tw93/Waza)，并包含直接复用的脚本与资料。技能内容的直接来源按 Waza 署名，Mole 链接用于说明作者身份。本仓库是个人维护的改编版本。

Waza 的版权声明为 `Copyright (c) 2026 Tw93`，采用 [MIT 许可证](licenses/tw93-Waza-LICENSE.txt)。每项受影响技能的目录内也保留 `LICENSE`，单独复制、安装或分发该技能时应一并保留。

来源在 2026-10-12 与 [Waza 提交 `a6d28b0e18f6`](https://github.com/tw93/Waza/tree/a6d28b0e18f6c199c45d9b8d9e6012c040c22161) 核对；该提交用于文件与许可证比对，不表示所有文件最初取自这一版本。

写作技能不包含 ASD-STE100 的完整标准或批准词典，也不声称满足该标准认证。需要正式采用标准时，查阅 [ASD-STE100 官方资料](https://www.asd-ste100.org/)。
