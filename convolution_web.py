import streamlit as st
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

st.set_page_config(page_title="Convolution (Mask Processing)", layout="wide")

st.title("🔧 Convolution (Mask Processing)")
st.write("Aplikasi untuk meningkatkan kualitas citra dengan berbagai filter convolution")

# =========================
# Fungsi Convolution
# =========================
def apply_convolution(image, filter_type, kernel_size):
    """
    Menerapkan berbagai filter convolution pada gambar
    """
    # Pastikan kernel size ganjil
    if kernel_size % 2 == 0:
        kernel_size += 1
    
    if filter_type == "Blur":
        kernel = np.ones((kernel_size, kernel_size), np.float32) / (kernel_size**2)
        result = cv2.filter2D(image, -1, kernel)
        
    elif filter_type == "Gaussian Blur":
        result = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
        
    elif filter_type == "Sharpen":
        kernel = np.array([
            [0, -1, 0],
            [-1, 5, -1],
            [0, -1, 0]
        ])
        result = cv2.filter2D(image, -1, kernel)
        
    elif filter_type == "Edge Detection":
        kernel = np.array([
            [-1, -1, -1],
            [-1, 8, -1],
            [-1, -1, -1]
        ])
        result = cv2.filter2D(image, -1, kernel)
        
    elif filter_type == "Emboss":
        kernel = np.array([
            [-2, -1, 0],
            [-1, 1, 1],
            [0, 1, 2]
        ])
        result = cv2.filter2D(image, -1, kernel)
        result = np.clip(result + 128, 0, 255).astype(np.uint8)
        
    elif filter_type == "Unsharp Masking":
        # Gaussian blur
        blurred = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
        # Unsharp mask
        result = cv2.addWeighted(image, 1.5, blurred, -0.5, 0)
        result = np.clip(result, 0, 255).astype(np.uint8)
        
    elif filter_type == "Laplacian":
        kernel = np.array([
            [0, -1, 0],
            [-1, 4, -1],
            [0, -1, 0]
        ])
        result = cv2.filter2D(image, -1, kernel)
        result = np.clip(result + 128, 0, 255).astype(np.uint8)
        
    elif filter_type == "Sobel X":
        kernel = np.array([
            [-1, 0, 1],
            [-2, 0, 2],
            [-1, 0, 1]
        ])
        result = cv2.filter2D(image, -1, kernel)
        result = np.clip(result + 128, 0, 255).astype(np.uint8)
        
    elif filter_type == "Sobel Y":
        kernel = np.array([
            [-1, -2, -1],
            [0, 0, 0],
            [1, 2, 1]
        ])
        result = cv2.filter2D(image, -1, kernel)
        result = np.clip(result + 128, 0, 255).astype(np.uint8)
    
    return result

def get_kernel_info(filter_type):
    """
    Mengembalikan informasi kernel untuk setiap filter
    """
    kernels = {
        "Blur": "Kernel rata-rata untuk penghalusan",
        "Gaussian Blur": "Kernel Gaussian untuk penghalusan natural",
        "Sharpen": np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]]),
        "Edge Detection": np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]]),
        "Emboss": np.array([[-2, -1, 0], [-1, 1, 1], [0, 1, 2]]),
        "Unsharp Masking": "Kombinasi gambar asli dan blur",
        "Laplacian": np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]]),
        "Sobel X": np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]),
        "Sobel Y": np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    }
    return kernels.get(filter_type, "Kernel khusus")

# =========================
# Sidebar Controls
# =========================
st.sidebar.title("🎛️ Pengaturan Filter")

# Upload Gambar
uploaded_file = st.sidebar.file_uploader(
    "📁 Upload Gambar", 
    type=["jpg", "png", "jpeg", "bmp"],
    help="Pilih gambar yang akan diproses"
)

if uploaded_file is not None:
    # Load image
    image = Image.open(uploaded_file)
    image = np.array(image)
    
    st.sidebar.success("✅ Gambar berhasil dimuat!")
    
    # Filter selection
    st.sidebar.subheader("🔍 Pilih Filter")
    filter_type = st.sidebar.selectbox(
        "Jenis Filter:",
        [
            "Blur",
            "Gaussian Blur", 
            "Sharpen",
            "Edge Detection",
            "Emboss",
            "Unsharp Masking",
            "Laplacian",
            "Sobel X",
            "Sobel Y"
        ],
        help="Pilih jenis filter convolution yang akan diterapkan"
    )
    
    # Kernel size (hanya untuk filter tertentu)
    if filter_type in ["Blur", "Gaussian Blur", "Unsharp Masking"]:
        kernel_size = st.sidebar.slider(
            "📏 Ukuran Kernel", 
            min_value=3, 
            max_value=15, 
            value=5, 
            step=2,
            help="Ukuran kernel (harus ganjil)"
        )
    else:
        kernel_size = 3  # Default untuk filter dengan kernel tetap
    
    # Intensity adjustment
    st.sidebar.subheader("⚙️ Penyesuaian")
    intensity = st.sidebar.slider(
        "🔆 Intensitas Efek",
        min_value=0.1,
        max_value=2.0,
        value=1.0,
        step=0.1,
        help="Mengatur intensitas efek filter"
    )
    
    # Process button
    if st.sidebar.button("🚀 Proses Gambar", type="primary"):
        with st.spinner("⏳ Memproses gambar..."):
            # Apply convolution
            result = apply_convolution(image, filter_type, kernel_size)
            
            # Apply intensity adjustment
            if intensity != 1.0:
                result = cv2.addWeighted(image, 1-intensity, result, intensity, 0)
                result = np.clip(result, 0, 255).astype(np.uint8)
            
            # Store in session state
            st.session_state.result = result
            st.session_state.original = image
            st.session_state.filter_used = filter_type
            st.session_state.kernel_size_used = kernel_size
        
        st.sidebar.success(f"✅ {filter_type} berhasil diterapkan!")

# =========================
# Main Content
# =========================
if uploaded_file is not None:
    
    # Display images
    st.subheader("🖼️ Hasil Pemrosesan")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**📷 Gambar Asli**")
        st.image(image)
    
    with col2:
        if 'result' in st.session_state:
            st.write(f"**✨ Hasil {st.session_state.filter_used}**")
            st.image(st.session_state.result)
        else:
            st.info("👆 Klik 'Proses Gambar' untuk melihat hasil")
    
    # Kernel Information
    if 'filter_used' in st.session_state:
        st.markdown("---")
        st.subheader("🔧 Informasi Kernel")
        
        col_info1, col_info2 = st.columns(2)
        
        with col_info1:
            kernel_info = get_kernel_info(st.session_state.filter_used)
            if isinstance(kernel_info, np.ndarray):
                st.write("**Matriks Kernel:**")
                st.code(str(kernel_info))
            else:
                st.write(f"**Deskripsi:** {kernel_info}")
        
        with col_info2:
            st.write("**Parameter yang Digunakan:**")
            st.write(f"- Filter: {st.session_state.filter_used}")
            st.write(f"- Ukuran Kernel: {st.session_state.kernel_size_used}x{st.session_state.kernel_size_used}")
            if intensity != 1.0:
                st.write(f"- Intensitas: {intensity}")
    
    # Histogram Analysis
    if 'result' in st.session_state:
        st.markdown("---")
        st.subheader("📊 Analisis Histogram")
        
        fig, axes = plt.subplots(1, 2, figsize=(12, 4))
        
        # Histogram Original
        if len(image.shape) == 3:
            colors = ['red', 'green', 'blue']
            labels = ['Red', 'Green', 'Blue']
            for i, (color, label) in enumerate(zip(colors, labels)):
                axes[0].hist(image[:,:,i].ravel(), bins=256, range=[0, 256], 
                           color=color, alpha=0.6, label=label)
            axes[0].legend()
        else:
            axes[0].hist(image.ravel(), bins=256, range=[0, 256], color='blue', alpha=0.7)
        
        axes[0].set_title('Histogram Gambar Asli')
        axes[0].set_xlabel('Intensitas Pixel')
        axes[0].set_ylabel('Frekuensi')
        axes[0].grid(True, alpha=0.3)
        
        # Histogram Result
        result_img = st.session_state.result
        if len(result_img.shape) == 3:
            for i, (color, label) in enumerate(zip(colors, labels)):
                axes[1].hist(result_img[:,:,i].ravel(), bins=256, range=[0, 256], 
                           color=color, alpha=0.6, label=label)
            axes[1].legend()
        else:
            axes[1].hist(result_img.ravel(), bins=256, range=[0, 256], color='orange', alpha=0.7)
        
        axes[1].set_title(f'Histogram Hasil {st.session_state.filter_used}')
        axes[1].set_xlabel('Intensitas Pixel')
        axes[1].set_ylabel('Frekuensi')
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        st.pyplot(fig)
        
        # Statistics
        st.subheader("📈 Statistik Gambar")
        
        col_stat1, col_stat2 = st.columns(2)
        
        with col_stat1:
            st.write("**Gambar Asli:**")
            if len(image.shape) == 3:
                mean_rgb = np.mean(image, axis=(0,1))
                std_rgb = np.std(image, axis=(0,1))
                st.write(f"- Mean RGB: [{mean_rgb[0]:.2f}, {mean_rgb[1]:.2f}, {mean_rgb[2]:.2f}]")
                st.write(f"- Std RGB: [{std_rgb[0]:.2f}, {std_rgb[1]:.2f}, {std_rgb[2]:.2f}]")
            else:
                st.write(f"- Mean: {np.mean(image):.2f}")
                st.write(f"- Std: {np.std(image):.2f}")
            st.write(f"- Min: {np.min(image)}")
            st.write(f"- Max: {np.max(image)}")
        
        with col_stat2:
            st.write("**Gambar Hasil:**")
            if len(result_img.shape) == 3:
                mean_rgb_result = np.mean(result_img, axis=(0,1))
                std_rgb_result = np.std(result_img, axis=(0,1))
                st.write(f"- Mean RGB: [{mean_rgb_result[0]:.2f}, {mean_rgb_result[1]:.2f}, {mean_rgb_result[2]:.2f}]")
                st.write(f"- Std RGB: [{std_rgb_result[0]:.2f}, {std_rgb_result[1]:.2f}, {std_rgb_result[2]:.2f}]")
            else:
                st.write(f"- Mean: {np.mean(result_img):.2f}")
                st.write(f"- Std: {np.std(result_img):.2f}")
            st.write(f"- Min: {np.min(result_img)}")
            st.write(f"- Max: {np.max(result_img)}")
    
    # Download Result
    if 'result' in st.session_state:
        st.markdown("---")
        
        # Convert to PIL for download
        result_pil = Image.fromarray(st.session_state.result)
        
        # Convert to bytes
        import io
        buf = io.BytesIO()
        result_pil.save(buf, format='PNG')
        byte_im = buf.getvalue()
        
        st.download_button(
            label="💾 Download Hasil",
            data=byte_im,
            file_name=f"hasil_{st.session_state.filter_used.lower().replace(' ', '_')}.png",
            mime="image/png"
        )

else:
    # Welcome screen
    st.info("👆 Silakan upload gambar di sidebar untuk memulai")
    
    # Information about filters
    st.subheader("🔍 Jenis-jenis Filter Convolution")
    
    filter_descriptions = {
        "🌫️ Blur": "Menghaluskan gambar dengan mengurangi noise dan detail",
        "🌟 Gaussian Blur": "Penghalusan dengan distribusi Gaussian yang natural",
        "⚡ Sharpen": "Mempertajam detail dan tepi pada gambar",
        "🔍 Edge Detection": "Mendeteksi dan menonjolkan tepi objek",
        "📐 Emboss": "Memberikan efek relief atau timbul pada gambar",
        "🎭 Unsharp Masking": "Teknik penajaman advanced untuk detail halus",
        "🔲 Laplacian": "Deteksi tepi dengan operator Laplacian",
        "↔️ Sobel X": "Deteksi tepi horizontal dengan operator Sobel",
        "↕️ Sobel Y": "Deteksi tepi vertikal dengan operator Sobel"
    }
    
    for filter_name, description in filter_descriptions.items():
        st.write(f"**{filter_name}:** {description}")

# =========================
# Footer Information
# =========================
st.markdown("---")
st.subheader("📖 Tentang Convolution")

with st.expander("Klik untuk melihat penjelasan"):
    st.markdown("""
    ### Convolution (Mask Processing)
    
    **Definisi:** Convolution adalah operasi matematika yang mengalikan setiap pixel dengan kernel (mask) 
    untuk menghasilkan efek tertentu pada gambar.
    
    **Cara Kerja:**
    1. **Kernel/Mask** - Matriks kecil (biasanya 3x3, 5x5, dll)
    2. **Sliding Window** - Kernel bergeser di seluruh gambar
    3. **Multiply & Sum** - Setiap posisi dikalikan dan dijumlahkan
    4. **Output** - Hasil menjadi nilai pixel baru
    
    **Kegunaan:**
    - **Blur** → Mengurangi noise, menghaluskan gambar
    - **Sharpen** → Meningkatkan ketajaman detail
    - **Edge Detection** → Mendeteksi batas objek
    - **Emboss** → Efek artistik relief
    - **Custom Effects** → Berbagai efek kreatif lainnya
    
    **Rumus Convolution:**
    ```
    Output(x,y) = Σ Σ Input(x+i, y+j) × Kernel(i,j)
    ```
    """)

st.caption("Program Convolution (Mask Processing) - Pengolahan Citra Digital")