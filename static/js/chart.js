fetch('/api/chart_data')
.then(response => response.json())
.then(data => {
    // Extract data from the response
    const sectors = data.sectors;
    const topics = data.topics;
    const countries = data.countries;
    const intense = data.intense;
    const likelihoods = data.likelihood;

    // Count the occurrences of each sector
    const sectorCounts = {};
    sectors.forEach(sector => {
        sectorCounts[sector] = (sectorCounts[sector] || 0) + 1;
    });

    // Count the occurrences of each topic
    const topicCounts = {};
    topics.forEach(topic => {
        topicCounts[topic] = (topicCounts[topic] || 0) + 1;
    });

    // Count the occurrences of each country
    const countryCounts = {};
    countries.forEach(country => {
        countryCounts[country] = (countryCounts[country] || 0) + 1;
    });

    // Count the occurrences of each intensity
    const intenseCounts={};
    intense.forEach(intensity => {
        intenseCounts[intensity] = (intenseCounts[intensity] || 0) + 1;
    });

    // Count the occurrences of each likehood
    const likelihoodCounts={};
    likelihood.forEach(likelihood => {
        likelihoodCounts[likelihood] = (likelihoodCounts[likelihood] || 0) + 1;
    });

    // Prepare the data for the chart
    const sectorData = Object.values(sectorCounts);
    const topicData = Object.values(topicCounts);
    const countryData = Object.values(countryCounts);
    const intenseData = Object.values(intenseCounts);
    const likelihoodsData = Object.values(likelihoodCounts);

    const chartData = {
        labels: Object.keys(sectorCounts),
        datasets: [{
            label: 'Sector',
            data: sectorData,
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1
        },
        {
            label: 'Topics',
            data: topicData,
            backgroundColor: 'rgba(192, 192, 75, 0.2)',
            borderColor: 'rgba(192, 192, 75, 1)',
            borderWidth: 1
        },
        {
            label: 'Country',
            data: countryData,
            backgroundColor: 'rgba(192, 75, 192, 0.2)',
            borderColor: 'rgba(192, 75, 192, 1)',
            borderWidth: 1
        },
        {
            label: 'Intensity',
            data: intenseData,
            backgroundColor: 'rgba(75, 192, 75, 0.2)',
            borderColor: 'rgba(75, 192, 75, 1)',
            borderWidth: 1
        },
        {
            label: 'Likelihood',
            data: likelihoodsData,
            backgroundColor: 'rgba(75, 192, 75, 0.2)',
            borderColor: 'rgba(75, 192, 75, 1)',
            borderWidth: 1
        }]
    };

    // Create the chart
    const ctx = document.getElementById('myChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: chartData,
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    stepSize: 1
                }
            }
        }
    });
});
