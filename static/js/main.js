// Hotel Pacific Reef — Scripts principales

document.addEventListener('DOMContentLoaded', function () {
  // Validación de fechas en formulario de reserva
  const fechaEntrada = document.querySelector('input[name="fecha_entrada"]');
  const fechaSalida = document.querySelector('input[name="fecha_salida"]');

  if (fechaEntrada && fechaSalida) {
    fechaEntrada.addEventListener('change', function () {
      fechaSalida.min = this.value;
      if (fechaSalida.value && fechaSalida.value <= this.value) {
        fechaSalida.value = '';
      }
    });
  }

  // Auto-cerrar alertas después de 5 segundos
  const alertas = document.querySelectorAll('.alert.alert-dismissible');
  alertas.forEach(function (alerta) {
    setTimeout(function () {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alerta);
      bsAlert.close();
    }, 5000);
  });
});
