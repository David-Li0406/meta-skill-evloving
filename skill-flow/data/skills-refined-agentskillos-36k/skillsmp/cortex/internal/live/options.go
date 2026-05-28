package live

func mergeOptions(primary map[string]any, fallback map[string]any) map[string]any {
	if len(primary) == 0 && len(fallback) == 0 {
		return nil
	}
	out := map[string]any{}
	for k, v := range fallback {
		out[k] = v
	}
	for k, v := range primary {
		out[k] = v
	}
	return out
}

func getStringOption(opts map[string]any, key string, def string) string {
	if opts == nil {
		return def
	}
	if v, ok := opts[key]; ok {
		if s, ok := v.(string); ok && s != "" {
			return s
		}
	}
	return def
}

func getBoolOption(opts map[string]any, key string, def bool) bool {
	if opts == nil {
		return def
	}
	if v, ok := opts[key]; ok {
		if b, ok := v.(bool); ok {
			return b
		}
	}
	return def
}

func getIntOption(opts map[string]any, key string, def int) int {
	if opts == nil {
		return def
	}
	if v, ok := opts[key]; ok {
		switch t := v.(type) {
		case int:
			return t
		case int64:
			return int(t)
		case float64:
			return int(t)
		}
	}
	return def
}
