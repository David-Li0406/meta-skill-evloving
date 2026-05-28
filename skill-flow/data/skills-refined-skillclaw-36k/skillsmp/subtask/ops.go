package install

import "errors"

type InstallRequest struct {
	Scope   Scope
	BaseDir string
	Skill   bool
	Plugin  bool
}

type InstallResult struct {
	SkillPath string
	PluginDir string

	UpdatedSkill  bool
	UpdatedPlugin bool

	Settings SettingsChange
}

func InstallAll(req InstallRequest) (InstallResult, error) {
	if req.BaseDir == "" {
		return InstallResult{}, errors.New("invalid base directory")
	}

	res := InstallResult{}
	if req.Skill {
		path, updated, err := syncSkillTo(req.Scope, req.BaseDir)
		if err != nil {
			return InstallResult{}, err
		}
		res.SkillPath = path
		res.UpdatedSkill = updated
	}

	if req.Plugin {
		dir, updated, err := InstallPluginTo(req.Scope, req.BaseDir)
		if err != nil {
			return InstallResult{}, err
		}
		res.PluginDir = dir
		res.UpdatedPlugin = updated

		ch, err := EnsurePluginEnabled(req.Scope, req.BaseDir)
		if err != nil {
			return InstallResult{}, err
		}
		res.Settings = ch
	}

	return res, nil
}

type UninstallRequest struct {
	Scope   Scope
	BaseDir string
	Skill   bool
	Plugin  bool
}

type UninstallResult struct {
	SkillPath string
	PluginDir string

	Settings SettingsChange
}

func UninstallAll(req UninstallRequest) (UninstallResult, error) {
	if req.BaseDir == "" {
		return UninstallResult{}, errors.New("invalid base directory")
	}

	res := UninstallResult{}
	if req.Skill {
		path, err := UninstallFrom(req.Scope, req.BaseDir)
		if err != nil {
			return UninstallResult{}, err
		}
		res.SkillPath = path
	}

	if req.Plugin {
		dir, err := UninstallPluginFrom(req.Scope, req.BaseDir)
		if err != nil {
			return UninstallResult{}, err
		}
		res.PluginDir = dir

		ch, err := RemovePluginEnabled(req.Scope, req.BaseDir)
		if err != nil {
			return UninstallResult{}, err
		}
		res.Settings = ch
	}

	return res, nil
}
