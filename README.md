# Agent Skills

在日常开发中维护的 17 个 AI 代理技能。覆盖需求梳理、问题排查、代码审查、架构精简、界面优化、研究和写作。

这些技能采用 `SKILL.md` 目录格式，可用于 Codex、Claude Code 等支持 Agent Skills 的工具。部分技能基于公开项目改编或受到公开资料启发，来源见 [第三方声明](THIRD_PARTY_NOTICES.md)。本仓库收录个人维护的通用技能，不包含平台内置技能、同步的第三方技能包或私有项目专用技能。

## 技能目录

| 类别 | 技能 | 用途 |
| --- | --- | --- |
| 需求与理解 | [goal-prompt](skills/goal-prompt/SKILL.md) | 把目标梳理成可执行任务，在已有授权下完成开发与交付 |
| 需求与理解 | [think](skills/think/SKILL.md) | 在实施前明确方案、约束、取舍和验证方式 |
| 需求与理解 | [how](skills/how/SKILL.md) | 读取真实代码，解释系统的结构和运行过程 |
| 开发与审查 | [hunt](skills/hunt/SKILL.md) | 先查清故障根因，再修复并验证 |
| 开发与审查 | [code-review](skills/code-review/SKILL.md) | 审查改动、分支或 PR 的缺陷，逐项核实后报告 |
| 开发与审查 | [adversarial-review](skills/adversarial-review/SKILL.md) | 通过另一家模型的命令行工具进行交叉审查 |
| 开发与审查 | [patch-audit](skills/patch-audit/SKILL.md) | 提交前检查改动是否必要，清理冗余和场景补丁 |
| 开发与审查 | [test-audit](skills/test-audit/SKILL.md) | 检查测试的实际价值和边界，审查低价值测试 |
| 开发与审查 | [prune](skills/prune/SKILL.md) | 删除过时流程、冗余状态和无价值中间层 |
| 交付与维护 | [batch-commit](skills/batch-commit/SKILL.md) | 将已授权改动按功能拆成清楚的提交 |
| 交付与维护 | [check](skills/check/SKILL.md) | 检查发布准备度，完成已授权的交付和队列维护 |
| 交付与维护 | [health](skills/health/SKILL.md) | 检查代理配置、指令漂移、工具连接和可维护性 |
| 界面 | [ui](skills/ui/SKILL.md) | 实现、优化和审查布局、文案及交互状态 |
| 界面 | [mobile-native](skills/mobile-native/SKILL.md) | 修复手机网页的触摸、滚动、安全区和显示问题 |
| 研究与表达 | [read](skills/read/SKILL.md) | 读取链接或 PDF，按需要提取、概括或保存内容 |
| 研究与表达 | [learn](skills/learn/SKILL.md) | 研究陌生领域，综合材料并保留来源依据 |
| 研究与表达 | [write](skills/write/SKILL.md) | 改写和打磨中文、英文、技术说明及产品文案 |

## 安装

先克隆仓库：

```bash
git clone https://github.com/Wanghaoyihaoyi/agent-skills.git
cd agent-skills
```

按需要安装单个技能，复制整个技能目录，保留其 `scripts/`、`references/` 和 `agents/` 文件。不要只复制 `SKILL.md`。

| 工具 | 用户级目录 | 项目级目录 |
| --- | --- | --- |
| Codex | `~/.agents/skills/` | `<项目>/.agents/skills/` |
| Claude Code | `~/.claude/skills/` | `<项目>/.claude/skills/` |

例如，将 `skills/hunt/` 复制到 `~/.agents/skills/hunt/`。目标目录已存在时，先比较差异，再决定更新，避免覆盖自己的版本。Codex 的目录发现和调用方式见 [官方技能文档](https://learn.chatgpt.com/docs/build-skills)；Claude Code 见 [官方技能文档](https://code.claude.com/docs/en/skills)。

`goal-prompt` 会按任务读取同级的 `think`、`hunt`、`ui`、`patch-audit`、`code-review`、`check` 和 `test-audit`。使用完整开发流程时，建议同时安装这些技能。其他技能按各自说明按需使用；缺少可选工具或技能时，应明确说明验证限制。

## 使用

在 Codex 中可用 `$技能名` 显式调用，在 Claude Code 中可用 `/技能名` 调用，也可用自然语言提出匹配任务。

```text
$hunt 查清这个接口为什么偶尔返回错误，并修复根因。
$how 解释用户点击提交后，数据经过哪些模块。
$patch-audit 检查本次改动是否堆叠了不必要的补丁。
$write 把这段说明改得清楚、直接，保留事实和原意。
```

技能中的示例命令按实际系统、工具和项目规则调整。技能不会自动授予提交、推送、发布、访问生产或删除数据的权限。`patch-audit` 的提交前要求是代理指令，不是 Git hook。

## 运行条件

大多数技能只包含说明。需要脚本时，再安装对应依赖。

- 通用脚本使用 Python 3；Shell 辅助脚本需要 Bash。
- `adversarial-review` 需要已登录的另一家模型命令行工具：Codex 使用 Claude CLI，Claude 使用 Codex CLI。可能产生模型调用费用。
- `read` 的网页提取脚本有标准库路径；`readability-lxml` 和 `html2text` 可提升提取质量。飞书 API 脚本需要 `requests` 和使用者自己的授权凭据。微信浏览器脚本需要 Playwright、BeautifulSoup、lxml 和浏览器运行环境。
- `read` 默认直接读取来源网站。使用 `--use-proxy` 时会把 URL 发给第三方提取服务，需按技能说明取得授权。
- `health` 的 Windows 启动器需要 PowerShell、Git Bash 和 Python；其他工具按实际检查范围使用。

## 检查仓库

```bash
python3 -m venv .venv
.venv/bin/python -m pip install 'PyYAML>=6,<7'
.venv/bin/python scripts/validate.py
```

检查包含技能元数据、仓库内 Markdown 文件链接、Python 语法和 Bash 语法。它不执行业务脚本、不调用模型、不访问外部服务，也不证明每个技能在所有工具中都已通过实际任务验收。Windows 可使用 `.venv/Scripts/python.exe`；缺少 Bash 时会明确报告跳过。

## 许可证与来源

本仓库的原创内容与新增改动采用 [MIT 许可证](LICENSE)。改编部分保留上游版权与适用许可证，详见 [第三方声明](THIRD_PARTY_NOTICES.md) 和 `licenses/`。
