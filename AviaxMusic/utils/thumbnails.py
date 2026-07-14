# a part of Opus Music Project 2025 ©
# this code is & will be our property as it is or even after modified 
# must give credits if used this code anywhere 
import os
import re
import textwrap
import numpy as np
from PIL import (
    Image,
    ImageDraw,
    ImageEnhance,
    ImageFilter,
    ImageFont,
)
from py_yt import VideosSearch
# config se YOUTUBE_IMG_URL load ho raha hai
from config import YOUTUBE_IMG_URL

def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    ratio = min(widthRatio, heightRatio)
    newWidth = int(image.size[0] * ratio)
    newHeight = int(image.size[1] * ratio)
    try:
        resample = Image.Resampling.LANCZOS
    except AttributeError:
        resample = Image.ANTIALIAS  # For Pillow<10
    image = image.resize((newWidth, newHeight), resample)
    return image

def get_dominant_color(image):
    """Extract the dominant color from the image"""
    image = image.convert('RGB')
    image = image.resize((50, 50))
    pixels = np.array(image)
    pixel_list = pixels.reshape(-1, 3)
    avg_color = tuple(pixel_list.mean(axis=0).astype(int))
    
    if sum(avg_color) < 200:  # If color is too dark
        brightened = tuple(min(255, int(c * 1.5)) for c in avg_color)
        return brightened
    
    return avg_color

def get_contrasting_color(bg_color):
    """Get a contrasting color for better visibility"""
    luminance = (0.299 * bg_color[0] + 0.587 * bg_color[1] + 0.114 * bg_color[2])
    return (255, 255, 255) if luminance < 128 else (50, 50, 50)

async def gen_thumb(videoid):
    final_path = f"cache/{videoid}.png"
    if os.path.isfile(final_path):
        return final_path
        
    url = f"https://www.youtube.com/watch?v={videoid}"
    try:
        results = VideosSearch(url, limit=1)
        result_data = await results.next()
        
        # Default details agar search na mile
        title = "Unknown Title"
        duration = "Unknown Duration"
        views = "Unknown Views"
        channel = "Unknown Channel"
        
        if result_data.get("result"):
            result = result_data["result"][0]
            title = re.sub(r"\W+", " ", result.get("title", "Unknown Title")).title()
            duration = result.get("duration", "Unknown Duration")
            views = result.get("viewCount", {}).get("short", "Unknown Views")
            channel = result.get("channel", {}).get("name", "Unknown Channel")
            
        # Ensure cache directory exists
        os.makedirs("cache", exist_ok=True)
        
        # --- MODIFIED: Yahan hum download karne ke bajaye aapki custom image open karenge ---
        # Agar aap koi local file use karna chahte hain toh 'assets/my_image.png' jaisa path dein
        # Ya phir config.py wala YOUTUBE_IMG_URL use karein (agar wo system file path hai)
        CUSTOM_IMAGE_PATH = YOUTUBE_IMG_URL 
        
        try:
            youtube = Image.open(CUSTOM_IMAGE_PATH)
        except Exception as e:
            # Agar image load nahi ho paayi toh process stop ho jayega
            print(f"Error loading custom image: {e}")
            return YOUTUBE_IMG_URL
            
        # Extract dominant color from the custom image
        bar_color = get_dominant_color(youtube)
        
        image1 = changeImageSize(1280, 720, youtube.copy())
        center_thumb = changeImageSize(940, 420, youtube.copy())
        
        # Rounded center image mask
        mask = Image.new("L", center_thumb.size, 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.rounded_rectangle(
            [0, 0, center_thumb.size[0], center_thumb.size[1]],
            radius=40,
            fill=255
        )
        
        # Background blur (softer)
        image2 = image1.convert("RGBA")
        background = image2.filter(ImageFilter.BoxBlur(18))
        background = ImageEnhance.Brightness(background).enhance(0.8)
        
        # Paste rounded image
        thumb_pos = (170, 90)
        center_thumb_rgba = center_thumb.convert("RGBA")
        background.paste(center_thumb_rgba, thumb_pos, mask)
        
        # Load fonts safely
        def safe_font(path, size):
            try:
                return ImageFont.truetype(path, size)
            except:
                return ImageFont.load_default()
                
        font = safe_font("AviaxMusic/assets/font.ttf", 30)
        font2 = safe_font("AviaxMusic/assets/font.ttf", 30)
        arial = safe_font("AviaxMusic/assets/font2.ttf", 30)
        
        # Draw text
        draw = ImageDraw.Draw(background)
        
        # Channel | Views
        draw.text((50, 565), f"{channel} | {views[:23]}", fill="white", font=arial)
        
        # Title
        title = textwrap.shorten(title, width=50, placeholder="...")
        draw.text((50, 600), title, fill="white", font=font, stroke_fill="white")
        
        # Start and End Time
        draw.text((50, 640), "00:25", fill="white", font=font2, stroke_width=1, stroke_fill="grey")
        draw.text((1150, 640), duration[:23], fill="white", font=font2, stroke_width=1, stroke_fill="white")
        
        # Duration bar with auto color
        draw.line((150, 660, 1130, 660), width=6, fill=bar_color)
        
        # Recreation Music text at right side
        rec_font = safe_font("OpusV/resources/font.ttf", 40)
        rec_text = "QUEEN X MUSIC"
        bbox = draw.textbbox((0, 0), rec_text, font=rec_font)
        rec_text_w = bbox[2] - bbox[0]
        rec_text_h = bbox[3] - bbox[1]
        rec_x = thumb_pos[0] + center_thumb.width + 25
        rec_y = thumb_pos[1] + (center_thumb.height // 2) - (rec_text_h // 2)
        draw.text((rec_x, rec_y), rec_text, fill="white", font=rec_font)
        
        # Save final image
        background.save(final_path, format="PNG")
        return final_path
        
    except Exception as e:
        print(f"Error in gen_thumb: {e}")
        return YOUTUBE_IMG_URL
        
