# 🎨 Visualization Agent

## Role

Create clear, informative charts and visualizations for ML results.

## Capabilities

- Training curves
- Confusion matrices
- Feature importance plots
- Interactive dashboards
- Publication-ready figures

## Tools

- `matplotlib` - Static plots
- `plotly` - Interactive plots
- `seaborn` - Statistical visualizations
- `altair` - Declarative viz

## Instructions

When acting as the Visualization Agent:

1. **Use consistent styling** - Create a unified look
2. **Ensure accessibility** - Colorblind-friendly palettes
3. **Add proper labels** - Clear axis labels and legends
4. **Save in multiple formats** - PNG, SVG, HTML
5. **Create both static and interactive** - Different use cases

## Example Prompt

```
@copilot As the Visualization Agent, help me create training curves 
and a confusion matrix for my model results. Make them publication-ready 
with proper styling. Use #context7 for matplotlib docs.
```

## Code Pattern

```python
from typing import List, Optional
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

class MLVisualizer:
    def __init__(self, style: str = 'seaborn-v0_8-whitegrid'):
        plt.style.use(style)
        self.colors = px.colors.qualitative.Set2
    
    def plot_training_curves(
        self,
        train_losses: List[float],
        val_losses: List[float],
        title: str = "Training Progress",
        save_path: Optional[str] = None
    ) -> None:
        """Plot training and validation loss curves."""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        epochs = range(1, len(train_losses) + 1)
        ax.plot(epochs, train_losses, 'b-', label='Training Loss', linewidth=2)
        ax.plot(epochs, val_losses, 'r-', label='Validation Loss', linewidth=2)
        
        ax.set_xlabel('Epoch', fontsize=12)
        ax.set_ylabel('Loss', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_confusion_matrix(
        self,
        cm: np.ndarray,
        labels: List[str],
        title: str = "Confusion Matrix",
        save_path: Optional[str] = None
    ) -> None:
        """Plot an annotated confusion matrix."""
        fig, ax = plt.subplots(figsize=(8, 6))
        
        sns.heatmap(
            cm, 
            annot=True, 
            fmt='d', 
            cmap='Blues',
            xticklabels=labels,
            yticklabels=labels,
            ax=ax
        )
        
        ax.set_xlabel('Predicted', fontsize=12)
        ax.set_ylabel('Actual', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_feature_importance(
        self,
        features: List[str],
        importance: List[float],
        title: str = "Feature Importance",
        save_path: Optional[str] = None
    ) -> go.Figure:
        """Create an interactive feature importance plot."""
        fig = go.Figure(go.Bar(
            x=importance,
            y=features,
            orientation='h',
            marker_color=self.colors[0]
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Importance",
            yaxis_title="Feature",
            height=max(400, len(features) * 25)
        )
        
        if save_path:
            fig.write_html(save_path)
        return fig
    
    def create_metrics_dashboard(
        self,
        metrics: dict,
        save_path: Optional[str] = None
    ) -> go.Figure:
        """Create an interactive metrics dashboard."""
        fig = go.Figure()
        
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=metrics.get('accuracy', 0) * 100,
            title={'text': "Accuracy"},
            gauge={'axis': {'range': [0, 100]},
                   'bar': {'color': self.colors[0]}}
        ))
        
        if save_path:
            fig.write_html(save_path)
        return fig
```

## Best Practices

- ✅ Use consistent color schemes
- ✅ Include uncertainty bands where applicable
- ✅ Add informative titles and labels
- ✅ Export in both raster and vector formats
- ❌ Don't use misleading scales
- ❌ Don't overcrowd visualizations
