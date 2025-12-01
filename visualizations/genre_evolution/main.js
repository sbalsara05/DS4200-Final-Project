
d3.csv("../../data/visualizations/monthly_genre_trends.csv").then(data => {

  data.forEach(d => {
    d.count = +d.count;
    d.month = d3.timeParse("%Y-%m")(d.month);
  });

// grouping genres for each line
const genres = d3.groups(data, d => d.macro_genre);

let 
  width = 1000,
  height = 800;

let margin = {
  top:50,
  bottom:50,
  left:50,
  right:50
}

let svg = d3.select('body')
            .append('svg')
            .attr('width', 1200)
            .attr('height', height)
            .style('background', 'lightyellow')

//define the scales
let yScale = d3.scaleLinear()
              .domain([0, d3.max(data, d => d.count)])
              .range([height - margin.bottom, margin.top])

let xScale = d3.scaleTime()
              .domain(d3.extent(data, d => d.month))
              .range([margin.left, width - margin.right])

// color for each genre
let color = d3.scaleOrdinal()
  .domain(genres.map(d => d[0]))
  .range(d3.schemeTableau10);

//draw the axis
let xAxis = svg.append('g')
              .call(d3.axisBottom().scale(xScale))
              .attr('transform', `translate(0, ${height - margin.bottom})`)

let yAxis = svg.append('g')
              .call(d3.axisLeft().scale(yScale))
              .attr('transform', `translate(${margin.left}, 0)`)

//Draw the labels
svg.append('text')
    .attr('x', width/2)
    .attr('y', height - 15)
    .text('Month')
    .style('text-anchor', 'middle')

  
    
svg.append('text')
  .attr('x', 0-height/2)
  .attr('y', 10)
  .text('Number of Songs')
  .style('text-anchor', 'middle')
  .attr('transform', 'rotate(-90)')


//draw the line
let line = d3.line()
            .x(d => xScale(d.month))
            .y(d => yScale(d.count))
            .curve(d3.curveMonotoneX)

svg.selectAll(".genre-line")
  .data(genres)
  .enter()
  .append("path")
  .attr("class", "genre-line")
  .attr("fill", "none")
  .attr("stroke", d => color(d[0]))
  .attr("stroke-width", 2)
  .attr("d", d => line(d[1]));

//creating legend for genres
let legend = svg.append("g")
  .attr("class", "legend")
  .attr("transform", `translate(${width - margin.right + 20}, ${margin.top})`);

  genres.forEach((d, i) => {
    let g = legend.append("g")
                  .attr("transform", `translate(0, ${i * 20})`); 
  
    g.append("rect")
     .attr("width", 15)
     .attr("height", 15)
     .attr("fill", color(d[0]));
  
    // text label
    g.append("text")
     .attr("x", 20)
     .attr("y", 12) 
     .text(d[0])
     .style("font-size", "12px")
     .attr("alignment-baseline", "middle");
  });
  


});
