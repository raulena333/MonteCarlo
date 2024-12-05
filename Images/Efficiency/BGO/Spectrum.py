import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab

# Set parameters for plot appearance
params = {
    'xtick.labelsize': 17,    
    'ytick.labelsize': 17,      
    'axes.titlesize': 18,
    'axes.labelsize': 18,
    'legend.fontsize': 16
}
pylab.rcParams.update(params)

# Input file path
input_file = "Images/Efficiency/BGO/spc-enddet-2.dat"

# Load data from the file
try:
    data = np.loadtxt(input_file, skiprows=7)  # Skip the header row
    energy, probability, error = data.T  # Transpose to extract columns
except Exception as e:
    print(f"Error loading data from {input_file}: {e}")
    exit()
    

E_peak = 2.5e4  # Peak energy (1e4 eV)
delta_E = 1000  # Energy range around the peak (in eV)

# Select the range around the peak
range_indices = np.where((energy >= (E_peak - delta_E)) & (energy <= (E_peak + delta_E)))

# Calculate the statistics for the peak region
peak_statistics = np.sum(probability[range_indices])

# Calculate the total statistics
total_statistics = np.sum(probability)

# Calculate the photopeak efficiency
photopeak_efficiency = peak_statistics / total_statistics

# Print the photopeak efficiency
print(f"Photopeak efficiency: {photopeak_efficiency:.4f}")


# Graficar el espectro y resaltar el área del fotopico
plt.plot(energy, probability, label='Espectro', color='b')
plt.fill_between(energy[range_indices], probability[range_indices], color='orange', alpha=0.5, label='Rango fotopico')
plt.title('Espectro de energía depositada')
plt.xlabel('Energía (eV)')
plt.ylabel('Probabilidad (1/eV)')
plt.legend()
plt.show()