# Agent Skills

在日常开发中维护的 18 个 AI 代理技能。覆盖需求梳理、问题排查、代码审查、架构精简、界面优化、研究和写作。

这些技能采用 `SKILL.md` 目录格式，可用于 Codex、Claude Code 等支持 Agent Skills 的工具。其中 9 项技能基于 [Tw93](https://github.com/tw93)（[Mole](https://github.com/tw93/Mole) 的作者）的 [Waza](https://github.com/tw93/Waza) 仓库改编；其他参考来源也保留署名，详见 [第三方声明](THIRD_PARTY_NOTICES.md)。本仓库收录个人维护的通用技能，不包含平台内置技能、同步的第三方技能包或私有项目专用技能。

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
| 交付与维护 | [kaneo-workflow](skills/kaneo-workflow/SKILL.md) | 开工检查待办，同步接手、交付和用户验收状态，补记独立工作 |
| 交付与维护 | [batch-commit](skills/batch-commit/SKILL.md) | 将已授权改动按功能拆成清楚的提交 |
| 交付与维护 | [check](skills/check/SKILL.md) | 检查发布准备度，完成已授权的交付和队列维护 |
| 交付与维护 | [health](skills/health/SKILL.md) | 检查代理配置、指令漂移与可维护性，按需对照重放单条规则 |
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

推荐让安装目录链接到仓库中的技能目录。链接指向同一份文件，修改安装目录或仓库目录都会更新当前技能；不需要维护第二份副本。

| 工具 | 用户级目录 | 项目级目录 |
| --- | --- | --- |
| Codex | `~/.agents/skills/` | `<项目>/.agents/skills/` |
| Claude Code | `~/.claude/skills/` | `<项目>/.claude/skills/` |

在仓库根目录中执行以下示例，安装 `hunt`：

```bash
for skill_dir in "$HOME/.agents/skills" "$HOME/.claude/skills"; do
  mkdir -p "$skill_dir"
  if [ -e "$skill_dir/hunt" ] || [ -L "$skill_dir/hunt" ]; then
    printf '已存在，请先比较差异：%s\n' "$skill_dir/hunt" >&2
  else
    ln -s "$PWD/skills/hunt" "$skill_dir/hunt"
  fi
done
```

目标目录已经存在时，命令会拒绝覆盖。迁移旧安装时，先比较全部文件并合并自己的改动，再把一致的旧目录替换成链接。其他技能同样按名称建立链接。保留仓库目录的位置；移动仓库后需要更新链接。

目录链接适用于 macOS/Linux。也可以复制完整技能目录（包含脚本、参考资料和许可证），但复制安装需要手动同步。Codex 的目录发现和调用方式见 [官方技能文档](https://learn.chatgpt.com/docs/build-skills)；Claude Code 见 [官方技能文档](https://code.claude.com/docs/en/skills)。

`goal-prompt` 按任务缺口使用同级的 `think`、`hunt`、`ui`、`patch-audit`、`code-review`、`check` 和 `test-audit`，不是每次全部运行。完整开发流程建议同时安装这些技能；已有同版本证据复用，缺少可选能力时说明限制。

## 使用

在 Codex 中可用 `$技能名` 显式调用，在 Claude Code 中可用 `/技能名` 调用，也可用自然语言提出匹配任务。

```text
$hunt 查清这个接口为什么偶尔返回错误，并修复根因。
$how 解释用户点击提交后，数据经过哪些模块。
$patch-audit 检查本次改动是否堆叠了不必要的补丁。
$write 把这段说明改得清楚、直接，保留事实和原意。
$prune 审计本仓库的死代码与废弃开关，核实间接引用和运行证据，清理已证明可退役的部分；不改线上配置。
$hunt 根据近期 CI 历史，按预计每日节省机器分钟排序优化建议，先只给表格。
$hunt 扫描近期 CI 偶发失败，修复根因明确的简单问题并验证，报告其余证据缺口。
$health 从近期会话找一条误导代理的 AGENTS.md 规则，在隔离环境重放同一任务，只改变这一条，比较质量与成本。
```

技能中的示例命令按实际系统、工具和项目规则调整。技能不会自动授予提交、推送、发布、访问生产或删除数据的权限。`patch-audit` 的提交前要求是代理指令，不是 Git hook。

## 工作流分工

| 当前需求 | 使用入口 | 后续 |
| --- | --- | --- |
| 想法还不清楚，希望梳理并完成开发 | `goal-prompt` | 按需借用 think；一份摘要，只补必要决定，已有实施授权直接继续 |
| 只判断设计、架构或方案取舍 | `think` | 交付结论或方案；未授权不实施 |
| 明确的小修改 | 直接提出修改要求 | 按风险实施与验证，不先套完整规划 |
| 死代码、废弃实验或常量化开关 | `prune` | 交叉核实代码、配置和运行证据；全量审计对账清单，保留应急能力 |
| CI 成本或偶发失败 | `hunt` | 按历史量化收益，修复明确原因；测试有效性由 test-audit 承接 |
| 规则导致无效工作 | `health` | 先用会话定位一条规则；已要求实验时隔离对照重放 |
| 已有故障 | `hunt` | 查清根因，在有效授权内修复和验证 |
| 审查代码缺陷 | 本仓库 `code-review` | 默认只读；修复、对外评论分别按实际授权 |
| 复审本轮复杂度 / 清理已有架构 | `patch-audit` / `prune` | 前者针对本轮改动，后者针对明确架构范围；复用同等检查证据 |
| 编写或审查测试 / 交付收尾 | `test-audit` / `check` | 按风险和授权使用，均不自动开启全仓清理或发布 |

`think` 是设计能力，`goal-prompt` 是完整任务入口，不需要先手动运行一个再复制到另一个。用户已要求实施时不重新索取“开干”；仅方案讨论等待必要实施授权。提交前 `patch-audit` 的要求保留，但同一份已审查内容不重复运行。

本仓库 `skills/code-review/` 是个人维护的通用入口，包含 Waza 的审查资料和脚本；Claude Code 官方插件也有名为 `code-review` 的 PR 命令，其固定多代理、评分与发布流程独立。使用时确认实际加载的文件；不要把同名等同于同一套规则，也不顺带改写平台维护的插件。

## 运行条件

大多数技能只包含说明。需要脚本时，再安装对应依赖。

- 通用脚本使用 Python 3；Shell 辅助脚本需要 Bash。
- `adversarial-review` 需要已登录的另一家模型命令行工具：Codex 使用 Claude CLI，Claude 使用 Codex CLI。可能产生模型调用费用。
- `read` 的网页提取脚本有标准库路径；`readability-lxml` 和 `html2text` 可提升提取质量。飞书 API 脚本需要 `requests` 和使用者自己的授权凭据。微信浏览器脚本需要 Playwright、BeautifulSoup、lxml 和浏览器运行环境。
- `read` 默认直接读取来源网站。使用 `--use-proxy` 时会把 URL 发给第三方提取服务，需按技能说明取得授权。
- `health` 的 Windows 启动器需要 PowerShell、Git Bash 和 Python；其他工具按实际检查范围使用。

## 只维护一份并推送更新

代理维护流程与检查要求见 [仓库维护规则](AGENTS.md)。维护者已持续授权：相关检查通过后，直接提交并推送本任务改动。

日常修改 `skills/<技能名>/`，或从已链接的安装目录编辑。两者指向同一份文件，Git 会直接看到这些改动。当前目录中的第三方同步技能和平台内置技能独立维护，不放进这个仓库。

改动前，在仓库里运行 `git pull --ff-only`。改完后先查看差异、运行检查，再只提交要公开的文件。例如更新 `hunt`：

```bash
git diff -- skills/hunt
.venv/bin/python scripts/validate.py
git add -- skills/hunt
git commit -m "feat: 更新 hunt 技能"
git push origin main
```

检查脚本的环境准备见下节。推送前核对公开内容，尤其是新增脚本、私有路径和凭据。技能在本机直接使用最新文件；GitHub 在推送后更新。

## 检查仓库

```bash
python3 -m venv .venv
.venv/bin/python -m pip install 'PyYAML>=6,<7'
.venv/bin/python scripts/validate.py
```

检查包含技能元数据、仓库内 Markdown 文件链接、Python 语法和 Bash 语法。它不执行业务脚本、不调用模型、不访问外部服务，也不证明每个技能在所有工具中都已通过实际任务验收。Windows 可使用 `.venv/Scripts/python.exe`；缺少 Bash 时会明确报告跳过。

## 许可证与来源

本仓库的原创内容与新增改动采用 [MIT 许可证](LICENSE)。改编部分保留上游版权与适用许可证，详见 [第三方声明](THIRD_PARTY_NOTICES.md) 和 `licenses/`。
