---
name: protein_analysis
description: 蛋白质 MD 模拟的高级分析，包括周期性边界条件校正、动态互相关矩阵（DCCM）、残基距离接触矩阵（RDCM）、主成分分析（PCA）和自由能形貌图（FEL）。使用此技能来指导蛋白质模拟后的数据分析流程。当用户需要进行蛋白质 MD 分析、计算相关性矩阵、执行 PCA 或绘制自由能形貌图时调用此技能。
---

# 蛋白质 MD 模拟分析指南

## 概述

本指南提供了蛋白质分子动力学模拟后的高级分析方法，包括周期性边界条件校正、动态互相关矩阵、残基距离接触矩阵、主成分分析和自由能形貌图等分析流程。

## 周期性边界条件校正

### 为什么需要周期性校正

主体模拟的轨迹得到之后，有时候会发现体系中的蛋白或者配体有跨盒子的现象，这时候就需要对轨迹的周期性边界条件（PBC）进行校正。这可以：
1. 避免分析过程中出现意外情况（如 RMSD 曲线有较大的突跃和突降）
2. 获得较为美观的轨迹，方便直接观察

### 一般流程

对蛋白配体体系，一般使用的流程为：
1. 选取某一个原子，以其对体系居中
2. 保证体系中分子的完整性
3. 消除平动和转动

### 详细步骤

#### 1. 居中（Center）

首先生成一个体系的索引文件，并在里面添加 center 组，组内只有一个原子，之后会以这个原子为盒子中心对体系进行居中。

**步骤 1.1：创建索引文件**

```bash
echo -e "q\n" | gmx make_ndx -f md.tpr -o index.ndx
```

如果需要蛋白复合物组，可以把蛋白和可能存在的配体组合到一个组：

```bash
echo -e "Protein | Lig \nq\n" | gmx make_ndx -f md.tpr -o index.ndx
```

**步骤 1.2：手动添加 center 组**

```bash
echo -e "\n[ center ]\n500\n" >> index.ndx
```

这里例子里选择的是序号为 500 的原子。

**步骤 1.3：寻找合适的中心原子**

可以使用 DuIvyTools 的 `find_center` 命令来寻找一个可以对蛋白进行居中的中心原子：

```bash
echo -e "Protein\n" | dit find_center -f npt.gro index.ndx
```

这个命令可以找到蛋白质内的最靠近中心的原子的序号。输出的第三列就是这个原子的序号。

**步骤 1.4：执行居中**

```bash
echo -e "center\nProtein_Lig\n" | gmx trjconv -s md.tpr -f md.xtc -o center.xtc -n index.ndx -pbc atom -center
```

- 第一次输入：选择要居中的组，选 center 组
- 第二次输入：选择要输出的组，选你自己定义的蛋白配体组

#### 2. 分子完整（Molecule）

对居中之后的轨迹做一遍保证分子完整性的校正：

```bash
echo -e "Protein_Lig\n" | gmx trjconv -s md.tpr -f center.xtc -o mol.xtc -n prolig.ndx -pbc mol -ur compact
```

选择蛋白配体组即可。

#### 3. Fit（去除平动和转动）

对蛋白去除一下平动和转动，方便查看配体和蛋白质之间的相互运动：

```bash
echo -e "Backbone\nProtein_Lig\n" | gmx trjconv -s md.tpr -f mol.xtc -o fit.xtc -n prolig.ndx -fit rot+trans
```

- 第一次输入：选择对蛋白质进行 fit，选 Backbone
- 第二次输入：选择蛋白配体组进行轨迹输出

#### 4. 处理 tpr 文件

得到的 fit.xtc 就是周期性校正之后的蛋白质（或者蛋白质配体复合物）的轨迹了。有些命令执行时还需要 tpr 文件和 xtc 文件里面的原子数目一致，因而也需要对 tpr 文件做一下处理：

```bash
echo -e "Protein_Lig\n" | gmx convert-tpr -s md.tpr -o fit.tpr -n index.ndx
```

选择和前面生成 xtc 的同样的组就行了。

#### 5. 可视化检查

不管校正到哪一步了，都可以把轨迹可视化出来，自己 visual check 一下。一般习惯把 xtc 转成 pdb，用 pymol 查看：

```bash
echo -e "Protein_Lig\n" | gmx trjconv -s md.tpr -f fit.xtc -o fit.pdb -dt 1000 -n prolig.ndx
```

加个 `-dt 1000`，选择合适的时间间隔，防止输出的 pdb 文件太大。

## 动态互相关矩阵（DCCM）

### 概述

DCCM 用于分析蛋白质原子之间的动态相关性，可以揭示蛋白质内部的协同运动模式。

### 计算步骤

**步骤 1：计算协方差矩阵**

```bash
echo -e "C-alpha\nC-alpha\n" | gmx covar -s md.tpr -f md.xtc -o eigenvalues.xvg -v eigenvectors.trr -xpma covar.xpm -ascii covar.dat
```

按照需要选择对齐的组和计算的组，通常都选择 C-alpha。

**步骤 2：转换为 DCCM**

使用 DuIvyTools 将 covar.dat 处理成 dccm.xpm：

```bash
dit dccm_ascii -f covar.dat -o dccm.xpm
```

**步骤 3：可视化**

使用 DuIvyTools 对 dccm.xpm 进行可视化：

```bash
dit xpm_show -f dccm.xpm -o dccm.png -zmin -1 -zmax 1 -cmap bwr -m contour
```

### 解释

- DCCM 值范围：-1 到 1
- 正值（红色）：正相关运动（原子向相同方向运动）
- 负值（蓝色）：负相关运动（原子向相反方向运动）
- 接近 0（白色）：无相关性

## 残基距离接触矩阵（RDCM）

### 概述

RDCM 显示残基之间的平均距离，可以用于分析蛋白质的结构和残基间的相互作用。

### 计算步骤

**步骤 1：计算残基距离矩阵**

```bash
echo -e "Protein\n" | gmx mdmat -f md.xtc -s md.tpr -mean rdcm.xpm
```

可以通过 `-b` 和 `-e` 等参数设置分析时间范围。

**步骤 2：可视化**

```bash
dit xpm_show -f rdcm.xpm -o rdcm.png
```

### 解释

- 颜色越深：残基距离越近，接触越紧密
- 对角线：残基自身的距离（为 0）
- 远离对角线的区域：不同残基间的接触

## 主成分分析（PCA）

### 概述

PCA 用于分析蛋白质的主要运动模式，提取蛋白质运动的主成分。

### 重要提示

**一定要在 PCA 之前消除轨迹的平动和转动**，以免分子的整体运动影响分子内部运动的分析。

### 计算步骤

**步骤 1：计算协方差矩阵和本征向量**

```bash
echo -e "C-alpha\nC-alpha\n" | gmx covar -s md.tpr -f md.xtc -o eigenvalues.xvg -v eigenvectors.trr -xpma covapic.xpm
```

- eigenvalues.xvg：记录了多个本征值的序号和大小
- eigenvectors.trr：投影到本征向量之后的轨迹
- covapic.xpm：轨迹的协方差矩阵

**步骤 2：分析本征值**

分析 eigenvalues.xvg，计算前几个本征值的占比。通常希望前两个本征值的大小和可以越大越好，这意味着前两个主成分可以代表蛋白的大部分运动信息。

**步骤 3：投影到主成分**

将轨迹投影到前两个主成分上：

```bash
echo -e "C-alpha\nC-alpha\n" | gmx anaeig -s md.tpr -f md.xtc -v eigenvectors.trr -first 1 -last 1 -proj pc1.xvg
echo -e "C-alpha\nC-alpha\n" | gmx anaeig -s md.tpr -f md.xtc -v eigenvectors.trr -first 2 -last 2 -proj pc2.xvg
```

这里要选择的组须得是和前面 `gmx covar` 命令选的一样。

### 解释

- 本征值：表示主成分所代表的运动幅度
- 本征向量：表示主成分的运动方向
- 投影值：表示轨迹在每个主成分上的投影

## 自由能形貌图（FEL）

### 方法一：利用 RMSD 和 Gyrate 绘制 FEL

#### 步骤 1：获得 RMSD 和 Gyrate 数据

**计算 RMSD：**

```bash
echo -e "Backbone\nProtein\n" | gmx rms -s md.tpr -f md.xtc -o rmsd.xvg
```

选择 backbone 进行对齐，选择 Protein 计算和输出。

**计算 Gyrate：**

```bash
echo -e "Protein\n" | gmx gyrate -s md.tpr -f md.xtc -o gyrate.xvg
```

选择 Protein 进行计算。gyrate.xvg 包含四列回旋半径的数据：总体的，XYZ 三个方向上各一列。

#### 步骤 2：组合数据

使用 DuIvyTools 工具进行 rmsd 和 gyrate 数据的组合：

```bash
dit xvg_combine -f rmsd.xvg gyrate.xvg -c 0,1 1 -o sham.xvg
```

这里选择 rmsd 的第 0 列（时间）和第 1 列（RMSD），以及 gyrate 的第 1 列（总回旋半径）。

#### 步骤 3：计算 FEL

使用 `gmx sham` 命令生成自由能形貌图：

```bash
gmx sham -tsham 310 -nlevels 100 -f sham.xvg -ls gibbs.xpm -g gibbs.log -lsh enthalpy.xpm -lss entropy.xpm
```

参数说明：
- `-tsham 310`：设定温度（单位：K）
- `-nlevels 100`：设定 FEL 的层次数量
- `-f sham.xvg`：读入组合文件
- `-ls gibbs.xpm`：输出自由能形貌图（Gibbs 自由能）
- `-g gibbs.log`：输出 log 文件
- `-lsh enthalpy.xpm`：焓的形貌图
- `-lss entropy.xpm`：熵的形貌图

#### 步骤 4：可视化

```bash
dit xpm_show -f gibbs.xpm -m contour -cmap jet -o fel.png
```

#### 步骤 5：寻找最低能量构象

**方法 A：使用 gibbs.log 和 bindex.ndx**

gibbs.log 记录了索引组与能量的关系，bindex.ndx 记录了索引组与帧数的关系。

例如，如果 Minimum 4 是能量最低点，它的索引组是 141，那么到 bindex.ndx 中找到索引 [ 141 ]，查看这个索引对应的时间帧。

**方法 B：使用 sham.xvg**

从 sham.xvg 可以看到数据的开始时刻和时间间隔。第几帧也就是 sham.xvg 的数据的第几行。

**提取构象：**

```bash
echo -e "Protein\n" | gmx trjconv -f md.xtc -s md.tpr -b 1010 -e 1010 -o protein.pdb
```

这里假设要提取时刻为 1010ps 的构象。

### 方法二：利用 PCA 绘制 FEL

#### 步骤 1：获得主成分数据

按照上述 PCA 方法获得前两个主成分的 xvg 文件（pc1.xvg 和 pc2.xvg）。

#### 步骤 2：组合数据

使用 DuIvyTools 组合两个文件：

```bash
dit xvg_combine -f pc1.xvg pc2.xvg -c 0,1 1 -o sham.xvg
```

#### 步骤 3：计算和可视化 FEL

按照方法一中的描述利用 `gmx sham` 命令得到 gibbs.xpm 并用 DuIvyTools 可视化。

## 分析流程建议

### 完整分析流程

1. **周期性校正**
   - 居中
   - 分子完整
   - Fit
   - 处理 tpr 文件

2. **基础分析**
   - RMSD
   - Gyrate
   - RMSF

3. **高级分析**
   - DCCM（动态互相关矩阵）
   - RDCM（残基距离接触矩阵）
   - PCA（主成分分析）
   - FEL（自由能形貌图）

### 注意事项

1. **轨迹预处理**
   - 在进行任何分析之前，确保轨迹已经进行了适当的周期性校正
   - 检查轨迹的质量，去除不稳定的起始部分

2. **时间范围选择**
   - 通常选择模拟的平衡期进行分析
   - 可以通过 RMSD 等指标确定平衡期

3. **原子组选择**
   - PCA 和 DCCM 通常选择 C-alpha 原子
   - 也可以根据需要选择其他原子组（如 Backbone、Side chain）

4. **可视化检查**
   - 每一步分析后都应该进行可视化检查
   - 确保结果的合理性

5. **参数选择**
   - FEL 的温度应该与模拟温度一致
   - 网格数量（nlevels）根据需要调整

## 常见问题

1. **为什么 RMSD 曲线有突跃？**
   - 可能是周期性边界条件没有正确处理
   - 需要进行 PBC 校正

2. **PCA 分析前需要做什么？**
   - 必须消除轨迹的平动和转动
   - 使用 `gmx trjconv -fit rot+trans` 进行 fit

3. **如何选择 FEL 的温度？**
   - 应该与模拟温度一致
   - 通常使用 NPT 模拟的温度

4. **DCCM 的正负值代表什么？**
   - 正值：正相关运动（同向运动）
   - 负值：负相关运动（反向运动）

5. **如何提取特定构象？**
   - 使用 `gmx trjconv` 命令
   - 通过 `-b` 和 `-e` 参数指定时间范围

6. **FEL 的颜色如何解释？**
   - 通常使用 colormap（如 jet、bwr）
   - 颜色代表自由能的高低
   - 深色区域代表低能量（稳定）构象