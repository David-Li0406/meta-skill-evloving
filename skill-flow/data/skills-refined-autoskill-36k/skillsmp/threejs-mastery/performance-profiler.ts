/**
 * Performance Profiler for Three.js Applications
 * Real-time monitoring and optimization suggestions
 * 
 * Usage:
 *   import { PerformanceProfiler } from './performance-profiler';
 *   const profiler = new PerformanceProfiler(renderer, scene);
 *   
 *   // In render loop
 *   profiler.begin();
 *   renderer.render(scene, camera);
 *   profiler.end();
 *   
 *   // Get statistics
 *   const stats = profiler.getStats();
 */

import * as THREE from 'three';

interface PerformanceStats {
  fps: number;
  frameTime: number;
  drawCalls: number;
  triangles: number;
  points: number;
  lines: number;
  geometries: number;
  textures: number;
  programs: number;
  memoryUsage: number;
  suggestions: string[];
}

export class PerformanceProfiler {
  private renderer: THREE.WebGPURenderer | THREE.WebGLRenderer;
  private scene: THREE.Scene;
  
  private fpsHistory: number[] = [];
  private frameTimeHistory: number[] = [];
  
  private lastTime: number = performance.now();
  private frameCount: number = 0;
  
  private maxHistoryLength: number = 60;
  
  // Thresholds
  private readonly FPS_WARNING = 50;
  private readonly FPS_CRITICAL = 30;
  private readonly DRAW_CALL_WARNING = 100;
  private readonly TRIANGLE_WARNING = 1000000;
  private readonly MEMORY_WARNING = 500; // MB
  
  constructor(
    renderer: THREE.WebGPURenderer | THREE.WebGLRenderer,
    scene: THREE.Scene
  ) {
    this.renderer = renderer;
    this.scene = scene;
    
    this.startMemoryMonitoring();
  }
  
  /**
   * Call at the start of render loop
   */
  begin(): void {
    this.lastTime = performance.now();
  }
  
  /**
   * Call at the end of render loop
   */
  end(): void {
    const now = performance.now();
    const deltaTime = now - this.lastTime;
    
    // Calculate FPS
    const fps = 1000 / deltaTime;
    this.fpsHistory.push(fps);
    if (this.fpsHistory.length > this.maxHistoryLength) {
      this.fpsHistory.shift();
    }
    
    // Track frame time
    this.frameTimeHistory.push(deltaTime);
    if (this.frameTimeHistory.length > this.maxHistoryLength) {
      this.frameTimeHistory.shift();
    }
    
    this.frameCount++;
  }
  
  /**
   * Get comprehensive performance statistics
   */
  getStats(): PerformanceStats {
    const info = this.renderer.info;
    
    const avgFPS = this.average(this.fpsHistory);
    const avgFrameTime = this.average(this.frameTimeHistory);
    
    const stats: PerformanceStats = {
      fps: avgFPS,
      frameTime: avgFrameTime,
      drawCalls: info.render.calls,
      triangles: info.render.triangles,
      points: info.render.points,
      lines: info.render.lines,
      geometries: info.memory.geometries,
      textures: info.memory.textures,
      programs: this.renderer.info.programs?.length ?? 0,
      memoryUsage: this.getMemoryUsage(),
      suggestions: this.generateSuggestions(info, avgFPS)
    };
    
    return stats;
  }
  
  /**
   * Print formatted statistics to console
   */
  printStats(): void {
    const stats = this.getStats();
    
    console.group('📊 Performance Statistics');
    console.log(`FPS: ${stats.fps.toFixed(1)} ${this.getFPSEmoji(stats.fps)}`);
    console.log(`Frame Time: ${stats.frameTime.toFixed(2)}ms`);
    console.log(`Draw Calls: ${stats.drawCalls}`);
    console.log(`Triangles: ${stats.triangles.toLocaleString()}`);
    console.log(`Geometries: ${stats.geometries}`);
    console.log(`Textures: ${stats.textures}`);
    console.log(`Memory: ${stats.memoryUsage.toFixed(2)}MB`);
    
    if (stats.suggestions.length > 0) {
      console.group('💡 Optimization Suggestions');
      stats.suggestions.forEach(suggestion => {
        console.log(`• ${suggestion}`);
      });
      console.groupEnd();
    }
    
    console.groupEnd();
  }
  
  /**
   * Generate optimization suggestions
   */
  private generateSuggestions(
    info: any,
    avgFPS: number
  ): string[] {
    const suggestions: string[] = [];
    
    // FPS checks
    if (avgFPS < this.FPS_CRITICAL) {
      suggestions.push('🔴 CRITICAL: FPS below 30 - Reduce scene complexity');
    } else if (avgFPS < this.FPS_WARNING) {
      suggestions.push('⚠️ FPS below 50 - Consider optimization');
    }
    
    // Draw calls
    if (info.render.calls > this.DRAW_CALL_WARNING) {
      suggestions.push(
        `Too many draw calls (${info.render.calls}) - Use geometry merging or instancing`
      );
    }
    
    // Triangles
    if (info.render.triangles > this.TRIANGLE_WARNING) {
      suggestions.push(
        `High triangle count (${info.render.triangles.toLocaleString()}) - Implement LOD system`
      );
    }
    
    // Memory
    const memory = this.getMemoryUsage();
    if (memory > this.MEMORY_WARNING) {
      suggestions.push(
        `High memory usage (${memory.toFixed(0)}MB) - Check for memory leaks`
      );
    }
    
    // Texture count
    if (info.memory.textures > 50) {
      suggestions.push(
        `Many textures loaded (${info.memory.textures}) - Use texture atlases`
      );
    }
    
    // Geometry count
    if (info.memory.geometries > 100) {
      suggestions.push(
        `Many geometries (${info.memory.geometries}) - Reuse geometries where possible`
      );
    }
    
    return suggestions;
  }
  
  /**
   * Get memory usage in MB
   */
  private getMemoryUsage(): number {
    if ('memory' in performance) {
      return (performance as any).memory.usedJSHeapSize / 1048576;
    }
    return 0;
  }
  
  /**
   * Start memory leak detection
   */
  private startMemoryMonitoring(): void {
    let lastMemory = this.getMemoryUsage();
    
    setInterval(() => {
      const currentMemory = this.getMemoryUsage();
      const delta = currentMemory - lastMemory;
      
      // Memory increasing consistently
      if (delta > 10 && currentMemory > 100) {
        console.warn('⚠️ Potential memory leak detected');
        this.diagnoseMemoryLeaks();
      }
      
      lastMemory = currentMemory;
    }, 10000); // Check every 10 seconds
  }
  
  /**
   * Diagnose potential memory leaks
   */
  private diagnoseMemoryLeaks(): void {
    const info = this.renderer.info;
    
    console.group('🔍 Memory Diagnostics');
    
    // Check for accumulating resources
    console.log('Geometries in memory:', info.memory.geometries);
    console.log('Textures in memory:', info.memory.textures);
    
    // Count objects in scene
    let objectCount = 0;
    this.scene.traverse(() => objectCount++);
    console.log('Objects in scene:', objectCount);
    
    // Suggestions
    console.log('\n💡 Common causes:');
    console.log('• Not disposing geometries/materials when removing objects');
    console.log('• Creating new geometries/materials every frame');
    console.log('• Event listeners not being removed');
    console.log('• Textures not being disposed');
    
    console.groupEnd();
  }
  
  /**
   * Get performance score (0-100)
   */
  getPerformanceScore(): number {
    const stats = this.getStats();
    let score = 100;
    
    // FPS penalty
    if (stats.fps < 60) {
      score -= (60 - stats.fps);
    }
    
    // Draw calls penalty
    if (stats.drawCalls > 50) {
      score -= Math.min((stats.drawCalls - 50) / 2, 20);
    }
    
    // Triangle penalty
    if (stats.triangles > 500000) {
      score -= Math.min((stats.triangles - 500000) / 50000, 15);
    }
    
    // Memory penalty
    if (stats.memoryUsage > 250) {
      score -= Math.min((stats.memoryUsage - 250) / 10, 15);
    }
    
    return Math.max(0, Math.min(100, score));
  }
  
  /**
   * Create visual performance overlay
   */
  createOverlay(): HTMLDivElement {
    const overlay = document.createElement('div');
    overlay.style.position = 'fixed';
    overlay.style.top = '10px';
    overlay.style.right = '10px';
    overlay.style.background = 'rgba(0, 0, 0, 0.8)';
    overlay.style.color = 'white';
    overlay.style.padding = '10px';
    overlay.style.fontFamily = 'monospace';
    overlay.style.fontSize = '12px';
    overlay.style.zIndex = '10000';
    overlay.style.borderRadius = '4px';
    overlay.style.minWidth = '200px';
    
    // Update overlay every frame
    const update = () => {
      const stats = this.getStats();
      const score = this.getPerformanceScore();
      
      overlay.innerHTML = `
        <div style="margin-bottom: 8px; font-weight: bold;">
          Performance: ${score.toFixed(0)}% ${this.getScoreEmoji(score)}
        </div>
        <div>FPS: ${stats.fps.toFixed(1)} ${this.getFPSEmoji(stats.fps)}</div>
        <div>Frame: ${stats.frameTime.toFixed(2)}ms</div>
        <div>Calls: ${stats.drawCalls}</div>
        <div>Tris: ${(stats.triangles / 1000).toFixed(0)}K</div>
        <div>Mem: ${stats.memoryUsage.toFixed(0)}MB</div>
        ${stats.suggestions.length > 0 ? `
          <div style="margin-top: 8px; color: #ffcc00;">
            ${stats.suggestions.length} suggestion(s)
          </div>
        ` : ''}
      `;
      
      requestAnimationFrame(update);
    };
    
    update();
    
    return overlay;
  }
  
  /**
   * Helper: Calculate average
   */
  private average(arr: number[]): number {
    if (arr.length === 0) return 0;
    return arr.reduce((a, b) => a + b, 0) / arr.length;
  }
  
  /**
   * Helper: FPS emoji
   */
  private getFPSEmoji(fps: number): string {
    if (fps >= 60) return '🟢';
    if (fps >= 50) return '🟡';
    if (fps >= 30) return '🟠';
    return '🔴';
  }
  
  /**
   * Helper: Score emoji
   */
  private getScoreEmoji(score: number): string {
    if (score >= 90) return '🟢';
    if (score >= 70) return '🟡';
    if (score >= 50) return '🟠';
    return '🔴';
  }
  
  /**
   * Export statistics to JSON
   */
  exportStats(): string {
    const stats = this.getStats();
    return JSON.stringify(stats, null, 2);
  }
  
  /**
   * Reset statistics
   */
  reset(): void {
    this.fpsHistory = [];
    this.frameTimeHistory = [];
    this.frameCount = 0;
  }
}

// Usage example
export function setupProfiler(
  renderer: THREE.WebGPURenderer | THREE.WebGLRenderer,
  scene: THREE.Scene,
  showOverlay: boolean = true
): PerformanceProfiler {
  const profiler = new PerformanceProfiler(renderer, scene);
  
  if (showOverlay) {
    const overlay = profiler.createOverlay();
    document.body.appendChild(overlay);
  }
  
  // Log stats every 5 seconds
  setInterval(() => {
    profiler.printStats();
  }, 5000);
  
  return profiler;
}
