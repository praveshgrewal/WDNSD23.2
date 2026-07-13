import cv2

# Open the default webcam (0 means first webcam)
camera = cv2.VideoCapture(0)

# Check if the webcam opened successfully
if not camera.isOpened():
    print("Error: Unable to access the camera.")
    exit()

while True:
    # Read one frame from the webcam
    success, frame = camera.read()

    if not success:
        print("Failed to capture image.")
        break

    # Convert the frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Show the original frame
    cv2.imshow("Original Camera", frame)

    # Show the grayscale frame
    cv2.imshow("Grayscale Camera", gray_frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera
camera.release()

# Close all OpenCV windows
cv2.destroyAllWindows()