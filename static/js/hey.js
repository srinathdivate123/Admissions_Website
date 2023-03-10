const renderChart = (data_val) => {
    console.log("CHART LOADED");
    var ctx = document.getElementById("myChart").getContext("2d");
    var myChart = new Chart(ctx, {
        type: "doughnut",
        data: {
            labels: [" Possibility", "Impossibility"],

            datasets: [{

                data: data_val,
                backgroundColor: [
                    'rgb(60, 179, 113)',
                    'rgb(240, 240, 240)',
                ],
                borderColor: [
                    'rgb(60, 179, 113)',
                    'rgb(240, 240, 240)',
                ],
                borderWidth: 1,
            }, ],
        },
        options: {
            title: {
                display: true,
                text: "Results",
            },
        },
    });
};

const getChartData = () => {
    fetch("chart")
        .then((res) => res.json())
        .then((results) => {
            console.log("results", results);
            const var1 = results.prediction;
            const [data_val] = [Object.values(var1)]
            console.log(data_val);

            renderChart(data_val);
        });

};

document.onload = getChartData();