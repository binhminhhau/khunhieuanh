import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

st.set_page_config(page_title="Studio Xử Lý Ảnh Python", layout="wide")

st.title("🛠️ Studio Xử Lý & Khử Nhiễu Ảnh Thông Minh")
st.write("Tải ảnh của bạn lên, tùy chỉnh bộ lọc và chọn định dạng muốn tải về.")



def sharpen_image(img_bgr, strength=1.0):
    """Làm nét ảnh bằng thuật toán Unsharp Masking."""

    blurred = cv2.GaussianBlur(img_bgr, (0, 0), 1.0)
    
  
    sharpened = cv2.addWeighted(img_bgr, 1.0 + strength, blurred, -strength, 0)

    return np.clip(sharpened, 0, 255).astype(np.uint8)

uploaded_file = st.file_uploader("Chọn một bức ảnh (JPG, PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    original_image_pil = Image.open(uploaded_file)
    img_array = np.array(original_image_pil)
    

    if img_array.shape[-1] == 4:
        img_array = cv2.cvtColor(img_array, cv2.COLOR_RGBA2RGB)
    
    img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

    st.sidebar.header("⚙️ Cài đặt bộ lọc")
    

    operation = st.sidebar.radio("Chọn thao tác chính:", ["Khử Nhiễu", "Làm Nét"])
    
    processed_bgr = None
    
    if operation == "Khử Nhiễu":
        st.sidebar.subheader("Tùy chỉnh Khử Nhiễu")
        h_val = st.sidebar.slider("Độ mạnh của bộ lọc (h):", min_value=1, max_value=30, value=10, 
                                 help="Giá trị càng cao khử nhiễu càng mạnh, nhưng ảnh có thể bị mờ đi.")

        with st.spinner("Đang khử nhiễu..."):
            processed_bgr = cv2.fastNlMeansDenoisingColored(img_bgr, None, h_val, h_val, 7, 21)
            
    elif operation == "Làm Nét":
        st.sidebar.subheader("Tùy chỉnh Làm Nét")
        sharp_strength = st.sidebar.slider("Độ sắc nét:", min_value=0.0, max_value=5.0, value=1.5, step=0.1,
                                         help="Kéo sang phải để tăng độ sắc nét của viền vật thể.")
        

        with st.spinner("Đang làm nét..."):
            processed_bgr = sharpen_image(img_bgr, strength=sharp_strength)

 
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🖼️ Ảnh gốc")
        st.image(original_image_pil, use_container_width=True)
        
    with col2:
        st.subheader(f"✨ Kết quả {operation}")
       
        processed_rgb = cv2.cvtColor(processed_bgr, cv2.COLOR_BGR2RGB)
        processed_image_pil = Image.fromarray(processed_rgb)
        st.image(processed_image_pil, use_container_width=True)

    st.markdown("---")
    st.subheader("📥 Tải kết quả về máy")
    
    col_fmt, col_btn = st.columns([1, 2])
    
    with col_fmt:
        file_format = st.selectbox("Chọn định dạng:", [".png", ".jpg", ".pdf"])
    
    with col_btn:
        st.write("") 
        st.write("")

        base_name = "ket_qua_xu_ly"
        final_filename = f"{base_name}{file_format}"

        buf = io.BytesIO()
        
        with st.spinner(f"Chuyển đổi sang {file_format}..."):
            if file_format == ".png":
                processed_image_pil.save(buf, format="PNG")
                mime_type = "image/png"
                
            elif file_format == ".jpg":

                if processed_image_pil.mode in ('RGBA', 'LA'):
                    background = Image.new('RGB', processed_image_pil.size, (255, 255, 255))
                    background.paste(processed_image_pil, mask=processed_image_pil.split()[3]) 
                    background.save(buf, format="JPEG", quality=90) 
                else:
                    processed_image_pil.convert('RGB').save(buf, format="JPEG", quality=90)
                mime_type = "image/jpeg"
                
            elif file_format == ".pdf":
                processed_image_pil.convert('RGB').save(buf, format="PDF")
                mime_type = "application/pdf"

        byte_im = buf.getvalue()

        st.download_button(
            label=f"📥 Bấm để tải {file_format.upper()}",
            data=byte_im,
            file_name=final_filename,
            mime=mime_type,
            type="primary"
        )