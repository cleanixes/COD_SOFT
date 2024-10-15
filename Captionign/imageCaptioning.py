

import torch
import torchvision.transforms as transforms
from torchvision.models.detection import fasterrcnn_resnet50_fpn
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
from PIL import Image


# !wget http://images.cocodataset.org/zips/val2017.zip
# !wget http://images.cocodataset.org/annotations/annotations_trainval2017.zip
# !unzip val2017.zip
# !unzip annotations_trainval2017.zip

import json
from torch.utils.data import Dataset, DataLoader

image_folder = r"C:\Users\harla\Downloads\CODSOFT\Captionign\val2017"
annotation_file = r"C:\Users\harla\Downloads\CODSOFT\Captionign\annotations"

class RabbitDataset(Dataset):
    def __init__(self, image_folder, annotation_file):
        # Open and load the JSON annotation file
        with open(annotation_file, 'r') as f:
            self.coco = json.load(f)
        
        # Store the image folder path
        self.image_folder = image_folder
        
        # Filter images that contain rabbits (category_id == 18)
        self.rabbit_images = [img for img in self.coco['images'] 
                              if any(ann['category_id'] == 18 for ann in self.coco['annotations'] 
                                     if ann['image_id'] == img['id'])]
    
    def __len__(self):
        # Return the number of rabbit images
        return len(self.rabbit_images)
    
    def __getitem__(self, idx):
        # Get the image info for the given index
        img_info = self.rabbit_images[idx]
        
        # Construct the full path to the image file
        img_path = f"{self.image_folder}/{img_info['file_name']}"
        
        # Open the image and convert it to RGB
        image = Image.open(img_path).convert("RGB")
        
        # Return the image and a label
        return image, "A photo of a rabbit"

# Step 3: Load pre-trained models
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load Faster R-CNN for object detection
detection_model = fasterrcnn_resnet50_fpn(pretrained=True)
detection_model.eval().to(device)

# Load pre-trained image captioning model
captioning_model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
image_processor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

captioning_model.eval().to(device)

# Step 4: Define the inference function
def caption_rabbit_image(image_path):
    # Load and preprocess the image
    image = Image.open(image_path).convert("RGB")
    transform = transforms.Compose([transforms.ToTensor()])
    img_tensor = transform(image).unsqueeze(0).to(device)
    
    # Detect objects
    with torch.no_grad():
        detections = detection_model(img_tensor)[0]
    
    # Check if a rabbit is detected (class 18 in COCO dataset)
    rabbit_detected = any(label == 18 for label in detections['labels'])
    
    if rabbit_detected:
        # Generate caption
        pixel_values = image_processor(image, return_tensors="pt").pixel_values.to(device)
        with torch.no_grad():
            output = captioning_model.generate(pixel_values, max_length=16, num_beams=4)
        caption = tokenizer.decode(output[0], skip_special_tokens=True)
        return f"Rabbit detected. Caption: {caption}"
    else:
        return "No rabbit detected in the image."

# Step 5: Test the model
test_image_path = r"C:\Users\harla\Downloads\CODSOFT\Captionign\val2017\000000171190.jpg"
result = caption_rabbit_image(test_image_path)
print(result)
