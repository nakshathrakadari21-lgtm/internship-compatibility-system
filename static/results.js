document.addEventListener('DOMContentLoaded', () => {
    // Chart Defaults for Dark Theme
    Chart.defaults.color = 'rgba(255, 255, 255, 0.95)';
    Chart.defaults.font.family = "'Poppins', sans-serif";
    Chart.defaults.scale.grid.color = 'rgba(255, 255, 255, 0.1)';
    Chart.defaults.scale.grid.borderColor = 'rgba(255, 255, 255, 0.2)';

    // 1. Compatibility Score Analysis (Bar Chart)
    const ctxBar = document.getElementById('compatibilityBarChart').getContext('2d');
    new Chart(ctxBar, {
        type: 'bar',
        data: {
            labels: ['Full Stack Dev', 'Data Analyst', 'Cloud Engineer', 'UI/UX Design', 'DevOps'],
            datasets: [{
                label: 'Compatibility Score (%)',
                data: [88, 65, 42, 30, 25],
                backgroundColor: 'rgba(79, 172, 254, 0.7)',
                borderColor: 'rgba(0, 242, 254, 1)',
                borderWidth: 1,
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: {
                duration: 1500,
                easing: 'easeOutQuart'
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });

    // 2. Domain Match Comparison (Pie Chart)
    const ctxPie = document.getElementById('domainPieChart').getContext('2d');
    new Chart(ctxPie, {
        type: 'doughnut',
        data: {
            labels: ['Web Dev', 'Data Science', 'Cloud', 'Others'],
            datasets: [{
                data: [45, 25, 20, 10],
                backgroundColor: [
                    'rgba(79, 172, 254, 0.8)',
                    'rgba(168, 85, 247, 0.8)',
                    'rgba(16, 185, 129, 0.8)',
                    'rgba(244, 63, 94, 0.8)'
                ],
                borderColor: 'rgba(255, 255, 255, 0.2)',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            },
            animation: {
                animateScale: true,
                animateRotate: true
            }
        }
    });

    // 3. User Performance Visualization (Line Chart)
    const ctxLine = document.getElementById('performanceLineChart').getContext('2d');
    new Chart(ctxLine, {
        type: 'line',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            datasets: [{
                label: 'Overall Skill Proficiency',
                data: [40, 48, 55, 62, 75, 82],
                borderColor: 'rgba(168, 85, 247, 1)',
                backgroundColor: 'rgba(168, 85, 247, 0.1)',
                borderWidth: 3,
                tension: 0.4,
                fill: true,
                pointBackgroundColor: 'rgba(255, 255, 255, 1)',
                pointBorderColor: 'rgba(168, 85, 247, 1)',
                pointRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });

    // 4. Internship Compatibility Trend Graph (Area Chart)
    const ctxTrend = document.getElementById('trendAreaChart').getContext('2d');
    new Chart(ctxTrend, {
        type: 'line',
        data: {
            labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5'],
            datasets: [{
                label: 'Top Match Score Trend',
                data: [50, 58, 65, 72, 88],
                borderColor: 'rgba(16, 185, 129, 1)',
                backgroundColor: 'rgba(16, 185, 129, 0.2)',
                borderWidth: 2,
                tension: 0.3,
                fill: true,
                pointStyle: 'rectRot',
                pointRadius: 6
            },
            {
                label: 'Average Market Requirement',
                data: [65, 66, 65, 68, 67],
                borderColor: 'rgba(244, 63, 94, 1)',
                borderDash: [5, 5],
                borderWidth: 2,
                tension: 0.1,
                fill: false,
                pointRadius: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });
});
