canvas = d3.select(".canvas")
// const height = 900
const marginLeft = 125
const marginTop = 130

var slider = document.getElementById("myRange");
// set the h5 with id="slider_value" to the current slider value
var output = document.getElementById("slider_value");
output.innerHTML = slider.value;
// Update the current slider value (each time you drag the slider handle)
slider.oninput = function () {
    output.innerHTML = this.value;
    myColor.domain([1, this.value])
    rect = svg.selectAll("rect")
        .style("fill", function (d) {
            return myColor(d.finger_difficulty)
        })
}

const width = 800
const height = 100
svg = canvas.append("svg")
    .attr("width", width + 100)
    .attr("height", height + 100)


rect = svg.selectAll("rect")

// Create OSMD object
var osmd = new opensheetmusicdisplay.OpenSheetMusicDisplay("osmdCanvas");

osmd.setOptions({
    backend: "svg",
    drawTitle: false,
    drawComposer: false,
});

var osmdCanvas = d3.select("#osmdCanvas");


// Build color scale
const myColor = d3.scaleLinear()
    .range(["#eeeeee", "red"])
    .domain([1, 300])

// parse the saint saens json file into a json object
fetch('/get_musicxml_data')
    .then(response => response.json())
    .then(data => {
        xmlMeasures = data
    });


fetch('/get_heatmap_data')
    .then(response => response.json())
    .then(data => {
        heatmap(data)
        pieChart(data)
        barChart(data)
    });

function barChart(data) {
    const noteCounts = d3.rollup(data, v => v.length, d => d.fullName);

    const sortedCounts = Array.from(noteCounts, ([name, value]) => ({ name, value }))
        .filter(d => d.name !== "Rest")
        .sort((a, b) => d3.descending(a.value, b.value));


    const margin = { top: 10, right: 30, bottom: 60, left: 120 };
    const width = 350;
    const height = 500;

    const svg = d3.select('#barChart')
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

    const x = d3.scaleLinear()
        .domain([0, d3.max(sortedCounts, d => d.value)])
        .range([0, width]);

    const y = d3.scaleBand()
        .domain(sortedCounts.map(d => d.name))
        .range([0, height])
        .paddingInner(0.2)
        .paddingOuter(0.2);

    y.bandwidth(y.bandwidth() + 10); // increase the height of each bar

    const colorScale = d3.scaleOrdinal()
        .domain(sortedCounts.map(d => d.name))
        .range(sortedCounts.map(d => `hsl(${d.midiNumber}, 70%, 50%)`));

    svg.selectAll('.bar')
        .data(sortedCounts)
        .join('rect')
        .attr('class', 'bar')
        .attr('x', 0)
        .attr('y', d => y(d.name))
        .attr('width', d => x(d.value))
        .attr('height', y.bandwidth())
        .attr('fill', d => colorScale(d.name));

    svg.append('g')
        .attr('transform', `translate(0,${height})`)
        .call(d3.axisBottom(x));

    svg.append('g')
        .call(d3.axisLeft(y).tickSize(0))
        .call(g => g.select('.domain').remove());
}

function pieChart(data) {
    // Filter the data to count the number of rests and non-rests
    const noteBeatCount = d3.sum(data.filter(d => d.fullName !== "Rest"), d => d.quarterLengthDuration);
    const restBeatCount = d3.sum(data.filter(d => d.fullName === "Rest"), d => d.quarterLengthDuration);

    // Set up the data for the pie chart
    const pieData = [
        { label: "Rests", value: restBeatCount },
        { label: "Notes", value: noteBeatCount }
    ];

    // Set up the dimensions for the chart
    const width = 200;
    const height = 200;
    const radius = Math.min(width, height) / 2;

    // Set up the color scale for the chart
    const color = d3.scaleOrdinal()
        .domain(pieData.map(d => d.label))
        .range(["#D3D3D3", "#87CEFA"]);

    // Set up the pie generator
    const pie = d3.pie()
        .sort(null)
        .value(d => d.value);

    // Set up the arc generator
    const arc = d3.arc()
        .outerRadius(radius - 10)
        .innerRadius(0);

    // Create the SVG element for the chart
    const svg = d3.select("#pieChart").append("svg")
        .attr("width", width)
        .attr("height", height)
        .append("g")
        .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

    // Add the slices to the chart
    const slices = svg.selectAll("path")
        .data(pie(pieData))
        .enter()
        .append("path")
        .attr("d", arc)
        .attr("fill", d => color(d.data.label));

    // Add labels to the slices
    const labels = svg.selectAll("text")
        .data(pie(pieData))
        .enter()
        .append("text")
        .attr("transform", d => "translate(" + arc.centroid(d) + ")")
        .attr("dy", "0.35em")
        .text(d => d.data.label);
}

function heatmap(data) {
    // Create a title for the heatmap using the piece name and movement
    d3.select("#title")
        .append("text")
        .text(data[0]['scoreName'] + ", Movement " + data[0]['movement']);

    // create a tooltip
    var tooltip = d3.select("#vis")
        .append("div")
        .style("opacity", 0)
        .attr("class", "tooltip")
        .style("background-color", "white")
        .style("border", "solid")
        .style("border-width", "2px")
        .style("border-radius", "5px")
        .style("padding", "5px")

    // console.log(data)
    rect = svg.selectAll("rect")

    let currentRect;

    const clickHandler = function (event, d) {
        if (currentRect) {
            d3.select(currentRect)
                .style("stroke", "none")
                .style("opacity", 0.8);
        }
        currentRect = this;

        diff = Math.round(d.finger_difficulty * 100) / 100;
        tooltip
            .html("Measure: " + d.measureNumber + "<br>" + "Diff: " + diff + "<br>" + "Tempo: " + d.tempi)
            .style("opacity", 1)
            .style("left", (event.x) + "px")
            .style("top", (event.y) + "px");

        osmdCanvas.style("display", "block");
        osmd.load(xmlMeasures[d.measureNumber - 1]['musicxml']).then(() => osmd.render());

        d3.select(this)
            .style("stroke", "black")
            .style("opacity", 1);
    };

    // group data by measure
    grouped_data = groupBy(data, 'measureNumber')


    // sum the difficulty for each measure
    measure_difficulty = []
    for (var key in grouped_data) {
        measure_difficulty.push({
            measureNumber: key,
            finger_difficulty: grouped_data[key].reduce((a, b) => a + b.finger_difficulty, 0),
            // make a list of all the tempi (only repeat if tempo changes)
            tempi: [...new Set(grouped_data[key].map(item => item.tempo))],
        })
    }


    rect.data(measure_difficulty)
        .enter()
        .append("rect")
        .attr("width", width / 20)
        .attr("height", 30)
        // .attr("height", height / Math.ceil(data.length / 20))
        .attr("x", function (d, i) {
            return (i % 20) * (width / 20 + 2)
        })
        .attr("y", function (d, i) {
            return Math.floor(i / 20) * (30 + 2)
        })
        // .attr("y", function (d, i) {
        //     return Math.floor(i / 20) * (height / Math.ceil(data.length / 20) + 2)
        // })
        .attr("rx", 4)
        .attr("ry", 4)
        // .style("fill", function(d) { return myColor(d.value)} )
        .style("stroke-width", 4)
        .style("stroke", "none")
        .style("opacity", 0.8)
        .style("fill", function (d) {
            return myColor(d.finger_difficulty)
        })
        // .attr("fill", function (d) {
        //     return d3.interpolateRdYlGn(d.finger_difficulty / 100)
        // })
        // .on("mouseover", mouseover)
        // .on("mousemove", mousemove)
        // .on("mouseleave", mouseleave)
        .on("click", clickHandler);

}

var groupBy = function (xs, key) {
    return xs.reduce(function (rv, x) {
        (rv[x[key]] = rv[x[key]] || []).push(x);
        return rv;
    }, {});
};

