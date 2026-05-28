package install

import "errors"

// ScopeStatus describes installation state for a specific scope.
type ScopeStatus struct {
	Scope    Scope
	BaseDir  string
	Skill    SkillStatus
	Plugin   PluginStatus
	Settings SettingsStatus
}

func GetScopeStatus(scope Scope, baseDir string) (ScopeStatus, error) {
	if baseDir == "" {
		return ScopeStatus{}, errors.New("invalid base directory")
	}

	skill, err := GetSkillStatusFor(scope, baseDir)
	if err != nil {
		return ScopeStatus{}, err
	}
	plugin, err := GetPluginStatusFor(scope, baseDir)
	if err != nil {
		return ScopeStatus{}, err
	}

	return ScopeStatus{
		Scope:    scope,
		BaseDir:  baseDir,
		Skill:    skill,
		Plugin:   plugin,
		Settings: GetSettingsStatusFor(scope, baseDir),
	}, nil
}
