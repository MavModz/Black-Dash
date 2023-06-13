fetch('/api/chart_data')
.then(response => response.json())
.then(data => {
    const sectors = data.sectors;
    const topics = data.topics;
    const countries = data.countries;

    // Count the occurrences of each sector
    const sectorCounts = {};
    sectors.forEach(sector => {
        sectorCounts[sector] = (sectorCounts[sector] || 0) + 1;
    });

    // Prepare the data for the chart
    const chartData = {
        labels: Object.keys(sectorCounts),
        datasets: [{
            label: 'Count',
            data: Object.values(sectorCounts),
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1
        }]
    };

    // Create the chart
    const ctx = document.getElementById('myChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: chartData,
        options: {
            plugins: {
                zoom: {
                    zoom: {
                        wheel: {
                            enabled: true
                        },
                        pinch: {
                            enabled: true
                        },
                        mode: 'xy'
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    stepSize: 1
                }
            }
        }
    });
});
