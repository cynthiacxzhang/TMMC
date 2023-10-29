# TMMC Circle Detection Program --> C1T1


# Imports 
import cv2
import numpy as np
import time

# Initialize the video capture
cap = cv2.VideoCapture(1)

# Duration and interval settings
total_duration = 15  # seconds
capture_interval = 3  # seconds
end_time = time.time() + total_duration
last_capture_time = 0  # the time of the last frame capture

#loop that reads the video capture

while time.time() < end_time:
    # Capture the frame from the video feed
    max_tested = 10
    for i in range(max_tested):
      cap = cv2.VideoCapture(i)
      if cap.read()[0]:          
        print(f"Camera index found: {i}")
        break
      cap.release()

    ret, frame = cap.read()

    # Check if frame read was successful --> give console output if not
    if not ret:
        print("Failed to grab frame")
        continue

    # If it's time for the next capture
    if time.time() - last_capture_time >= capture_interval:
        # Update the last capture time
        last_capture_time = time.time()

        # Convert the image to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Apply Canny edge detection
        edges = cv2.Canny(gray, 100, 150)

        # Detect circles as before
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1.2, minDist=250, param1=50, param2=70, minRadius=5, maxRadius=150)

        # If circles are detected, draw them -- this function does not change)
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            for (x, y, r) in circles:
                cv2.circle(frame, (x, y), r, (0, 255, 0), 4)

        # Save or display the frame
        cv2.imshow("Edges", edges)
        cv2.imshow("Output", frame)
        cv2.imwrite(f"capture_{int(last_capture_time)}.jpg", frame)  # saving the frame
        print(f"Captured at: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_capture_time))}")

    # Exit loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
