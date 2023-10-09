import cv2
import numpy as np
import os
import tkinter as tk
from tkinter import filedialog


fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
max_detect = 0


def detect_motion(frame, detected_fish, fish_count):

    frame = cv2.resize(frame, (360, 240))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.rectangle(frame, (0, 0), (frame.shape[1], 40), (0, 0, 0), -1)
    color = (0, 255, 0)
    texto_estado = "Estado: No se ha detectado movimiento"

    area_pts = np.array([[0, 40], [720, 40], [720, 450], [0, 450]])

    imAux = np.zeros(shape=(frame.shape[:2]), dtype=np.uint8)
    imAux = cv2.drawContours(imAux, [area_pts], -1, (255), -1)
    image_area = cv2.bitwise_and(gray, gray, mask=imAux)

    fgmask = fgbg.apply(image_area)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    fgmask = cv2.dilate(fgmask, None, iterations=2)

    cnts = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    for cnt in cnts:
        if cv2.contourArea(cnt) > 200:
            x, y, w, h = cv2.boundingRect(cnt)
            if (x, y, w, h) not in detected_fish:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                texto_estado = "Estado: ALERTA Movimiento Detectado!"
                color = (0, 0, 255)
                fish_count += 1
                detected_fish.append((x, y, w, h))
                print(f"Peces detectados {fish_count}")

    cv2.drawContours(frame, [area_pts], -1, color, 2)
    cv2.putText(frame, texto_estado , (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, color,2)
    cv2.putText(frame, "Peces detectados: " + str(fish_count), (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255),1)
    cv2.imshow('fgmask', fgmask)
    cv2.imshow("frame", frame)

    # Resto del código de procesamiento (sin el bucle while)

    return fish_count

# def write_file_txt(start_times,end_times):
#     # Guarda los momentos en un archivo de texto
#     with open("momentos_pesca.txt", "w") as file:
#         for i in range(len(start_times)):
#             file.write(f"Pez {i + 1}: {start_times[i]}s - {end_times[i]}s\n")

#     # Si quedó un pez sin finalizar, regístralo
#     if len(start_times) > len(end_times):
#         file.write(f"Pez {len(start_times) + 1}: {start_times[-1]}s - {cap.get(cv2.CAP_PROP_POS_MSEC) / 1000}s\n")

def write_file_txt(video_file_name, start_times, end_times):
    file_name = f"{video_file_name}_momentos_pesca.txt"

    with open(file_name, "w") as file:
        for i in range(len(start_times)):
            file.write(f"Pez {i + 1}: {start_times[i]}s - {end_times[i]}s\n")

    # If there's a fish detected but not finished, record it
    if len(start_times) > len(end_times):
        file.write(f"Pez {len(start_times) + 1}: {start_times[-1]}s - {end_times[-1]}s\n")

# Function to process a single video
def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
 
    # Get the video file name without the extension
    video_file_name = os.path.splitext(os.path.basename(video_path))[0]

    # Initialize variables for this video
    fish_count = 0
    start_time = None
    detected_fish = []
    start_times = []
    end_times = []

    while True:
        ret, frame = cap.read()
        if ret == False:
            break

        fish_counter = detect_motion(frame, detected_fish, fish_count)

        if fish_counter > 0 and start_time is None:
            # Fish detected, but no start time recorded yet
            start_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
        elif fish_counter == 0 and start_time is not None:
            # Fish is no longer detected, record end time
            end_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
            start_times.append(start_time)
            end_times.append(end_time)
            start_time = None  # Reset start time

        k = cv2.waitKey(70) & 0xFF
        if k == 27:
            break

    # Close the text file

    write_file_txt(video_file_name, start_times, end_times)
    cap.release()

# Function to process all videos in a folder
def process_videos_in_folder(folder_path):
    video_files = [f for f in os.listdir(folder_path) if f.endswith('.mp4') or f.endswith('.avi')]

    for video_file in video_files:
        video_path = os.path.join(folder_path, video_file)
        print(f"Processing video: {video_path}")
        process_video(video_path)

def select_folder():
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal de Tkinter

    folder_path = filedialog.askdirectory()
    return folder_path

if __name__ == "__main__":
    
    folder_path = select_folder()

    if not os.path.exists(folder_path):
        print("Folder does not exist.")
    else:
        process_videos_in_folder(folder_path)


# filePath = r"video_files\test5.mp4"
# print("Versión de OpenCV instalada:", cv2.__version__)
# cap = cv2.VideoCapture(filePath)
# # Extract the video file name without the extension
# # video_file_name = "pez1.mp4"  # Replace with the actual video file name
# # video_file_name_without_extension = video_file_name.split('.')[0]

# fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
# kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
# max_detect = 0

# fish_count = 0
# start_time = None

# detected_fish = []  # Lista para realizar un seguimiento de los peces detectados

# start_times = []  # Lista para almacenar los tiempos de inicio
# end_times = []    # Lista para almacenar los tiempos de finalización

# # Flag to indicate whether a fish has been detected
# fish_detected = False

# while True:
#     ret, frame = cap.read()
#     if ret == False:
#         break

#     fish_counter = detect_motion(frame, detected_fish, fish_count)

#     # Check if a fish is currently detected
#     if fish_counter > 0 and start_time is None:
#         # Fish detected, but no start time recorded yet
#         start_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
#         print(start_time)
#     elif fish_counter == 0 and start_time is not None:
#         # Fish is no longer detected, record end time
#         end_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
#         start_times.append(start_time)
#         end_times.append(end_time)
#         start_time = None  # Reset start time


#     k = cv2.waitKey(70) & 0xFF
#     if k == 27:
#         write_file_txt(start_times,end_times)
#         break


# write_file_txt(start_times,end_times)
# cap.release()
# cv2.destroyAllWindows()
