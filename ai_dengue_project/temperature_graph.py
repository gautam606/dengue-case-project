import matplotlib.pyplot as plt

days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
temperature = [28, 30, 27, 32, 31, 29, 26]

plt.plot(days, temperature, marker='o', linestyle='-', color='blue', linewidth=2, markersize=8)
plt.title('Temperature Variation Over Days', fontsize=16, fontweight='bold')
plt.xlabel('Days', fontsize=12)
plt.ylabel('Temperature (°C)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()
