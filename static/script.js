async function updateTelemetry(){
    const response = await fetch('/api/telemetry')
    const data = await response.json()

    document.getElementById("current").textContent = data.current_cpu
    document.getElementById("predicted").textContent = data.predicted_cpu
    document.getElementById("status").textContent = data.status
}

updateTelemetry() // run once when the page loads
setInterval(updateTelemetry, 3000) // run again every 3 seconds