// Package capacity provides capacity planning utilities for Kubernetes/OpenShift clusters.
// It includes calculations for pod capacity, resource headroom, and usage trending.
package capacity

import (
	"fmt"
	"math"
	"time"
)

// PodProfile defines standard pod resource profiles
type PodProfile string

const (
	PodProfileSmall  PodProfile = "small"
	PodProfileMedium PodProfile = "medium"
	PodProfileLarge  PodProfile = "large"
	PodProfileCustom PodProfile = "custom"
)

// DefaultPodProfiles defines the default resource requirements for each profile
var DefaultPodProfiles = map[PodProfile]PodResources{
	PodProfileSmall:  {CPUMillicores: 100, MemoryMB: 64},
	PodProfileMedium: {CPUMillicores: 200, MemoryMB: 128},
	PodProfileLarge:  {CPUMillicores: 400, MemoryMB: 256},
}

// PodResources represents the resource requirements for a pod
type PodResources struct {
	CPUMillicores int64 `json:"cpu_millicores"`
	MemoryMB      int64 `json:"memory_mb"`
}

// NamespaceQuota represents the resource quota for a namespace
type NamespaceQuota struct {
	CPULimitMillicores    int64 `json:"cpu_limit_millicores"`
	MemoryLimitBytes      int64 `json:"memory_limit_bytes"`
	PodCountLimit         int   `json:"pod_count_limit"`
	CPUUsedMillicores     int64 `json:"cpu_used_millicores"`
	MemoryUsedBytes       int64 `json:"memory_used_bytes"`
	CurrentPodCount       int   `json:"current_pod_count"`
	HasQuota              bool  `json:"has_quota"`
}

// AvailableCapacity represents the remaining capacity in a namespace
type AvailableCapacity struct {
	CPUMillicores int64 `json:"cpu_millicores"`
	MemoryBytes   int64 `json:"memory_bytes"`
	PodSlots      int   `json:"pod_slots"`
}

// PodEstimate represents the estimated pod count for a specific profile
type PodEstimate struct {
	CPUMillicores int64  `json:"cpu_millicores"`
	MemoryMB      int64  `json:"memory_mb"`
	MaxPods       int    `json:"max_pods"`
	SafePods      int    `json:"safe_pods"`
	LimitingFactor string `json:"limiting_factor"`
}

// TrendingInfo represents resource usage trending data
type TrendingInfo struct {
	DailyCPUGrowthPercent    float64 `json:"daily_cpu_growth_percent"`
	DailyMemoryGrowthPercent float64 `json:"daily_memory_growth_percent"`
	DaysUntil85Percent       int     `json:"days_until_85_percent"`
	ProjectedDate            string  `json:"projected_date,omitempty"`
}

// CapacityResult represents the complete capacity calculation result
type CapacityResult struct {
	Namespace          string                     `json:"namespace"`
	NamespaceQuota     *NamespaceQuotaOutput      `json:"namespace_quota"`
	CurrentUsage       *CurrentUsageOutput        `json:"current_usage"`
	AvailableCapacity  *AvailableCapacityOutput   `json:"available_capacity"`
	PodEstimates       map[string]*PodEstimate    `json:"pod_estimates"`
	RecommendedLimit   *RecommendedLimit          `json:"recommended_limit"`
	Trending           *TrendingInfo              `json:"trending,omitempty"`
	Recommendation     string                     `json:"recommendation"`
}

// NamespaceQuotaOutput represents the quota output format
type NamespaceQuotaOutput struct {
	CPULimit       string `json:"cpu_limit"`
	MemoryLimit    string `json:"memory_limit"`
	PodCountLimit  int    `json:"pod_count_limit"`
}

// CurrentUsageOutput represents the current usage output format
type CurrentUsageOutput struct {
	CPU           string  `json:"cpu"`
	Memory        string  `json:"memory"`
	CPUPercent    float64 `json:"cpu_percent"`
	MemoryPercent float64 `json:"memory_percent"`
	PodCount      int     `json:"pod_count"`
}

// AvailableCapacityOutput represents available capacity output format
type AvailableCapacityOutput struct {
	CPU      string `json:"cpu"`
	Memory   string `json:"memory"`
	PodSlots int    `json:"pod_slots"`
}

// RecommendedLimit represents the recommended pod deployment limit
type RecommendedLimit struct {
	PodProfile     string `json:"pod_profile"`
	SafePodCount   int    `json:"safe_pod_count"`
	MaxPodCount    int    `json:"max_pod_count"`
	LimitingFactor string `json:"limiting_factor"`
	Explanation    string `json:"explanation"`
}

// Calculator provides capacity calculation functionality
type Calculator struct {
	safetyMargin float64 // Default safety margin (e.g., 0.15 for 15%)
}

// NewCalculator creates a new capacity calculator
func NewCalculator(safetyMargin float64) *Calculator {
	if safetyMargin < 0 || safetyMargin > 1 {
		safetyMargin = 0.15 // Default to 15%
	}
	return &Calculator{
		safetyMargin: safetyMargin,
	}
}

// CalculatePodCapacity calculates how many pods can be deployed
func (c *Calculator) CalculatePodCapacity(
	quota *NamespaceQuota,
	podProfile PodProfile,
	customResources *PodResources,
	safetyMarginOverride *float64,
) (*CapacityResult, error) {
	// Validate inputs
	if quota == nil {
		return nil, fmt.Errorf("namespace quota is required")
	}

	// Use override safety margin if provided
	safetyMargin := c.safetyMargin
	if safetyMarginOverride != nil {
		safetyMargin = *safetyMarginOverride / 100.0 // Convert from percentage
	}

	// Calculate available capacity
	availableCPU := quota.CPULimitMillicores - quota.CPUUsedMillicores
	availableMemory := quota.MemoryLimitBytes - quota.MemoryUsedBytes
	availablePodSlots := quota.PodCountLimit - quota.CurrentPodCount

	// Ensure non-negative
	if availableCPU < 0 {
		availableCPU = 0
	}
	if availableMemory < 0 {
		availableMemory = 0
	}
	if availablePodSlots < 0 {
		availablePodSlots = 0
	}

	// Calculate estimates for all profiles
	podEstimates := make(map[string]*PodEstimate)
	for profile, resources := range DefaultPodProfiles {
		estimate := c.calculateEstimate(resources, availableCPU, availableMemory, availablePodSlots, safetyMargin)
		podEstimates[string(profile)] = estimate
	}

	// Calculate custom profile if provided
	if customResources != nil {
		estimate := c.calculateEstimate(*customResources, availableCPU, availableMemory, availablePodSlots, safetyMargin)
		podEstimates["custom"] = estimate
	}

	// Determine recommended limit based on requested profile
	var recommendedResources PodResources
	if customResources != nil && podProfile == PodProfileCustom {
		recommendedResources = *customResources
	} else if resources, ok := DefaultPodProfiles[podProfile]; ok {
		recommendedResources = resources
	} else {
		recommendedResources = DefaultPodProfiles[PodProfileMedium]
	}

	recommendedEstimate := c.calculateEstimate(recommendedResources, availableCPU, availableMemory, availablePodSlots, safetyMargin)

	// Build recommended limit
	recommendedLimit := &RecommendedLimit{
		PodProfile:     string(podProfile),
		SafePodCount:   recommendedEstimate.SafePods,
		MaxPodCount:    recommendedEstimate.MaxPods,
		LimitingFactor: recommendedEstimate.LimitingFactor,
		Explanation:    c.generateExplanation(recommendedEstimate, recommendedResources, availableCPU, availableMemory),
	}

	// Build result
	result := &CapacityResult{
		NamespaceQuota: &NamespaceQuotaOutput{
			CPULimit:      formatCPU(quota.CPULimitMillicores),
			MemoryLimit:   formatMemory(quota.MemoryLimitBytes),
			PodCountLimit: quota.PodCountLimit,
		},
		CurrentUsage: &CurrentUsageOutput{
			CPU:           formatCPU(quota.CPUUsedMillicores),
			Memory:        formatMemory(quota.MemoryUsedBytes),
			CPUPercent:    calculatePercent(quota.CPUUsedMillicores, quota.CPULimitMillicores),
			MemoryPercent: calculatePercent(quota.MemoryUsedBytes, quota.MemoryLimitBytes),
			PodCount:      quota.CurrentPodCount,
		},
		AvailableCapacity: &AvailableCapacityOutput{
			CPU:      formatCPU(availableCPU),
			Memory:   formatMemory(availableMemory),
			PodSlots: availablePodSlots,
		},
		PodEstimates:     podEstimates,
		RecommendedLimit: recommendedLimit,
		Recommendation:   c.generateRecommendation(recommendedEstimate, quota, safetyMargin),
	}

	return result, nil
}

// calculateEstimate calculates pod estimates for given resources
func (c *Calculator) calculateEstimate(
	resources PodResources,
	availableCPU, availableMemory int64,
	availablePodSlots int,
	safetyMargin float64,
) *PodEstimate {
	// Calculate max pods based on CPU
	var maxPodsByCPU int
	if resources.CPUMillicores > 0 {
		maxPodsByCPU = int(availableCPU / resources.CPUMillicores)
	} else {
		maxPodsByCPU = availablePodSlots
	}

	// Calculate max pods based on memory (convert MB to bytes)
	var maxPodsByMemory int
	memoryBytes := resources.MemoryMB * 1024 * 1024
	if memoryBytes > 0 {
		maxPodsByMemory = int(availableMemory / memoryBytes)
	} else {
		maxPodsByMemory = availablePodSlots
	}

	// Calculate max pods based on pod count limit
	maxPodsBySlots := availablePodSlots

	// The limiting factor is the minimum
	maxPods := minInt(maxPodsByCPU, maxPodsByMemory, maxPodsBySlots)
	if maxPods < 0 {
		maxPods = 0
	}

	// Calculate safe pods with safety margin
	safePods := int(float64(maxPods) * (1 - safetyMargin))
	if safePods < 0 {
		safePods = 0
	}

	// Determine limiting factor
	var limitingFactor string
	switch {
	case maxPodsBySlots <= maxPodsByCPU && maxPodsBySlots <= maxPodsByMemory:
		limitingFactor = "pod_count"
	case maxPodsByMemory <= maxPodsByCPU:
		limitingFactor = "memory"
	default:
		limitingFactor = "cpu"
	}

	return &PodEstimate{
		CPUMillicores:  resources.CPUMillicores,
		MemoryMB:       resources.MemoryMB,
		MaxPods:        maxPods,
		SafePods:       safePods,
		LimitingFactor: limitingFactor,
	}
}

// generateExplanation generates an explanation for the capacity limit
func (c *Calculator) generateExplanation(
	estimate *PodEstimate,
	resources PodResources,
	availableCPU, availableMemory int64,
) string {
	switch estimate.LimitingFactor {
	case "memory":
		cpuPods := 0
		if resources.CPUMillicores > 0 {
			cpuPods = int(availableCPU / resources.CPUMillicores)
		}
		return fmt.Sprintf("Memory constrains capacity. CPU could support %d more pods.", cpuPods)
	case "cpu":
		memoryBytes := resources.MemoryMB * 1024 * 1024
		memPods := 0
		if memoryBytes > 0 {
			memPods = int(availableMemory / memoryBytes)
		}
		return fmt.Sprintf("CPU constrains capacity. Memory could support %d more pods.", memPods)
	case "pod_count":
		return "Pod count limit constrains capacity. Consider increasing ResourceQuota pod limit."
	default:
		return "Multiple factors constrain capacity."
	}
}

// generateRecommendation generates a recommendation message
func (c *Calculator) generateRecommendation(
	estimate *PodEstimate,
	quota *NamespaceQuota,
	safetyMargin float64,
) string {
	targetPercent := int((1 - safetyMargin) * 100)
	
	if estimate.MaxPods == 0 {
		return "No capacity available for additional pods. Consider increasing namespace quota or removing unused pods."
	}

	if estimate.SafePods == 0 {
		return fmt.Sprintf("Very limited capacity. Only %d pods can be added, but this would exceed %d%% target utilization.",
			estimate.MaxPods, targetPercent)
	}

	memoryPercent := calculatePercent(quota.MemoryUsedBytes, quota.MemoryLimitBytes)
	
	recommendation := fmt.Sprintf("Can safely run %d more %s-profile pods. Keep <%d%% %s for stability.",
		estimate.SafePods,
		estimate.LimitingFactor,
		targetPercent+15, // Add buffer for visibility
		estimate.LimitingFactor,
	)

	if memoryPercent > 70 {
		recommendation += fmt.Sprintf(" Current memory usage is %.1f%%, monitor closely.", memoryPercent)
	}

	return recommendation
}

// CalculateTrending calculates usage trending based on historical data
func (c *Calculator) CalculateTrending(
	historicalCPU []float64, // Daily CPU percentages for past 7 days
	historicalMemory []float64, // Daily memory percentages for past 7 days
	currentCPUPercent float64,
	currentMemoryPercent float64,
) *TrendingInfo {
	if len(historicalCPU) < 2 || len(historicalMemory) < 2 {
		// Not enough data for trending, use estimates
		return &TrendingInfo{
			DailyCPUGrowthPercent:    1.0, // Default 1% daily growth
			DailyMemoryGrowthPercent: 1.5, // Default 1.5% daily growth
			DaysUntil85Percent:       c.estimateDaysUntilThreshold(currentCPUPercent, currentMemoryPercent, 1.0, 1.5, 85),
			ProjectedDate:            c.projectDate(c.estimateDaysUntilThreshold(currentCPUPercent, currentMemoryPercent, 1.0, 1.5, 85)),
		}
	}

	// Calculate daily growth rates using linear regression
	cpuGrowth := c.calculateDailyGrowth(historicalCPU)
	memoryGrowth := c.calculateDailyGrowth(historicalMemory)

	// Days until 85% threshold
	daysUntil85 := c.estimateDaysUntilThreshold(currentCPUPercent, currentMemoryPercent, cpuGrowth, memoryGrowth, 85)

	return &TrendingInfo{
		DailyCPUGrowthPercent:    cpuGrowth,
		DailyMemoryGrowthPercent: memoryGrowth,
		DaysUntil85Percent:       daysUntil85,
		ProjectedDate:            c.projectDate(daysUntil85),
	}
}

// calculateDailyGrowth calculates the average daily growth rate
func (c *Calculator) calculateDailyGrowth(values []float64) float64 {
	if len(values) < 2 {
		return 0
	}

	// Simple linear regression to find slope
	n := float64(len(values))
	var sumX, sumY, sumXY, sumX2 float64

	for i, v := range values {
		x := float64(i)
		sumX += x
		sumY += v
		sumXY += x * v
		sumX2 += x * x
	}

	// Slope = (n*sumXY - sumX*sumY) / (n*sumX2 - sumX*sumX)
	denominator := n*sumX2 - sumX*sumX
	if denominator == 0 {
		return 0
	}

	slope := (n*sumXY - sumX*sumY) / denominator
	return math.Round(slope*100) / 100 // Round to 2 decimal places
}

// estimateDaysUntilThreshold estimates days until reaching a threshold
func (c *Calculator) estimateDaysUntilThreshold(
	currentCPU, currentMemory float64,
	cpuGrowth, memoryGrowth float64,
	threshold float64,
) int {
	// Calculate days for each resource
	daysCPU, daysMemory := 999, 999

	if cpuGrowth > 0 && currentCPU < threshold {
		daysCPU = int((threshold - currentCPU) / cpuGrowth)
	}

	if memoryGrowth > 0 && currentMemory < threshold {
		daysMemory = int((threshold - currentMemory) / memoryGrowth)
	}

	// Return the minimum (whichever reaches threshold first)
	result := minInt(daysCPU, daysMemory)
	if result > 365 {
		result = 365 // Cap at 1 year
	}
	if result < 0 {
		result = 0
	}
	return result
}

// projectDate calculates the projected date given days from now
func (c *Calculator) projectDate(days int) string {
	if days <= 0 || days > 365 {
		return ""
	}
	projected := time.Now().AddDate(0, 0, days)
	return projected.Format("2006-01-02")
}

// Helper functions

func formatCPU(millicores int64) string {
	if millicores >= 1000 {
		return fmt.Sprintf("%d", millicores/1000) + " cores"
	}
	return fmt.Sprintf("%dm", millicores)
}

func formatMemory(bytes int64) string {
	const (
		KB = 1024
		MB = 1024 * KB
		GB = 1024 * MB
	)

	switch {
	case bytes >= GB:
		return fmt.Sprintf("%.1fGi", float64(bytes)/float64(GB))
	case bytes >= MB:
		return fmt.Sprintf("%dMi", bytes/MB)
	case bytes >= KB:
		return fmt.Sprintf("%dKi", bytes/KB)
	default:
		return fmt.Sprintf("%d bytes", bytes)
	}
}

func calculatePercent(used, total int64) float64 {
	if total == 0 {
		return 0
	}
	return math.Round(float64(used)/float64(total)*1000) / 10 // Round to 1 decimal
}

func minInt(values ...int) int {
	if len(values) == 0 {
		return 0
	}
	min := values[0]
	for _, v := range values[1:] {
		if v < min {
			min = v
		}
	}
	return min
}
