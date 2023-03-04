function heatmap(data) {

    const svg = d3.select(DOM.svg(w, h))

    const dayLabels = svg.selectAll(".dayLabel")
        .data(days)
        .enter().append("text")
        .text(function (d) { return d; })
        .attr("x", 0)
        .attr("y", function (d, i) { return i * gridSize; })
        .attr("font-size", "9pt")
        .attr("fill", "#aaa")
        .attr("transform", "translate(0," + (margin.left + gridSize / 1.5) + ")")
        .attr("class", "dayLabel mono axis");

    const timeLabels = svg.selectAll(".timeLabel")
        .data(hours)
        .enter().append("text")
        .text(function (d) { return d; })
        .attr("x", function (d, i) { return i * gridSize; })
        .attr("y", 0)
        .style("text-anchor", "middle")
        .attr("transform", "translate(" + (80 + gridSize / 2) + ", 12)")
        .attr("class", "timeLabel mono axis");

    const cards = svg.selectAll(".hour")
        .data(data, function (d) { return d.reservation_hour + ':' + d.index; });


    const cardsEnter = cards.enter().append("rect")
        .attr("x", function (d) { return (d.reservation_hour) * gridSize; })
        .attr("y", function (d) { return (d.index) * gridSize; })
        .attr("transform", "translate(80,20)")
        .attr("rx", 4)
        .attr("ry", 4)
        .attr("class", "hour bordered")
        .attr("width", gridSize)
        .attr("height", gridSize)
        .style("fill", colors[0]);

    cardsEnter.append("title");

    cardsEnter.transition().duration(1000)
        .style("fill", function (d) { return colorScale(d.revenue); });

    cardsEnter.select("title").text(function (d) { return d.revenue; });

    cards.exit().remove();
    return svg.node();
}
