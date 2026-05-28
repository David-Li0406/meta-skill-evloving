# prompts.md

## 示例：用户没说算例 → 默认 001
用户：把 Boundary.csv 的 T_001:SNQ 全部设成 1200，然后跑预测并给我输出汇总。

期望动作：
1) sample_id=001
2) modify_boundary 生成备份并修改
3) patch job-config output 到新文件夹
4) 执行 python -m real_predict.main ...
5) summarize_output 输出 summary.md

## 示例：用户要验证“只改了 6:00-12:00”
用户：只改 6:00-12:00 的 T_001:SNQ=1200，并给我对比报告。

期望动作：
1) modify_boundary 带 start/end time
2) diff_boundary 生成 md/csv 报告
