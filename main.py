import tkinter as tk
import gsw
import matplotlib.pyplot as plt

# Veri depolamak için boş listeler oluştur
depth_values = []
sigma_theta_values = []
temperature_values = []
salinity_values = []

# Sigma-theta hesaplama fonksiyonu
def calculate_sigma_theta():
    depth_values.clear()
    sigma_theta_values.clear()
    temperature_values.clear()
    salinity_values.clear()

    for i in range(20):
        try:
            depth_value = float(depth_entries[i].get())
            salinity_value = float(salinity_entries[i].get())
            temperature_value = float(temperature_entries[i].get())

            pressure = gsw.p_from_z(-1 * depth_value)
            sigma_theta = gsw.sigma0(salinity_value, temperature_value)

            depth_values.append(depth_value)
            sigma_theta_values.append(sigma_theta)
            temperature_values.append(temperature_value)
            salinity_values.append(salinity_value)

        except ValueError:
            result_label.config(text="Lütfen geçerli değerler girin.")
            return

    update_plots()

# Grafiği güncelleyen fonksiyon
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
    plt.xlabel('Tuzluluk (PSU)')
    plt.ylabel('Derinlik (metre)')
    plt.title('Derinlik ve Tuzluluk Grafiği')

    plt.tight_layout()
    plt.show()

# Tkinter penceresini oluştur
root = tk.Tk()
root.title("Oceanographic Data Analyzer")

# Veri giriş alanları
depth_entries = []
salinity_entries = []
temperature_entries = []

for i in range(20):
    frame = tk.Frame(root)
    frame.pack()

    depth_label = tk.Label(frame, text=f"Derinlik {i + 1} (metre):")
    depth_label.pack(side=tk.LEFT)
    depth_entry = tk.Entry(frame)
    depth_entry.pack(side=tk.LEFT)
    depth_entries.append(depth_entry)

    salinity_label = tk.Label(frame, text=f"Tuzluluk {i + 1} (PSU):")
    salinity_label.pack(side=tk.LEFT)
    salinity_entry = tk.Entry(frame)
    salinity_entry.pack(side=tk.LEFT)
    salinity_entries.append(salinity_entry)

    temperature_label = tk.Label(frame, text=f"Sıcaklık {i + 1} (°C):")
    temperature_label.pack(side=tk.LEFT)
    temperature_entry = tk.Entry(frame)
    temperature_entry.pack(side=tk.LEFT)
    temperature_entries.append(temperature_entry)

# Hesapla düğmesi
calculate_button = tk.Button(root, text="Hesapla ve Grafikleri Göster", command=calculate_sigma_theta)
calculate_button.pack()

# Sonuç etiketi
result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()
