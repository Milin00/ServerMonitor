
// Djangoからグラフデータを取得
const chartDataElement = document.getElementById('chart-data');

if (!chartDataElement) {
    console.error('グラフデータが見つかりません');
} else {
    const chartData = JSON.parse(chartDataElement.textContent);

    const ctx = document.getElementById('systemChart');

    if (ctx) {
        new Chart(ctx, {
            type: 'line',

            data: {
                labels: chartData.labels,

                datasets: [
                    {
                        label: 'CPU使用率',
                        data: chartData.cpu,
                        borderColor: '#3498db',
                        backgroundColor: '#3498db',
                        borderWidth: 2,
                        tension: 0.3
                    },
                    {
                        label: 'メモリ使用率',
                        data: chartData.memory,
                        borderColor: '#e74c3c',
                        backgroundColor: '#e74c3c',
                        borderWidth: 2,
                        tension: 0.3
                    },
                    {
                        label: 'ディスク使用率',
                        data: chartData.disk,
                        borderColor: '#f39c12',
                        backgroundColor: '#f39c12',
                        borderWidth: 2,
                        tension: 0.3
                    }
                ]
            },

            options: {
                responsive: true,
                maintainAspectRatio: true,

                scales: {
                    y: {
                        beginAtZero: true,
                        min: 0,
                        max: 100,
                        title: {
                            display: true,
                            text: '使用率（%）'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: '時刻'
                        }
                    }
                }
            }
        });
    }
}
