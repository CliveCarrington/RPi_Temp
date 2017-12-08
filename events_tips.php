<?php

$hostname = 'localhost';
$username = 'pi_select';
$password = 'xxxxxxxxxx';

try {
    $dbh = new PDO("mysql:host=$hostname;dbname=measurements",
                               $username, $password);

    /*** The SQL SELECT statement ***/
    $sth = $dbh->prepare("
       SELECT dtg
       FROM `events` 
    ");
    $sth->execute();

    /* Fetch all of the remaining rows in the result set */
    $result = $sth->fetchAll(PDO::FETCH_ASSOC);

    /*** close the database connection ***/
    $dbh = null;
}

catch(PDOException $e)
    {
        echo $e->getMessage();
    }

$json_data = json_encode($result);     

?>

<!DOCTYPE html>
<meta charset="utf-8">
<style>

body { font: 12px sans-serif; }

.axis path,
.axis line {
  fill: none;
  stroke: grey;
  shape-rendering: crispEdges;
}

.dot { stroke: none; fill: steelblue; }

.grid .tick { stroke: lightgrey; opacity: 0.7; }
.grid path { stroke-width: 0;}

div.tooltip {
  position: absolute;
  text-align: center;
  width: 80px;
  height: 30px;
  padding: 2px;
  font: 12px sans-serif;
  background: #ddd;
  border: solid 0px #aaa;
  border-radius: 8px;
  pointer-events: none;
}

</style>
<body>
<script src="http://d3js.org/d3.v3.min.js"></script>
<script>

// Get the data
<?php echo "data=".$json_data.";" ?>

// Parse the date / time formats
parseDate = d3.time.format("%Y-%m-%d").parse;
parseTime = d3.time.format("%H:%M:%S").parse;

data.forEach(function(d) {
    dtgSplit = d.dtg.split(" ");     // split on the space
    d.date = parseDate(dtgSplit[0]); // get the date seperatly
    d.time = parseTime(dtgSplit[1]); // get the time seperatly
});

// Get the number of days in the date range to calculate height
var oneDay = 24*60*60*1000; // hours*minutes*seconds*milliseconds
var dateStart = d3.min(data, function(d) { return d.date; });
var dateFinish = d3.max(data, function(d) { return d.date; });
var numberDays = Math.round(Math.abs((dateStart.getTime() -
                           dateFinish.getTime())/(oneDay)));

var margin = {top: 40, right: 20, bottom: 30, left: 100},
    width = 600 - margin.left - margin.right,
    height = numberDays * 8;

var formatDay_Time = d3.time.format("%H:%M"); // Format tooltip time
var formatWeek_Year = d3.time.format("%d-%m-%Y"); // Format tooltip date

var x = d3.time.scale().range([0, width]);
var y = d3.time.scale().range([0, height]);

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom")
    .ticks(7)
    .tickFormat(d3.time.format("%H:%M"));

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left")
    .ticks(7,0,0);

var svg = d3.select("body")
    .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
    .append("g")
        .attr("transform", "translate(" + margin.left + ","
                                        + margin.top + ")");

// State the functions for the grid
function make_x_axis() {
    return d3.svg.axis()
      .scale(x)
      .orient("bottom")
      .ticks(7)
}
        
// Set the domains
x.domain([new Date(1899, 12, 01, 0, 0, 1), 
          new Date(1899, 12, 02, 0, 0, 0)]);
y.domain(d3.extent(data, function(d) { return d.date; }));

// tickSize: Get or set the size of major, minor and end ticks
svg.append("g").classed("grid x_grid", true)
    .attr("transform", "translate(0," + height + ")")
    .style("stroke-dasharray", ("3, 3, 3"))
    .call(make_x_axis()
        .tickSize(-height, 0, 0)
        .tickFormat(""))

// Draw the Axes and the tick labels
svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis)
  .selectAll("text")
    .style("text-anchor", "middle");

svg.append("g")
    .attr("class", "y axis")
    .call(yAxis)
  .selectAll("text")
    .style("text-anchor", "end");


// Tooltip stuff
var div = d3.select("body").append("div")
    .attr("class", "tooltip")
    .style("opacity", 1e-6);


// draw the plotted circles
svg.selectAll(".dot")
    .data(data)
  .enter().append("circle")
    .attr("class", "dot")
    .attr("r", 4.5)
    .style("opacity", 0.5)
    .attr("cx", function(d) { return x(d.time); })
    .attr("cy", function(d) { return y(d.date); })
    .on("mouseover", function(d) {
        div.transition()
            .duration(200)
            .style("opacity", 1);
        div.html(
            formatDay_Time(d.time) + "<br/>"  + 
            formatWeek_Year(d.date) )	
                .style("left", (d3.event.pageX) + "px")
                .style("top", (d3.event.pageY - 36) + "px");
        })  // tooltip

        .on("mouseout", function(d) {
            div.transition()
                .duration(500)
                .style("opacity", 1e-6);
        });    

</script>
</body>
