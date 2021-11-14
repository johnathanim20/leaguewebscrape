function pickrate(k) {
    url = "http://127.0.0.1:5000/champions";
    console.log(url)

    fetch(url)
        .then(response => {
            console.log(response);
            if(!response.ok) {
                throw Error("ERROR");
            }
            return response.json();
        })
        .then(data => {
            if(data.error) {
                    const b = `<p> ERROR: ` + data.message + `</p>`
                    document.querySelector('#errorget').insertAdjacentHTML('beforeend',b);
            }
            console.log(data.result)
            arr = data.result
      for (var i = 0; i < arr.length; i++) {
        arr[i].win_rate = arr[i].win_rate.replace("%","");
      }
            arr.sort(function(a, b){return parseFloat(a.pick_rate) - parseFloat(b.pick_rate)})
            arr.reverse()
            dataArray = arr.slice(0,k)
            makeBarChart(dataArray)
            console.log(dataArray)
        })
        .catch(error => {
            console.log(error);
        });
}

function makeBarChart(dataArr) {
    d3.selectAll("svg > *").remove();
    var svg = d3.select("svg");
    var margin = 50;
    var widtht = svg.attr("width") - margin;
    var heightt = svg.attr("height") - margin;

    var chart = svg.append('g')
        .attr('transform', `translate(${margin}, ${margin})`);


    var xScale = d3.scaleBand().range([0, widtht]).padding(.5);
    var yScale = d3.scaleLinear().range([heightt-70, 0]);

    xScale.domain(dataArr.map(d => {return d.name}));
    yScale.domain([0,100]);

    chart.append('g')
        .call(d3.axisLeft(yScale));

    chart.append('g')
        .attr('transform', `translate(0, ${heightt-70})`)
        .call(d3.axisBottom(xScale))
      .selectAll('text').attr("transform", `translate(-12,35) rotate(-75)`);
    chart.selectAll()
        .data(dataArr)
        .enter()
        .append('rect')
        .attr('x', (s) => xScale(s.name))
        .attr('y', (s) => yScale(parseFloat(s.pick_rate)))
        .attr('height', (s) => heightt - 70 - yScale(parseFloat(s.pick_rate)))
        .attr('width', xScale.bandwidth());





}