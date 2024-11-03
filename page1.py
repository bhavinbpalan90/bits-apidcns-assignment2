#pip3 install sacremoses
#pip3 install sentencepiece
# pip install pyttsx3
# pip install transformers
# pip install torch
# pip install pyaudio


import tkinter as tk
from tkinter import scrolledtext, messagebox
import speech_recognition as sr
from googletrans import Translator, LANGUAGES
from PIL import Image, ImageTk
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import pyttsx3
from gtts import gTTS
import playsound
import os


# Initialize the translator
translator = Translator()
    
# Function to convert text to speech
def respond(text):
	print("text to speak is ", text.text)
	tts = gTTS(text=text.text, lang='hi')
	filename = "response.mp3"
	tts.save(filename)
	playsound.playsound(filename)
	os.remove(filename)  # Remove the file after playing

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
    
# Function to translate hi text to English
def translate_to_hindi(english):
    text = english
    if not text:
        messagebox.showwarning("Warning", "Please enter or speak some text to translate.")
        return

    translated = translator.translate(text, dest='hi')
    output_text.config(state=tk.NORMAL)  # Enable editing
    output_text.delete(1.0, tk.END)  # Clear the output field
    output_text.insert(tk.END, translated.text)  # Insert translated text
    output_text.config(state=tk.DISABLED)  # Disable editing
    print ("English to Hindi Translation ", translated)
    respond(translated)

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
	#output_text.config(state=tk.NORMAL)  # Enable editing
	#output_text.delete(1.0, tk.END)  # Clear the output field
	#output_text.insert(tk.END, translated_text)  # Insert translated text
	#output_text.config(state=tk.DISABLED)  # Disable editing
	translate_to_hindi(translated_text)

	print("Direct Model Translation Output:", translated_text)
	
# def en_hi_translate(text):
# 	tokenizer = AutoTokenizer.from_pretrained("AbhirupGhosh/opus-mt-finetuned-en-hi")
# 	model = AutoModelForSeq2SeqLM.from_pretrained("AbhirupGhosh/opus-mt-finetuned-en-hi")
# 	text = input_text.get().strip()
# 
# 	# Tokenize the input text
# 	inputs = tokenizer(text, return_tensors="pt")
# 
# 	# Generate translation from model
# 	translated_tokens = model.generate(**inputs)
# 
# 	# Decode the translation and print the result
# 	translated_text = tokenizer.decode(translated_tokens[0], skip_special_tokens=True)
# 	print ("English to Hindi Translation ", translated_text)
# 		
# 	return
# 
# 	output_text.config(state=tk.NORMAL)  # Enable editing
# 	output_text.delete(1.0, tk.END)  # Clear the output field
# 	output_text.insert(tk.END, translated_text)  # Insert translated text
# 	output_text.config(state=tk.DISABLED)  # Disable editing
# 	
# 	respond(translated_text)
# 
# 	print("Direct Model Translation Output:", translated_text)


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






 
