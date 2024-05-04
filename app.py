from PIL import Image, ImageDraw, ImageFont
from takeAiSuggestion import give_tip
import ctypes
import pyautogui

# Function to set the wallpaper
def set_wallpaper(image_path):
    # Call the Windows API function to set the wallpaper
    ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)

def wrap_text(text, font, max_width):
    lines = []
    words = text.split()
    while words:
        line = ''
        while words and font.getmask(line + words[0]).getbbox()[2] <= max_width:
            line += words.pop(0) + ' '
        lines.append(line)
    return lines

def generate_image(title, text, save_path, topic):
    # Get the screen size
    width, height = pyautogui.size()
    
    image = Image.open('./baseBackground.jpg')
    # Resize the image to match screen size
    image = image.resize((width, height))

    # Create a draw object to draw on the image
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
    y_text = y_title + 50 # Adjust this value to place the text below the title

    # Draw the wrapped text on the image
    for line in wrapped_text:
        draw.text((x, y_text), line, fill="white", font=font)
        y_text += font.getmask(line).getbbox()[3] + 10 # Add the height of the line to the y-axis
        
    # Draw the wrapped text on the image
    draw.text((x, y_text + 20), f"- {topic} -", fill="#80dfff", font=topic_font)
    
    # Save the image
    image.save(save_path)

# Example usage
interests = ['javascript', 'typescript', 'bash', 'ssh', 'HTML', 'python']

aiResponse = give_tip(interests)

title = aiResponse['title']
text = aiResponse['text']
topic_of_today = aiResponse['topic']
save_path = "C:\\Users\\User\\Documents\\winWallpaperGenerator\\newImage.jpg"

# generate_image(textJson, save_path)
generate_image(title, text, save_path, topic_of_today)
print(len(text))
# Call the function to set the new wallpaper
set_wallpaper(save_path)
