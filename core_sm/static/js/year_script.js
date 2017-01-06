
function changeChart () {
    var elChart = document.getElementById('year-table').innerHTML = '{{ div_line }}
                                                                     {{ script_line }}';
}

var newChart = document.getElementById('year-table');
newChart.onclick = changeChart;