document.addEventListener('DOMContentLoaded', function () {
  const privacyModal = document.getElementById('privacyPolicyModal');

  if (privacyModal) {
    privacyModal.addEventListener('shown.bs.modal', () => {
      console.log('Privacy Policy modal was opened.');
    });
  }
});
