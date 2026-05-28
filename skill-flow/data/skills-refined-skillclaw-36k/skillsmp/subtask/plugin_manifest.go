package install

import (
	"crypto/sha256"
	"encoding/hex"
	"io/fs"
	"os"
	"sort"
	"strings"
	"sync"

	"github.com/zippoxer/subtask/plugin"
)

type embeddedPluginFile struct {
	RelPath string
	Data    []byte
	Perm    os.FileMode
}

var (
	pluginManifestOnce sync.Once
	pluginManifest     []embeddedPluginFile
	pluginManifestSHA  string
	pluginManifestErr  error
)

func embeddedPluginManifest() ([]embeddedPluginFile, string, error) {
	pluginManifestOnce.Do(func() {
		var files []embeddedPluginFile
		err := fs.WalkDir(plugin.FS, ".", func(p string, d fs.DirEntry, err error) error {
			if err != nil {
				return err
			}
			if d.IsDir() {
				return nil
			}

			data, err := plugin.FS.ReadFile(p)
			if err != nil {
				return err
			}

			rel := p
			perm := os.FileMode(0o644)
			if strings.HasPrefix(rel, "scripts/") {
				perm = 0o755
			}

			files = append(files, embeddedPluginFile{
				RelPath: rel,
				Data:    data,
				Perm:    perm,
			})
			return nil
		})
		if err != nil {
			pluginManifestErr = err
			return
		}

		sort.Slice(files, func(i, j int) bool {
			return files[i].RelPath < files[j].RelPath
		})

		h := sha256.New()
		for _, f := range files {
			_, _ = h.Write([]byte(f.RelPath))
			_, _ = h.Write([]byte{0})
			_, _ = h.Write(f.Data)
			_, _ = h.Write([]byte{0})
		}

		pluginManifest = files
		pluginManifestSHA = hex.EncodeToString(h.Sum(nil))
	})

	return pluginManifest, pluginManifestSHA, pluginManifestErr
}
