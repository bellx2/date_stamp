import streamlit as st
import tempfile
import urllib.parse
import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

st.title(":frame_with_picture: 日付スタンプツール")
st.write("画像に日付を追加するWebツールです")

base_width = 1280  # 基準となる幅
base_height = 960  # 基準となる高さ
base_font_size = 36  # 基準となるフォントサイズ

col1, ressult_col = st.columns(2)

with col1:
    image_file = st.file_uploader("画像アップロード", type=[
        'png', 'jpeg', 'jpg'], accept_multiple_files=False)
    if image_file is not None:
        file_details = {"FileName": image_file.name,
                        "FileType": image_file.type}
        img = Image.open(image_file).convert('RGB')
        width, height = img.size
        exif = img.getexif()
        exif_dict = exif.get_ifd(0x8769)
        if exif_dict is not None and 36867 in exif_dict:
            dt = datetime.strptime(
                exif_dict[36867], '%Y:%m:%d %H:%M:%S').date().strftime('%Y %m %d')
        else:
            dt = datetime.now().date().strftime('%Y %m %d')
        photo_date = st.text_input("日付: ", value=dt)
        with tempfile.NamedTemporaryFile(delete=True, suffix=".jpg") as tmp:
            scaling_factor = (width / base_width + height / base_height) / 2
            font_size = int(base_font_size * scaling_factor)
            font = ImageFont.truetype('./arial.ttf', font_size)

            draw = ImageDraw.Draw(img)

            bbox = font.getbbox(photo_date)
            text_width = bbox[2] - bbox[0]  # 幅
            text_height = bbox[3] - bbox[1]  # 高さ

            margin = 10
            draw.text((img.width-text_width-font_size, img.height-text_height*2), photo_date, font=font, fill='#E46C3B',
                      stroke_width=1,
                      stroke_fill='red')
            img.save(tmp.name, quality=80)
            with ressult_col:
                st.image(img, caption="右クリックで画像保存", use_column_width=True)
                st.download_button(
                    label="JPEGダウンロード",
                    data=open(tmp.name, 'rb').read(),
                    file_name=urllib.parse.quote(
                        os.path.splitext(image_file.name)[0]+'.JPG'),
                    mime="image/jpeg"
                )
