<?php

#Initialize parameters
$min_year = 1937;
$max_year = 2020;
$year = $max_year;
$most_pop = true;
$sex = 'B';
$names = [];
$n = 0;
$data = [];

#Load most popular data
$pop_states = file_get_contents("mostPopStates.json");
$pop_nat = file_get_contents("mostPopNat.json");
$gray_connection = file_get_contents("grayConnection.json");

#If names are already entered as GET requests (if link was shared), then
#sanitize, format, remove duplicates
if ((isset($_GET["name1"])) || (isset($_GET["name2"])) || (isset($_GET["name3"])) 
    || (isset($_GET["name4"])) || (isset($_GET["name5"]))) {
  for ($i=1; $i<6; $i++) {
    if (isset($_GET["name".$i])) {
      $new = ucwords(strtolower(preg_replace('/[^a-zA-Z]/','',
                      htmlentities($_GET["name".$i]))));
      if (strlen($new)>15) {
        $new = substr($new,0,15);
      }
      if (($new != "") && !(in_array($new,$names))) {
        array_push($names, $new);
      }
    }
  }

  #if some names still exist after filtering, adjust map mode away from
  #showing most popular data, find relevant json data files for names,
  #and set up array to use with map.
  if ($names != []) {
    $n = count($names);
    $most_pop = false;
    for ($i = 0; $i < $n; $i++) {
      $file_name = "namesData/".substr($names[$i], 0, 1)."/".$names[$i].".json";
      if (file_exists($file_name)) {
        array_push($data, json_decode(file_get_contents($file_name)));
      } else {
        array_push($data, []);
        for ($y = $min_year; $y < $max_year+1; $y++) {
            array_push($data[$i], []);
            for ($j = 0 ;$j < 52; $j++) {
              array_push($data[$i][$y - $min_year], 0);
            }
          }
      } 
    }
  }
}

#set year if requested
if (isset($_GET["year"])) {
  $year_in = htmlentities($_GET["year"]);
  if (is_numeric($year_in)) {
    $year_in = intval($year_in);
    if (($year_in<$max_year+1) && ($year_in>$min_year-1)) {
      $year = $year_in;
    }
  }
}

#set sex if requested
if (isset($_GET["sex"])) {
  $sex_in = htmlentities($_GET["sex"]);
  if (in_array($sex,['B','F','M'])) {
    $sex = $sex_in;
  }
}

?>


<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Interactive map of popular baby names in the USA</title>
		<link rel="stylesheet" 
    href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="stylesheet" 
    href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    <link rel="stylesheet" href="myMap.css">
	</head>

	<body>
    <nav class="navbar navbar-expand-md navbar-light" style="background-color:#aaaaaa;">
	    <a class="navbar-brand headline" href="javascript:void(0);" onclick="funButton()">
        Popular Baby Names
      </a>
	    <button id="hamburger" class="navbar-toggler" type="button" data-toggle="collapse" 
      data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" 
      aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
  	  </button>
  	  <div class="collapse navbar-collapse" id="navbarSupportedContent">
  	    <ul class="navbar-nav ml-auto">
  		    <li class="nav-item sexChoice">
            <a class="nav-link sexChoice" href="javascript:void(0);" id="menuF" 
            onclick="menuFunctionSex('F')">
              Girl Names<span id="menuFsr" class="sr-only"></span>
            </a>
          </li>
          <li class="nav-item sexChoice">
            <a class="nav-link sexChoice" href="javascript:void(0);" id="menuM" 
            onclick="menuFunctionSex('M')">
              Boy Names <span id="menuMsr" class="sr-only"></span>
            </a>
          </li>
          <li class="nav-item active sexChoice">
      	    <a class="nav-link active sexChoice" href="javascript:void(0);" id="menuB" 
            onclick="menuFunctionSex('B')">
              Both <span id="menuBsr" class="sr-only">(current)</span>
            </a>
          </li>
          <li class="nav-item dropdown sexChoice">
            <a class="nav-link dropdown-toggle sexChoice" href="#" id="menuCustom" 
            role="button" data-toggle="dropdown" aria-haspopup="true" 
            aria-expanded="false">
              Custom Selection <span id="menuCustomsr" class="sr-only"></span>
            </a>
            <div class="dropdown-menu" style="background-color:#aaaaaa;" id="dd" 
            aria-labelledby="navbarDropdown">
              <div class="px-1">
                <p>Enter names to see their relative popularity</p>
              </div>
              <div class="dropdown-divider"></div>
              <form class="px-1 py-2">
                <div class="form-group nameTxtBox">
                  <input type="text" class="form-control mb-1" id="name1" />
                  <input type="text" class="form-control mb-1" id="name2" />
                  <input type="text" class="form-control mb-1" id="name3" />
                  <input type="text" class="form-control mb-1" id="name4" />
                  <input type="text" class="form-control" id="name5" />
                </div>
                <button id="submitNames" type="button" class="btn btn-outline-light">
                  Submit
                </button>
                <button id="clearFields" type="button" class="btn btn-outline-light">
                  Clear
                </button>
              </form>
              <div id="flash" class="px-1"></div>
            </div>
          </li>
        </ul>
      </div>
    </nav>

    <div class="container pt-3">
      <div class="row mt-4">
        <div id="map" class="col-md-9 col-12">
          <?php require_once "usa.svg"; ?>
        </div>
        <div id="results" class="mt-5 col-md-3 col-12"></div>
      </div>

      <div id="controls">
        <div id="rangeDiv" class="row mt-2">
          <input id="sldYear" type="range" class="custom-range color-info" step="1" />
        </div>

        <div class="row mt-1">
          <div class="col-6 col-md-2 btn-group my-auto">
            <button id="back" type="button" value="back" class="btn btn-outline-primary">
              <i class="fa fa-step-backward"></i>
            </button>
            <button id="play" type="button" value="play" class="btn btn-outline-primary">
              <i class="fa fa-play"></i>
            </button>
            <button id="next" type="button" value="next" class="btn btn-outline-primary">
              <i class="fa fa-step-forward"></i>
            </button>
          </div>

          <div class="col-6 col-md-2 my-auto custom-control custom-switch my-auto">
            <input type="checkbox" class="custom-control-input ml-xs-2 ml-sm-2" 
            id="seeNames" checked="true">
            <label class="custom-control-label ml-xs-2 ml-sm-2" for="seeNames">
              Show names
            </label>
          </div>
        </div>
      </div>
    </div>
    
    <div id="about" class="row mt-3">
      <h3>About</h3>
        <p>
          This interactive map shows the most popular baby names for each US state 
          and DC by year (1937 to 2020) according to the Social Security Administration. 
          The data used is provided on 
          <a href="https://www.ssa.gov/oact/babynames/index.html">their website</a>. 
          As explained on their site, they do not include any name in the data that 
          occured fewer than five times in a state. They limit each name to its 
          first 15 letters after removing spaces and any puntuation. 
          They also only present names with the very first letter capitalized 
          and all others in lower case. So this is all true for when you enter a 
          custom choice into the map as well. For instance, "Matthew Alexander" 
          and "mAtThEwAlExAnDeRrRrR" are both considered to be the single name 
          "Matthewalexande" in the map above. Check out the SSA's 
          <a href="https://www.ssa.gov/oact/babynames/background.html">Background 
          Information</a> page for more about their methods. 
          They also have some visualizations of their own.
        </p>

        <p>
          Tip: click the title to quickly shuffle the colors if you don't 
          like the current selection.
        </p>

        <p>
          I made this map after my friend shared 
          <a href="https://jezebel.com/map-sixty-years-of-the-most-popular-names-for-girls-s-1443501909">
          this gif</a> with me of the most popular names for girls by state from 1960 to 2012. 
          I wanted to know the rest of the story. I also wanted to teach myself some basic web dev 
          stuff so I ripped off the idea and tried to make it more interactive. I hope that you enjoy it.
        </p>

        <p>
          The map is a modified version of <a href="https://simplemaps.com/resources/svg-us">this US map</a>.
        </p>
      </div>

      <div id="popup"></div>

    </div>

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    <script>
      const mostPopS = <?= $pop_states ?>;
      const mostPopN = <?= $pop_nat ?>;
      const grayConnection = <?= $gray_connection ?>;
      const maxYear = <?= $max_year ?>;
      const minYear = <?= $min_year ?>;
      var names = <?= json_encode($names) ?>;
      var year = <?= $year ?>;
      var n = <?= $n ?>;
      var rawData = <?= json_encode($data) ?>;
      var mostPop = "<?= $most_pop ?>";
      var sex = "<?= $sex ?>";
    </script>
    <script src="myMap.js"></script>	
  </body>
</html>