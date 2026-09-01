/**
 * =========================================================================
 * CORE ENGINE (Mobile Protection & Dynamic Alerts)
 * =========================================================================
 */

// Ganti dengan URL Web App dari Google Apps Script setelah di-deploy
const GAS_API_URL = "URL_WEB_APP_GAS_ANDA_DISINI"; 

const AppCore = {
  /**
   * Fungsi untuk menampilkan notifikasi dinamis
   */
  showAlert: function(type, title, text) {
    let iconColor = type === 'success' ? 'var(--primary)' : 
                    type === 'warning' ? 'var(--accent-1)' : 
                    type === 'error' ? 'var(--danger)' : 'var(--accent-2)';

    return Swal.fire({
      icon: type,
      title: title,
      html: text,
      confirmButtonColor: 'var(--primary)',
      background: 'var(--bg-color)',
      color: 'var(--text-color)',
      backdrop: `rgba(0,0,0,0.6)`
    });
  },

  /**
   * Fungsi untuk meminta konfirmasi sebelum eksekusi aksi kritis
   */
  confirmAction: function(title, text, confirmText, callback) {
    Swal.fire({
      title: title,
      text: text,
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: 'var(--accent-1)',
      cancelButtonColor: '#6c757d',
      confirmButtonText: confirmText,
      cancelButtonText: 'Batal'
    }).then((result) => {
      if (result.isConfirmed) {
        callback();
      }
    });
  },

  /**
   * Wrapper Fetch API dengan penguncian tombol otomatis (Anti Double-Tap)
   */
  fetchAPI: async function(buttonId, payload, successMessage) {
    const btn = document.getElementById(buttonId);
    if (!btn || btn.classList.contains('is-loading')) return; // Kebal jika sedang diproses

    // Kunci tombol & ubah UI
    const originalText = btn.innerHTML;
    btn.classList.add('is-loading');
    btn.innerHTML = '⏳ Memproses...';

    try {
      const response = await fetch(GAS_API_URL, {
        method: "POST",
        body: JSON.stringify(payload)
      });
      
      const data = await response.json();
      
      if (data.status === "success") {
        this.showAlert('success', 'Berhasil!', successMessage || data.message);
      } else {
        this.showAlert('error', 'Gagal', data.message);
      }
    } catch (error) {
      this.showAlert('error', 'Koneksi Terputus', 'Periksa sinyal internet Anda.');
    } finally {
      // Kembalikan tombol ke keadaan semula
      btn.classList.remove('is-loading');
      btn.innerHTML = originalText;
    }
  },

  /**
   * Fitur Refresh Page (Hard Reload)
   */
  refreshApp: function() {
    window.location.reload(true);
  },

  /**
   * Fitur Clear Cache Global
   */
  clearCache: function() {
    this.confirmAction(
      'Bersihkan Cache?',
      'Aksi ini akan menghapus memori sementara aplikasi di HP Anda.',
      'Ya, Bersihkan!',
      () => {
        localStorage.clear();
        sessionStorage.clear();
        this.showAlert('success', 'Cache Bersih', 'Sistem terasa lebih ringan sekarang.').then(() => {
          window.location.reload(true);
        });
      }
    );
  }
};