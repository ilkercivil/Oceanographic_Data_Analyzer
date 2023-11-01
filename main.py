import tkinter as tk
import gsw
import matplotlib.pyplot as plt

# Tuzla Tersanesi'nin enlem ve boylam koordinatları
latitude_tuzla = 40.818099
longitude_tuzla = 29.296284

# Veri depolamak için boş listeler oluştur
depth_values = []
sigma_theta_values = []
temperature_values = []
salinity_values = []

# Veri giriş alanları
depth_entries = []
ppt_entries = []
temperature_entries = []

# create_data_entry_fields fonksiyonu
def create_data_entry_fields(frame, label_text, entry_variable):
    label = tk.Label(frame, text=label_text)
    label.pack(side=tk.LEFT)
    entry = tk.Entry(frame, textvariable=entry_variable)
    entry.pack(side=tk.LEFT)

# Hesaplama ve grafik güncelleme fonksiyonu
def calculate_sigma_theta():
    if not validate_data_entry_fields():
        return

    for i in range(20):
        depth_value = float(depth_entries[i].get())
        ppt_value = float(ppt_entries[i].get())
        temperature_value = float(temperature_entries[i].get())

        pressure = gsw.p_from_z(-1 * depth_value, latitude_tuzla)
        sigma_theta = gsw.sigma0(ppt_value, temperature_value)

        depth_values.append(depth_value)
        sigma_theta_values.append(sigma_theta)
        temperature_values.append(temperature_value)
        salinity_values.append(ppt_value)

    update_plots()

# Grafik güncelleme fonksiyonu
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

# Veri girişlerini doğrulama fonksiyonu
def validate_data_entry_fields():
    for i in range(20):
        depth_value = depth_entries[i].get()
        ppt_value = ppt_entries[i].get()
        temperature_value = temperature_entries[i].get()

        if not (depth_value and ppt_value and temperature_value):
            result_label.config(text="Lütfen tüm alanları doldurun.")
            return False

    return True

# root penceresini oluştur
root = tk.Tk()
root.title("Oceanographic Data Analyzer")

for i in range(20):
    frame = tk.Frame(root)
    frame.pack()

    depth_entry_variable = tk.StringVar()
    ppt_entry_variable = tk.StringVar()
    temperature_entry_variable = tk.StringVar()

    create_data_entry_fields(frame, "Derinlik {} (metre):".format(i + 1), depth_entry_variable)
    create_data_entry_fields(frame, "Tuzluluk {} (PPT):".format(i + 1), ppt_entry_variable)
    create_data_entry_fields(frame, "Sıcaklık {} (°C):".format(i + 1), temperature_entry_variable)

    depth_entries.append(depth_entry_variable)
    ppt_entries.append(ppt_entry_variable)
    temperature_entries.append(temperature_entry_variable)

# Hesapla düğmesi
calculate_button = tk.Button(root, text="Hesapla ve Grafikleri Göster", command=calculate_sigma_theta)
calculate_button.pack()

# Sonuç etiketi
result_label = tk.Label(root, text="Sigma-theta ve Derinlik Grafiği")
result_label.pack()

root.mainloop()
