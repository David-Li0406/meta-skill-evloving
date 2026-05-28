---
name: duivytools
description: DuIvyTools 是一个用于可视化 GROMACS 的 xvg 和 xpm 文件的命令行工具，包含 30+ 个命令。使用此技能来处理 GROMACS 模拟结果文件的可视化和数据处理。当用户需要可视化 xvg/xpm 文件、生成 mdp 模板、处理索引文件或执行其他 MD 分析任务时调用此技能。
---

# DuIvyTools 使用指南

## 概述

DuIvyTools 是一个基于命令行的 MD 分析工具，可以对 GROMACS 的结果文件进行快速的可视化和分析。它提供了约 30 个命令，涵盖 XVG 文件可视化、XPM 文件处理、索引文件管理和实用工具等功能。

## 安装

DuIvyTools 可以通过 pip 安装：

```bash
pip install DuIvyTools -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 命令分类

### XVG 相关命令（12个）

#### xvg_show
轻松显示 xvg 文件中的所有数据。默认第 0 列是 X 值，第 1 列及之后的是数据。

```bash
dit xvg_show -f rmsd.xvg gyrate.xvg
```

#### xvg_compare
比较多个 xvg 文件的数据，比 xvg_show 更灵活。可以通过 `-c` 选择数据列，设置计算和显示滑动平均。

```bash
dit xvg_compare -f rmsd.xvg gyrate.xvg -c 1 1,2
dit xvg_compare -f energy.xvg -c 1,3 -l "LJ(SR)" "Coulomb(SR)" -xs 0.001 -x "Time(ns)" -smv
```

#### xvg_ave
计算 xvg 中每一列数据的平均值、标准偏差和标准误差。

```bash
dit xvg_ave -f rmsd.xvg -b 1000 -e 2001
```

#### xvg_rama
将 gmx rama 命令得到的蛋白质二面角（phi 和 psi）数据转换成拉式图。

```bash
dit xvg_rama -f rama.xvg
```

#### xvg_show_distribution
展示 xvg 数据的分布。使用 `-m pdf` 显示核密度估计，`-m cdf` 显示累积核密度估计。

```bash
dit xvg_show_distribution -f gyrate.xvg -c 1,2
dit xvg_show_distribution -f gyrate.xvg -c 1,2 -m pdf -eg plotly
```

#### xvg_show_stack
绘制堆积折线图，适用于显示蛋白质二级结构含量的变化。

```bash
dit xvg_show_stack -f dssp_sc.xvg -c 2-7 -xs 0.001 -x "Time (ns)"
```

#### xvg_show_scatter
选择两列或三列数据（第三列用于着色），绘制散点图。

```bash
dit xvg_show_scatter -f gyrate.xvg -c 1,2,0 -zs 0.001 -z "Time(ns)" -eg plotly
```

#### xvg_box_compare
将选中的数据列以小提琴图和散点图的形式呈现出来。

```bash
dit xvg_box_compare -f gyrate.xvg -c 1,2,3,4 -l Gyrate Gx Gy Gz -z "Time(ns)" -zs 0.001
dit xvg_box_compare -f gyrate.xvg -c 1,2,3,4 -l Gyrate Gx Gy Gz -z "Time(ns)" -zs 0.001 -m withoutScatter
```

#### xvg_combine
从多个 xvg 文件中读取数据并按照用户的选择组合成一个新的 xvg 文件。

```bash
dit xvg_combine -f RMSD.xvg Gyrate.xvg -c 0,1 1 -l RMSD Gyrate -x "Time(ps)"
dit xvg_combine -f f1.xvg f2.xvg -c 1,2 2,3 -o res.xvg
```

#### xvg_ave_bar
计算并行模拟的平均值并绘制柱状图，适用于比较不同体系的模拟结果。

```bash
dit xvg_ave_bar -f bar_0_0.xvg,bar_0_1.xvg bar_1_0.xvg,bar_1_1.xvg -c 1,2 -l MD_0 MD_1 -al Hbond Pair -csv hhh.csv -y Number
```

#### xvg_energy_compute
计算蛋白质和配体之间的相互作用能。

```bash
dit xvg_energy_compute -f energy.xvg
```

### XPM 相关命令（5个）

#### xpm_show
可视化 xpm 文件。支持四种绘图引擎（matplotlib, plotly, gnuplot, plotext）和多种绘图模式（imshow, pcolormesh, 3d, contour）。

```bash
dit xpm_show -f DSSP.xpm
dit xpm_show -f FEL.xpm -m pcolormesh -ip linear -ipf 5 -cmap solar
dit xpm_show -f FEL.xpm -m 3d -x PC1 -y PC2 -z Energy -t FEL --alpha 0.5
dit xpm_show -f FEL.xpm -m contour -cmap jet --colorbar_location bottom
dit xpm_show -f FEL.xpm -m contour -cmap jet -zmin 0 -zmax 20
```

#### xpm2csv
将 xpm 文件转换为 csv 文件，格式为 (x, y, z) 三列数据。

```bash
dit xpm2csv -f test.xpm -o test.csv
```

#### xpm2dat
将 xpm 文件转换为 M*N 的 dat 文件。

```bash
dit xpm2dat -f test.xpm -o test.dat
```

#### xpm_diff
计算两个相同尺寸、相同物理含义的 xpm 图片的差值。

```bash
dit xpm_diff -f DCCM0.xpm DCCM1.xpm -o DCCM0-1.xpm
```

#### xpm_merge
将两个相同尺寸、相同 X 和 Y 轴的 xpm 图片沿对角线一半一半拼接起来。

```bash
dit xpm_merge -f DCCM0.xpm DCCM1.xpm -o DCCM0-1.xpm
```

### NDX 相关命令（4个）

#### ndx_add
给 index 索引文件添加一个新的组。

```bash
dit ndx_add -f index.ndx -o test.ndx -al lig -c 1-10
dit ndx_add -al lig mol -c 1-10-3,11-21 21-42
```

#### ndx_split
将一个 index 索引组均匀切分成几个组。

```bash
dit ndx_split -f index.ndx -al 1 2
dit ndx_split -f index.ndx -al Protein 2 -o test.ndx
```

#### ndx_show
输出 ndx 文件中所有的索引组的名字。

```bash
dit ndx_show -f test.ndx
```

#### ndx_rm_dup
删除 ndx 文件中所有重复的索引组（名字和索引都相同的组）。

```bash
dit ndx_rm_dup -f test.ndx -o res.ndx
```

### 其他工具命令（9个）

#### mdp_gen
生成 GROMACS mdp 文件模板。**注意：生成的 mdp 模板文件不一定适合你的体系，请生成之后一定打开自行设置和调整相关的参数。**

```bash
dit mdp_gen
dit mdp_gen -o nvt.mdp
```

#### show_style
生成不同绘图引擎的格式控制文件。

```bash
dit show_style
dit show_style -eg plotly
dit show_style -eg gnuplot
dit show_style -eg plotly -o DIT_plotly.json
```

#### find_center
寻找 gro 文件中组分的几何中心。可以通过指定索引文件和索引组寻找特定组的几何中心。

```bash
dit find_center -f test.gro
dit find_center -f test.gro index.ndx
dit find_center -f test.gro index.ndx -m AllAtoms
```

#### dccm_ascii
读取 gmx covar 命令以 -ascii 方式导出的协方差矩阵数据，生成动态互相关矩阵的 xpm 文件。

```bash
dit dccm_ascii -f covar.dat -o dccm.xpm
```

#### dssp
读取 GROMACS 2023 的 dssp 命令生成的 dat 文件，处理成 GROMACS 2022 及更老版本中常见的 DSSP 的 xpm 和 sc.xvg 文件。

```bash
dit dssp -f dssp.dat -o dssp.xpm
dit dssp -f dssp.dat -c 1-42,1-42,1-42 -b 1000 -e 2001 -dt 10 -x "Time (ps)"
```

## 通用参数说明

### 输入输出参数
- `-f INPUT [INPUT ...]`：指定输入文件，可以同时输入多组文件，组内文件用逗号隔开，组间用空格隔开
- `-o OUTPUT`：指定输出文件名
- `-ns, --noshow`：不显示图片

### 数据选择参数
- `-c COLUMNS [COLUMNS ...]`：选择数据列，计数从 0 开始。例如 `-c 1-7,10 0,1,4` 表示第一组文件的第 1-6 列和第 10 列，第二组文件的第 0、1、4 列
- `-b BEGIN`：指定起始行索引（包含）
- `-e END`：指定结束行索引（不包含）
- `-dt DT`：指定步长，默认为 1

### 标签和标题参数
- `-l LEGENDS [LEGENDS ...]`：指定图例
- `-x XLABEL`：指定 X 轴标签
- `-y YLABEL`：指定 Y 轴标签
- `-z ZLABEL`：指定 Z 轴标签（用于颜色）
- `-t TITLE`：指定图片标题

### 数据范围参数
- `-xmin XMIN`、`-xmax XMAX`：指定 X 轴数值范围
- `-ymin YMIN`、`-ymax YMAX`：指定 Y 轴数值范围
- `-zmin ZMIN`、`-zmax ZMAX`：指定 Z 轴数值范围（colorbar）

### 数据变换参数
- `-xs XSHRINK`：X 值乘以缩放因子，默认 1.0
- `-ys YSHRINK`：Y 值乘以缩放因子，默认 1.0
- `-zs ZSHRINK`：Z 值乘以缩放因子，默认 1.0
- `-xp XPLUS`：X 值加上偏移量，默认 0.0
- `-yp YPLUS`：Y 值加上偏移量，默认 0.0
- `-zp ZPLUS`：Z 值加上偏移量，默认 0.0

### 精度和刻度参数
- `--x_precision X_PRECISION`：X 轴数据显示精度
- `--y_precision Y_PRECISION`：Y 轴数据显示精度
- `--z_precision Z_PRECISION`：Z 轴数据显示精度
- `--x_numticks X_NUMTICKS`：X 轴刻度数量
- `--y_numticks Y_NUMTICKS`：Y 轴刻度数量
- `--z_numticks Z_NUMTICKS`：Z 轴刻度数量

### 统计和滑动平均参数
- `-smv [{,CI,origin}]`：显示滑动平均值。`-smv` 显示原始数据作为背景，`-smv CI` 显示置信区间
- `-ws WINDOWSIZE`：滑动平均窗口大小，默认 50
- `-cf CONFIDENCE`：置信区间可信度，默认 0.95

### 绘图引擎和样式参数
- `-eg {matplotlib,plotext,plotly,gnuplot}`：指定绘图引擎，默认 matplotlib
- `-cmap COLORMAP`：指定 colormap
- `--colorbar_location {None,left,top,bottom,right}`：colorbar 位置（仅 matplotlib）
- `--legend_location {inside,outside}`：图例位置
- `--legend_ncol LEGEND_NCOL`：图例列数，默认 1
- `--alpha ALPHA`：透明度
- `-m {withoutScatter,pcolormesh,3d,contour,AllAtoms,pdf,cdf}`：模式选择
- `-al ADDITIONAL_LIST [ADDITIONAL_LIST ...]`：附加参数

### 插值参数
- `-ip INTERPOLATION`：插值方法
- `-ipf INTERPOLATION_FOLD`：插值倍数，默认 10

### 数据导出参数
- `-csv CSV`：将数据导出为 csv 文件

## 使用建议

1. **查看帮助**：使用 `dit <command> -h` 查看每个命令的详细帮助信息
2. **绘图引擎选择**：
   - matplotlib：最常用的引擎，功能最全
   - plotly：交互式图表，适合网页展示
   - gnuplot：适合高质量静态图
   - plotext：在终端中直接绘制简单图形

3. **列和行索引**：DIT 中列和行的计数都是从 0 开始的

4. **数据范围**：`-b` 声明的起始行被包括在计算数据中，`-e` 声明的行则不被包括

5. **Latex 支持**：标签和标题支持简单的 Latex 语法，如 `-l "$nm^2$" "$\Delta G_{energy}$"`

6. **插值使用**：对 Continuous 类型的 xpm 图片进行插值时，需要用户自己保证出图的物理意义

7. **xpm 切割**：可以使用 `-xmin`、`-xmax`、`-ymin`、`-ymax` 对 xpm 图片进行切割

8. **自定义样式**：可以将自定义的 mplstyle 文件放置在当前工作目录，DIT 会自动加载并应用

## 常见问题

1. **如何不显示 legend？**：将 `-l` 参数设置为空字符串，如 `-l "" "" ""`

2. **如何选择多列数据？**：使用逗号分隔，如 `-c 1,2,3`

3. **如何选择一个范围的列？**：使用短横，如 `-c 1-7`（不包括第 7 列）

4. **如何组合多个文件的数据？**：使用 `xvg_combine` 命令，通过 `-c` 参数分别指定每个文件的列

5. **如何计算滑动平均？**：添加 `-smv` 参数，可通过 `-ws` 调整窗口大小，`-cf` 调整置信度

6. **如何导出数据？**：使用 `-csv` 参数将数据导出为 csv 文件