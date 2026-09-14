import streamlit as st
import requests


st.title("💻 Laptop Price Predictor")

st.write("Enter the laptop specifications to predict its price.")


# -----------------------------
# Laptop Information
# -----------------------------

company = st.selectbox(
    "Company",
    ["Dell", "HP", "Lenovo", "Asus", "Acer", "Apple", "MSI", "Other"]
)

type_name = st.selectbox(
    "Laptop Type",
    ["Notebook", "Ultrabook", "Gaming", "2 in 1 Convertible", "Workstation"]
)

inches = st.number_input(
    "Screen Size (inches)",
    min_value=10.0,
    max_value=25.0,
    value=15.6
)

ram = st.selectbox(
    "RAM (GB)",
    [2, 4, 8, 12, 16, 24, 32, 64]
)

opsys = st.selectbox(
    "Operating System",
    ["Windows 10", "Windows 7", "macOS", "Linux", "Chrome OS", "Other"]
)

weight = st.number_input(
    "Weight (kg)",
    min_value=0.5,
    max_value=6.0,
    value=2.0
)


# -----------------------------
# Display
# -----------------------------

screen_width = st.number_input(
    "Screen Width (pixels)",
    min_value=800,
    max_value=5000,
    value=1920
)

screen_height = st.number_input(
    "Screen Height (pixels)",
    min_value=600,
    max_value=4000,
    value=1080
)

ips = st.selectbox(
    "IPS Display",
    [0, 1]
)


# -----------------------------
# CPU
# -----------------------------

cpu_brand = st.selectbox(
    "CPU Brand",
    ["Intel", "AMD", "Samsung", "Other"]
)

cpu_speed = st.number_input(
    "CPU Speed (GHz)",
    min_value=0.5,
    max_value=5.0,
    value=2.5
)


# -----------------------------
# Storage
# -----------------------------

ssd = st.number_input(
    "SSD (GB)",
    min_value=0.0,
    value=256.0
)

hdd = st.number_input(
    "HDD (GB)",
    min_value=0.0,
    value=0.0
)

hybrid = st.number_input(
    "Hybrid Storage (GB)",
    min_value=0.0,
    value=0.0
)

flash = st.number_input(
    "Flash Storage (GB)",
    min_value=0.0,
    value=0.0
)


# -----------------------------
# GPU
# -----------------------------

gpu_brand = st.selectbox(
    "GPU Brand",
    ["Intel", "Nvidia", "AMD", "ARM", "Other"]
)


# -----------------------------
# Prediction
# -----------------------------

if st.button("Predict Price"):

    laptop_data = {

        "Company": company,
        "TypeName": type_name,
        "Inches": inches,
        "Ram": ram,
        "OpSys": opsys,
        "Weight": weight,

        "ScreenWidth": screen_width,
        "ScreenHeight": screen_height,
        "IPS": ips,

        "CpuBrand": cpu_brand,
        "CpuSpeed": cpu_speed,

        "SSD_GB": ssd,
        "HDD_GB": hdd,
        "Hybrid_GB": hybrid,
        "Flash_GB": flash,

        "GpuBrand": gpu_brand
    }


    response = requests.post(
        "http://127.0.0.1:8000/predict",
        json=laptop_data
    )


    if response.status_code == 200:

        result = response.json()

        st.success("Prediction successful!")

        st.metric(
            "Predicted Laptop Price",
            f"₹{result['predicted_price']:,.2f}"
        )

    else:

        st.error("Prediction failed")

        st.write(response.text)