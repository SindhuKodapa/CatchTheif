# Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-custom-labels-developer-guide/blob/master/LICENSE-SAMPLECODE.)

import boto3
import io
import json
from PIL import Image, ImageDraw, ImageFont

access_key = 'XXXXX'
secret_key = 'YYYYY'
token = 'ZZZZ'

def display_image(bucket, photo, response):
    # Load image from S3 bucket
    s3_connection = boto3.resource('s3', region_name = 'us-east-1', aws_access_key_id = access_key, aws_secret_access_key = secret_key, aws_session_token = token)
    s3_object = s3_connection.Object(bucket, photo)
    s3_response = s3_object.get()
    stream = io.BytesIO(s3_response['Body'].read())
    image = Image.open(stream)

    # Ready image to draw bounding boxes on it.
    imgWidth, imgHeight = image.size
    draw = ImageDraw.Draw(image)

    # Calculate and display bounding boxes for each detected custom label
    print('Detected custom labels for ' + photo)
    annotations = []
    for customLabel in response['CustomLabels']:
        label_data = {}
        print('Label: ' + str(customLabel['Name']))
        print('Confidence: ' + str(customLabel['Confidence']))
        
        if 'Geometry' in customLabel:
            box = customLabel['Geometry']['BoundingBox']
            left = imgWidth * box['Left']
            top = imgHeight * box['Top']
            width = imgWidth * box['Width']
            height = imgHeight * box['Height']

            # Append label data for the current label
            label_data = {
                "classname": customLabel['Name'],
                "top": int(top),
                "left": int(left),
                "height": int(height),
                "width": int(width)
            }
            annotations.append(label_data)

    return annotations, imgWidth, imgHeight

def show_custom_labels(model, bucket, photo, min_confidence):
    client = boto3.client('rekognition', region_name = 'us-east-1', aws_access_key_id = access_key, aws_secret_access_key = secret_key, aws_session_token = token)

    # Call DetectCustomLabels
    response = client.detect_custom_labels(Image={'S3Object': {'Bucket': bucket, 'Name': photo}},
                                           MinConfidence=min_confidence,
                                           ProjectVersionArn=model)

    return response

def process_images_in_bucket(model, bucket, min_confidence):
    s3_client = boto3.client('s3', region_name = 'us-east-1', aws_access_key_id = access_key, aws_secret_access_key = secret_key, aws_session_token = token)
    result = s3_client.list_objects_v2(Bucket=bucket)
    

    output_data = []

    # Process each image in the bucket
    for obj in result.get('Contents', []):
        #print(obj)
        photo = obj['Key']
        if('png' not in photo): 
            continue
        print(f'Processing {photo}...')

        # Get custom labels for the current image
        response = show_custom_labels(model, bucket, photo, min_confidence)
        #print(response)

        # Get annotations and image dimensions
        annotations, imgWidth, imgHeight = display_image(bucket, photo, response)

        # Add image data to output
        image_data = {
            "filename": photo,
            "height": imgHeight,
            "width": imgWidth,
            "annotations": annotations
        }
        output_data.append(image_data)

    return output_data

def write_output_to_json(output_data, output_file):
    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=4)

def main():
    bucket = 'challenge-2-evaluation'
    model = 'arn:aws:rekognition:us-east-1:848643745672:project/metro/version/metro.2024-10-13T11.06.32/1728831992426'
    min_confidence = 50
    output_file = 'output_labels_challenge2_latest.json'

    # Process all images in the bucket and get output data
    output_data = process_images_in_bucket(model, bucket, min_confidence)

    # Write output to JSON file
    write_output_to_json(output_data, output_file)
    print(f"Output written to {output_file}")

if __name__ == "__main__":
    main()
