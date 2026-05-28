---
name: processing-oceandata
description: 完成海洋数据处理完整流程 - 当用户选择好训练模型后，根据模型需要的数据输入完成数据处理，加载等任务，为后续训练该模型做准备。还应完成包含数据统计分析、可视化和详细报告生成等任务，禁止修改skill中的内容，若skill功能不足以完成任务在当前项目中新建脚本。当用户提及数据处理时调用。
---

# processing-oceandata
根据用户选择的模型完成完整的海洋数据处理流程,将原始海洋数据处理成适合模型的深度学习训练数据，完成包括数据读取、预处理、切块、统计分析、可视化和报告生成等任务。

## 快速开始
1. 首先运行 nvidia-smi 检查 GPU 状态
2. 根据 GPU 占用情况选择空闲的 GPU
3. 设置 CUDA_VISIBLE_DEVICES 环境变量
4. 列出所有可用的conda环境并激活
5. 列出SKILL中models中所有可供选择的模型供用户选择，禁止自己重新编写模型架构，只允许调整模型参数和训练参数
6. 根据.claude/skills/data-processing/datasets/ocean_dataset.py模型输入要求，使用.claude/skills/data-processing/data_analysis，
.claude/skills/data-processing/plot中脚本完成数据处理，加载，可视化完整的数据处理流程
7. 按照生成的数据和图表，严格按照skill中report.md生成详细的报告 
8. 确认所有输出文件已正确保存

## 支持的数据格式

### 1. HDF5 格式 (.h5, .hdf5)
必需变量:
- `uovo_data`: (N, 2, H, W) - u和v速度分量
- `mask`: (patches_per_day, H, W) 或 (N, H, W) - 陆地/海洋掩码
- `lat`: (patches_per_day, H, W) 或 (N, H, W) - 纬度网格
- `lon`: (patches_per_day, H, W) 或 (N, H, W) - 经度网格

### 2. MATLAB 格式 (.mat)
必需变量:
- `u_combined`: (time, H, W) - 东向速度
- `v_combined`: (time, H, W) - 北向速度
- `x`: (H, W) - 经度网格 (可选)
- `y`: (H, W) - 纬度网格 (可选)

### 3. NetCDF 格式 (.nc) 
支持标准的 CF 约定和多种命名方式:
- 速度变量: u, v, uo, vo, ucur, vcur 等
- 坐标变量: lat/latitude, lon/longitude
- 可选掩码: mask, land_mask, sea_mask
- 时间维度: time, TIME
- 深度维度: depth, level (自动选择指定层级)

**NetCDF 配置示例**:
```yaml
data:
  data_path: 'path/to/ocean_data.nc'
  nc_config:
    u_var: ['u', 'uo', 'eastward_velocity']  # 按优先级尝试
    v_var: ['v', 'vo', 'northward_velocity']
    lat_var: ['lat', 'latitude']
    lon_var: ['lon', 'longitude']
    depth_level: 0  # 0=表层, -1=底层
```

详细配置参见: `configs/netcdf_example_config.yaml`


## 模型列表
models中可供选择的模型：base,cnn_model,crossformer,fengwu,Fengwu_improved,fuxi,graphcast,nng,NNG_improved,oneforcast,pangu,resnet_model,transformer_former
## 环境要求
- 列出并使用 可用的conda 环境
- 激活命令示例: `conda activate ...` 或 `source activate ...`

## GPU 资源检查与分配 (必须优先执行)

### 步骤 0: GPU 状态检查
在执行任何代码之前,**必须先检查 GPU 使用情况**:

```bash
nvidia-smi
```

**要求**:
1. 仔细查看 `nvidia-smi` 输出,识别哪些 GPU 正在被占用
2. 查看每个 GPU 的显存使用情况 (Memory-Usage 列)
3. 查看每个 GPU 上运行的进程 (Processes 部分)
4. 选择**空闲的 GPU** 来运行数据处理任务
5. 如果所有 GPU 都被占用,选择显存占用最少的 GPU
6. 通过设置 `CUDA_VISIBLE_DEVICES` 环境变量指定使用的 GPU

**示例**:
```bash
# 检查 GPU 状态
nvidia-smi

# 假设 GPU 0,1 正在使用,GPU 2,3 空闲
# 则使用 GPU 2 来运行任务
export CUDA_VISIBLE_DEVICES=2

# 或者使用多个空闲 GPU
export CUDA_VISIBLE_DEVICES=2,3
```

**重要提示**:
- 数据处理脚本本身可能不需要 GPU (主要是 CPU 密集型),但检查 GPU 状态是为了避免资源冲突
- 如果后续需要在 GPU 上运行可视化或其他计算,使用已选定的空闲 GPU
- 在报告中记录使用的 GPU 编号和选择原因

## 处理流程

### 1. 数据读取与初步分析

### 2.列出所有可供选择的模型供用户选择
注意要把所有模型列出来，而不是仅仅在终端提供几个选项供用户选择（重要）
models中可供选择的模型：base,cnn_model,crossformer,fengwu,Fengwu_improved,fuxi,graphcast,nng,NNG_improved,oneforcast,pangu,resnet_model,transformer_former
### 2. 原始数据统计分析 (必须完成)
变量名:
最小值: 
最大值: 
平均值: 
标准差: 
NaN比例: 
## 🌍 空间分布

### 地理范围

- **经度范围：** 
- **纬度范围：**
- **空间分辨率：** 
- **网格大小：** 

### 空间可视化


---

## ⏱️ 时间特征

### 时间序列统计

- **起始时间：** 
- **结束时间：** 
- **时间间隔：** 
- **总天数：** 
- **预测时间步：** 

### 时间序列可视化

## 📈 数据质量检查

### 质量指标

| 检查项 | 状态 | 详情 |
|--------|------|------|
| **数据完整性** |  | |
| **时间连续性** | |  |
| **数值范围** | | |
| **NaN 处理** ||  |

### 数据质量可视化

### 3. 原始数据可视化 (必须生成以下图表)
### 3.1 生成输出数据的可视化


#### 3.2数据分布直方图



### 4. 处理后数据验证与可视化
仿照步骤3完成处理后数据概览，文件信息，数据信息，数据统计和可视化。

### 5. 报告生成 (重点)

生成一份详细的 Markdown 格式报告

报告必须严格遵守skill中report.md的要求。

### 容错处理
- 禁止修改SKILL中的内容，需要修改或者新建脚本放在用户目录中
- 检查输入文件是否存在
- 验证数据维度是否正确
- 处理可能的内存不足问题
- 捕获并报告异常

## 输出文件清单

## 验收标准

- [ ] 执行 nvidia-smi 检查 GPU 状态
- [ ] 正确选择空闲的 GPU
- [ ] 设置 CUDA_VISIBLE_DEVICES 环境变量
- [ ] 成功读取用户提供的原始数据
- [ ] 完成统计分析 
- [ ] 生成可视化图表
- [ ] 成功生成可供模型训练的正确格式的文件
- [ ] 生成完整详细的中文的 Markdown 报告
- [ ] 报告中所有图表链接有效
- [ ] 报告中统计数据准确
- [ ] 报告中记录了 GPU 选择信息
- [ ] 所有文件保存在指定输出目录

