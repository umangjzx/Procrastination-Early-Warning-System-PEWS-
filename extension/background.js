let switchesLastInterval = 0;

chrome.tabs.onActivated.addListener(() => {
  switchesLastInterval += 1;
});

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === "complete") {
    switchesLastInterval += 1;
  }
});

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "getTabSwitches") {
    sendResponse({ tab_switches: switchesLastInterval });
    switchesLastInterval = 0;
  }
  return true;
});
