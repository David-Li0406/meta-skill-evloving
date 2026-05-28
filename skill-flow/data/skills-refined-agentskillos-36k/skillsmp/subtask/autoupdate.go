package install

// AutoUpdateResult captures which installed components were updated to match embedded assets.
type AutoUpdateResult struct {
	UpdatedSkill  bool
	UpdatedPlugin bool
}

func AutoUpdateIfInstalled(scope Scope, baseDir string) (AutoUpdateResult, error) {
	var res AutoUpdateResult

	if isSkillInstalled(scope, baseDir) {
		_, updated, err := syncSkillTo(scope, baseDir)
		if err != nil {
			return AutoUpdateResult{}, err
		}
		res.UpdatedSkill = updated
	}

	if isPluginInstalled(scope, baseDir) {
		_, updated, err := InstallPluginTo(scope, baseDir)
		if err != nil {
			return AutoUpdateResult{}, err
		}
		res.UpdatedPlugin = updated
	}

	return res, nil
}
