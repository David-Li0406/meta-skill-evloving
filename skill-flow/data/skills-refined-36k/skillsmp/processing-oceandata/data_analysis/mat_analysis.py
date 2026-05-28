"""
数据分析脚本 - 自动识别和分析 MAT 类型数据
本脚本用于加载、分析和可视化 MATLAB 格式的海洋流场数据，自动识别变量名和数据结构。

功能:
- 自动查找项目中的 MAT 文件
- 自动识别速度场变量 (u, v)
- 自动识别坐标变量 (lon, lat)
- 自动检测其他相关变量 (adt, ssh, temperature, salinity 等)
- 生成详细的统计分析报告
"""

import scipy.io
import numpy as np
import os
import argparse
import glob
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional


# 常见变量名映射（按优先级排序）
VELOCITY_U_NAMES = [
    'u', 'U', 'u_combined', 'ucur', 'UCUR', 'u_velocity',
    'eastward_velocity', 'water_u', 'u_component'
]

VELOCITY_V_NAMES = [
    'v', 'V', 'v_combined', 'vcur', 'VCUR', 'v_velocity',
    'northward_velocity', 'water_v', 'v_component'
]

LONGITUDE_NAMES = [
    'lon', 'longitude', 'LON', 'LONGITUDE', 'x', 'X',
    'nav_lon', 'Lon', 'Longitude'
]

LATITUDE_NAMES = [
    'lat', 'latitude', 'LAT', 'LATITUDE', 'y', 'Y',
    'nav_lat', 'Lat', 'Latitude'
]

# 其他可能的海洋变量
OCEAN_VARIABLES = {
    'adt': ['adt', 'ADT', 'adt_combined', 'sea_surface_height_above_geoid', 'sla'],
    'ssh': ['ssh', 'SSH', 'sea_surface_height', 'ssh_combined', 'zos'],
    'temperature': ['temp', 'temperature', 'TEMP', 'Temperature', 'sst', 'SST', 'thetao'],
    'salinity': ['sal', 'salinity', 'SAL', 'Salinity', 'sss', 'SSS', 'so'],
}


def find_mat_files(search_dir: Path, recursive: bool = True) -> List[Path]:
    """
    在指定目录中查找所有 MAT 文件

    Args:
        search_dir: 搜索目录
        recursive: 是否递归搜索子目录

    Returns:
        MAT 文件路径列表
    """
    mat_files = []

    if recursive:
        mat_files = list(search_dir.rglob('*.mat'))
    else:
        mat_files = list(search_dir.glob('*.mat'))

    # 排除 MATLAB 系统文件
    mat_files = [f for f in mat_files if not f.name.startswith('._')]

    return sorted(mat_files)


def find_variable(mat_data: Dict, var_names: List[str], var_type: str) -> Optional[Tuple[str, np.ndarray]]:
    """
    在 MAT 数据中查找匹配的变量

    Args:
        mat_data: MATLAB 数据字典
        var_names: 可能的变量名列表（按优先级排序）
        var_type: 变量类型描述（用于日志）

    Returns:
        (变量名, 数据数组) 或 None
    """
    # 获取所有非系统变量
    available_vars = [k for k in mat_data.keys() if not k.startswith('__')]

    for var_name in var_names:
        if var_name in available_vars:
            data = mat_data[var_name]
            if isinstance(data, np.ndarray):
                print(f"  ✓ 找到 {var_type}: '{var_name}' {data.shape}")
                return var_name, data

    print(f"  ✗ 未找到 {var_type}")
    print(f"    尝试过: {var_names[:5]}...")
    print(f"    可用变量: {available_vars}")
    return None


def inspect_mat_file(mat_path: Path) -> Dict:
    """
    检查 MAT 文件内容并返回变量信息

    Args:
        mat_path: MAT 文件路径

    Returns:
        包含变量信息的字典
    """
    print(f"\n{'='*60}")
    print(f"检查 MAT 文件: {mat_path.name}")
    print(f"{'='*60}")

    mat_data = scipy.io.loadmat(str(mat_path))

    # 获取所有非系统变量
    variables = {k: v for k, v in mat_data.items() if not k.startswith('__')}

    print(f"\n发现 {len(variables)} 个变量:")
    for var_name, var_data in variables.items():
        if isinstance(var_data, np.ndarray):
            print(f"  - {var_name:20s} {str(var_data.shape):20s} dtype={var_data.dtype}")
        else:
            print(f"  - {var_name:20s} {str(type(var_data)):20s}")

    return variables


def load_mat_data_auto(mat_path: Path) -> Dict:
    """
    自动识别并加载 MAT 数据文件

    Args:
        mat_path: MAT 文件路径

    Returns:
        包含识别到的所有数据的字典
    """
    print(f"\n{'='*60}")
    print(f"自动加载 MAT 文件: {mat_path.name}")
    print(f"{'='*60}\n")

    mat_data = scipy.io.loadmat(str(mat_path))
    result = {'file_path': mat_path, 'variables': {}}

    # 1. 查找速度场变量
    print("1. 查找速度场变量...")
    u_result = find_variable(mat_data, VELOCITY_U_NAMES, 'U 速度 (东向)')
    v_result = find_variable(mat_data, VELOCITY_V_NAMES, 'V 速度 (北向)')

    if u_result is None or v_result is None:
        print("\n⚠️  警告: 未找到必需的速度场变量 (u, v)")
        return result

    u_name, u_data = u_result
    v_name, v_data = v_result

    result['variables']['u'] = {'name': u_name, 'data': u_data}
    result['variables']['v'] = {'name': v_name, 'data': v_data}

    # 检查形状一致性
    if u_data.shape != v_data.shape:
        print(f"\n⚠️  警告: U 和 V 速度形状不一致: {u_data.shape} vs {v_data.shape}")

    # 2. 查找坐标变量
    print("\n2. 查找坐标变量...")
    lon_result = find_variable(mat_data, LONGITUDE_NAMES, '经度')
    lat_result = find_variable(mat_data, LATITUDE_NAMES, '纬度')

    if lon_result is not None and lat_result is not None:
        lon_name, lon_data = lon_result
        lat_name, lat_data = lat_result
        result['variables']['lon'] = {'name': lon_name, 'data': lon_data}
        result['variables']['lat'] = {'name': lat_name, 'data': lat_data}
    else:
        # 生成虚拟坐标
        print("  → 生成虚拟坐标网格")
        if u_data.ndim >= 2:
            H, W = u_data.shape[-2:]
            lon_data = np.arange(W)[np.newaxis, :].repeat(H, axis=0)
            lat_data = np.arange(H)[:, np.newaxis].repeat(W, axis=1)
            result['variables']['lon'] = {'name': 'generated_lon', 'data': lon_data}
            result['variables']['lat'] = {'name': 'generated_lat', 'data': lat_data}

    # 3. 查找其他海洋变量
    print("\n3. 查找其他海洋变量...")
    for var_type, var_names in OCEAN_VARIABLES.items():
        var_result = find_variable(mat_data, var_names, var_type.upper())
        if var_result is not None:
            var_name, var_data = var_result
            result['variables'][var_type] = {'name': var_name, 'data': var_data}

    # 4. 生成掩码
    print("\n4. 生成数据掩码...")
    mask = np.isnan(u_data) | np.isnan(v_data)
    result['mask'] = mask

    total_points = mask.size
    masked_points = np.sum(mask)
    valid_points = total_points - masked_points

    print(f"  总数据点: {total_points:,}")
    print(f"  有效数据点: {valid_points:,} ({valid_points/total_points*100:.2f}%)")
    print(f"  掩码数据点: {masked_points:,} ({masked_points/total_points*100:.2f}%)")

    return result


def compute_statistics(data: np.ndarray, mask: np.ndarray, var_name: str) -> Dict:
    """
    计算变量的统计信息

    Args:
        data: 数据数组
        mask: 掩码数组 (True 表示无效数据)
        var_name: 变量名称

    Returns:
        统计信息字典
    """
    # 移除 NaN 和 mask 区域
    valid_data = data[~mask]

    if valid_data.size == 0:
        return {
            'name': var_name,
            'min': np.nan,
            'max': np.nan,
            'mean': np.nan,
            'std': np.nan,
            'median': np.nan,
            'percentile_25': np.nan,
            'percentile_75': np.nan,
            'nan_ratio': 100.0,
            'valid_points': 0,
            'total_points': mask.size
        }

    stats = {
        'name': var_name,
        'min': np.nanmin(valid_data),
        'max': np.nanmax(valid_data),
        'mean': np.nanmean(valid_data),
        'std': np.nanstd(valid_data),
        'median': np.nanmedian(valid_data),
        'percentile_25': np.nanpercentile(valid_data, 25),
        'percentile_75': np.nanpercentile(valid_data, 75),
        'nan_ratio': np.sum(mask) / mask.size * 100,
        'valid_points': valid_data.size,
        'total_points': mask.size
    }

    return stats


def analyze_data(data_dict: Dict) -> Dict:
    """
    分析加载的数据并生成统计信息

    Args:
        data_dict: load_mat_data_auto 返回的数据字典

    Returns:
        包含所有统计信息的字典
    """
    print(f"\n{'='*60}")
    print("数据统计分析")
    print(f"{'='*60}\n")

    variables = data_dict.get('variables', {})
    mask = data_dict.get('mask')

    if mask is None:
        print("⚠️  警告: 未找到掩码，无法进行统计分析")
        return {}

    stats_results = {}

    # 分析速度场
    for var_key in ['u', 'v']:
        if var_key in variables:
            var_info = variables[var_key]
            var_name = var_info['name']
            var_data = var_info['data']

            print(f"分析 {var_key.upper()} 速度 (变量名: '{var_name}')...")
            stats = compute_statistics(var_data, mask, var_name)
            stats_results[var_key] = stats

            # 打印统计信息
            print(f"  最小值: {stats['min']:.6f}")
            print(f"  最大值: {stats['max']:.6f}")
            print(f"  平均值: {stats['mean']:.6f}")
            print(f"  标准差: {stats['std']:.6f}")
            print(f"  中位数: {stats['median']:.6f}")
            print(f"  有效数据比例: {100-stats['nan_ratio']:.2f}%\n")

    # 分析其他海洋变量
    for var_key in ['adt', 'ssh', 'temperature', 'salinity']:
        if var_key in variables:
            var_info = variables[var_key]
            var_name = var_info['name']
            var_data = var_info['data']

            # 为其他变量生成掩码（可能与速度场掩码不同）
            var_mask = mask | np.isnan(var_data)

            print(f"分析 {var_key.upper()} (变量名: '{var_name}')...")
            stats = compute_statistics(var_data, var_mask, var_name)
            stats_results[var_key] = stats

            print(f"  最小值: {stats['min']:.6f}")
            print(f"  最大值: {stats['max']:.6f}")
            print(f"  平均值: {stats['mean']:.6f}")
            print(f"  标准差: {stats['std']:.6f}")
            print(f"  有效数据比例: {100-stats['nan_ratio']:.2f}%\n")

    # 分析空间范围
    if 'lon' in variables and 'lat' in variables:
        lon_data = variables['lon']['data']
        lat_data = variables['lat']['data']

        lon_valid = lon_data[~np.isnan(lon_data)]
        lat_valid = lat_data[~np.isnan(lat_data)]

        spatial_info = {
            'lon_min': np.min(lon_valid),
            'lon_max': np.max(lon_valid),
            'lat_min': np.min(lat_valid),
            'lat_max': np.max(lat_valid),
            'lon_range': np.max(lon_valid) - np.min(lon_valid),
            'lat_range': np.max(lat_valid) - np.min(lat_valid)
        }

        stats_results['spatial'] = spatial_info

        print("空间范围:")
        print(f"  经度: {spatial_info['lon_min']:.4f}° ~ {spatial_info['lon_max']:.4f}° (范围: {spatial_info['lon_range']:.4f}°)")
        print(f"  纬度: {spatial_info['lat_min']:.4f}° ~ {spatial_info['lat_max']:.4f}° (范围: {spatial_info['lat_range']:.4f}°)\n")

    # 时间信息
    if 'u' in variables:
        u_data = variables['u']['data']
        if u_data.ndim >= 3:
            time_steps = u_data.shape[0]
            spatial_shape = u_data.shape[1:]

            temporal_info = {
                'time_steps': time_steps,
                'spatial_shape': spatial_shape
            }

            stats_results['temporal'] = temporal_info

            print("时间信息:")
            print(f"  时间步数: {time_steps}")
            print(f"  空间形状: {spatial_shape}\n")

    return stats_results


def print_summary_table(stats_results: Dict):
    """
    打印统计信息汇总表

    Args:
        stats_results: analyze_data 返回的统计结果
    """
    print(f"\n{'='*80}")
    print("统计信息汇总表")
    print(f"{'='*80}\n")

    # 变量统计表
    print(f"{'变量名':<20} {'最小值':>12} {'最大值':>12} {'平均值':>12} {'标准差':>12} {'有效率':>10}")
    print("-" * 80)

    for var_key in ['u', 'v', 'adt', 'ssh', 'temperature', 'salinity']:
        if var_key in stats_results:
            stats = stats_results[var_key]
            valid_ratio = 100 - stats['nan_ratio']
            print(f"{stats['name']:<20} {stats['min']:>12.6f} {stats['max']:>12.6f} "
                  f"{stats['mean']:>12.6f} {stats['std']:>12.6f} {valid_ratio:>9.2f}%")

    print()


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='自动识别和分析 MAT 格式的海洋数据',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  # 自动查找并分析项目中的第一个 MAT 文件
  python mat_analysis.py

  # 分析指定的 MAT 文件
  python mat_analysis.py --mat_path /path/to/data.mat

  # 检查 MAT 文件内容（不进行分析）
  python mat_analysis.py --mat_path /path/to/data.mat --inspect-only

  # 在指定目录搜索 MAT 文件
  python mat_analysis.py --search_dir /path/to/directory
        """
    )

    parser.add_argument(
        '--mat_path',
        type=str,
        default=None,
        help='MAT 文件路径（如果不指定，将自动搜索）'
    )

    parser.add_argument(
        '--search_dir',
        type=str,
        default=None,
        help='搜索 MAT 文件的目录（默认：项目根目录）'
    )

    parser.add_argument(
        '--inspect-only',
        action='store_true',
        help='仅检查文件内容，不进行统计分析'
    )

    parser.add_argument(
        '--output_dir',
        type=str,
        default=None,
        help='输出目录（默认：./outputs）'
    )

    args = parser.parse_args()

    print(f"\n{'='*60}")
    print("MAT 数据自动分析工具")
    print(f"{'='*60}\n")

    # 确定搜索目录
    if args.search_dir:
        search_dir = Path(args.search_dir)
    else:
        # 查找项目根目录
        current = Path.cwd()
        while current != current.parent:
            if (current / '.claude').exists() or (current / '.git').exists():
                search_dir = current
                break
            current = current.parent
        else:
            search_dir = Path.cwd()

    print(f"搜索目录: {search_dir}\n")

    # 查找或使用指定的 MAT 文件
    if args.mat_path:
        mat_path = Path(args.mat_path)
        if not mat_path.exists():
            print(f"❌ 错误: 文件不存在: {mat_path}")
            return
        print(f"使用指定的 MAT 文件: {mat_path.name}\n")
    else:
        # 自动查找 MAT 文件
        print("自动查找 MAT 文件...")
        mat_files = find_mat_files(search_dir)

        if not mat_files:
            print(f"❌ 未找到 MAT 文件在目录: {search_dir}")
            print("请使用 --mat_path 参数指定文件路径")
            return

        if len(mat_files) == 1:
            mat_path = mat_files[0]
            print(f"找到 1 个 MAT 文件: {mat_path.name}\n")
        else:
            print(f"找到 {len(mat_files)} 个 MAT 文件:")
            for i, f in enumerate(mat_files, 1):
                print(f"  [{i}] {f.relative_to(search_dir)}")
            mat_path = mat_files[0]
            print(f"\n使用第一个文件: {mat_path.name}")
            print("要使用其他文件，请用 --mat_path 参数指定\n")

    # 仅检查模式
    if args.inspect_only:
        inspect_mat_file(mat_path)
        return

    # 自动加载数据
    data_dict = load_mat_data_auto(mat_path)

    if not data_dict.get('variables'):
        print("\n❌ 未能识别有效的数据变量")
        print("使用 --inspect-only 查看文件内容")
        return

    # 统计分析
    stats_results = analyze_data(data_dict)

    # 打印汇总表
    if stats_results:
        print_summary_table(stats_results)

    # 保存结果（可选）
    if args.output_dir:
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # 保存统计信息为 JSON
        import json
        stats_file = output_dir / f'{mat_path.stem}_statistics.json'

        # 转换 numpy 类型为 Python 原生类型
        def convert_numpy(obj):
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, (np.integer, np.floating)):
                return obj.item()
            elif isinstance(obj, dict):
                return {k: convert_numpy(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_numpy(v) for v in obj]
            return obj

        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(convert_numpy(stats_results), f, indent=2, ensure_ascii=False)

        print(f"✅ 统计信息已保存到: {stats_file}")

    print(f"\n{'='*60}")
    print("分析完成！")
    print(f"{'='*60}\n")


if __name__ == '__main__':
    main()
