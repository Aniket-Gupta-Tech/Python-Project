import cv2
import os
import time

ASCII_CHARS = "@%#*+=-:. "

def clear_terminal():
    # Faster & stable for Windows
    print("\033[H\033[J", end="")

def resize_frame(frame, width=100):
    h, w = frame.shape
    aspect_ratio = h / w
    height = int(aspect_ratio * width * 0.55)
    return cv2.resize(frame, (width, height))

def frame_to_ascii(frame):
    ascii_img = ""
    scale = len(ASCII_CHARS) - 1

    for row in frame:
        for pixel in row:
            index = int(pixel / 255 * scale)
            ascii_img += ASCII_CHARS[index]
        ascii_img += "\n"

    return ascii_img

def video_to_ascii(video_path, fps=20):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("❌ Video open nahi ho rahi")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        resized = resize_frame(gray)
        ascii_frame = frame_to_ascii(resized)

        clear_terminal()
        print(ascii_frame)
        time.sleep(1 / fps)

    cap.release()
    print("✅ Video finished")

video_to_ascii("sample.mp4", fps=10)
