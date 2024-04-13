from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time

def read_image(img_file_path):
    """
    Reads an image from the specified file path and returns the detected text using Microsoft Azure computer vision (inspired by the Azure quickstart guide)

    Parameters:
        img_file_path (str): The path to the image file.

    Returns:
        text: The detected text from the image, line by line.
    """
    # Set up the client
    subscription_key = os.environ["4053b232aba945f4b67f07df004bae7a"]
    endpoint = os.environ["https://madcomimagereader.cognitiveservices.azure.com/"]
    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
    
    # GOpen the image and process the text
    read_image = open(img_file_path, "rb")
    read_response = computervision_client.read_in_stream(read_image,  raw=True)

    # Get the operation location (URL with an ID at the end) from the response
    read_operation_location = read_response.headers["Operation-Location"]
    
    # Grab the ID from the URL
    operation_id = read_operation_location.split("/")[-1]

    # Call the "GET" API and wait for it to retrieve the results 
    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status not in ['notStarted', 'running']:
            break
        time.sleep(1)

    # Print the detected text, line by line
    text = ''
    if read_result.status == OperationStatusCodes.succeeded:
        for text_result in read_result.analyze_result.read_results:
            for line in text_result.lines:
                text+='\n' + line.text
    return text