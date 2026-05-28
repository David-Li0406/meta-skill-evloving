#!/usr/bin/env python
"""
验证模型配置统一化
检查所有配置文件、类映射和命名规范
"""

import sys
import os
import yaml
from pathlib import Path

# 设置路径
PROJECT_ROOT = Path('/home/xgc/work/NeuralFramework')
sys.path.insert(0, str(PROJECT_ROOT))

from models import _model_dict

def print_header(title):
    """打印标题"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80)

def print_section(title):
    """打印小节标题"""
    print(f"\n{title}")
    print("-"*80)

def validate_model_naming():
    """验证模型命名"""
    print_header("1. 模型命名验证")
    
    expected_models = {
        "Fuxi": ["Fuxi", "Fuxi_Light", "Fuxi_Full", "Fuxi_Auto"],
        "NNG": ["NNG", "NNG_Light", "NNG_Full", "NNG_Auto"],
        "OneForecast": ["OneForecast", "OneForecast_Light", "OneForecast_Balanced", "OneForecast_Full", "OneForecast_Auto"],
        "GraphCast": ["GraphCast", "GraphCast_Light", "GraphCast_Full", "GraphCast_Auto"],
    }
    
    all_pass = True
    
    for series, models in expected_models.items():
        print_section(f"{series} 系列")
        for model_name in models:
            if model_name in _model_dict:
                model_class = _model_dict[model_name]
                print(f"  ✅ {model_name:30s} → {model_class.__name__}")
            else:
                print(f"  ❌ {model_name:30s} → NOT FOUND")
                all_pass = False
    
    return all_pass

def validate_config_files():
    """验证配置文件"""
    print_header("2. 配置文件验证")
    
    config_dir = PROJECT_ROOT / "configs" / "models"
    
    expected_configs = {
        "Fuxi": ["fuxi_light_conf.yaml", "fuxi_balanced_conf.yaml", "fuxi_full_conf.yaml", "fuxi_auto_conf.yaml"],
        "NNG": ["nng_light_conf.yaml", "nng_balanced_conf.yaml", "nng_full_conf.yaml", "nng_auto_conf.yaml"],
        "OneForecast": ["oneforcast_light_conf.yaml", "oneforcast_balanced_conf.yaml", "oneforcast_full_conf.yaml", "oneforcast_auto_conf.yaml"],
        "GraphCast": ["graphcast_light_conf.yaml", "graphcast_balanced_conf.yaml", "graphcast_full_conf.yaml", "graphcast_auto_conf.yaml"],
    }
    
    all_pass = True
    config_count = 0
    
    for series, configs in expected_configs.items():
        print_section(f"{series} 系列配置")
        for config_file in configs:
            config_path = config_dir / config_file
            config_count += 1
            
            if config_path.exists():
                try:
                    with open(config_path, 'r') as f:
                        config = yaml.safe_load(f)
                    
                    # 检查必需字段
                    required_fields = ['input_len', 'output_len', 'in_channels']
                    missing = [f for f in required_fields if f not in config]
                    
                    if not missing:
                        print(f"  ✅ {config_file:40s} [有效]")
                    else:
                        print(f"  ⚠️  {config_file:40s} [缺少字段: {', '.join(missing)}]")
                        all_pass = False
                        
                except Exception as e:
                    print(f"  ❌ {config_file:40s} [读取错误: {e}]")
                    all_pass = False
            else:
                print(f"  ❌ {config_file:40s} [不存在]")
                all_pass = False
    
    print(f"\n总计: {config_count} 个配置文件")
    return all_pass

def validate_autoregressive():
    """验证自回归实现"""
    print_header("3. 自回归版本验证")
    
    auto_models = {
        "Fuxi_Auto": "FuxiAutoregressive",
        "NNG_Auto": "NNGAutoregressive",
        "OneForecast_Auto": "OneForecastAutoregressive",
        "GraphCast_Auto": "GraphCastAutoregressive",
    }
    
    all_pass = True
    
    for model_name, expected_class in auto_models.items():
        if model_name in _model_dict:
            model_class = _model_dict[model_name]
            class_name = model_class.__name__
            
            if class_name == expected_class:
                print(f"  ✅ {model_name:30s} → {class_name}")
            else:
                print(f"  ⚠️  {model_name:30s} → {class_name} (期望: {expected_class})")
                all_pass = False
        else:
            print(f"  ❌ {model_name:30s} → NOT FOUND")
            all_pass = False
    
    return all_pass

def validate_mapping_file():
    """验证model_mapping.yaml"""
    print_header("4. 配置映射文件验证")
    
    mapping_file = PROJECT_ROOT / "configs" / "models" / "model_mapping.yaml"
    
    if not mapping_file.exists():
        print("  ❌ model_mapping.yaml 不存在")
        return False
    
    try:
        with open(mapping_file, 'r') as f:
            mappings = yaml.safe_load(f)
        
        expected_keys = [
            # 新命名
            "Fuxi", "Fuxi_Light", "Fuxi_Full", "Fuxi_Auto",
            "NNG", "NNG_Light", "NNG_Full", "NNG_Auto",
            "OneForecast", "OneForecast_Light", "OneForecast_Balanced", "OneForecast_Full", "OneForecast_Auto",
            "GraphCast", "GraphCast_Light", "GraphCast_Full", "GraphCast_Auto",
            # 旧命名（向后兼容）
            "OceanFuxi", "OceanFuxi_Light", "OceanFuxi_Full",
            "OceanNNG", "OceanNNG_Light", "OceanNNG_Full",
            "OceanOneForecast", "OceanOneForecast_Light", "OceanOneForecast_Balanced",
        ]
        
        all_pass = True
        for key in expected_keys:
            if key in mappings:
                config_path = PROJECT_ROOT / mappings[key]
                if config_path.exists():
                    status = "✅"
                else:
                    status = "⚠️ "
                    all_pass = False
                print(f"  {status} {key:35s} → {mappings[key]}")
            else:
                print(f"  ❌ {key:35s} → NOT IN MAPPING")
                all_pass = False
        
        return all_pass
        
    except Exception as e:
        print(f"  ❌ 读取mapping文件失败: {e}")
        return False

def validate_backward_compatibility():
    """验证向后兼容性"""
    print_header("5. 向后兼容性验证")
    
    old_to_new = {
        "OceanFuxi": "Fuxi",
        "OceanFuxi_Light": "Fuxi_Light",
        "OceanFuxi_Full": "Fuxi_Full",
        "OceanNNG": "NNG",
        "OceanNNG_Light": "NNG_Light",
        "OceanNNG_Full": "NNG_Full",
        "OceanOneForecast": "OneForecast",
        "OceanOneForecast_Light": "OneForecast_Light",
        "OceanOneForecast_Balanced": "OneForecast_Balanced",
    }
    
    all_pass = True
    
    for old_name, new_name in old_to_new.items():
        if old_name in _model_dict and new_name in _model_dict:
            old_class = _model_dict[old_name]
            new_class = _model_dict[new_name]
            
            if old_class == new_class:
                print(f"  ✅ {old_name:35s} → {new_name:25s} [{old_class.__name__}]")
            else:
                print(f"  ❌ {old_name:35s} → {new_name:25s} [类不匹配]")
                all_pass = False
        else:
            print(f"  ❌ {old_name:35s} → {new_name:25s} [缺失]")
            all_pass = False
    
    return all_pass

def validate_config_consistency():
    """验证配置一致性"""
    print_header("6. Full版本配置一致性验证")
    
    print("\n检查Full版本配置是否与reference_models架构一致：")
    
    full_configs = {
        "Fuxi_Full": {
            "file": "fuxi_full_conf.yaml",
            "expected": {
                "embed_dim": 512,
                "depth": 48,
                "window_size": 7,
                "num_heads": 8,
                "num_groups": 32,
            }
        },
        "NNG_Full": {
            "file": "nng_full_conf.yaml",
            "expected": {
                "hidden_dim": 128,
                "processor_layers": 16,
                "mesh_level": 5,
            }
        },
    }
    
    config_dir = PROJECT_ROOT / "configs" / "models"
    all_pass = True
    
    for model, info in full_configs.items():
        print_section(model)
        config_path = config_dir / info["file"]
        
        if not config_path.exists():
            print(f"  ❌ 配置文件不存在: {info['file']}")
            all_pass = False
            continue
        
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            
            for param, expected_value in info["expected"].items():
                actual_value = config.get(param)
                if actual_value == expected_value:
                    print(f"  ✅ {param:20s} = {actual_value} (符合reference_models)")
                else:
                    print(f"  ⚠️  {param:20s} = {actual_value} (期望: {expected_value})")
                    all_pass = False
                    
        except Exception as e:
            print(f"  ❌ 读取配置失败: {e}")
            all_pass = False
    
    return all_pass

def print_summary(results):
    """打印总结"""
    print_header("验证总结")
    
    all_tests = [
        ("模型命名", results["naming"]),
        ("配置文件", results["configs"]),
        ("自回归实现", results["autoregressive"]),
        ("配置映射", results["mapping"]),
        ("向后兼容", results["backward_compat"]),
        ("配置一致性", results["consistency"]),
    ]
    
    passed = sum(1 for _, result in all_tests if result)
    total = len(all_tests)
    
    print()
    for test_name, result in all_tests:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {status:10s} - {test_name}")
    
    print()
    print(f"总计: {passed}/{total} 项测试通过")
    print()
    
    if passed == total:
        print("🎉 所有验证通过！模型配置统一化完成。")
        print()
        print("✨ 统一命名方案:")
        print("   - Light: 轻量级版本")
        print("   - Balanced: 平衡版本（默认推荐）")
        print("   - Full: 完整版本（与reference_models一致）")
        print("   - Auto: 自回归版本（长期预测）")
        print()
        print("📚 相关文档:")
        print("   - docs/MODEL_GUIDE.md - 模型使用指南")
        print("   - docs/MODEL_CONFIGURATION_SUMMARY.md - 配置总结")
        print("   - docs/MODEL_NAMING_MIGRATION.md - 迁移指南")
        return True
    else:
        print("⚠️  部分验证未通过，请检查上述输出。")
        return False

def main():
    """主函数"""
    print()
    print("╔" + "="*78 + "╗")
    print("║" + " "*20 + "模型配置统一化验证工具" + " "*26 + "║")
    print("╚" + "="*78 + "╝")
    
    results = {
        "naming": validate_model_naming(),
        "configs": validate_config_files(),
        "autoregressive": validate_autoregressive(),
        "mapping": validate_mapping_file(),
        "backward_compat": validate_backward_compatibility(),
        "consistency": validate_config_consistency(),
    }
    
    success = print_summary(results)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())

