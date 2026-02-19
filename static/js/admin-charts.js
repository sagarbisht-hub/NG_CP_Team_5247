// Admin Dashboard Charts
function initAdminCharts(chartData) {
    // Status Distribution Pie Chart (Doughnut)
    const statusCtx = document.getElementById('statusChart').getContext('2d');
    new Chart(statusCtx, {
        type: 'doughnut',
        data: {
            labels: ['Pending', 'In Progress', 'Completed'],
            datasets: [{
                data: [chartData.pending_jobs, chartData.assigned_jobs, chartData.completed_jobs],
                backgroundColor: [
                    'rgba(251, 191, 36, 0.8)',
                    'rgba(102, 126, 234, 0.8)',
                    'rgba(16, 185, 129, 0.8)'
                ],
                borderColor: [
                    'rgb(251, 191, 36)',
                    'rgb(102, 126, 234)',
                    'rgb(16, 185, 129)'
                ],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 10,
                        font: {
                            size: 11,
                            weight: 'bold'
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.parsed || 0;
                            const total = chartData.total_jobs;
                            const percentage = ((value / total) * 100).toFixed(1);
                            return label + ': ' + value + ' (' + percentage + '%)';
                        }
                    }
                }
            }
        }
    });

    // Category Performance Bar Chart (Histogram)
    const categoryCtx = document.getElementById('categoryChart').getContext('2d');
    new Chart(categoryCtx, {
        type: 'bar',
        data: {
            labels: chartData.category_labels,
            datasets: [{
                label: 'Number of Jobs',
                data: chartData.category_counts,
                backgroundColor: 'rgba(102, 126, 234, 0.8)',
                borderColor: 'rgb(102, 126, 234)',
                borderWidth: 2,
                borderRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1,
                        font: {
                            size: 10
                        }
                    }
                },
                x: {
                    ticks: {
                        font: {
                            size: 10
                        }
                    }
                }
            }
        }
    });

    // Revenue by Category Line Chart
    const revenueCtx = document.getElementById('revenueChart').getContext('2d');
    new Chart(revenueCtx, {
        type: 'line',
        data: {
            labels: chartData.revenue_labels,
            datasets: [{
                label: 'Average Price (₹)',
                data: chartData.revenue_data,
                backgroundColor: 'rgba(245, 87, 108, 0.2)',
                borderColor: 'rgb(245, 87, 108)',
                borderWidth: 2,
                fill: true,
                tension: 0.4,
                pointRadius: 4,
                pointBackgroundColor: 'rgb(245, 87, 108)',
                pointBorderColor: '#fff',
                pointBorderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'bottom',
                    labels: {
                        padding: 10,
                        font: {
                            size: 11
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return '₹' + value;
                        },
                        font: {
                            size: 10
                        }
                    }
                },
                x: {
                    ticks: {
                        font: {
                            size: 10
                        }
                    }
                }
            }
        }
    });

    // Urgency Levels Polar Area Chart
    const urgencyCtx = document.getElementById('urgencyChart').getContext('2d');
    new Chart(urgencyCtx, {
        type: 'polarArea',
        data: {
            labels: ['Low Priority', 'Medium Priority', 'High Priority'],
            datasets: [{
                data: [chartData.urgency_low, chartData.urgency_medium, chartData.urgency_high],
                backgroundColor: [
                    'rgba(16, 185, 129, 0.7)',
                    'rgba(251, 191, 36, 0.7)',
                    'rgba(239, 68, 68, 0.7)'
                ],
                borderColor: [
                    'rgb(16, 185, 129)',
                    'rgb(251, 191, 36)',
                    'rgb(239, 68, 68)'
                ],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 10,
                        font: {
                            size: 11,
                            weight: 'bold'
                        }
                    }
                }
            },
            scales: {
                r: {
                    ticks: {
                        font: {
                            size: 9
                        }
                    }
                }
            }
        }
    });
}
