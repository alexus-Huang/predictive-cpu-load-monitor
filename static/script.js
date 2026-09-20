async function updateTelemetry(){
    const response = await fetch('/api/telemetry')
    const data = await response.json()

    document.getElementById("current").textContent = data.current_cpu + "%"
    document.getElementById("predicted").textContent = data.predicted_cpu + "%"
    document.getElementById("status").textContent = data.status

    const statusBox = document.getElementById("status-box")
    statusBox.classList.remove("normal", "warning")
    statusBox.classList.add(data.status === "WARNING" ? "warning" : "normal")
}

updateTelemetry()
setInterval(updateTelemetry, 3000)