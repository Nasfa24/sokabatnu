/**
 * =========================================================================
 * SOKABAT NU 2029 - GLOBAL APP CONTROLLER (PWA & NETWORK MANAGER)
 * =========================================================================
 */

// KUNCI INI HARUS BERISI URL DEPLOYMENT "WEB APP" YANG PALING BARU
const API_URL = "https://script.google.com/macros/s/AKfycbyhZ5TzJKBNV3nsd059EAta3FrfhpbmRK5OQF54JejeI7HsXwqrDuBrS7Rfjl0vUNWygg/exec";

// ==========================================
// FUNGSI UNIVERSAL PEMANGGIL API (LAPIS BAJA)
// ==========================================
async function callAPI(action, dataObj = {}) {
  // Jangan munculkan loading ganda jika action adalah getStats (background loading)
  if (action !== 'getStats' && action !== 'getPemilih' && action !== 'getTimProgress') {
    Swal.fire({
      title: 'Menembus Database...',
      text: 'Menyinkronkan data dengan Satelit Pusat',
      allowOutsideClick: false,
      allowEscapeKey: false,
      showConfirmButton: false,
      didOpen: () => { Swal.showLoading(); }
    });
  }

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "text/plain;charset=utf-8" }, // STANDAR MUTLAK
      body: JSON.stringify({ action: action, data: dataObj }),
      redirect: "follow" // STANDAR MUTLAK
    });

    const textResponse = await response.text();
    let result;
    try {
      result = JSON.parse(textResponse);
    } catch (e) {
      console.error("SERVER GOOGLE MENOLAK:", textResponse);
      throw new Error("Koneksi diblokir oleh Server Google. Pastikan Akses Deployment 'Anyone'.");
    }

    if (action !== 'getStats' && action !== 'getPemilih' && action !== 'getTimProgress') {
      Swal.close();
    }
    return result;

  } catch (error) {
    if (action !== 'getStats' && action !== 'getPemilih' && action !== 'getTimProgress') {
      Swal.close();
      Swal.fire({ icon: 'error', title: 'Koneksi Gagal', text: error.message, confirmButtonColor: '#e74c3c' });
    }
    throw error; 
  }
}

// ==========================================
// ENGINE INSTALASI APLIKASI (PWA)
// ==========================================
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('./sw.js')
      .then(reg => console.log('✅ Sistem Aplikasi Terinstal (PWA Aktif)'))
      .catch(err => console.log('❌ PWA Gagal:', err));
  });
}

// ==========================================
// DETEKSI SINYAL INTERNET
// ==========================================
window.addEventListener('offline', () => {
  if (typeof Swal !== 'undefined') Swal.fire({ toast: true, position: 'top', icon: 'error', title: 'Sinyal Terputus!', showConfirmButton: false, timer: 3000 });
});

window.addEventListener('online', () => {
  if (typeof Swal !== 'undefined') Swal.fire({ toast: true, position: 'top', icon: 'success', title: 'Sinyal Kembali', showConfirmButton: false, timer: 3000 });
});

document.body.style.overscrollBehaviorY = 'contain';