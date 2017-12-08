<?php

$hostname = 'localhost';
$username = 'pi_select';
$password = 'xxxxxxxxxx';

try {
    $dbh = new PDO("mysql:host=$hostname;dbname=measurements",
                               $username, $password);

    /*** The SQL SELECT statement ***/

    $sth = $dbh->prepare("
SELECT *
FROM  downloads
ORDER BY  dtg, book_name
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

body { font: 10px sans-serif;}

text.shadow {
  stroke: white;
  stroke-width: 2px;
  opacity: 0.9;
}

.axis path,
.axis line {
  fill: none;
  stroke: #000;
  shape-rendering: crispEdges;
}

.x.axis path { display: none; }

.area.above { fill: rgb(252,141,89); }
.area.below { fill: rgb(145,207,96); }

.line {
  fill: none;
  stroke: #000;
  stroke-width: 1.5px;
}

</style>
<body>
<script src="http://d3js.org/d3.v3.min.js"></script>
<script>

var title = "Science vs Style - Daily Leanpub Book Sales";

var margin = {top: 20, right: 20, bottom: 50, left: 50},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

var parsedtg = d3.time.format("%Y-%m-%d %H:%M:%S").parse;

var x = d3.time.scale().range([0, width]);
var y = d3.scale.linear().range([height, 0]);

var xAxis = d3.svg.axis().scale(x).orient("bottom");
var yAxis = d3.svg.axis().scale(y).orient("left");

var lineScience = d3.svg.area()
    .interpolate("basis")
    .x(function(d) { return x(d.dtg); })
    .y(function(d) { return y(d["Science"]); });

var lineStyle = d3.svg.area()
    .interpolate("basis")
    .x(function(d) { return x(d.dtg); })
    .y(function(d) { return y(d["Style"]); });

var area = d3.svg.area()
    .interpolate("basis")
    .x(function(d) { return x(d.dtg); })
    .y1(function(d) { return y(d["Science"]); });

var svg = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform",
        "translate(" + margin.left + "," + margin.top + ")");

<?php echo "dataNest=".$json_data.";" ?>

  dataNest.forEach(function(d) {
      d.dtg = parsedtg(d.dtg);
      d.downloaded = +d.downloaded;
  });

  var data = d3.nest()
      .key(function(d) {return d.dtg;})
      .entries(dataNest);

  data.forEach(function(d) {
      d.dtg = d.values[0]['dtg'];
      d["Science"] = d.values[0]['downloaded'];
      d["Style"] = d.values[1]['downloaded'];
  });

  for(i=data.length-1;i>0;i--) {
          data[i].Science   = data[i].Science  -data[(i-1)].Science ;
          data[i].Style     = data[i].Style    -data[(i-1)].Style ;
   }

  data.shift(); // Removes the first element in the array
  
    x.domain(d3.extent(data, function(d) { return d.dtg; }));
    y.domain([
//      d3.min(data, function(d) {
//          return Math.min(d["Science"], d["Style"]); }),
//      d3.max(data, function(d) {
//          return Math.max(d["Science"], d["Style"]); })
      0,1400
    ]);

    svg.datum(data);

    svg.append("clipPath")
        .attr("id", "clip-below")
      .append("path")
        .attr("d", area.y0(height));

    svg.append("clipPath")
        .attr("id", "clip-above")
      .append("path")
        .attr("d", area.y0(0));

    svg.append("a")
      .attr("xlink:href", "https://leanpub.com/datastyle")
      .append("path")
        .attr("class", "area above")
        .attr("clip-path", "url(#clip-above)")
        .attr("d", area.y0(function(d) { return y(d["Style"]); }));

    svg.append("a")
      .attr("xlink:href", "https://leanpub.com/rprogramming")
      .append("path")
        .attr("class", "area below")
        .attr("clip-path", "url(#clip-below)")
        .attr("d", area.y0(function(d) { return y(d["Style"]); }));

    svg.append("path")
        .attr("class", "line")
        .style("stroke", "darkgreen")
        .attr("d", lineScience);

    svg.append("path")
        .attr("class", "line")
        .style("stroke", "red")
        .attr("d", lineStyle);

    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis)
      .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("Daily Downloads from Leanpub");

    // ******* Title Block ********
    svg.append("text") // Title shadow
      .attr("x", (width / 2))
      .attr("y", 50 )
      .attr("text-anchor", "middle")
      .style("font-size", "30px")
      .attr("class", "shadow")
      .text(title);

    svg.append("text") // Title
      .attr("x", (width / 2))
      .attr("y", 50 )
      .attr("text-anchor", "middle")
      .style("font-size", "30px")
      .style("stroke", "none")
      .text(title);

    // ******* Legend Block ********
    var block = 300;   // rectangle width and position
  
    svg.append("rect") // Style Legend Rectangle
      .attr("x", ((width / 2)/2)-(block/2))
      .attr("y", height+(margin.bottom/2) )
      .attr("width", block)
      .attr("height", "25")
      .attr("class", "area above");

    svg.append("rect") // Science Legend Rectangle
      .attr("x", ((width / 2)/2)+(width / 2)-(block/2))
      .attr("y", height+(margin.bottom/2) )
      .attr("width", block)
      .attr("height", "25")
      .attr("class", "area below");

    svg.append("text") // Style Legend Text shadow
      .attr("x", ((width / 2)/2))
      .attr("y", height+(margin.bottom/2) + 5)
      .attr("dy", ".71em")
      .attr("text-anchor", "middle")
      .style("font-size", "18px")
      .attr("class", "shadow")
      .text("The Elements of Data Analytic Style");

    svg.append("text") // Science Legend Text shadow
      .attr("x", ((width / 2)/2)+(width / 2))
      .attr("y", height+(margin.bottom/2) + 5)
      .attr("dy", ".71em")
      .attr("text-anchor", "middle")
      .style("font-size", "18px")
      .attr("class", "shadow")
      .text("R Programming for Data Science");

    svg.append("a")
      .attr("xlink:href", "https://leanpub.com/datastyle")
      .append("text") // Style Legend Text
      .attr("x", ((width / 2)/2))
      .attr("y", height+(margin.bottom/2) + 5)
      .attr("dy", ".71em")
      .attr("text-anchor", "middle")
      .style("font-size", "18px")
      .style("stroke", "none")
      .text("The Elements of Data Analytic Style");

    svg.append("a")
      .attr("xlink:href", "https://leanpub.com/rprogramming")
      .append("text") // Science Legend Text
      .attr("x", ((width / 2)/2)+(width / 2))
      .attr("y", height+(margin.bottom/2) + 5)
      .attr("dy", ".71em")
      .attr("text-anchor", "middle")
      .style("font-size", "18px")
      .style("stroke", "none")
      .text("R Programming for Data Science");

</script>
</body>
