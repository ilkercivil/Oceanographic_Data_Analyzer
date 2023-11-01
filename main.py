import tkinter as tk
import gsw
import matplotlib.pyplot as plt

# Veri depolamak için boş listeler oluştur
depth_values = []
sigma_theta_values = []
temperature_values = []
salinity_values = []

# Tuzla Tersanesi'nin enlem ve boylam koordinatları
latitude_tuzla = 40.818099
longitude_tuzla = 29.296284


# Sigma-theta hesaplama fonksiyonu
def calculate_sigma_theta():
    try:
        depth_value = float(depth_entry.get())
        salinity_value = float(salinity_entry.get())
        temperature_value = float(temperature_entry.get())

        # Basınç değerini hesapla, Tuzla Tersanesi'nin koordinatlarını kullanarak
        pressure = gsw.p_from_z(-1 * depth_value, latitude_tuzla)

        # Sigma-theta hesaplama
        sigma_theta = gsw.sigma0(salinity_value, temperature_value)

        # Veriyi listelere ekle
        depth_values.append(depth_value)
        sigma_theta_values.append(sigma_theta)
        temperature_values.append(temperature_value)
        salinity_values.append(salinity_value)

        # Grafiği güncelle
        update_plots()
    except ValueError:
        result_label.config(text="Lütfen geçerli değerler girin.")


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

# Derinlik giriş alanı
depth_label = tk.Label(root, text="Derinlik (metre):")
depth_label.pack()
depth_entry = tk.Entry(root)
depth_entry.pack()

# Tuzluluk giriş alanı
salinity_label = tk.Label(root, text="Tuzluluk (PSU):")
salinity_label.pack()
salinity_entry = tk.Entry(root)
salinity_entry.pack()

# Sıcaklık giriş alanı
temperature_label = tk.Label(root, text="Sıcaklık (°C):")
temperature_label.pack()
temperature_entry = tk.Entry(root)
temperature_entry.pack()

# Hesapla düğmesi
calculate_button = tk.Button(root, text="Hesapla ve Grafikleri Göster", command=calculate_sigma_theta)
calculate_button.pack()

# Sonuç etiketi
result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()
