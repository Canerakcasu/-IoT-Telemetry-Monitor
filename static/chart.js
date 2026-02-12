// Global storage for chart instances to allow proper cleanup
let chartInstances = [];
let currentDevice = 'all';

// Helper for chart configuration
function getChartOptions(title, color) {
    return {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { display: false },
            title: { display: true, text: title, color: '#aaa', font: { size: 11 } },
            tooltip: {
                backgroundColor: '#252525',
                titleColor: '#fff',
                bodyColor: '#fff',
                borderColor: '#333',
                borderWidth: 1,
                displayColors: false
            }
        },
        scales: {
            x: {
                display: false, // Hide X axis labels to save space
                grid: { display: false }
            },
            y: {
                grid: { color: 'rgba(255,255,255,0.05)' },
                ticks: { color: '#888', font: { size: 10 } }
            }
        },
        elements: {
            point: { radius: 0, hitRadius: 10, hoverRadius: 4 },
            line: { tension: 0.4, borderWidth: 2 }
        }
    };
}

async function loadCharts(deviceId = 'all') {
    currentDevice = deviceId || 'all';
    
    try {
        // Fetch all data to process client-side
        const response = await fetch('/telemetry/all');
        const data = await response.json();

        // Identify the container. We look for a container we created, or the placeholder from the HTML template.
        let container = document.getElementById('dynamic-dashboard-container');
        
        if (!container) {
            // If our dynamic container doesn't exist, try to find the static charts and replace them
            const staticPlaceholder = document.getElementById('temperatureChart');
            if (staticPlaceholder) {
                // Find the row containing the static charts
                const row = staticPlaceholder.closest('.row');
                if (row) {
                    // Create our new container
                    container = document.createElement('div');
                    container.id = 'dynamic-dashboard-container';
                    // Insert it before the row
                    row.parentNode.insertBefore(container, row);
                    // Remove the static row entirely
                    row.remove();
                }
            }
        }

        // If we still don't have a container (e.g. on a page without charts), exit
        if (!container) return;

        // Cleanup existing charts
        chartInstances.forEach(chart => chart.destroy());
        chartInstances = [];
        container.innerHTML = ''; // Clear HTML

        if (!data.telemetry || data.telemetry.length === 0) {
            container.innerHTML = `
                <div class="alert alert-info text-center">
                    No telemetry data available. Please send data via Postman.
                </div>`;
            return;
        }

        // Group data by Device ID
        const groupedData = {};
        data.telemetry.forEach(t => {
            if (!groupedData[t.device_id]) groupedData[t.device_id] = [];
            groupedData[t.device_id].push(t);
        });

        // Determine which devices to show
        const devicesToShow = (currentDevice === 'all') 
            ? Object.keys(groupedData) 
            : Object.keys(groupedData).filter(id => id === currentDevice);

        if (devicesToShow.length === 0 && currentDevice !== 'all') {
            container.innerHTML = `<div class="alert alert-warning">No data for device: ${currentDevice}</div>`;
            return;
        }

        // Render a card for each device
        devicesToShow.forEach(devId => {
            const devData = groupedData[devId].sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));
            
            // Prepare data arrays
            const labels = devData.map(t => new Date(t.timestamp).toLocaleTimeString());
            const temps = devData.map(t => t.temperature);
            const hums = devData.map(t => t.humidity);
            const bats = devData.map(t => t.battery);

            // Generate Table Rows (Last 5 entries)
            const tableRows = devData.slice().reverse().slice(0, 5).map(t => `
                <tr>
                    <td><small>${new Date(t.timestamp).toLocaleTimeString()}</small></td>
                    <td>${t.temperature}°C</td>
                    <td>${t.humidity}%</td>
                    <td>${t.battery}%</td>
                </tr>
            `).join('');

            // Create Card Element
            const card = document.createElement('div');
            card.className = 'card mb-4';
            card.style.borderColor = 'var(--border)';
            
            card.innerHTML = `
                <div class="card-header d-flex justify-content-between align-items-center">
                    <h5 class="mb-0" style="color: var(--primary);"><i class="fas fa-microchip me-2"></i> ${devId}</h5>
                    <span class="badge bg-secondary">${devData.length} Data Points</span>
                </div>
                <div class="card-body">
                    <div class="row">
                        <!-- Charts Section -->
                        <div class="col-lg-9">
                            <div class="row">
                                <div class="col-md-4 mb-3">
                                    <div class="chart-card p-2" style="height: 200px;">
                                        <canvas id="chart-temp-${devId}"></canvas>
                                    </div>
                                </div>
                                <div class="col-md-4 mb-3">
                                    <div class="chart-card p-2" style="height: 200px;">
                                        <canvas id="chart-hum-${devId}"></canvas>
                                    </div>
                                </div>
                                <div class="col-md-4 mb-3">
                                    <div class="chart-card p-2" style="height: 200px;">
                                        <canvas id="chart-bat-${devId}"></canvas>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <!-- Table Section -->
                        <div class="col-lg-3">
                            <div class="table-responsive" style="height: 200px; overflow-y: auto; border: 1px solid var(--border); border-radius: 8px;">
                                <table class="table table-sm table-hover mb-0" style="font-size: 0.8rem;">
                                    <thead style="position: sticky; top: 0; background: var(--card-bg); z-index: 1;">
                                        <tr>
                                            <th>Time</th>
                                            <th>Temp</th>
                                            <th>Hum</th>
                                            <th>Bat</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        ${tableRows}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            `;

            container.appendChild(card);

            // Instantiate Charts
            const createChart = (metric, data, color, title) => {
                const ctx = document.getElementById(`chart-${metric}-${devId}`).getContext('2d');
                const chart = new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: labels,
                        datasets: [{
                            data: data,
                            borderColor: color,
                            backgroundColor: color + '20', // Hex + opacity
                            fill: true
                        }]
                    },
                    options: getChartOptions(title, color)
                });
                chartInstances.push(chart);
            };

            createChart('temp', temps, '#FF8C00', 'Temperature (°C)');
            createChart('hum', hums, '#00A8E8', 'Humidity (%)');
            createChart('bat', bats, '#4CAF50', 'Battery (%)');
        });

    } catch (error) {
        console.error('Error loading charts:', error);
    }
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    const sel = document.getElementById('deviceSelect');
    if (sel) {
        sel.addEventListener('change', (e) => loadCharts(e.target.value));
        loadCharts(sel.value || 'all');
    } else {
        loadCharts('all');
    }
});

// Auto-refresh
setInterval(() => loadCharts(currentDevice), 5000);
