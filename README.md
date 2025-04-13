## Goal

Identify a specific theft vehicle from a limited set of images, based on a given license plate number using computer vision and AWS Rekognition.

## Approach

- Used a pretrained object detection model to label vehicles and license plates in the limited dataset
- Manually verified and refined bounding boxes to ensure accuracy
- Labeled each image with Bounding box coordinates, Vehicle Type
- Implemented data augmentation techniques (e.g., rotation, brightness shifts, cropping, flipping) to simulate real-world variations and improve model robustness
- Utilized AWS Rekognition to detect text from vehicle and extract potential license plate numbers

