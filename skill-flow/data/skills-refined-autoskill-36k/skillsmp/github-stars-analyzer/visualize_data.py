"""
Data visualization module.
Generates charts and graphs for repository analysis.
"""

from typing import Dict, List, Any, Optional
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import numpy as np
from datetime import datetime
import io
import base64


class DataVisualizer:
    """Generate visualizations for repository analysis."""

    def __init__(self):
        """Initialize data visualizer."""
        plt.style.use('seaborn-v0_8-darkgrid')
        self.colors = ['#0366d6', '#28a745', '#6f42c1', '#d73a49', '#f66a0a']

    def generate_metrics_chart(self, analysis: Dict[str, Any], output_path: Optional[str] = None) -> Optional[str]:
        """
        Generate a bar chart of key metrics.

        Args:
            analysis: Repository analysis data
            output_path: Optional path to save image

        Returns:
            Base64 encoded image if output_path not provided, else None
        """
        metrics = analysis["metrics"]
        labels = ['Stars', 'Forks', 'Watchers', 'Open Issues', 'Contributors']
        values = [
            metrics["stars"],
            metrics["forks"],
            metrics["watchers"],
            metrics["open_issues"],
            metrics["contributors"]
        ]

        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(labels, values, color=self.colors[:len(labels)])

        # Add value labels on bars
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + max(values)*0.01,
                   f'{value:,}', ha='center', va='bottom', fontsize=10)

        ax.set_title(f'Key Metrics: {analysis["basic_info"]["full_name"]}', fontsize=14, fontweight='bold')
        ax.set_ylabel('Count', fontsize=12)
        ax.grid(axis='y', alpha=0.3)

        plt.tight_layout()

        if output_path:
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            plt.close()
            return None
        else:
            # Return base64 encoded image
            buf = io.BytesIO()
            plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
            plt.close()
            buf.seek(0)
            img_str = base64.b64encode(buf.read()).decode('utf-8')
            return img_str

    def generate_popularity_health_chart(self, analysis: Dict[str, Any], output_path: Optional[str] = None) -> Optional[str]:
        """
        Generate a radar chart for popularity and health scores.

        Args:
            analysis: Repository analysis data
            output_path: Optional path to save image

        Returns:
            Base64 encoded image if output_path not provided, else None
        """
        categories = ['Popularity', 'Health', 'Growth', 'Activity', 'Community']
        scores = [
            analysis["popularity_score"],
            analysis["health_score"],
            min(100, analysis["metrics"]["stars_per_day"] * 10),  # Growth score
            min(100, analysis["activity"]["commits_per_day"] * 50),  # Activity score
            min(100, analysis["metrics"]["contributors"] * 5)  # Community score
        ]

        # Number of variables
        N = len(categories)

        # What will be the angle of each axis in the plot
        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        angles += angles[:1]  # Close the loop
        scores += scores[:1]  # Close the loop

        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))

        # Draw one axe per variable + add labels
        plt.xticks(angles[:-1], categories, size=12)

        # Draw ylabels
        ax.set_rlabel_position(0)
        plt.yticks([20, 40, 60, 80, 100], ["20", "40", "60", "80", "100"], color="grey", size=10)
        plt.ylim(0, 100)

        # Plot data
        ax.plot(angles, scores, linewidth=2, linestyle='solid', color=self.colors[0])
        ax.fill(angles, scores, alpha=0.25, color=self.colors[0])

        # Add title
        plt.title(f'Repository Score Analysis: {analysis["basic_info"]["full_name"]}',
                 size=14, fontweight='bold', pad=20)

        plt.tight_layout()

        if output_path:
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            plt.close()
            return None
        else:
            buf = io.BytesIO()
            plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
            plt.close()
            buf.seek(0)
            img_str = base64.b64encode(buf.read()).decode('utf-8')
            return img_str

    def generate_comparison_chart(self, comparison: Dict[str, Any], metric: str = 'stars',
                                 output_path: Optional[str] = None) -> Optional[str]:
        """
        Generate a comparison chart for multiple repositories.

        Args:
            comparison: Comparative analysis data
            metric: Metric to compare ('stars', 'forks', 'popularity_score', 'health_score')
            output_path: Optional path to save image

        Returns:
            Base64 encoded image if output_path not provided, else None
        """
        repositories = comparison["repositories"]
        metric_labels = {
            'stars': 'Stars',
            'forks': 'Forks',
            'popularity_score': 'Popularity Score',
            'health_score': 'Health Score'
        }

        if metric not in metric_labels:
            metric = 'stars'

        # Get repository names and metric values
        repo_names = [repo["basic_info"]["full_name"] for repo in repositories]
        metric_values = [repo["metrics"].get(metric, repo.get(metric, 0)) for repo in repositories]

        # Sort by metric value
        sorted_data = sorted(zip(repo_names, metric_values), key=lambda x: x[1], reverse=True)
        repo_names = [name for name, _ in sorted_data]
        metric_values = [value for _, value in sorted_data]

        fig, ax = plt.subplots(figsize=(12, 6))
        bars = ax.barh(repo_names, metric_values, color=self.colors[0])

        # Add value labels
        for bar, value in zip(bars, metric_values):
            width = bar.get_width()
            ax.text(width + max(metric_values)*0.01, bar.get_y() + bar.get_height()/2,
                   f'{value:,.0f}' if isinstance(value, (int, float)) and value >= 1 else f'{value:.2f}',
                   va='center', fontsize=10)

        ax.set_xlabel(metric_labels[metric], fontsize=12)
        ax.set_title(f'Repository Comparison: {metric_labels[metric]}', fontsize=14, fontweight='bold')
        ax.invert_yaxis()  # Highest value at top
        ax.grid(axis='x', alpha=0.3)

        plt.tight_layout()

        if output_path:
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            plt.close()
            return None
        else:
            buf = io.BytesIO()
            plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
            plt.close()
            buf.seek(0)
            img_str = base64.b64encode(buf.read()).decode('utf-8')
            return img_str

    def generate_language_pie_chart(self, languages: Dict[str, int], output_path: Optional[str] = None) -> Optional[str]:
        """
        Generate a pie chart of programming languages.

        Args:
            languages: Dictionary of languages and bytes
            output_path: Optional path to save image

        Returns:
            Base64 encoded image if output_path not provided, else None
        """
        if not languages:
            return None

        # Sort languages by bytes (descending)
        sorted_languages = sorted(languages.items(), key=lambda x: x[1], reverse=True)

        # Take top 5 languages, group others as "Other"
        if len(sorted_languages) > 5:
            top_languages = sorted_languages[:5]
            other_bytes = sum(bytes for _, bytes in sorted_languages[5:])
            labels = [lang for lang, _ in top_languages] + ['Other']
            sizes = [bytes for _, bytes in top_languages] + [other_bytes]
        else:
            labels = [lang for lang, _ in sorted_languages]
            sizes = [bytes for _, bytes in sorted_languages]

        # Calculate percentages
        total_bytes = sum(sizes)
        percentages = [(size / total_bytes) * 100 for size in sizes]

        # Create pie chart
        fig, ax = plt.subplots(figsize=(8, 8))
        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labels,
            autopct=lambda pct: f'{pct:.1f}%',
            startangle=90,
            colors=self.colors[:len(labels)]
        )

        # Style the text
        for text in texts:
            text.set_fontsize(11)
        for autotext in autotexts:
            autotext.set_fontsize(10)
            autotext.set_color('white')
            autotext.set_fontweight('bold')

        ax.set_title('Programming Language Distribution', fontsize=14, fontweight='bold')
        ax.axis('equal')  # Equal aspect ratio ensures pie is drawn as circle

        plt.tight_layout()

        if output_path:
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            plt.close()
            return None
        else:
            buf = io.BytesIO()
            plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
            plt.close()
            buf.seek(0)
            img_str = base64.b64encode(buf.read()).decode('utf-8')
            return img_str

    def generate_growth_timeline(self, growth_data: List[Dict[str, Any]], output_path: Optional[str] = None) -> Optional[str]:
        """
        Generate a timeline chart of star growth.

        Args:
            growth_data: List of growth data points
            output_path: Optional path to save image

        Returns:
            Base64 encoded image if output_path not provided, else None
        """
        if not growth_data:
            return None

        # Extract dates and star counts
        dates = [point["date"] for point in growth_data]
        stars = [point["stars"] for point in growth_data]

        # Convert dates to datetime objects
        date_objects = [datetime.strptime(date, "%Y-%m-%d") for date in dates]

        fig, ax = plt.subplots(figsize=(12, 6))

        # Plot star growth
        ax.plot(date_objects, stars, marker='o', linewidth=2, color=self.colors[0])

        # Calculate and plot trend line
        if len(stars) > 1:
            x_numeric = np.arange(len(stars))
            z = np.polyfit(x_numeric, stars, 1)
            p = np.poly1d(z)
            ax.plot(date_objects, p(x_numeric), '--', color=self.colors[1], alpha=0.7, label='Trend')

        # Format x-axis dates
        fig.autofmt_xdate()
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Stars', fontsize=12)
        ax.set_title('Star Growth Timeline', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)

        # Add star count annotations at significant points
        if len(stars) >= 3:
            # First, middle, and last points
            for idx in [0, len(stars)//2, -1]:
                ax.annotate(f'{stars[idx]:,}',
                           xy=(date_objects[idx], stars[idx]),
                           xytext=(0, 10),
                           textcoords='offset points',
                           ha='center',
                           fontsize=10,
                           fontweight='bold')

        ax.legend()
        plt.tight_layout()

        if output_path:
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            plt.close()
            return None
        else:
            buf = io.BytesIO()
            plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
            plt.close()
            buf.seek(0)
            img_str = base64.b64encode(buf.read()).decode('utf-8')
            return img_str