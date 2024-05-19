from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
import azure.cognitiveservices.speech as speechsdk
from msrest.authentication import CognitiveServicesCredentials
import os
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
    subscription_key = os.environ["VISION_KEY"]
    endpoint = os.environ["VISION_ENDPOINT"]
    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
    
    # Open the image and process the text
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
        time.sleep(.5)

    # Print the detected text, line by line
    text = ''
    if read_result.status == OperationStatusCodes.succeeded:
        for text_result in read_result.analyze_result.read_results:
            for line in text_result.lines:
                text+='\n' + line.text
    return text

def text_to_speech(text):    
    # Set up the client
    speech_config = speechsdk.SpeechConfig(os.environ['SPEECH_KEY'], os.environ['SPEECH_REGION'])
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

    # Specify the voice for the AI to use
    speech_config.speech_synthesis_voice_name='en-US-BrianMultilingualNeural'

    # Create the speech synthesizer
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    # Read the text provided as a parameter and synthesize to the default speaker.
    speech_synthesizer.speak_text_async(text).get()