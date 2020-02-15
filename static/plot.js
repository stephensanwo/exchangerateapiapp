const trace5 = {
  x: [1, 2, 3, 4],
  y: [10, 15, 13, 17],
  type: 'scatter'
};

const trace6 = {
  x: [1, 2, 3, 4],
  y: [16, 5, 11, 9],
  type: 'scatter'
};

const data3 = [trace5, trace6];

const layout3 = {
    showlegend: true,
		legend: {"orientation": "h",},
		autosize: false,
  	margin: {
			l: 20,
			r: 0,
    	b: 20,
    	t: 20,
    	pad:0
  },
};

Plotly.newPlot('chart_div2', data3, layout3, {displayModeBar: false});
