// Load and display service worker status
function loadStatus() {
  chrome.runtime.sendMessage({action: 'getStatus'}, (response) => {
    const statusDiv = document.getElementById('status');
    if (response) {
      const lastTime = response.lastAlarm 
        ? new Date(response.lastAlarm).toLocaleString()
        : 'Never';
      statusDiv.innerHTML = `
        <strong>Alarm Count:</strong> ${response.count}<br>
        <strong>Last Alarm:</strong> ${lastTime}
      `;
    } else {
      statusDiv.textContent = 'Service worker not responding';
    }
  });
}

// Load on popup open
loadStatus();

// Refresh button
document.getElementById('refreshBtn').addEventListener('click', loadStatus);