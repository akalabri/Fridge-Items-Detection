from ultralytics import YOLO
import cv2
import cvzone
import math
import csv
import time
from collections import Counter

# Default Inventory Values
st_milk_inventory = 10
ch_milk_inventory = 10
sando_inventory = 10
biscuit_inventory = 10
chocolate_inventory = 10

# Function to read initial inventory values from the last row of the CSV file
def read_initial_inventory():
    try:
        with open('Fridge_Inventory.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            last_row = None
            for row in reader:
                last_row = row
            if last_row:
                global st_milk_inventory, ch_milk_inventory, sando_inventory, biscuit_inventory, chocolate_inventory
                st_milk_inventory = int(last_row['St Milk'])
                ch_milk_inventory = int(last_row['Ch Milk'])
                sando_inventory = int(last_row['Sando'])
                biscuit_inventory = int(last_row['Biscuit'])
                chocolate_inventory = int(last_row['Chocolate'])
    except FileNotFoundError:
        print("Inventory file not found. Using default values.")

# Read initial inventory values from the last row of the CSV file
read_initial_inventory()

# Print the initial inventory values
print("Initial Inventory Values:")
print(f"St Milk Inventory: {st_milk_inventory}")
print(f"Ch Milk Inventory: {ch_milk_inventory}")
print(f"Sando Inventory: {sando_inventory}")
print(f"Biscuit Inventory: {biscuit_inventory}")
print(f"Chocolate Inventory: {chocolate_inventory}")


cap = cv2.VideoCapture("../Videos/Rashid.mp4")
model = YOLO("../Yolo-Weights/inventory.pt")

classNames = ['Hamza', 'Rashid', 'Umaimah', 'biscuit', 'ch milk', 'chocolate', 'sando', 'st milk']

detections = []

while True:
    success, img = cap.read()
    if not success:
        break  # Break the loop when the video is finished

    results = model(img, stream=True)
    detect = []
    for r in results:
        boxes = r.boxes
        for box in boxes:
            # Bounding Box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            # cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,255),3)
            w, h = x2 - x1, y2 - y1
            cvzone.cornerRect(img, (x1, y1, w, h))
            # Confidence
            conf = math.ceil((box.conf[0] * 100)) / 100
            # Class Name
            cls = int(box.cls[0])
            cvzone.putTextRect(img, f'{classNames[cls]} {conf}', (max(0, x1), max(35, y1)), scale=1, thickness=1)
            if conf > 0.8:
                detect.append(classNames[cls])

    if len(detect) > len(detections):
        detections = detect

    cv2.imshow("Video", img)
    cv2.waitKey(1)

print("Detections:", detections)

# Determine the detected person
detected_person = None
if detections:
    for person in ['Rashid', 'Umaimah', 'Hamza']:
        if person in detections:
            detected_person = person
            break

# Count the occurrences of items in the detections
item_counts = Counter(detections)

# Update inventory based on item counts
biscuit_inventory -= item_counts['biscuit']
ch_milk_inventory -= item_counts['ch milk']
chocolate_inventory -= item_counts['chocolate']
sando_inventory -= item_counts['sando']
st_milk_inventory -= item_counts['st milk']

# Rest of your code after the loop
current_datetime = time.strftime("%Y-%m-%d %H:%M:%S")

# Save answers to a CSV file
with open('Fridge_Inventory.csv', 'a', newline='') as csvfile:
    fieldnames = ['Date/Time', 'Person', 'St Milk', 'Ch Milk', 'Sando', 'Biscuit', 'Chocolate','Type']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write the header row if the file is empty
    if csvfile.tell() == 0:
        writer.writeheader()

    writer.writerow({
        'Date/Time': current_datetime,
        'Person': detected_person,
        'St Milk': st_milk_inventory,
        'Ch Milk': ch_milk_inventory,
        'Sando': sando_inventory,
        'Biscuit': biscuit_inventory,
        'Chocolate': chocolate_inventory,
        'Type': 'Consume'
    })


