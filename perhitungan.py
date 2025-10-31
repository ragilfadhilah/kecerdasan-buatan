import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# --- Variabel Input dan Output ---
permintaan = ctrl.Antecedent(np.arange(0, 5001, 1), 'permintaan')
persediaan = ctrl.Antecedent(np.arange(0, 1001, 1), 'persediaan')
produksi = ctrl.Consequent(np.arange(0, 8001, 1), 'produksi')

# --- Fungsi Keanggotaan Permintaan ---
permintaan['turun'] = fuzz.trapmf(permintaan.universe, [0, 0, 1000, 3000])
permintaan['naik'] = fuzz.trapmf(permintaan.universe, [1000, 3000, 5000, 5000])

# --- Fungsi Keanggotaan Persediaan ---
persediaan['sedikit'] = fuzz.trapmf(persediaan.universe, [0, 0, 200, 400])
persediaan['sedang'] = fuzz.trimf(persediaan.universe, [200, 400, 800])
persediaan['banyak'] = fuzz.trapmf(persediaan.universe, [400, 800, 1000, 1000])

# --- Fungsi Keanggotaan Produksi ---
produksi['berkurang'] = fuzz.trapmf(produksi.universe, [0, 0, 2000, 7000])
produksi['bertambah'] = fuzz.trapmf(produksi.universe, [2000, 7000, 8000, 8000])

# --- Aturan Fuzzy ---
rule1 = ctrl.Rule(permintaan['turun'] & persediaan['banyak'], produksi['berkurang'])
rule2 = ctrl.Rule(permintaan['turun'] & persediaan['sedang'], produksi['berkurang'])
rule3 = ctrl.Rule(permintaan['turun'] & persediaan['sedikit'], produksi['bertambah'])
rule4 = ctrl.Rule(permintaan['naik'] & persediaan['banyak'], produksi['berkurang'])
rule5 = ctrl.Rule(permintaan['naik'] & persediaan['sedang'], produksi['bertambah'])
rule6 = ctrl.Rule(permintaan['naik'] & persediaan['sedikit'], produksi['bertambah'])

# --- Sistem Kontrol Fuzzy ---
produksi_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6])
produksi_simulasi = ctrl.ControlSystemSimulation(produksi_ctrl)

# --- Input Nilai (bisa diganti sesuai soal) ---
produksi_simulasi.input['permintaan'] = 2000
produksi_simulasi.input['persediaan'] = 700

# --- Jalankan Simulasi ---
produksi_simulasi.compute()

# --- Hasil ---
print(f"Hasil Produksi (defuzzifikasi): {produksi_simulasi.output['produksi']:.2f} kemasan")

# --- (Opsional) Tampilkan Grafik ---
produksi.view(sim=produksi_simulasi)
