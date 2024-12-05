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

# Paths for the two detectors
paths = ["BGO", "PVC"]

# List of energies corresponding to the files
energies = [1e4, 2.5e4, 5e4, 7.5e4, 1e5, 2.5e5, 5e5, 7.5e5, 1e6, 2.5e6, 5e6, 7.5e6, 1e7]

# Initialize a dictionary to store efficiencies for both detectors
photopeak_efficiencies = {path: [] for path in paths}

# Loop over both paths (BGO and PVC)
for path in paths:
    for i, E_peak in enumerate(energies):
        # Generate the file name
        input_file = f'Images/Efficiency/{path}/spc-enddet-{i+1}.dat'

        try:
            # Load data from the file
            data = np.loadtxt(input_file, skiprows=7)  # Skip the header row
            energy, probability, error = data.T  # Transpose to extract columns

            # Define the energy range around the peak
            delta_E = 1000  # Energy range around the peak (in eV)

            # Select the range around the peak
            range_indices = np.where((energy >= (E_peak - delta_E)) & (energy <= (E_peak + delta_E)))

            # Calculate the statistics for the peak region
            peak_statistics = np.sum(probability[range_indices])

            # Calculate the total statistics
            total_statistics = np.sum(probability)

            # Calculate the photopeak efficiency
            photopeak_efficiency = peak_statistics / total_statistics

            # Append the efficiency to the list for the current detector
            photopeak_efficiencies[path].append(photopeak_efficiency)

        except Exception as e:
            print(f"Error processing file {input_file}: {e}")
            photopeak_efficiencies[path].append(np.nan)  # Append NaN if there is an error with the file

# Plot the photopeak efficiency vs. energy for both detectors
plt.figure(figsize=(10, 7))
for path in paths:
    plt.scatter(energies, photopeak_efficiencies[path], marker='o', label=f'{path} Detector')

plt.xscale('log')  # Log scale for the energy axis
plt.yscale('linear')
plt.xlabel('Energia (eV)')
plt.ylabel('Eficiencia del Fotopico')
plt.legend()
plt.savefig("EfficencyPlot.pdf")
plt.show()

# Print the efficiencies for each energy and detector
for path in paths:
    print(f"Efficiencies for {path} Detector:")
    for i, efficiency in enumerate(photopeak_efficiencies[path]):
        print(f"  Energy: {energies[i]:.1e} eV, Photopeak Efficiency: {efficiency:.4f}")


