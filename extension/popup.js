const statusEl = document.getElementById("status");
const btn = document.getElementById("check-backend");

function checkBackend() {
  statusEl.textContent = "Backend: checking...";
  fetch("http://127.0.0.1:8000/")
    .then((res) => res.json())
    .then((data) => {
      statusEl.textContent = "Backend: " + (data.status || "OK");
    })
    .catch(() => {
      statusEl.textContent =
        "Backend: not reachable. Start `uvicorn main:app` in backend.";
    });
}

btn.addEventListener("click", checkBackend);
checkBackend();
