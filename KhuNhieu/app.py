import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io


st.set_page_config(page_title="Web Khử Nhiễu Ảnh", layout="centered")

st.title("🛠️ Ứng dụng Web Khử Nhiễu Ảnh")
st.write("Tải ảnh của bạn lên và điều chỉnh thanh trượt để loại bỏ nhiễu hạt (noise) trên ảnh.")


uploaded_file = st.file_uploader("Chọn một bức ảnh (JPG, PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    original_image = Image.open(uploaded_file)
    img_array = np.array(original_image)
    
    img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

    st.subheader("🖼️ Ảnh gốc")
    st.image(original_image, use_container_width=True)

    st.markdown("---")
    st.subheader("⚙️ Tùy chỉnh mức độ khử nhiễu")
    
    h_val = st.slider("Độ mạnh của bộ lọc (h):", min_value=1, max_value=30, value=10, 
                      help="Giá trị càng cao khử nhiễu càng mạnh, nhưng ảnh có thể bị mờ đi.")

    if st.button("Bắt đầu khử nhiễu", type="primary"):
        with st.spinner("Đang xử lý ảnh, vui lòng chờ..."):
            denoised_bgr = cv2.fastNlMeansDenoisingColored(
                img_bgr, None, h_val, h_val, 7, 21
            )
            
            denoised_rgb = cv2.cvtColor(denoised_bgr, cv2.COLOR_BGR2RGB)
            denoised_image = Image.fromarray(denoised_rgb)

            st.subheader("✨ Ảnh đã khử nhiễu")
            st.image(denoised_image, use_container_width=True)

            buf = io.BytesIO()
            denoised_image.save(buf, format="PNG")
            byte_im = buf.getvalue()

            st.download_button(
                label="📥 Tải ảnh kết quả về máy",
                data=byte_im,
                file_name="anh_da_khu_nhieu.png",
                mime="image/png"
            )