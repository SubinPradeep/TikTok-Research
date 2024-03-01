import streamlit as st
from moviepy.video.io.VideoFileClip import VideoFileClip
import os

def split_video(input_file, output_prefix, num_parts):
    video_clip = VideoFileClip(input_file)
    total_duration = video_clip.duration
    part_duration = total_duration / num_parts

    output_files = []

    for part_number in range(num_parts):
        start_time = part_number * part_duration
        end_time = min((part_number + 1) * part_duration, total_duration)

        subclip = video_clip.subclip(start_time, end_time)

        output_file = f"{output_prefix}_part{part_number + 1}.mp4"
        output_files.append(output_file)
        subclip.write_videofile(output_file, codec="libx264", audio_codec="aac")

    video_clip.close()

    return output_files

def display_split_files(split_files):
    st.write("### Split Files:")
    for file_path in split_files:
        st.markdown(f"**{file_path}**")
        st.video(file_path)

def main():
    st.title("MP4 Splitter")

    uploaded_file = st.file_uploader("Upload an MP4 file", type=["mp4"])
    if uploaded_file is not None:
        num_parts = st.number_input("Enter the number of equal parts:", min_value=1, step=1, value=2)

        if st.button("Split"):
            st.info("Splitting... This may take a moment.")
            input_path = f"uploaded_video.mp4"
            with open(input_path, 'wb') as f:
                f.write(uploaded_file.read())
            split_files = split_video(input_path, "output_part", num_parts)
            st.success("Splitting complete. Check the generated files.")

            # Store split file paths in a variable for later use
            st.session_state.split_files = split_files

    # Display the split files
    if hasattr(st.session_state, "split_files"):
        display_split_files(st.session_state.split_files)

if __name__ == "__main__":
    main()
