document.addEventListener("DOMContentLoaded", function () {
  const toggleBtn = document.getElementById("toggleChartBtn");
  const chartContainer = document.getElementById("chartContainer");
  const toggleIcon = document.getElementById("toggleIcon");

  toggleBtn.addEventListener("click", () => {
    if (chartContainer.style.display === "none") {
      chartContainer.style.display = "block";
      toggleIcon.textContent = "▼";
    } else {
      chartContainer.style.display = "none";
      toggleIcon.textContent = "►";
    }
  });

  // Chart.js Configuration
  const getRandomColor = () => {
    const hue = Math.floor(Math.random() * 360);
    return `hsl(${hue}, 80%, 50%)`;
  };

  try {
    if (
      !chartData ||
      !chartData.timestamps ||
      chartData.timestamps.length === 0
    ) {
      console.error("No valid data found for plotting.");
      return;
    }

    let ctx = document.getElementById("datasetChart").getContext("2d");
    const datasets = chartData.series.map((seriesItem) => {
      return {
        label: seriesItem.name, // "X", "Y", "Z", "Norm"
        data: seriesItem.data.map((point) => ({ x: point[0], y: point[1] })), // Convert tuples to Chart.js format
        borderColor: getRandomColor(),
        fill: false,
        pointRadius: 0, // Hide points for performance
        tension: 0.1, // Slight smoothing
      };
    });

    new Chart(ctx, {
      type: "line",
      data: {
        datasets: datasets,
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: false, // Improves performance
        scales: {
          x: {
            type: "linear", // Properly handle timestamps
            title: { display: true, text: "Timestamps" },
            grid: { color: "rgba(200, 200, 200, 0.3)", lineWidth: 0.3 },
          },
          y: {
            title: { display: true, text: "Values" },
            grid: { color: "rgba(200, 200, 200, 0.3)", lineWidth: 0.3 },
          },
        },
        elements: {
          line: { borderWidth: 1 },
          point: { radius: 0 }, // Hide points for better performance
        },
      },
    });
  } catch (error) {
    console.error("Error rendering chart:", error);
  }
});
