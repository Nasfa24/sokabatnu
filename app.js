/**
 * =========================================================================
 * ECMS 2029 - GLOBAL APP CONTROLLER (PWA & NETWORK MANAGER)
 * =========================================================================
 * Menangani siklus hidup Progressive Web App (PWA), instalasi, 
 * dan mendeteksi status sinyal internet (Offline/Online) secara real-time.
 * =========================================================================
 */

// 1. REGISTRASI SERVICE WORKER (PWA)
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('sw.js')
      .then(registration => {
        console.log('✅ Sistem PWA Aktif di scope:', registration.scope);
      })
      .catch(error => {
        console.error('❌ Gagal memuat PWA:', error);
      });
  });
}

// 2. SISTEM DETEKSI SINYAL INTERNET (REAL-TIME)
window.addEventListener('offline', () => {
  if (typeof Swal !== 'undefined') {
    Swal.fire({
      toast: true,
      position: 'top',
      icon: 'error',
      title: 'Koneksi Terputus!',
      text: 'HP Anda sedang offline. Beberapa fitur mungkin tertahan.',
      showConfirmButton: false,
      timer: 4000,
      background: '#fffbf2',
      color: '#d97706'
    });
  }
});

window.addEventListener('online', () => {
  if (typeof Swal !== 'undefined') {
    Swal.fire({
      toast: true,
      position: 'top',
      icon: 'success',
      title: 'Sinyal Kembali!',
      text: 'Sistem terhubung kembali ke satelit pusat.',
      showConfirmButton: false,
      timer: 3000
    });
  }
});

// 3. PROTEKSI PULL-TO-REFRESH DI HP (Mencegah Reload Tidak Sengaja)
document.body.style.overscrollBehaviorY = 'contain';