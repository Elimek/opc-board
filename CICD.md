# OPC CICD — 质量说明

这个仓库没有持续集成脚本。

不存在的文件：

- `quality-harness.sh`
- `scripts/test-harness.sh`
- 任何会打印 `43/43` 的测试套件

不要把文档里的测试数字当成已经跑过。

## 仓库里实际有的

- 已发布的导师 SKILL：只有 `skills/strategy/zhangxuefeng/`（张雪峰 / Zhang Xuefeng）
- 静态页面：`index.html`、`dashboard/`、`checklist/weekly-board-meeting.html`
- [Issue #7](https://github.com/Elimek/opc-board/issues/7) **仍然开着**。以前写在这里的 v1.3.0「Naval stance table、Musk engineering-only」修复，对应的 SKILL 文件不在这棵树里，不能算已经上线。

## 以前这张表写过、但现在不能当成已上线

| 旧版本说法 | 现在怎么读 |
| --- | --- |
| v1.3.0 修复了 #7 | #7 仍开放。那些 SKILL 不在仓库里 |
| v1.2.0 董事会结构调整 | 落地页上有席位名字。除张雪峰外都没有 SKILL |
| v1.1.0 Lidangzzz 深度蒸馏 | `skills/` 下没有 Lidangzzz |
| v1.0.0 初始发布 | 静态页面在。CLI、九份 SKILL、43 个测试不在 |

## 以后如果真的改了一份 SKILL

1. 对真实存在的文件提 Issue 或 PR（不要关掉还没在树里验证的 Issue）。
2. 人工对照：立场、至少一个反方案、证据、置信度。
3. 没有脚本可以代替这一步。

预定的「每周日审计 cron」不在这个仓库里。
