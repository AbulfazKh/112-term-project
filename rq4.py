import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# 1. VERİYİ YÜKLE
# ---------------------------------------------------------
try:
    # Temiz veriyi yüklemeye çalışıyoruz
    df = pd.read_csv('cleaned_kidney_data.csv')
except FileNotFoundError:
    print("HATA: 'cleaned_kidney_data.csv' dosyası bulunamadı!")
    print("Lütfen temizlenmiş veri dosyasını bu kodun yanına taşıyın.")
    exit()

# ---------------------------------------------------------
# 2. VERİYİ HAZIRLA
# ---------------------------------------------------------
# CKD Status (İleri Seviye mi?) sütununu oluştur
df['CKD_Status'] = df['ckd_stage'].apply(
    lambda x: 'Advanced CKD' if x in ['Moderate', 'Severe'] else 'Early/No CKD'
)

# ---------------------------------------------------------
# 3. GRAFİĞİ ÇİZ
# ---------------------------------------------------------
sns.set_theme(style="whitegrid")
plt.figure(figsize=(10, 6))

# Boxplot
sns.boxplot(
    data=df,
    x='hypertension',
    y='age',
    hue='CKD_Status',
    palette="Set2"
)

# ---------------------------------------------------------
# 4. BAŞLIK VE ETİKETLER
# ---------------------------------------------------------
plt.title('Age Distribution by Hypertension and Kidney Disease Status', fontsize=14)
plt.xlabel('Hypertension Status', fontsize=12)
plt.ylabel('Age (Years)', fontsize=12)
plt.legend(title='Kidney Health')

sns.despine(trim=True)
plt.tight_layout()

# Resmi kaydet
plt.savefig('age_hypertension_ckd_analysis.png', dpi=300)

# HATALI OLAN SATIRIN DÜZELTİLMİŞ HALİ:
print("Grafik başarıyla oluşturuldu ve kaydedildi.")

plt.show()