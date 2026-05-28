#!/usr/bin/env python3
"""
Test suite for enhanced chart type detection algorithm (Phase 1).
Tests multi-dimensional analysis combining semantic + structural + rule-based detection.
"""

import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from skills.scripts.generator_v3 import PresentationGenerator


def test_semantic_analysis():
    """Test Layer 1: Semantic field analysis."""
    print("🧪 Testing Semantic Field Analysis...")
    
    generator = PresentationGenerator()
    
    # Test temporal data
    temporal_data = [
        {'label': '2020年收入', 'value': 100},
        {'label': '2021年收入', 'value': 120},
        {'label': '2022年收入', 'value': 150}
    ]
    result = generator._analyze_fields_semantic(temporal_data)
    assert result['is_temporal'] == True, "Failed to detect temporal data"
    print("✓ Temporal data detection works")
    
    # Test categorical data
    categorical_data = [
        {'label': '产品类别A', 'value': 30},
        {'label': '产品类别B', 'value': 25}
    ]
    result = generator._analyze_fields_semantic(categorical_data)
    assert result['is_categorical'] == True, "Failed to detect categorical data"
    print("✓ Categorical data detection works")


def test_structure_analysis():
    """Test Layer 2: Structure inference."""
    print("🧪 Testing Structure Analysis...")
    
    generator = PresentationGenerator()
    
    # Test 2D data (scatter plot)
    xy_data = [
        {'x': 10, 'y': 20, 'label': 'Point A'},
        {'x': 15, 'y': 25, 'label': 'Point B'}
    ]
    result = generator._analyze_data_structure(xy_data)
    assert result['has_xy'] == True, "Failed to detect XY data"
    print("✓ XY data detection works")
    
    # Test 3D data (bubble chart)
    xyz_data = [
        {'x': 10, 'y': 20, 'z': 5, 'label': 'Bubble A'},
        {'x': 15, 'y': 25, 'z': 8, 'label': 'Bubble B'}
    ]
    result = generator._analyze_data_structure(xyz_data)
    assert result['has_xyz'] == True, "Failed to detect XYZ data"
    print("✓ XYZ data detection works")
    
    # Test range data (box plot)
    range_data = [
        {'label': 'Dataset A', 'min': 10, 'max': 20, 'median': 15},
        {'label': 'Dataset B', 'min': 15, 'max': 30, 'median': 22}
    ]
    result = generator._analyze_data_structure(range_data)
    assert result['has_ranges'] == True, "Failed to detect range data"
    print("✓ Range data detection works")
    
    # Test flow data (sankey)
    flow_data = [
        {'source': '访问', 'target': '浏览', 'value': 1000},
        {'source': '浏览', 'target': '购买', 'value': 500}
    ]
    result = generator._analyze_data_structure(flow_data)
    assert result['has_flow'] == True, "Failed to detect flow data"
    print("✓ Flow data detection works")


def test_decision_tree():
    """Test Layer 3: Rule-based decision tree."""
    print("🧪 Testing Decision Tree...")
    
    generator = PresentationGenerator()
    
    # Test 1: BCG Matrix detection
    bcg_data = [
        {'label': '产品A', 'market_share': 30, 'growth_rate': 10},
        {'label': '产品B', 'market_share': 15, 'growth_rate': 20}
    ]
    section = {'title': 'Portfolio Analysis'}
    x_analysis = generator._analyze_fields_semantic(bcg_data)
    structure_analysis = generator._analyze_data_structure(bcg_data)
    result = generator._apply_decision_tree(x_analysis, structure_analysis, section, bcg_data)
    assert result == 'bcg_matrix', f"Expected 'bcg_matrix', got '{result}'"
    print("✓ BCG Matrix detection works")
    
    # Test 2: Gantt chart detection
    gantt_data = [
        {'label': '需求分析', 'start': '2024-01', 'end': '2024-02', 'progress': 80},
        {'label': '设计开发', 'start': '2024-02', 'end': '2024-03', 'progress': 60}
    ]
    section = {'title': 'Project Timeline'}
    x_analysis = generator._analyze_fields_semantic(gantt_data)
    structure_analysis = generator._analyze_data_structure(gantt_data)
    result = generator._apply_decision_tree(x_analysis, structure_analysis, section, gantt_data)
    assert result == 'gantt', f"Expected 'gantt', got '{result}'"
    print("✓ Gantt chart detection works")
    
    # Test 3: Waterfall detection
    waterfall_data = [
        {'label': '起始', 'value': 100, 'is_start': True},
        {'label': '增加', 'value': 20},
        {'label': '减少', 'value': -10},
        {'label': '结束', 'value': 110}
    ]
    section = {'title': 'Revenue Breakdown'}
    x_analysis = generator._analyze_fields_semantic(waterfall_data)
    structure_analysis = generator._analyze_data_structure(waterfall_data)
    result = generator._apply_decision_tree(x_analysis, structure_analysis, section, waterfall_data)
    assert result == 'waterfall', f"Expected 'waterfall', got '{result}'"
    print("✓ Waterfall detection works")
    
    # Test 4: Sankey detection
    sankey_data = [
        {'label': '访问', 'source': '首页', 'target': '浏览', 'value': 1000},
        {'label': '浏览', 'source': '浏览', 'target': '购买', 'value': 500}
    ]
    section = {'title': 'User Journey'}
    x_analysis = generator._analyze_fields_semantic(sankey_data)
    structure_analysis = generator._analyze_data_structure(sankey_data)
    result = generator._apply_decision_tree(x_analysis, structure_analysis, section, sankey_data)
    assert result == 'sankey', f"Expected 'sankey', got '{result}'"
    print("✓ Sankey detection works")


def test_backwards_compatibility():
    """Test that new algorithm maintains backward compatibility with existing tests."""
    print("🧪 Testing Backward Compatibility...")
    
    generator = PresentationGenerator()
    
    # Test existing line chart detection
    line_data = [
        {'label': 'Q1', 'value': 100},
        {'label': 'Q2', 'value': 120},
        {'label': 'Q3', 'value': 150},
        {'label': 'Q4', 'value': 180}
    ]
    section = {'title': 'Quarterly Revenue'}
    result = generator._determine_chart_type_v4(line_data, section)
    assert result == 'line', f"Expected 'line', got '{result}'"
    print("✓ Backward compatible line chart detection")
    
    # Test existing pie chart detection
    pie_data = [
        {'label': '产品A', 'value': 35, 'unit': '%'},
        {'label': '产品B', 'value': 25, 'unit': '%'},
        {'label': '产品C', 'value': 20, 'unit': '%'}
    ]
    section = {'title': 'Market Share'}
    result = generator._determine_chart_type_v4(pie_data, section)
    assert result == 'doughnut', f"Expected 'doughnut', got '{result}'"
    print("✓ Backward compatible pie/doughnut detection")
    
    # Test existing radar chart detection
    radar_data = [
        {'label': '技术能力', 'value': 85},
        {'label': '沟通能力', 'value': 75},
        {'label': '领导能力', 'value': 90},
        {'label': '创新能力', 'value': 80},
        {'label': '执行能力', 'value': 88}
    ]
    section = {'title': 'Team Assessment'}
    result = generator._determine_chart_type_v4(radar_data, section)
    assert result == 'radar', f"Expected 'radar', got '{result}'"
    print("✓ Backward compatible radar chart detection")


def run_all_tests():
    """Run all test suites."""
    print("\n" + "="*60)
    print("PHASE 1: Enhanced Chart Type Detection - Test Suite")
    print("="*60 + "\n")
    
    try:
        test_semantic_analysis()
        test_structure_analysis()
        test_decision_tree()
        test_backwards_compatibility()
        
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED!")
        print("="*60)
        return True
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        print("="*60)
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
