from youtube_transcript_api import YouTubeTranscriptApi
import sys
import time

def get_video_id(url):
    """Extracts the video ID from a YouTube URL"""
    # Handle different types of YouTube URLs
    if "v=" in url:
        video_id = url.split("v=")[1]
        # Remove additional parameters like timestamps
        if "&" in video_id:
            video_id = video_id.split("&")[0]
    elif "youtu.be/" in url:
        video_id = url.split("youtu.be/")[1]
        # Remove additional parameters like timestamps
        if "?" in video_id:
            video_id = video_id.split("?")[0]
    else:
        raise ValueError("Could not extract video ID from URL")

    return video_id

def get_transcript(video_url):
    """Fetches the transcript for a YouTube video"""
    try:
        video_id = get_video_id(video_url)

        # Create API instance with retry mechanism
        ytt_api = YouTubeTranscriptApi()

        # Try to get the transcript list (up to 3 attempts)
        for attempt in range(3):
            try:
                transcript_list = ytt_api.list(video_id)
                break
            except Exception as e:
                if attempt == 2:  # Last attempt failed
                    raise e
                print(f"Attempt {attempt + 1} failed, retrying...")
                time.sleep(2)  # Wait 2 seconds before retrying

        # Attempt to get English or other language transcripts
        transcript = None
        languages_to_try = ['en', 'zh', 'ja', 'ko', 'es', 'fr', 'de', 'it', 'pt', 'ru', 'ar', 'hi']

        for lang in languages_to_try:
            try:
                transcript = transcript_list.find_transcript([lang])
                print(f"Using {lang} transcript...")
                break
            except:
                continue

        # If preferred language not found, try any available transcript
        if transcript is None:
            try:
                # Try to get manually created transcripts
                transcript = transcript_list.find_manually_created_transcript(languages_to_try)
                print(f"Using manually created transcript ({transcript.language_code})...")
            except:
                try:
                    # If no manual transcript, try generated one
                    transcript = transcript_list.find_generated_transcript(languages_to_try)
                    print(f"Using auto-generated transcript ({transcript.language_code})...")
                except:
                    try:
                        # Fallback to the first available transcript
                        transcript = list(transcript_list)[0]
                        print(f"Using default transcript ({transcript.language_code})...")
                    except:
                        print("No available transcripts found.")
                        return None

        # Try to fetch the actual transcript data (up to 3 attempts)
        for attempt in range(3):
            try:
                transcript_data = transcript.fetch()
                break
            except Exception as e:
                if attempt == 2:  # Last attempt failed
                    raise e
                print(f"Attempt {attempt + 1} to fetch transcript data failed, retrying...")
                time.sleep(2)  # Wait 2 seconds before retrying

        # Combine all parts into a full text
        full_text = " ".join([entry.text for entry in transcript_data])

        # Format output with timestamps
        formatted_text = ""
        for entry in transcript_data:
            start_time = entry.start
            text = entry.text

            # Convert start time to HH:MM:SS format
            hours = int(start_time // 3600)
            minutes = int((start_time % 3600) // 60)
            seconds = int(start_time % 60)

            time_str = f"[{hours:02d}:{minutes:02d}:{seconds:02d}]"
            formatted_text += f"{time_str} {text}\n"

        return formatted_text

    except Exception as e:
        print(f"Error fetching transcript: {str(e)}")
        return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python get_youtube_transcript.py <YouTube_URL>")
        sys.exit(1)
    
    video_url = sys.argv[1]
    print(f"Fetching transcript for '{video_url}'...")
    
    transcript = get_transcript(video_url)
    
    if transcript:
        print("\n" + "="*50)
        print("Transcript:")
        print("="*50)
        print(transcript)
        
        # Save to file
        try:
            video_id = get_video_id(video_url)
            filename = f"youtube_transcript_{video_id}.txt"
        except:
            filename = "youtube_transcript.txt"
            
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"YouTube URL: {video_url}\n\n")
            f.write("Transcript:\n")
            f.write("="*50 + "\n")
            f.write(transcript)
        
        print(f"\nTranscript saved to '{filename}'.")
    else:
        print("Failed to retrieve transcript.")
