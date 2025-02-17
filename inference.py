import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
from inference_sdk import InferenceHTTPClient

# Define the list of insects
insects = ['Apple Scab Leaf', 'Apple leaf', 'Apple rust leaf', 'Bell_pepper leaf spot', 'Bell_pepper leaf', 
           'Blueberry leaf', 'Cherry leaf', 'Corn Gray leaf spot', 'Corn leaf blight', 'Corn rust leaf', 'Peach leaf', 
           'Potato leaf early blight', 'Potato leaf late blight', 'Potato leaf', 'Raspberry leaf', 'Soyabean leaf', 
           'Soybean leaf', 'Squash Powdery mildew leaf', 'Strawberry leaf', 'Tomato Early blight leaf', 'Tomato Septoria leaf spot', 
           'Tomato leaf bacterial spot', 'Tomato leaf late blight', 'Tomato leaf mosaic virus', 'Tomato leaf yellow virus', 
           'Tomato leaf', 'Tomato mold leaf', 'Tomato two spotted spider mites leaf', 'grape leaf black rot', 'grape leaf'
        ]

def get_detections(image_path):
    model_id = 4
    
    # initialize the client
    CLIENT = InferenceHTTPClient(
        api_url="https://detect.roboflow.com",
        api_key="l23zfyKCBvNxpu8wohnr"
    )

    # infer on a local image
    predictions = CLIENT.infer(f"{image_path}", model_id=f"new-vq4aw/{model_id}")
    
    response = {
        "Total Detections": len(predictions["predictions"]),
        "Detections": []
    }

    # Add each detection to the response
    for i in range(len(predictions["predictions"])):
        converted_class = int(predictions["predictions"][i]['class'])
        response["Detections"].append({
            "Detection No": i + 1,
            "Class": insects[converted_class]
        })

    return response, predictions


# Function to make predictions and plot results
def predict_and_plot(image_path):

    # Make prediction
    response, predictions = get_detections(image_path)

    # Print total detections
    length_of_json = len(predictions["predictions"])
    
    # Load the image
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    # Define font
    font = ImageFont.load_default()

    # Draw bounding boxes and labels
    for i in range(length_of_json):
        pred = predictions["predictions"][i]
        x, y, width, height = pred['x'], pred['y'], pred['width'], pred['height']
        class_id = int(pred['class'])
        label = insects[class_id]
        confidence = pred['confidence']

        # Calculate bounding box coordinates
        left = x - width / 2
        top = y - height / 2
        right = x + width / 2
        bottom = y + height / 2

        # Draw bounding box
        draw.rectangle([left, top, right, bottom], outline="red", width=2)

        # Draw label and confidence
        label_text = f"{label} ({confidence:.2f})"
        bbox = draw.textbbox((left, top), label_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        draw.rectangle([left, top - text_height, left + text_width, top], fill="red")
        draw.text((left, top - text_height), label_text, font=font, fill="white")

    # Save the plotted image
    plot_image_path = "prediction_plot.png"
    image.save(plot_image_path)
    print(f"Plotted image saved as: {plot_image_path}")

    # Optionally, display the image using matplotlib
    plt.imshow(image)
    plt.axis('off')
    plt.show()

    return plot_image_path
