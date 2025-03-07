# File to read the hand gestures
import cv2
import mediapipe
import numpy
import json

# Initialize the camera and MediaPipe Hands
camera = cv2.VideoCapture(0)
hand_model = mediapipe.solutions.hands
hand_tracker = hand_model.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)
draw_util = mediapipe.solutions.drawing_utils

def detect_hand_landmarks(frame):
    landmarks = []  # Default values if no landmarks are detected
    processed_frame = hand_tracker.process(frame)  # Process the input frame
    hand_landmarks = processed_frame.multi_hand_landmarks  # Stores the output of the hand tracking
    if hand_landmarks:  # Check if landmarks are found
        for hand in hand_landmarks:  # Process landmarks for each hand
            for idx, landmark in enumerate(hand.landmark):  # Loop through the 21 landmarks and retrieve their coordinates
                draw_util.draw_landmarks(frame, hand, hand_model.HAND_CONNECTIONS)  # Draw landmarks and connections
                height, width, _ = frame.shape  # Height, width, and channel for the frame
                x_pos, y_pos = int(landmark.x * width), int(landmark.y * height)  # Convert relative coordinates to pixel positions
                landmarks.append([idx, x_pos, y_pos])  # Append the index and coordinates to the list
    return landmarks

# Get the width and height of the camera feed
cam_width, cam_height = int(camera.get(3)), int(camera.get(4))

previous_position = None

delta_X = 0
delta_Y = 0

while True:
    ret, frame = camera.read()
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    hand_landmarks = detect_hand_landmarks(rgb_frame)
    
    # Calculate the mean position of all landmarks
    center_x = int(cam_width / 2)
    center_y = int(cam_height / 2)

    avg_x = center_x
    avg_y = center_y
    if len(hand_landmarks) != 0:
        avg_x = hand_landmarks[0][1]
        avg_y = hand_landmarks[0][2]

    # Calculate the deviation if previous position exists
    if previous_position is not None:
        delta_X = avg_x - previous_position[0]
        delta_Y = avg_y - previous_position[1]

    # Update previous position
    previous_position = (avg_x, avg_y)

    # Calculate the angle of the position vector with respect to the center of the screen
    angle = numpy.arctan2(avg_y - center_y, avg_x - center_x)

    angle_x = numpy.cos(angle)
    angle_y = numpy.sin(angle)
    # Print the angle
    print("Angle:", angle, " Deviation X:", delta_X, " Deviation Y:", delta_Y, " Angle X:", angle_x, " Angle Y:", angle_y)

    # Save angle in a JSON file
    with open("angle.json", "w") as file:
        json.dump(
            {
                "angle_x": angle_x, 
                "angle_y": angle_y, 
                "deviation_x": delta_X, 
                "deviation_y": delta_Y 
            }, file)

    if hand_landmarks:
        # Optional: Print landmark details
        pass

    cv2.imshow("Hand Landmarks", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
