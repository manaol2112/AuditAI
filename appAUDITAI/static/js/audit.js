document.addEventListener('DOMContentLoaded', function () {
    var trigger = document.querySelector('[data-bs-toggle="offcanvas"]');
    var offcanvasElement = document.querySelector('.offcanvas');
    var bootstrapOffcanvas = new bootstrap.Offcanvas(offcanvasElement);
  
    trigger.addEventListener('click', function () {
      bootstrapOffcanvas.toggle();
    });
  });