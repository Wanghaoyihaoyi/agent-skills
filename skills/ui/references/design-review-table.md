# 设计评审与门禁

仅在用户要求审查、打磨、抛光界面时读取。小修复不走全套；新页面或明确改版才按需取用其中一节。不一次加载全部。

> 融合来源：[emilkowalski/skills](https://github.com/emilkowalski/skills) 的表格评审与动效禁令；[pbakaus/impeccable](https://github.com/pbakaus/impeccable)（Apache 2.0）的 craft-floor 禁令与 register 分流思路；[vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) 的无障碍审计；[leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) 的 pre-flight 纪律；评测方法参考 [designskill.qiaomu.ai](https://designskill.qiaomu.ai/) 的八个发现。CSS 写法一律转为对应平台实现。

## 评审格式（强制）

审查 UI 代码必须用 Before/After/Why 三列表格，一行一个问题。不用 "Before:/After:" 分行罗列。

| Before | After | Why |
|---|---|---|
| 所有属性一起过渡 300ms | 只过渡实际变化的属性 160-200ms | 全量过渡拖尾、难打断 |
| 从 scale(0) 弹出 | 从 scale(0.95)+opacity 进场 | 无中生有显得假 |
| 下拉用 ease-in | 进场用 ease-out 系曲线 | ease-in 启动慢显得卡 |
| 按钮无按压态 | 按压 scale(0.97) 或颜色变化 | 确认界面听到了用户 |
| Popover 从中心放大 | 从触发点对齐放大（Modal 除外） | 空间连续性 |

## 禁令清单（第一作用是禁止，而非教学）

评测站发现一：打破 AI 惯性靠禁令，不靠正面示范。命中即返工：

- 不用紫渐变、默认 Inter、当头居中 Hero、三等分卡片那一套模板味构图；已有品牌方向优先。
- 不给高频操作加装饰动画；不用一个动画与另一套机制同时控制同一属性。
- 不给所有按钮统一加缩放；不无故播放首帧动画。
- Web 不写 `transition: all`；Flutter 不给所有属性套隐式动画。只动画实际变化的属性。
- 触屏 hover 样式必须包在能力查询里（Web）；Flutter 不假设 hover 存在。
- 禁 `user-scalable=no` 式禁缩放；输入字号问题修字号，不禁缩放。
- 暖纸奶油底、beige+espresso 配色不是默认选项，有明确品牌依据才用（impeccable anti-cream）。

## 拨盘：按任务收敛或放开

约束型任务看纪律，开放型任务看胆量，是两种能力：

| 任务 | 姿态 | 做法 |
|---|---|---|
| 任务型界面 Operate（工作台、设置、表单、向导） | 收敛 5/5/6 | 扫描性、一致性、原生预期优先；品牌只落在精确细节 |
| 营销说服 Persuade（落地页、活动） | 可放开 | 氛围和记忆点优先，但保留报名/转化的操作可用性 |
| 开放命题（404、空状态、引导） | 拉满 | 做完整叙事场景，同时给出用户迷路后的恢复路径（推荐链接、返回入口） |

要三个方案时，字体家族、色彩体系、控件语言全维度割裂，不用表面换色冒充多样性。

## 两道验收：好看与合格分开

截图赢不了验收，验收也赢不了截图。生产项目走两遍：

1. 视觉遍：布局、层级、记忆点、跨页一致性；开放命题加叙事完整度。
2. 工程遍：焦点管理（陷阱、Esc 关闭、焦点返还）、语义与可访问名称、对比度、reduced-motion 兜底、等宽数字、长文本与字体回退。Flutter 对应用 `FocusScope`、`Semantics`、`MediaQuery.disableAnimations`、tabular figures。

只改视觉不破工程；只补工程不顺手改版。修好一遍再看下一遍，不每调一次截一次图。

## 工艺密度与 DNA

新表面要求：注入 2-3 个可溯源的具体值（参考站名、token、截图位置），不写“高级感”这类空词；每屏至少 5 个有意的细节（对齐、间距、语义、空态、错误态各算一个），凑数的不算。

## 交互验收抽查点

向导与表单：不选必填点下一步必须正确报错，且聚焦首个错误字段并抖动或文字说明；危险操作二次确认；Toast 进出同向；异步结果注明归属，迟到回调不覆盖新状态。
