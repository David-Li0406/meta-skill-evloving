#!/usr/bin/env python3
"""
提示优化脚本

使用A/B测试和指标跟踪自动测试和优化提示。
"""

import json
import time
from typing import List, Dict, Any
from dataclasses import dataclass
import numpy as np


@dataclass
class TestCase:
    input: Dict[str, Any]
    expected_output: str
    metadata: Dict[str, Any] = None


class PromptOptimizer:
    def __init__(self, llm_client, test_suite: List[TestCase]):
        self.client = llm_client
        self.test_suite = test_suite
        self.results_history = []

    def evaluate_prompt(self, prompt_template: str, test_cases: List[TestCase] = None) -> Dict[str, float]:
        """根据测试案例评估提示模板。"""
        if test_cases is None:
            test_cases = self.test_suite

        metrics = {
            'accuracy': [],
            'latency': [],
            'token_count': [],
            'success_rate': []
        }

        for test_case in test_cases:
            start_time = time.time()

            # 使用测试案例输入渲染提示
            prompt = prompt_template.format(**test_case.input)

            # 获取LLM响应
            response = self.client.complete(prompt)

            # 测量延迟
            latency = time.time() - start_time

            # 计算指标
            metrics['latency'].append(latency)
            metrics['token_count'].append(len(prompt.split()) + len(response.split()))
            metrics['success_rate'].append(1 if response else 0)

            # 检查准确性
            accuracy = self.calculate_accuracy(response, test_case.expected_output)
            metrics['accuracy'].append(accuracy)

        # 聚合指标
        return {
            'avg_accuracy': np.mean(metrics['accuracy']),
            'avg_latency': np.mean(metrics['latency']),
            'p95_latency': np.percentile(metrics['latency'], 95),
            'avg_tokens': np.mean(metrics['token_count']),
            'success_rate': np.mean(metrics['success_rate'])
        }

    def calculate_accuracy(self, response: str, expected: str) -> float:
        """计算响应和期望输出之间的准确性分数。"""
        # 简单精确匹配
        if response.strip().lower() == expected.strip().lower():
            return 1.0

        # 使用词重叠的部分匹配
        response_words = set(response.lower().split())
        expected_words = set(expected.lower().split())

        if not expected_words:
            return 0.0

        overlap = len(response_words & expected_words)
        return overlap / len(expected_words)

    def optimize(self, base_prompt: str, max_iterations: int = 5) -> Dict[str, Any]:
        """迭代优化提示。"""
        current_prompt = base_prompt
        best_prompt = base_prompt
        best_score = 0

        for iteration in range(max_iterations):
            print(f"\n迭代 {iteration + 1}/{max_iterations}")

            # 评估当前提示
            metrics = self.evaluate_prompt(current_prompt)
            print(f"准确性：{metrics['avg_accuracy']:.2f}, 延迟：{metrics['avg_latency']:.2f}s")

            # 跟踪结果
            self.results_history.append({
                'iteration': iteration,
                'prompt': current_prompt,
                'metrics': metrics
            })

            # 如果改进则更新最佳
            if metrics['avg_accuracy'] > best_score:
                best_score = metrics['avg_accuracy']
                best_prompt = current_prompt

            # 如果足够好则停止
            if metrics['avg_accuracy'] > 0.95:
                print("达到目标准确性！")
                break

            # 为下一次迭代生成变体
            variations = self.generate_variations(current_prompt, metrics)

            # 测试变体并选择最佳
            best_variation = current_prompt
            best_variation_score = metrics['avg_accuracy']

            for variation in variations:
                var_metrics = self.evaluate_prompt(variation)
                if var_metrics['avg_accuracy'] > best_variation_score:
                    best_variation_score = var_metrics['avg_accuracy']
                    best_variation = variation

            current_prompt = best_variation

        return {
            'best_prompt': best_prompt,
            'best_score': best_score,
            'history': self.results_history
        }

    def generate_variations(self, prompt: str, current_metrics: Dict) -> List[str]:
        """生成要测试的提示变体。"""
        variations = []

        # 变体1：添加显式格式指令
        variations.append(prompt + "\n\n以清晰、简洁的格式提供你的答案。")

        # 变体2：添加逐步指令
        variations.append("让我们一步步解决这个问题。\n\n" + prompt)

        # 变体3：添加验证步骤
        variations.append(prompt + "\n\n在响应前验证你的答案。")

        # 变体4：使其更简洁
        concise = self.make_concise(prompt)
        if concise != prompt:
            variations.append(concise)

        # 变体5：添加示例（如果没有的话）
        if "example" not in prompt.lower():
            variations.append(self.add_examples(prompt))

        return variations[:3]  # 返回前3个变体

    def make_concise(self, prompt: str) -> str:
        """移除冗余词使提示更简洁。"""
        replacements = [
            ("in order to", "to"),
            ("due to the fact that", "because"),
            ("at this point in time", "now"),
            ("in the event that", "if"),
        ]

        result = prompt
        for old, new in replacements:
            result = result.replace(old, new)

        return result

    def add_examples(self, prompt: str) -> str:
        """向提示添加示例部分。"""
        return f"""{prompt}

示例：
输入：样本输入
输出：样本输出
"""

    def compare_prompts(self, prompt_a: str, prompt_b: str) -> Dict[str, Any]:
        """A/B测试两个提示。"""
        print("测试提示A...")
        metrics_a = self.evaluate_prompt(prompt_a)

        print("测试提示B...")
        metrics_b = self.evaluate_prompt(prompt_b)

        return {
            'prompt_a_metrics': metrics_a,
            'prompt_b_metrics': metrics_b,
            'winner': 'A' if metrics_a['avg_accuracy'] > metrics_b['avg_accuracy'] else 'B',
            'improvement': abs(metrics_a['avg_accuracy'] - metrics_b['avg_accuracy'])
        }

    def export_results(self, filename: str):
        """将优化结果导出到JSON。"""
        with open(filename, 'w') as f:
            json.dump(self.results_history, f, indent=2)


def main():
    # 使用示例
    test_suite = [
        TestCase(
            input={'text': '这部电影太棒了！'},
            expected_output='正面'
        ),
        TestCase(
            input={'text': '最糟糕的购买。'},
            expected_output='负面'
        ),
        TestCase(
            input={'text': '还行，没什么特别的。'},
            expected_output='中性'
        )
    ]

    # 用于演示的模拟LLM客户端
    class MockLLMClient:
        def complete(self, prompt):
            # 模拟LLM响应
            if 'amazing' in prompt:
                return '正面'
            elif 'worst' in prompt.lower():
                return '负面'
            else:
                return '中性'

    optimizer = PromptOptimizer(MockLLMClient(), test_suite)

    base_prompt = "分类以下文本的情感：{text}\n情感："

    results = optimizer.optimize(base_prompt)

    print("\n" + "="*50)
    print("优化完成！")
    print(f"最佳准确性：{results['best_score']:.2f}")
    print(f"最佳提示：\n{results['best_prompt']}")

    optimizer.export_results('optimization_results.json')


if __name__ == '__main__':
    main()