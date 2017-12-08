<?php

$hostname = 'localhost';
$username = 'pi_select';
$password = 'xxxxxxxxxx';

try {
    $dbh = new PDO("mysql:host=$hostname;dbname=measurements",
                               $username, $password);

    /*** The SQL SELECT statement ***/
    $sth = $dbh->prepare("
    SELECT * FROM (
        SELECT `dtg` AS date,
        `level` AS value
        FROM `light`
        ORDER BY date DESC
        LIMIT 0,36
    ) sub
    ORDER BY date ASC
    ");
    $sth->execute();

    /* Fetch all of the remaining rows in the result set */
    $result = $sth->fetchAll(PDO::FETCH_ASSOC);

    /*** close the database connection ***/
    $dbh = null;
}
catch(PDOException $e)
    { echo $e->getMessage(); }

$json_data = json_encode($result);     

?>
<!DOCTYPE html>
<meta charset="utf-8">

<head>
    <style>

    .axis {
      font: 14px sans-serif;
    }

    .axis path,
    .axis line {
      fill: none;
      stroke: #000;
      shape-rendering: crispEdges;
    }

    </style>
</head>

<body>

<script src="http://d3js.org/d3.v3.min.js"></script>

<script>

var margin = {top: 20, right: 20, bottom: 70, left: 60},
    width = 960 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;

// Parse the date / time
var parseDate = d3.time.format("%Y-%m-%d %H:%M:%S").parse;

// specify the scale/range for each dimension
var x = d3.scale.ordinal().rangeRoundBands([0, width], .05);
var y = d3.scale.linear().range([height, 0]);

// axis formatting
var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom")
    .tickFormat(d3.time.format("%H:%M"));
var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left")
    .ticks(10);

// setup the svg area
var svg = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", 
          "translate(" + margin.left + "," + margin.top + ")");

// Get the data
<?php echo "data=".$json_data.";" ?>

// wrangle the data into the correct formats and units
data.forEach(function(d) {
    d.date = parseDate(d.date);
    d.value = +d.value;
});
    
// Scale the range of the data
x.domain(data.map(function(d) { return d.date; }));
y.domain([0, d3.max(data, function(d) { return d.value; })]);

// Add the X Axis
svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis)
  .selectAll("text")
    .style("text-anchor", "end")
    .attr("dx", "-.8em")
    .attr("dy", "-.35em")
    .attr("transform", "rotate(-90)" );

// Add the Y Axis and the Y axis label
svg.append("g")
    .attr("class", "y axis")
    .call(yAxis)
  .append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", -50)
    .attr("dy", ".71em")
   .style("text-anchor", "end")
    .text("Light Level (V)");

// Add the bars
svg.selectAll("bar")
    .data(data)
  .enter().append("rect")
    .style("fill", "steelblue")
    .attr("x", function(d) { return x(d.date); })
    .attr("width", x.rangeBand())
    .attr("y", function(d) { return y(d.value); })
    .attr("height", function(d) { return height - y(d.value); });

</script>

</body>
