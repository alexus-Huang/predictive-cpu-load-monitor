const ctx = document.getElementById('cpuChart').getContext('2d');
const cpuChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [
            {
                label: 'Current CPU',
                data: [],
                borderColor: '#3DDC97',
                tension: 0.3
            },
            {
                label: 'Predicted CPU',
                data: [],
                borderColor: '#FF5D5D',
                tension: 0.3
            }
        ]
    },
    options: {
        scales: {
            y: { min: 0, max: 100 }
        },
        plugins: {
            legend: {
                labels: {
                    usePointStyle: true,
                    pointStyle: 'line',
                    color: '#E8EDF2'
                }
            }
        }
    }
});

async function updateTelemetry(){
    const response = await fetch('/api/telemetry')
    const data = await response.json()
    const now = new Date().toLocaleTimeString();

    document.getElementById("current").textContent = data.current_cpu + "%"
    document.getElementById("predicted").textContent = data.predicted_cpu + "%"
    document.getElementById("status").textContent = data.status

    const statusBox = document.getElementById("status-box")
    statusBox.classList.remove("normal", "warning")
    statusBox.classList.add(data.status === "WARNING" ? "warning" : "normal")

    cpuChart.data.labels.push(now);
    const maxPoints = 20;
    if (cpuChart.data.labels.length > maxPoints) {
        cpuChart.data.labels.shift();
        cpuChart.data.datasets[0].data.shift();
        cpuChart.data.datasets[1].data.shift();
    }
    cpuChart.data.datasets[0].data.push(data.current_cpu);
    cpuChart.data.datasets[1].data.push(data.predicted_cpu);

    cpuChart.update();
}

updateTelemetry()
setInterval(updateTelemetry, 3000)