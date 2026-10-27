# 原生动效

仅在 Flutter、SwiftUI、UIKit 或 Compose 的动效、按压反馈工作中读取。先复用当前项目和平台组件；不要因为示例存在就给所有交互套同一种曲线或缩放。

| 需要 | Flutter | SwiftUI | UIKit / Compose |
|---|---|---|---|
| 状态变化的过渡 | 现有隐式动画组件或项目控制器 | 绑定明确状态的 animation | UIViewPropertyAnimator / animateAsState 系列 |
| 按压反馈 | 现有按钮与交互组件 | ButtonStyle 的按压状态 | isHighlighted / InteractionSource |
| 减少动态效果 | 平台可访问性设置与项目封装 | accessibilityReduceMotion | 平台可访问性与动画设置 |

具体 API 以项目实际依赖版本为准。反馈可以是颜色、形状或静态状态，不强制缩放。可交互过渡应能从当前位置继续、反转或取消，不能由遗留定时器覆盖新状态。

减少动态效果时保留明确的进度与状态文字；冻结唯一的忙碌指示会让用户误以为卡住。曲线与时长沿用项目语义，新增值说明用途，不把同一动作散落成多组常量。

动效验证看过渡过程：按需截图连续帧或录屏，并检查快速重复操作、退出和中断。单张最终截图不能证明动效平稳；测试通过也不能替代实际观感。

## 动画决策（取自 emil-design-eng，转为原生实现）

> 来源：[emilkowalski/skills](https://github.com/emilkowalski/skills) 的决策框架与组件细节；CSS 示例已转为 Flutter/SwiftUI 对等实现，不照搬 Web 代码。

### 1. 该不该动

| 频率 | 决策 |
|---|---|
| 每天 100+ 次（快捷操作、反复开关） | 不做动画 |
| 每天几十次（hover、列表导航） | 去掉或大幅减弱 |
| 偶发（弹窗、抽屉、Toast） | 标准动画 |
| 罕见/首次（引导、庆祝） | 可加愉悦感 |

键盘触发的操作一律不动效。Raycast 开关无动画即是最优体验。

### 2. 为什么动

每个动画必须能回答目的：空间一致性（Toast 同向进出）、状态指示（按钮变形表态）、解释说明、按压反馈、防闪变。只为“好看”且高频出现的不做。

### 3. 用什么曲线

进场/退场用 ease-out（先快后慢，感觉跟手）；屏内位移/变形用 ease-in-out；颜色和 hover 用 ease；恒定运动（跑马灯、进度条）用 linear。UI 动画不用 ease-in（启动慢显得卡）。

| Web（emil 原值） | Flutter 对等 | 用途 |
|---|---|---|
| `cubic-bezier(0.23,1,0.32,1)` | `Curves.easeOutCubic` / `Cubic(0.23,1,0.32,1)` | 通用交互进场 |
| `cubic-bezier(0.77,0,0.175,1)` | `Curves.easeInOutCubic` | 屏内位移 |
| `cubic-bezier(0.32,0.72,0,1)` | `Cubic(0.32,0.72,0,1)` | 抽屉/灵动岛式曲线 |

弹簧只用在可拖拽、可打断、需动量的手势上；普通进场不用弹簧。Flutter 用 `SpringSimulation`，bounce 保持 0.1-0.3，大部分场景 `Curves.easeOutBack` 小幅度即可。

### 4. 多快

| 元素 | 时长 |
|---|---|
| 按压反馈 | 100-160ms |
| Tooltip、小 popover | 125-200ms |
| 下拉、选择器 | 150-250ms |
| 弹窗、抽屉 | 200-500ms |

UI 动画上限 300ms。180ms 的下拉比 400ms 的显得更快；spinner 转得快会让加载显得更快（实际耗时相同）。第一个 tooltip 可延迟，后续相邻 tooltip 即时出现、无动画，整个工具栏会显得更快。

### 组件细节

- 按压必须有反馈：`AnimatedScale(scale: 0.97)` 或颜色/形状变化也行，不强制所有按钮都缩放；幅度 0.95-0.98。
- 不从 `scale(0)` 进场：从 `scale(0.9+)` + opacity 进场，无中生有显得假。
- Popover 从触发点放大（按触发位置算 `Alignment`）；Modal 居中放大，不跟触发点。
- 可被快速重复触发的过渡（Toast、开关）用可中断的 transition/显式控制器，不用播完才能停的 keyframe 式写法；被打断时从当前位置反转，不从零重播。
- 交叉淡入淡出调不好时，加轻微模糊过渡（Flutter 用 `ImageFiltered`/`BackdropFilter` 点到为止），可掩盖两态重叠的生硬感；配按压缩放 0.97 更完整。
- stagger 入场只用于偶发列表，间隔 50-70ms；高频列表不用。

### 验收

动效类改动的价值在截图之外，必须实际交互或录屏验收，不看单张截图下结论。快速重复点、打断、退出三项必测。
