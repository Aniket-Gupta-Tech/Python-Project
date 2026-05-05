import streamlit as st
import yt_dlp
import os

st.title("YouTube to MP3 Converter")

url = st.text_input("Enter YouTube Video URL")

if st.button("Download MP3"):
    if url:
        with st.spinner("Downloading and converting..."):

            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': '%(title)s.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)
                    mp3_file = os.path.splitext(filename)[0] + ".mp3"

                st.success("Download Completed!")
                
                with open(mp3_file, "rb") as f:
                    st.download_button(
                        label="Download MP3 File",
                        data=f,
                        file_name=os.path.basename(mp3_file),
                        mime="audio/mp3"
                    )

            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter a valid URL")