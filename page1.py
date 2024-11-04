#pip3 install sacremoses
#pip3 install sentencepiece
# pip install pyttsx3
# pip install transformers
# pip install torch
# pip install pyaudio
# pip3 install SpeechRecognition 

import torch
import pandas as pd
import utils
from datasets import Dataset
from huggingface_hub import InferenceClient
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer, pipeline
 


import tkinter as tk
from tkinter import scrolledtext, messagebox
import speech_recognition as sr
#from googletrans import Translator, LANGUAGES
from PIL import Image, ImageTk
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import pyttsx3
from gtts import gTTS
import playsound
import os
from openai import OpenAI

# Initialize the translator
#translator = Translator()

# Replace with your API Key
# Set your OpenAI API key
openapi_api_key = "XXXXX"

client = InferenceClient(api_key="hf_XXXXXX")

classifier = pipeline("text-classification", model='dkkh8788/finetuned_classification_model_v3',
                      tokenizer='dkkh8788/finetuned_classification_model_v3', device='mps')

def generate_response(feedback, sentiment):

    if sentiment == "POSITIVE":
        prompt = f"Generate an appropriate positive response in maximum 30 words to the customer thanking and expressing gratitude."
    else:
        prompt = f"Generate an appropriate empathetic response in maximum 30 words to the customer apologizing for the inconvenience and offering assistance."

    messages = [
        { "role": "assistant", "content": f"{feedback}\n\nQuestion: {prompt}" },
    ]
 
    output = client.chat.completions.create(
        model="microsoft/Phi-3.5-mini-instruct",
        messages=messages,
        stream=True,
        temperature=0.5,
        max_tokens=1024,
        top_p=0.7
    )
 
    # Collect all chunks in a list and join them after the loop
    full_response = []
 
    for chunk in output:
        full_response.append(chunk.choices[0].delta.content)
 
    # Join and return the entire response as a single string
    return ("".join(full_response))

def perform_sentiment_analysis(text):  
  sentiment_analyzer = pipeline(
                        'sentiment-analysis', model=
                            'distilbert/distilbert-base-uncased-finetuned-sst-2-english', device="mps")

  result = sentiment_analyzer(text)
  return result[0]['label']
     


##################################  START ####################################

# Function to convert speech to text
def speech_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            messagebox.showinfo("Info", "Please speak something...")
            audio = r.listen(source)
            text = r.recognize_google(audio, language='hi-IN')
            print("Direct Model STT Output:", text)
            input_text.delete(0, tk.END)  # Clear the input field
            input_text.insert(tk.END, text)  # Insert recognized text
            hi_en_translate()
        except sr.UnknownValueError:
            messagebox.showerror("Error", "Could not understand the audio.")
        except sr.RequestError:
            messagebox.showerror("Error", "Could not request results; check your internet connection.")


# function to translate hindi text to English
def hi_en_translate():
	tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-hi-en")
	model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-hi-en")
	text = input_text.get().strip()

	# Tokenize the input text
	inputs = tokenizer(text, return_tensors="pt")

	# Generate translation from model
	translated_tokens = model.generate(**inputs)

	# Decode the translation and print the result
	translated_text = tokenizer.decode(translated_tokens[0], skip_special_tokens=True)
	print ("Hindi to English Translation ", translated_text)
	classify_text(translated_text)
	
#### Text Classification to identify Order Detail / Product Setup / Feedback ######
def classify_text(text):
    result = classifier(text)
    output_text = result[0]['label']
    input_text = text
    # print(f"Classification Result: {result}")
    print(f"Text: {text}. [ Predicted Class: {result[0]['label']} ]\n")
    filter(input_text, output_text)

def filter(text, category):
  if category == "feedback":
    sentiment = perform_sentiment_analysis(text)
    # Further process the query based on sentiment
    response = generate_response(text, sentiment)
  else:
    response = utils.getResponse(text)

  translate_to_hindi_openai(response)

###### Converting English Response to Hindi ######################  
def translate_to_hindi_openai(text):

	client = OpenAI(api_key=openapi_api_key)
	response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # or "gpt-4" if you have access
        messages=[
            {"role": "user", "content": f"Translate the following English text to Hindi: '{text}'"}
        ]
    )
    
    
    # Extract the translation from the response
	translated_text=str(response.choices[0].message.content)
	#translated_text = response['choices'][0]['message']['content']
	print ("English to Hindi Translation openai", translated_text)
	output_text.config(state=tk.NORMAL)  # Enable editing
	output_text.delete(1.0, tk.END)  # Clear the output field
	output_text.insert(tk.END, translated_text)  # Insert translated text
	output_text.config(state=tk.DISABLED)  # Disable editing
	respond(translated_text)
    #return translated_text
    
   
########### Convert Text to Speech ###############
def respond(text):
	tts = gTTS(text=text, lang='hi')
	filename = "response.mp3"
	tts.save(filename)
	playsound.playsound(filename)
	os.remove(filename)  # Remove the file after playing


# Function to detect language
def detect_language(text):
    detected = translator.detect(text)
    return LANGUAGES.get(detected.lang, "Unknown")
    


#################### UI Elements ##############################

# Create the main window
root = tk.Tk()
root.title("ABC Customer Support")
root.geometry("600x500")
root.resizable(False, False)

# Frame for input
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

# Microphone button
mic_icon = Image.open("mic_icon.png")  # Ensure you have a mic icon image in the same directory
mic_icon = mic_icon.resize((30, 30))
mic_photo = ImageTk.PhotoImage(mic_icon)

mic_button = tk.Button(input_frame, image=mic_photo, command=speech_to_text, borderwidth=0)
mic_button.pack(side=tk.LEFT)

# Input text box
input_text = tk.Entry(input_frame, width=50)
input_text.pack(side=tk.LEFT, padx=10)

# Translate Button
translate_button = tk.Button(root, text="Submit", command=hi_en_translate)
translate_button.pack(pady=5)

# Output field for translated text
output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=15, state=tk.DISABLED)
output_text.pack(pady=10, padx=10)

# Start the GUI loop
root.mainloop()

################## TextToSpeech ########################
# Initialize text-to-speech engines
tts_engine = pyttsx3.init()

# Configure the text-to-speech voice
voices = tts_engine.getProperty("voices")
tts_engine.setProperty("voice", voices[1].id)  # Select the first voice (can be customized)

 
