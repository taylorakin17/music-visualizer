canvas = d3.select(".canvas")
// const height = 900
const marginLeft = 125
const marginTop = 130
// const svg = d3.select(DOM.svg(width, height))
//     .attr('viewBox', `-${marginLeft} -${marginTop} ${width} ${height}`)

const width = 800
const height = 400
svg = canvas.append("svg")
    .attr("width", width + 100)
    .attr("height", height + 100)

data_simple = [1, 2, 3]

rect = svg.selectAll("rect")

// Build color scale
const myColor = d3.scaleLinear()
    .range(["#eeeeee", "red"])
    .domain([1, 300])


fetch('/get_heatmap_data')
    .then(response => response.json())
    .then(data => {
        heatmap(data)
    });

function heatmap(data) {

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
        .attr("width", "100px")
        .attr("height", "100px")

    console.log(data)
    rect = svg.selectAll("rect")

    // Three function that change the tooltip when user hover / move / leave a cell
    const mouseover = function (event, d) {
        tooltip
            .style("opacity", 1)
        d3.select(this)
            .style("stroke", "black")
            .style("opacity", 1)
    }
    const mousemove = function (event, d) {
        // truncate d.finger_difficulty to 2 decimal places
        diff = Math.round(d.finger_difficulty * 100) / 100
        tooltip
            .html("Measure: " + d.measureNumber + "<br>" + "Diff: " + diff)
            .style("left", (event.x) + "px")
            .style("top", (event.y) + "px")
    }
    const mouseleave = function (event, d) {
        tooltip
            .style("opacity", 0)
        d3.select(this)
            .style("stroke", "none")
            .style("opacity", 0.8)
    }

    // group data by measure
    grouped_data = groupBy(data, 'measureNumber')


    // sum the difficulty for each measure
    measure_difficulty = []
    for (var key in grouped_data) {
        measure_difficulty.push({
            measureNumber: key,
            finger_difficulty: grouped_data[key].reduce((a, b) => a + b.finger_difficulty, 0)
        })
    }
    console.log(measure_difficulty)


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
            console.log(d);
            return myColor(d.finger_difficulty)
        })
        // .attr("fill", function (d) {
        //     return d3.interpolateRdYlGn(d.finger_difficulty / 100)
        // })
        .on("mouseover", mouseover)
        .on("mousemove", mousemove)
        .on("mouseleave", mouseleave)

}

var groupBy = function (xs, key) {
    return xs.reduce(function (rv, x) {
        (rv[x[key]] = rv[x[key]] || []).push(x);
        return rv;
    }, {});
};



