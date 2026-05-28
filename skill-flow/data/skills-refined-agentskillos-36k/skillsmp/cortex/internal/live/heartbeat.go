package live

import "time"

func startHeartbeat(interval time.Duration, beat func()) func() {
	if interval <= 0 || beat == nil {
		return func() {}
	}
	stop := make(chan struct{})
	go func() {
		beat()
		ticker := time.NewTicker(interval)
		defer ticker.Stop()
		for {
			select {
			case <-ticker.C:
				beat()
			case <-stop:
				return
			}
		}
	}()
	return func() { close(stop) }
}
