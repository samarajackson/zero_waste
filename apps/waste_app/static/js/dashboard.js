$(document).ready(function () {
  months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
  var data = [{
    x: months,
    y: amounts,
    type: 'bar',
    marker: {
      color: 'rgb(159, 85, 173)'
    }
  }];
  var layout={
    title:"My Progress",
    yaxis:{
      title:"Trash in Pounds"
    }
  }
  Plotly.newPlot('history', data, layout, { showSendToCloud: true });





});