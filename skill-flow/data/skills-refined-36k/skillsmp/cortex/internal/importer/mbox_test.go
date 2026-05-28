package importer

import (
	"context"
	"os"
	"path/filepath"
	"testing"

	"github.com/Napageneral/cortex/internal/db"
)

func TestImportMBox_Basic(t *testing.T) {
	tmpDir := t.TempDir()
	t.Setenv("COMMS_DATA_DIR", tmpDir)

	if err := db.Init(); err != nil {
		t.Fatalf("db.Init: %v", err)
	}
	d, err := db.Open()
	if err != nil {
		t.Fatalf("db.Open: %v", err)
	}
	defer d.Close()

	mbox := "From someone@example.com Sat Jan 01 00:00:00 2022\n" +
		"Date: Sat, 01 Jan 2022 00:00:00 +0000\n" +
		"From: Someone <someone@example.com>\n" +
		"To: Tyler <tyler@intent-systems.com>\n" +
		"Subject: =?UTF-8?Q?Hello?=\n" +
		"Message-ID: <msg-1@example.com>\n" +
		"X-GM-MSGID: 111\n" +
		"X-GM-THRID: 222\n" +
		"X-GM-LABELS: (\\Inbox IMPORTANT UNREAD)\n" +
		"\n" +
		"Body 1\n" +
		"\n" +
		"From tyler@intent-systems.com Sat Jan 02 00:00:00 2022\n" +
		"Date: Sun, 02 Jan 2022 00:00:00 +0000\n" +
		"From: Tyler <tyler@intent-systems.com>\n" +
		"To: Someone <someone@example.com>\n" +
		"Subject: Re: Hello\n" +
		"Message-ID: <msg-2@example.com>\n" +
		"X-GM-MSGID: 112\n" +
		"X-GM-THRID: 222\n" +
		"X-GM-LABELS: (SENT)\n" +
		"\n" +
		"Body 2\n"

	mboxPath := filepath.Join(tmpDir, "test.mbox")
	if err := os.WriteFile(mboxPath, []byte(mbox), 0644); err != nil {
		t.Fatalf("write mbox: %v", err)
	}

	res, err := ImportMBox(context.Background(), d, MBoxImportOptions{
		AdapterName:     "gmail-tyler@intent-systems.com",
		AccountEmail:    "tyler@intent-systems.com",
		Path:            mboxPath,
		CommitEvery:     1,
		MaxMessageBytes: 1024 * 1024,
	})
	if err != nil {
		t.Fatalf("ImportMBox: %v", err)
	}
	if res.MessagesSeen != 2 {
		t.Fatalf("expected 2 messages, got %d", res.MessagesSeen)
	}
	if res.EventsCreated == 0 {
		t.Fatalf("expected created events > 0")
	}

	var cnt int
	if err := d.QueryRow(`SELECT COUNT(*) FROM events WHERE channel = 'gmail'`).Scan(&cnt); err != nil {
		t.Fatalf("count events: %v", err)
	}
	if cnt != 2 {
		t.Fatalf("expected 2 gmail events, got %d", cnt)
	}

	var tags int
	if err := d.QueryRow(`SELECT COUNT(*) FROM event_tags`).Scan(&tags); err != nil {
		t.Fatalf("count event_tags: %v", err)
	}
	if tags == 0 {
		t.Fatalf("expected some event_tags")
	}
}
