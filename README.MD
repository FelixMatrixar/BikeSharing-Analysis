# Cara Menjalankan Dashboard

## Setup Environment

1. Buatlah environment menggunakan Conda dengan menjalankan perintah berikut:

   ```
   conda create --name main-ds python=3.9
   ```

2. Aktifkan environment yang telah dibuat dengan perintah:

   ```
   conda activate main-ds
   ```

3. Install paket-paket yang diperlukan dengan menggunakan pip:

   ```
   pip install -r requirements.txt
   ```

   atau alternatifnya :

   ```
   pip install altair jupyter matplotlib numpy pandas seaborn scipy streamlit babel
   ```

## Menjalankan Streamlit App

1. Untuk menjalankan aplikasi Streamlit, jalankan perintah berikut:
   ```
   streamlit run dashboard.py
   ```
