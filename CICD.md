# OPC CICD — 质量说明

这个仓库没有持续集成脚本。

不存在的文件：

- `quality-harness.sh`
- `scripts/test-harness.sh`
- 任何会打印 `43/43` 的测试套件

不要把文档里的测试数字当成已经跑过。

## 仓库里实际有的

- 已发布的导师 SKILL：张雪峰 `skills/strategy/zhangxuefeng/`，以及原样复制的 Naval、Buffett、段永平、Trump、Dan Koe、Elon Musk。路径见 README。Bryan Johnson、Huberman、Lidangzzz 没有文件。
- 静态页面：`index.html`、`dashboard/`、`checklist/weekly-board-meeting.html`
- [Issue #7](https://github.com/Elimek/opc-board/issues/7) **仍然开着**。树里现在有上游复制的 Naval 和 Musk 文件。那不是 #7 的修复，不能算已经上线。

## 以前这张表写过、但现在不能当成已上线

| 旧版本说法 | 现在怎么读 |
| --- | --- |
| v1.3.0 修复了 #7 | #7 仍开放。Naval 和 Musk 的文件是后来复制的上游快照，不是那次修复 |
| v1.2.0 董事会结构调整 | 落地页上有席位名字。现在另有六份复制的 SKILL。CHO 和 Lidangzzz 仍然没有文件 |
| v1.1.0 Lidangzzz 深度蒸馏 | `skills/` 下没有 Lidangzzz。上游 LICENSE 不是 MIT，没有复制 |
| v1.0.0 初始发布 | 静态页面在。CLI、九份 SKILL、43 个测试不在 |

## 以后如果真的改了一份 SKILL

1. 对真实存在的文件提 Issue 或 PR（不要关掉还没在树里验证的 Issue）。
2. 人工对照：立场、至少一个反方案、证据、置信度。
3. 没有脚本可以代替这一步。

预定的「每周日审计 cron」不在这个仓库里。
