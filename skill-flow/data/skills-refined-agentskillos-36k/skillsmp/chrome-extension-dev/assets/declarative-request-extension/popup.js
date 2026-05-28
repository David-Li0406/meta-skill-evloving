// Popup for declarative request blocker

console.log('Request Blocker popup loaded');

// You can extend this to show statistics
// about blocked requests if needed

chrome.declarativeNetRequest.getEnabledRulesets((rulesets) => {
  console.log('Active rulesets:', rulesets);
});