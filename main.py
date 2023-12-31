import tkinter as tk
from PIL import Image, ImageTk
import gsw
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Tuzla Tersanesi'nin enlem ve boylam koordinatları
latitude_tuzla = 40.818099
longitude_tuzla = 29.296284

# Veri depolamak için boş listeler oluştur
depth_values = []
sigma_theta_values = []
temperature_values = []
salinity_values = []

# Veri giriş alanları
data_entries = []

# create_data_entry_fields fonksiyonu
def create_data_entry_fields(frame, label_text, entry_variable):
    label = tk.Label(frame, text=label_text)
    label.pack(side=tk.LEFT)
    entry = tk.Entry(frame, textvariable=entry_variable)
    entry.pack(side=tk.LEFT)

# Tabakalaşma Derinliği Hesaplama İşlevi
def calculate_stratification_depth_internal(temperature, salinity, depth):
    density = gsw.rho(temperature, salinity, depth)
    stratification_depth = None
    for i in range(1, len(depth)):
        if abs(density[i] - density[0]) > 0.1:  # Örnek bir eşik değeri
            stratification_depth = depth[i]
            break
    return stratification_depth

# Sonuçları Excel dosyasına kaydetmek için işlev
def save_to_excel():
    if depth_values:
        data = {
            "Derinlik (metre)": depth_values,
            "Sigma-theta (σθ)": sigma_theta_values,
            "Sıcaklık (°C)": temperature_values,
            "Tuzluluk (PPT)": salinity_values
        }

        df = pd.DataFrame(data)
        df.to_excel("oceanographic_data.xlsx", index=False)
        result_label.config(text="Veriler başarıyla Excel dosyasına kaydedildi.")
    else:
        result_label.config(text="Kaydedilecek veri yok.")

# Veri girişi ekranı açma işlevi
def open_data_entry():
    data_frame = tk.Frame(root)
    data_frame.pack()

    data_entry_variable_depth = tk.StringVar()
    data_entry_variable_ppt = tk.StringVar()
    data_entry_variable_temperature = tk.StringVar()

    create_data_entry_fields(data_frame, "Derinlik (metre):", data_entry_variable_depth)
    create_data_entry_fields(data_frame, "Tuzluluk (PPT):", data_entry_variable_ppt)
    create_data_entry_fields(data_frame, "Sıcaklık (°C):", data_entry_variable_temperature)

    data_entries.append((data_entry_variable_depth, data_entry_variable_ppt, data_entry_variable_temperature))

# Hesapla düğmesi işlevi
def calculate_sigma_theta():
    depth_values.clear()
    sigma_theta_values.clear()
    temperature_values.clear()
    salinity_values.clear()

    for entry in data_entries:
        depth_entry, ppt_entry, temperature_entry = entry
        depth = depth_entry.get().strip()
        ppt = ppt_entry.get().strip()
        temperature = temperature_entry.get().strip()

        if depth and ppt and temperature:
            try:
                depth_value = float(depth)
                ppt_value = float(ppt)
                temperature_value = float(temperature)

                pressure = gsw.p_from_z(-1 * depth_value, latitude_tuzla)
                sigma_theta = gsw.sigma0(ppt_value, temperature_value)

                depth_values.append(depth_value)
                sigma_theta_values.append(sigma_theta)
                temperature_values.append(temperature_value)
                salinity_values.append(ppt_value)
            except ValueError:
                result_label.config(text="Geçerli verileri girin.")
                return
        else:
            result_label.config(text="Lütfen tüm alanları doldurun.")
            return

    update_plots()

# Grafik güncelleme işlevi
def update_plots():
    plt.figure(figsize=(12, 6))

    # Derinlik ve Sigma-theta grafiği
    plt.subplot(131)
    plt.plot(sigma_theta_values, depth_values)
    plt.xlabel('Sigma-theta (σθ)')
    plt.ylabel('Derinlik (metre)')
    plt.title('Derinlik ve Sigma-theta Grafiği')

    # Derinlik ve Sıcaklık grafiği
    plt.subplot(132)
    plt.plot(temperature_values, depth_values)
    plt.xlabel('Sıcaklık (°C)')
    plt.ylabel('Derinlik (metre)')
    plt.title('Derinlik ve Sıcaklık Grafiği')

    # Derinlik ve Tuzluluk grafiği
    plt.subplot(133)
    plt.plot(salinity_values, depth_values)
    plt.xlabel('Tuzluluk (PPT)')
    plt.ylabel('Derinlik (metre)')
    plt.title('Derinlik ve Tuzluluk Grafiği')

    plt.tight_layout()
    plt.show()

# Tabakalaşma Değerlendir düğmesi
def evaluate_stratification():
    if depth_values and temperature_values and salinity_values:
        depth_profile = np.array(depth_values)
        temperature_profile = np.array(temperature_values)
        salinity_profile = np.array(salinity_values)

        stratification_depth = calculate_stratification_depth_internal(temperature_profile, salinity_profile, depth_profile)

        if stratification_depth is not None:
            result_label.config(text=f"Tabakalaşma derinliği: {stratification_depth:.2f} metre")
        else:
            result_label.config(text="Tabakalaşma yok veya belirli bir derinlikte başlamış değil.")
    else:
        result_label.config(text="Hesaplamak için veri yok.")

# root penceresini oluştur
root = tk.Tk()
root.title("Oceanographic Data Analyzer")

# Açılış ekranının boyutunu ayarla
root.geometry("800x600")

# Veri girişi ekranı açma düğmesi
open_data_entry_button = tk.Button(root, text="Yeni Veri Ekle", command=open_data_entry)
open_data_entry_button.pack()

# Hesapla düğmesi
calculate_button = tk.Button(root, text="Hesapla ve Grafikleri Göster", command=calculate_sigma_theta)
calculate_button.pack()

# Hesapla ve kaydet düğmesi
save_button = tk.Button(root, text="Hesapla ve Excel'e Kaydet", command=save_to_excel)
save_button.pack()

# Tabakalaşma Değerlendir düğmesi
evaluate_stratification_button = tk.Button(root, text="Tabakalaşma Değerlendir", command=evaluate_stratification)
evaluate_stratification_button.pack()

# Sonuç etiketi
result_label = tk.Label(root, text="Sigma-theta ve Derinlik Grafiği")
result_label.pack()

# Logo dosyasını yükleyin ve tkinter için uygun hale getirin
logo_image = Image.open("haliclogo.png")
# Logo'yu %50 küçült
logo_image = logo_image.resize((logo_image.width // 2, logo_image.height // 2))
logo = ImageTk.PhotoImage(logo_image)

# Logo görüntüsünü bir Label widget'e yerleştirin ve sağ alt köşeye yerleştirin
logo_label = tk.Label(root, image=logo)
logo_label.pack(side="bottom", anchor="se")

root.mainloop()
