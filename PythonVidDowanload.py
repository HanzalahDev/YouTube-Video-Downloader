from pytube import YouTube

# Prompt the user for the video URL
video_url = input("Enter the YouTube video URL: ")

# Prompt the user for the download path
download_path = input("Enter the download path (leave blank for current directory): ")

# Prompt the user for download type: audio or video
download_type = input("Do you want to download audio only or video? (Enter 'audio' or 'video'): ").strip().lower()

try:
    # Create a YouTube object
    yt = YouTube(video_url)

    # Print the title of the video
    print(f'Video Title: {yt.title}')

    if download_type == "video":
        # List available video resolutions
        print("Available resolutions:")
        video_streams = yt.streams.filter(progressive=True)  # Get progressive streams (video + audio)
        for stream in video_streams:
            print(stream)

        # Prompt user to select a resolution
        resolution = input("Enter the resolution you want (e.g., '720p', '1080p'): ")
        video_stream = video_streams.filter(res=resolution).first()

        if video_stream:
            video_stream.download(output_path=download_path)  # Download the video
            print(f'Video "{yt.title}" has been downloaded successfully at {resolution}!')
        else:
            print("Selected resolution is not available.")
    
    elif download_type == "audio":
        # Download audio stream
        audio_stream = yt.streams.filter(only_audio=True).first()
        audio_stream.download(output_path=download_path)  # Download the audio
        print(f'Audio from "{yt.title}" has been downloaded successfully!')
    
    else:
        print("Invalid option. Please enter 'audio' or 'video'.")

except Exception as e:
    # Handle any exceptions that occur during the process
    print(f"An error occurred: {e}")
