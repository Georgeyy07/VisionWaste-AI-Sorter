import cv2 # OpenCV computer vision library to help us see through the webcam
import requests # this handles the "phone call" to the ai server
import base64 # turns the photo into a long string of text the ai can read
from flask import Flask, jsonify # the toolkit for making our local website/api

app = Flask(__name__)

# Where the ai is on laptop
ollamaUrl = "http://localhost:11434/api/generate" 
# We are using the llava model because it can actually look at images quickly and very little ai hallucination
modelName = "llava" 

def captureFrame():
    # link up with the laptop's webcam camera
    camera = cv2.VideoCapture(0) 
    
    # give the camera a second to blink and adjust to the lights, test run
    for _ in range(10): 
        camera.read() 
        
    # take the actual photo
    success, image = camera.read() 
    
    # let go of the camera so other apps aren't blocked from using it, for hardware
    camera.release() 
    
    # if the camera is acting up, just return nothing
    if not success: 
        return None

    # shrink the photo a bit so it travels faster over the wifi
    image = cv2.resize(image, (336, 336))
    
    # turn the image into a jpeg format
    _, buffer = cv2.imencode('.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, 95])
    
    # encode it into that base64 text format the ai likes
    return base64.b64encode(buffer).decode('utf-8')

def classifyImage(photoData):
    print("The Pico just sent over a new sorting request!", flush=True)
    
    # packing up the photo and the instructions into one bundle
    dataBundle = {
        "model": "llava",
        "prompt": (
            "Ignore the human."
            "Focus only on the item being held or placed in front of the camera. "
            "Identify the item in a few words, then classify it. "
            "Use this guide to help you decide: "
            "RECYCLING: plastic bottles, cans, cardboard, paper, glass bottles, newspapers, magazines, cereal boxes, water bottles, juice cartons. "
            "COMPOST: food scraps, banana peels, apple cores, vegetable peels, eggshells, coffee grounds, paper towels, napkins, bread, fruit. "
            "TRASH: plastic bags, chip bags, styrofoam, face masks, rubber gloves, broken glass, candy wrappers, straws, tape, foil pouches. "
            "Pick exactly one category. Do not mention the other two categories anywhere in your response. "
            "End your response with just the one word: Recycling, Compost, or Trash. "
            "Example of a good response: 'Banana peel. Compost' "
            "If you are unsure, default to Trash. " # brute forced prompt, but it works and is very important for accuracy
        ),
        "images": [photoData], 
        "stream": False,       
        "options": {
            "num_predict": 120, # limiting words to eliminate ai rambling
            "temperature": 0,   # stay consistent, don't get creative
            "num_ctx": 2048,
            "num_thread": 8     
        }
    }

    try:
        print("Sending to AI, AI is thinking...", flush=True)
        # send the bundle to the ollama server
        aiResponse = requests.post(ollamaUrl, json=dataBundle, timeout=130)
        aiResponse.raise_for_status()
        
        # read what the ai said and make it all lowercase to avoid typos, prompt should handle the wording errors
        finalAnswer = aiResponse.json().get("response", "").strip().lower()
        print(f"AI Response:\n{finalAnswer}\n", flush=True)

        # look for the magic words in the ai's answer
        if "recycling" in finalAnswer:
            return "Recycling"
        elif "compost" in finalAnswer:
            return "Compost"
        elif "trash" in finalAnswer:
            return "Trash"
        else:
            print("I couldn't find a clear category, so we'll go with Trash", flush=True)
            return "Trash"

    except Exception as error:
        print(f"Error with laptop: {error}", flush=True)
        return "Trash" 

# this is the web address the pico 2 w will visit
@app.route('/classify', methods=['GET'])
def checkTrash():
    # step 1: take the photo
    currentPhoto = captureFrame() 
    if currentPhoto is None:
        return jsonify({"error": "I couldn't open the camera!"}), 500
    
    # step 2: ask the ai to identify it
    finalCategory = classifyImage(currentPhoto) 
    
    # step 3: send the answer back to the pico
    return jsonify({"category": finalCategory})

if __name__ == '__main__':
    # run the server so the pico can find it on your home wifi
    app.run(host='0.0.0.0', port=5001, debug=False, threaded=True)