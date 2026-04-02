# Konfigurasi Sumber Video Egg Detection
# ========================================

# Pilih sumber input video
# Opsi:
#   0 = Webcam Laptop (index 0)
#   1 = Webcam (index 1, jika ada multiple cameras)
#   'file' = File video (ubah nama file di bawah)
#   'rtsp' = IP Camera RTSP (ubah URL di bawah)

VIDEO_SOURCE = 0  # << UBAH INI SESUAI KEBUTUHAN

# Nama file video (jika VIDEO_SOURCE = 'file')
VIDEO_FILE = 'TELOR.mp4'

# URL RTSP untuk IP Camera (jika VIDEO_SOURCE = 'rtsp')
# Format: rtsp://username:password@ip_address:port/path
RTSP_URL = 'rtsp://admin:password@192.168.1.100:554/Streaming/Channels/101'

# Settings frame
FRAME_RESIZE_PERCENT = 40  # % ukuran frame untuk processing (lebih kecil = lebih cepat)
OFFSET_REF_LINES = 50      # Offset untuk garis referensi

# Deteksi telur (Updated - lebih toleran untuk real-time)
DISTANCE_THRESHOLD = 200
RADIUS_MIN = 2        # More tolerant (was 5)
RADIUS_MAX = 120      # Lebih besar (was 50)
AREA_MIN = 10         # Lebih kecil (was 100)
AREA_MAX = 30000      # Lebih besar (was 5000)
