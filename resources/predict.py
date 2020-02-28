from datetime import datetime
from PIL import Image
from torchvision import transforms
from urllib.request import urlopen

import logging
import os
import sys
import torch

model = torch.hub.load('pytorch/vision:v0.5.0', 'resnet18', pretrained=True)
model.eval()

def get_class_labels():
    class_dict = {}
    counter = 0
    try:
        dirname = os.path.dirname(__file__)
        with open(os.path.join(dirname, 'labels.txt'), 'r') as infile:
            for line in infile.readlines():
                out = line.split("'")
                class_dict[counter] = out[1]
                counter += 1
    except FileNotFoundError:
        logging.info(os.listdir(os.curdir))
        logging.info(os.curdir)
        raise

    return class_dict

def predict_image_from_url(image_url):
    class_dict = get_class_labels()
    with urlopen(image_url) as testImage:
        input_image = Image.open(testImage).convert('RGB')
        preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        input_tensor = preprocess(input_image)
        input_batch = input_tensor.unsqueeze(0) # create a mini-batch as expected by the model

        # move the input and model to GPU for speed if available
        if torch.cuda.is_available():
            input_batch = input_batch.to('cuda')
            model.to('cuda')

        with torch.no_grad():
            output = model(input_batch)
        # Tensor of shape 1000, with confidence scores over Imagenet's 1000 classes
        print(output[0])
        # The output has unnormalized scores. To get probabilities, you can run a softmax on it.
        softmax = (torch.nn.functional.softmax(output[0], dim=0))
        out = class_dict[softmax.argmax().item()]

        response = {
            'created': datetime.utcnow().isoformat(),
            'predictedTagName': out,
            'prediction': softmax.max().item()
        }

        logging.info(f'returning {response}')
        return response

if __name__ == '__main__':
    predict_image_from_url(sys.argv[1])
