/**
 * For usage, visit Chart.js docs https://www.chartjs.org/docs/latest/
 */
const lineConfig = {
  type: 'line',
  data: {
    labels: ["Domingo","Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"],
    datasets: [
      {
        label: 'Comentarios',
        backgroundColor: '#0694a2',
        borderColor: '#0694a2',
        data: [],
        fill: false,
      },
    ],
  },
  options: {
    responsive: true,
    legend: {
      display: false,
    },
    tooltips: {
      mode: 'index',
      intersect: false,
    },
    hover: {
      mode: 'nearest',
      intersect: true,
    },
    scales: {
      x: {
        display: true,
        scaleLabel: {
          display: true,
          labelString: 'Día',
        },
      },
      y: {
        display: true,
        scaleLabel: {
          display: true,
          labelString: 'Cantidad',
        },
      },
    },
  },
};

// Change this to the id of your chart element in HTML
const lineCtx = document.getElementById('line');
window.myLine = new Chart(lineCtx, lineConfig);

const parseDate = (dateString) => {
  try {
    // Normalizar espacios y reemplazar AM/PM
    const cleanedDate = dateString
      .replace(/[\u00A0\s]+/g, ' ') // Reemplaza espacios invisibles por espacios normales
      .replace('a. m.', 'AM')
      .replace('p. m.', 'PM');

    // Separar partes de fecha y hora
    const [datePart, timePart] = cleanedDate.split(',').map((part) => part.trim());
    if (!datePart || !timePart) {
      console.error('Formato de fecha no válido:', dateString);
      return null;
    }

    // Extraer día, mes y año
    const [day, month, year] = datePart.split('/');
    if (!day || !month || !year) {
      console.error('Formato de fecha no válido:', datePart);
      return null;
    }

    // Convertir tiempo AM/PM a 24 horas
    const [time, period] = timePart.split(' ');
    const [hours, minutes, seconds] = time.split(':').map(Number);
    let formattedHours = hours;

    if (period === 'PM' && hours < 12) {
      formattedHours += 12;
    } else if (period === 'AM' && hours === 12) {
      formattedHours = 0;
    }

    const formattedTime = `${String(formattedHours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;

    // Crear string ISO 8601
    const isoString = `${year}-${month.padStart(2, '0')}-${day.padStart(2, '0')}T${formattedTime}`;
    const date = new Date(isoString);

    if (isNaN(date.getTime())) {
      console.error('Fecha inválida creada:', isoString);
      return null;
    }

    return date;
  } catch (error) {
    console.error('Error al parsear la fecha:', dateString, error);
    return null;
  }
};


const countCommentsByDay = (data) => {
  const labels = ["Domingo","Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"];
  const counts = Array(7).fill(0);

  Object.values(data).forEach((record) => {
    const savedDate = record.saved;
    if (!savedDate) return;

    const date = parseDate(savedDate);
    if (!date) return;

    const dayIndex = (date.getDay() + 6) % 7;
    counts[dayIndex]++;
  });

  return { labels, counts };
};

const updateLineChart = () => {
  fetch('/api/v1/landing')
    .then((response) => response.json())
    .then((data) => {
      const { labels, counts } = countCommentsByDay(data);

      // Actualizar datos del gráfico
      window.myLine.data.labels = labels;
      window.myLine.data.datasets[0].data = counts;

      window.myLine.update();
    })
    .catch((error) => console.error('Error al actualizar el gráfico:', error));
};

updateLineChart();
