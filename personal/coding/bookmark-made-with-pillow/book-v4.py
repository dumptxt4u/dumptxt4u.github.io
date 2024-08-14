from PIL import Image, ImageDraw, ImageFont
import os
from PyPDF2 import PdfFileReader, PdfFileWriter
from pdf2image import convert_from_path

def split_pdf_to_images(pdf_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    images = convert_from_path(pdf_path)
    for i, image in enumerate(images):
        image_path = os.path.join(output_folder, f'page_{i + 1}.png')
        image.save(image_path, 'PNG')
        print(f'Saved {image_path}')

def add_text(draw, text, font, fill_color, position):
    draw.text(position, text, font=font, fill=fill_color)

def add_white_rectangle_with_text(image_path):
    with Image.open(image_path) as img:
        width, height = img.size
        rect_height = int(height * 0.0675)
        rect_y = height - rect_height
        line_y = height - int(height * 0.05)  # 20% above the bottom
        text_y = height - int(height * 0.060)  # 8% above the bottom
        
        # Create drawing context
        draw = ImageDraw.Draw(img)
        
        # Add white rectangle
        draw.rectangle([(0, rect_y), (width, height)], fill="white")
        
        # Draw bold line
       # draw.line([(100, rect_y), (width-100, rect_y)], fill="black", width=10)
        
        # Load a font
        font_path = "Arimo-Regular.ttf" # Adjust the font path as needed
        font_size = 42
        font = ImageFont.truetype(font_path, font_size)
        
        # Add text
        text = "Trivandrum Maths and Computer Tuition - 9037030309 , 0471 2963471 "
        #font = ImageFont.truetype("/home/jack/fonts/DejaVuSans-Bold.ttf", 41)
        left, top, right, bottom = font.getbbox("pharetra. purus")
        width = right - left
        height = bottom - top
        text_width, text_height = width , height
        #text_width, text_height = font.getsize(text)  # Use getsize method of

        #ImageFont
        text_x = ( text_width) // 2  # Center the text horizontally
        add_text(draw, text, font, "black", (text_x, text_y))
        
        img.save(image_path)
        print(f'Updated {image_path}')

def images_to_pdf(images_folder, output_pdf_path):
    images = [Image.open(os.path.join(images_folder, f)) for f in sorted(os.listdir(images_folder)) if f.endswith('.png')]
    if images:
        images[0].save(output_pdf_path, save_all=True, append_images=images[1:])
        print(f'Saved {output_pdf_path}')

def process_pdf(pdf_path, output_folder, output_pdf_path):
    images_folder = os.path.join(output_folder, 'images')
    split_pdf_to_images(pdf_path, images_folder)

    for filename in os.listdir(images_folder):
        if filename.endswith('.png'):
            image_path = os.path.join(images_folder, filename)
            add_white_rectangle_with_text(image_path)

    images_to_pdf(images_folder, output_pdf_path)

if __name__ == "__main__":
    input_pdf = 'input.pdf'  # Replace with your input PDF file path
    output_folder = 'output'  # Folder to store intermediate files
    output_pdf = 'output/processed_output.pdf'  # Output PDF file path

    process_pdf(input_pdf, output_folder, output_pdf)

