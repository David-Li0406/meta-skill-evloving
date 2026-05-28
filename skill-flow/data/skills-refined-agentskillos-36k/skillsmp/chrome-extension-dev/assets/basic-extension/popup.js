// Save data to storage
document.getElementById('saveBtn').addEventListener('click', () => {
  chrome.storage.local.set({
    timestamp: Date.now(),
    message: 'Hello from popup!'
  }, () => {
    console.log('Data saved');
  });
});

// Load data from storage
document.getElementById('loadBtn').addEventListener('click', () => {
  chrome.storage.local.get(['timestamp', 'message'], (result) => {
    if (result.timestamp) {
      alert(`Saved at: ${new Date(result.timestamp).toLocaleString()}\nMessage: ${result.message}`);
    } else {
      alert('No data found');
    }
  });
});