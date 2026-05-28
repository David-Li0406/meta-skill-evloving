"""Simple player CLI"""
import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path.home() / ".deep-reading"))

from player.mpv_controller import MpvController, format_time
from db import get_connection

def get_source(source_id: str) -> dict:
    """Get source from database"""
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM sources WHERE id = ?",
        (source_id,)
    ).fetchone()
    conn.close()

    if not row:
        raise ValueError(f"Source not found: {source_id}")

    return dict(row)

def list_sources():
    """List all available sources"""
    conn = get_connection()
    rows = conn.execute(
        "SELECT id, title, author, duration, processing_state FROM sources ORDER BY created_at DESC"
    ).fetchall()
    conn.close()

    if not rows:
        print("No sources found. Use 'dr fetch <url>' to add content.")
        return

    print("Available sources:\n")
    for row in rows:
        duration = format_time(row["duration"]) if row["duration"] else "?"
        state = row["processing_state"]
        print(f"  [{row['id']}]")
        print(f"    {row['title']}")
        print(f"    by {row['author']} | {duration} | {state}")
        print()

def play(source_id: str):
    """Play a source"""
    source = get_source(source_id)
    cache_path = Path(source["cache_path"])
    audio_path = cache_path / "audio.mp3"

    if not audio_path.exists():
        print(f"Audio file not found: {audio_path}")
        sys.exit(1)

    print(f"Playing: {source['title']}")
    print(f"By: {source['author']}")
    print()
    print("Controls: [space] pause, [j/k] seek, [+/-] speed, [q] quit")
    print()

    mpv = MpvController()
    mpv.start(str(audio_path))

    import tty
    import termios
    import select

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        tty.setraw(fd)
        while True:
            pos = mpv.get_position()
            dur = mpv.get_duration()
            speed = mpv.get_speed()
            paused = "⏸" if mpv.get_paused() else "▶"

            # Progress bar
            progress = pos / dur if dur > 0 else 0
            bar_width = 30
            filled = int(bar_width * progress)
            bar = "━" * filled + "●" + "─" * (bar_width - filled - 1)

            status = f"\r  {paused} {bar} {format_time(pos)} / {format_time(dur)} [{speed:.1f}x]   "
            sys.stdout.write(status)
            sys.stdout.flush()

            # Check for input
            if select.select([sys.stdin], [], [], 0.1)[0]:
                ch = sys.stdin.read(1)
                if ch == 'q':
                    break
                elif ch == ' ':
                    mpv.toggle_pause()
                elif ch == '+' or ch == '=':
                    mpv.speed_up()
                elif ch == '-':
                    mpv.speed_down()
                elif ch == 'j':
                    mpv.seek(30)
                elif ch == 'k':
                    mpv.seek(-10)
                elif ch == 'J':
                    mpv.seek(60)
                elif ch == 'K':
                    mpv.seek(-30)

            # Check if playback ended
            if pos >= dur - 0.5 and dur > 0:
                break

    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        mpv.stop()
        print("\n\nPlayback ended.")

def main():
    parser = argparse.ArgumentParser(description="Play content")
    parser.add_argument("source_id", nargs="?", help="Source ID to play")
    parser.add_argument("-l", "--list", action="store_true", help="List sources")
    args = parser.parse_args()

    if args.list or not args.source_id:
        list_sources()
    else:
        play(args.source_id)

if __name__ == "__main__":
    main()
