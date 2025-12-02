console.log("PEWS content script loaded");
let lastScrollY = window.scrollY;
let lastMouseX = 0;
let lastMouseY = 0;
let mouseDistance = 0;
let lastActivityTime = Date.now();

function resetMouseBase(e) {
  lastMouseX = e.clientX;
  lastMouseY = e.clientY;
}
window.addEventListener("mousemove", resetMouseBase, { once: true });

document.addEventListener("mousemove", (e) => {
  const dx = e.clientX - lastMouseX;
  const dy = e.clientY - lastMouseY;
  mouseDistance += Math.hypot(dx, dy);
  lastMouseX = e.clientX;
  lastMouseY = e.clientY;
  lastActivityTime = Date.now();
});

document.addEventListener("scroll", () => {
  lastActivityTime = Date.now();
});

function collectAndSend() {
  console.log("Sending to backend:", payload);
  const now = Date.now();
  const dy = Math.abs(window.scrollY - lastScrollY);
  const scrollSpeed = dy; // pixels per interval (3 seconds)
  lastScrollY = window.scrollY;

  const idleTime = now - lastActivityTime;

  chrome.runtime.sendMessage({ type: "getTabSwitches" }, (response) => {
    const tabSwitches = response?.tab_switches ?? 0;

    const payload = {
      tab_switches: tabSwitches,
      scroll_speed: scrollSpeed,
      mouse_distance: mouseDistance,
      idle_time: idleTime,
      url: window.location.href
    };

    mouseDistance = 0;

    fetch("http://127.0.0.1:8000/collect", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    })
      .then((res) => res.json())
      .then((data) => {
        const score = data.distraction_probability;
        if (score >= 70) {
          console.log("⚠️ High distraction probability:", score + "%");
          showWarningOverlay(score);
        }
      })
      .catch((err) => console.error("PEWS error:", err));
  });
}

function showWarningOverlay(score) {
  let existing = document.getElementById("pews-overlay");
  if (existing) {
    existing.remove();
  }

  const overlay = document.createElement("div");
  overlay.id = "pews-overlay";
  overlay.style.position = "fixed";
  overlay.style.top = "10px";
  overlay.style.right = "10px";
  overlay.style.zIndex = "999999";
  overlay.style.padding = "10px 14px";
  overlay.style.background = "rgba(220, 38, 38, 0.95)";
  overlay.style.color = "#fff";
  overlay.style.borderRadius = "999px";
  overlay.style.fontSize = "13px";
  overlay.style.fontFamily = "system-ui, sans-serif";
  overlay.style.boxShadow = "0 10px 30px rgba(0,0,0,0.2)";

  overlay.textContent =
    "🔥 Distraction risk: " + score + "% – take a 2-min break?";

  document.body.appendChild(overlay);

  setTimeout(() => {
    overlay.remove();
  }, 4000);
}

// send every 3s
setInterval(collectAndSend, 3000);
