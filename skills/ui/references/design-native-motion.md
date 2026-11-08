# 原生动效

用于 Flutter、SwiftUI、UIKit 或 Compose 的过渡与按压反馈。先复用项目及平台已有动效，按实际目的和触发频率选用。

| 需要 | Flutter | SwiftUI | UIKit / Compose |
| --- | --- | --- | --- |
| 状态过渡 | 现有隐式动画组件或项目控制器 | 绑定明确状态的动画 | UIViewPropertyAnimator / animateAsState 系列 |
| 按压反馈 | 现有按钮与交互组件 | ButtonStyle 的按压状态 | isHighlighted / InteractionSource |
| 减少动态效果 | 平台可访问性设置与项目封装 | accessibilityReduceMotion | 平台可访问性与动画设置 |

- 颜色、形状或静态变化都能给出按压反馈。过渡方向和起点应体现空间关系，例如锚定浮层从触发处展开。只让实际变化的属性参与过渡。
- 曲线和时长采用项目令牌，根据动作距离、频率和平台预期调整。跟手拖动可采用平台阻尼或弹簧，吸附避免多余晃动。高频按键、点击与快速切换先保证响应，重复触发时从当前位置继续或反转。
- 减少动态效果时可用即时切换、弱淡入及状态文字。进度和状态来自真实任务事件。加载指示随任务结束，避免持续动画掩盖无进展。
- 实际交互或录屏检查开始、中间帧和落点，按风险覆盖连续操作、打断、退出和减弱动效。验证焦点、点击区域及内容裁切。

动效目的与组件细节参考 [emilkowalski/skills](https://github.com/emilkowalski/skills)，结合原生与桌面工程约束改写。
