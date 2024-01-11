import streamlit as st
from PIL import Image
import tempfile
import urllib.parse
import os
from datetime import datetime
from PIL import ImageDraw
from PIL import ImageFont

st.title(":frame_with_picture: Date Stamper")

image_file = st.file_uploader("Upload Image", type=[
                              'png', 'jpeg', 'jpg'], accept_multiple_files=False)
if image_file is not None:
    file_details = {"FileName": image_file.name, "FileType": image_file.type}
    img = Image.open(image_file).convert('RGB')
    exif = img.getexif()
    exif_dict = exif.get_ifd(0x8769)
    if exif_dict is not None and 36867 in exif_dict:
        dt = datetime.strptime(
            exif_dict[36867], '%Y:%m:%d %H:%M:%S').date().strftime('%Y %m %d')
    else:
        dt = ""
    photo_date = st.text_input("Date: ", value=dt)
    with tempfile.NamedTemporaryFile(delete=True, suffix=".jpg") as tmp:
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('Arial.ttf', 48)
        draw.text((img.width-300, img.height-130), photo_date, font=font, fill='#E46C3B',
                  stroke_width=1,
                  stroke_fill='red')
        img.save(tmp.name, quality=80)
        st.download_button(
            label="JPEG : Download ",
            data=open(tmp.name, 'rb').read(),
            file_name=urllib.parse.quote(
                os.path.splitext(image_file.name)[0] + "_d.jpg"),
            mime="image/jpeg"
        )
        st.image(img)
