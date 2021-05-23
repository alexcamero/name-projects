<?php

if (!(isset($_GET["name1"]) || isset($_GET["name2"]) || isset($_GET["name3"]) || isset($_GET["name4"]) || isset($_GET["name5"]))) {
	echo json_encode("No names have been submitted");
	return;
}

$names = [];

for ($i=1; $i<6; $i++) {
	if (isset($_GET["name".$i])) {
		$new = ucwords(strtolower(preg_replace('/[^a-zA-Z]/','',htmlentities($_GET["name".$i]))));
		if (strlen($new)>15) {
				$new = substr($new,0,15);
			}
		if (($new != "") && !(in_array($new,$names))) {
			array_push($names, $new);
		}
	}
}

if ($names == []) {
	echo json_encode("No names have been submitted");
	return;
}

$data = [];


for ($i=0;$i<count($names);$i++) {
	$file_name = "namesData/".substr($names[$i],0,1)."/".$names[$i].".json";
	if (file_exists($file_name)) {
		$data[$i] = json_decode(file_get_contents($file_name));
	} else {
		$data[$i] = -1;
	}	
}


echo json_encode(array("names"=>$names,"data"=>$data)); 

?>