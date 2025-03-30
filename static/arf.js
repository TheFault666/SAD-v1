const API_BASE_URL = "http://127.0.0.1:8000";  // FastAPI backend URL

// Fetch available slave nodes and populate dropdown
async function fetchTargets() {
    try {
        let response = await fetch(`${API_BASE_URL}/get_targets`);
        let targets = await response.json();

        let dropdown = document.getElementById("target-select");
        dropdown.innerHTML = "";

        targets.forEach(target => {
            let option = document.createElement("option");
            option.value = target;
            option.textContent = target;
            dropdown.appendChild(option);
        });
    } catch (error) {
        console.error("Error fetching targets:", error);
    }
}

// Run security scan on the selected machine
async function runScan() {
    let endpoint = document.getElementById("target-select").value;

    if (!endpoint) {
        alert("Please select a target machine!");
        return;
    }

    document.getElementById("scan-result").innerText = "Running scan...";

    try {
        let response = await fetch(`${API_BASE_URL}/run_scan/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ target: endpoint })
        });

        let data = await response.json();
        document.getElementById("scan-result").innerText = JSON.stringify(data, null, 2);
    } catch (error) {
        console.error("Error running scan:", error);
        document.getElementById("scan-result").innerText = "Scan failed. See console for details.";
    }
}

// Load targets when the page loads
document.addEventListener("DOMContentLoaded", fetchTargets);

// Attach event listener to the button
document.getElementById("scan-btn").addEventListener("click", runScan);
