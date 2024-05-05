from takeAiSuggestion import give_tip
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv
import os
import ctypes
import pyautogui

# Load the .env file 
load_dotenv()

# Load your interest from .env file and making a liste
env_inrerests = os.getenv("INTERESTS")
interests = env_inrerests.split(',')

# Make sure you have changed it to your actual path!
env_path = os.getenv("PATH_TO_THE_PROJECT")

# Function to set the wallpaper
def set_wallpaper(env_path):
    # Complete the path to the new image
    path = env_path + "\\assets\\newBackgroung.jpg"
    # Call the Windows API function to set the wallpaper
    ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 3)

# Function to wrap the text
def wrap_text(text, font, max_width):
    lines = []
    words = text.split()
    while words:
        line = ''
        while words and font.getmask(line + words[0]).getbbox()[2] <= max_width:
            line += words.pop(0) + ' '
        lines.append(line)
    return lines

def generate_image(title, text, topic):
    # Get the screen size
    width, height = pyautogui.size()
    
    # Open and resize the image to match the screen size
    image = Image.open('./assets/baseBackground.jpg')
    image = image.resize((width, height))

    # Create a draw object to draw the text on the image
    draw = ImageDraw.Draw(image)
    
    # Define the font and text size
    title_font = ImageFont.truetype("./fonts/tiza.ttf", 60)
    font = ImageFont.truetype("./fonts/tiza.ttf", 30)
    topic_font = ImageFont.truetype("./fonts/tiza.ttf", 20)
    
    # Split the text into lines to fit the maximum width
    max_width = width // 1.5  # Maximum width before adding a line break
    
    wrapped_title = wrap_text(title, font, 800)
    wrapped_text = wrap_text(text, font, max_width)

    # Calculate the x position to center the title and text in the image
    title_bbox = draw.multiline_textbbox((0, 0), wrapped_title[0], font=title_font)
    x = (width - title_bbox[2]) // 2
    y_title = 150
    

    # Draw the wrapped title on the image
    for line in wrapped_title:
        draw.text((x, y_title), line, fill="#ffff99", font=title_font)
        y_title += title_font.getmask(line).getbbox()[3]  # Add the height of the line to the y-axis
    
    # Calculate the position to place the text below the title
    y_text = y_title + 50

    # Draw the wrapped text on the image
    for line in wrapped_text:
        draw.text((x, y_text), line, fill="white", font=font)
        y_text += font.getmask(line).getbbox()[3] + 10 # Add the height of the line to the y-axis
        
    # Draw the current topic on the image
    draw.text((x, y_text + 20), f"- {topic} -", fill="#80dfff", font=topic_font)
    
    # Save the image
    image.save('./assets/newBackgroung.jpg')



# Asking llama3 for advice 
aiResponse = give_tip(interests)
title = aiResponse['title']
text = aiResponse['text']
topic_of_today = aiResponse['topic']

# generate_image
generate_image(title, text, topic_of_today)
# Call the function to set the new wallpaper
set_wallpaper(env_path)
