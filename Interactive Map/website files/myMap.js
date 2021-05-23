/* =====================================================
CONSTANTS and VARIABLES 
================================================ */

const states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 
'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 
'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'];

const statesWLines = ['RI','CT','NJ','MA','VT','NH','DC','MD','DE'];
const statesNCentered = ['RI','CT','NJ','MA','DC','MD','DE'];
const statesBottom = ['AK','HI','TX','FL','LA'];
const statesRight = ['ME','NH','VT','MA','CT','RI','NY','PA','NJ','MD','DE','DC','VA','WV','OH','KY','TN','IN','MI','NC','SC','GA','FL','AL','MS','IL','WI'];
const boyGirlBoth = {'F':'Girl', 'M':'Boy', 'B':''};

const grays = ["#606060","#696969","#787878","#888888","#989898","#686868","#707070","#808080","#909090","#A8A8A8","#A0A0A0","#A9A9A9",
"#B0B0B0","#BEBEBE","#C8C8C8","#B8B8B8","#C0C0C0","#D0D0D0","#D3D3D3","#DCDCDC","#E0E0E0","#E8E8E8","#D8D8D8","#F0F0F0","#F5F5F5"];


const popNameColors = {"Mary":0, "Linda":1, "Lisa":2, "Jennifer":3, "Jessica":4, "Ashley":5, 
"Emily":6, "Emma":7, "Isabella":8, "Sophia":9, "Olivia":10, "Robert":11, "James":12, 
"Michael":13, "David":14, "Jacob":15, "Noah":16, "Liam":17};

var popColors = ["#56C6A9","#B55A30","#9BB7D4","#FDAC53","#0072B5","#A0DAA9","#926AA6","#00A170","#D2386C",
"#4B5335","#F5DF4D","#FFA500","#798EA4","#CD212A","#00758F","#6B5876","#E8A798","#FA7A35"];

var colors = ['#FDAC53', '#9BB7D4', '#B55A30', '#F5DF4D', '#0072B5', '#A0DAA9', '#E9897E', '#00A170', '#D2386C'];
var winners = [];
var customData = {};



/* =====================================================
FUNCTIONS 
================================================ */


function manageIncoming(rawData) {
	for (i=0;i<n;i++) {
      	if (rawData[i] === -1) {
      		rawData[i] = [];
      		for (y=minYear;y<maxYear+1;y++) {
      			rawData[i].push([]);
      			for (j=0;j<52;j++) {
      				rawData[i][y-minYear].push(0);
      			}
      		}
      	}
      }
      customData = {};
      for (y=minYear;y<maxYear+1;y++) {
      	customData[y] = {'NAT':[]};
      	for (i=0;i<n;i++) {
      		customData[y]['NAT'].push(rawData[i][y-minYear][0]);
      	}
      	for (j=0;j<51;j++) {
      		customData[y][states[j]] = [];
      		for (i=0;i<n;i++) {
      			customData[y][states[j]].push(rawData[i][y-minYear][j+1]);
      		}
      	}
      }
}


function funButton() {
	shuffleColors();
	update();
}


function menuFunctionSex(newSexChoice) {
	mostPop = true;
	sex = newSexChoice;
	update();
	if ($("#seeNames").prop("checked")==true) {
		$(".lineTo").css("display","block");
	}
	$(".sexChoice").removeClass("active");
	$(".sr-only").html("");
	$("#menu"+sex).addClass("active");
	$("#menu"+sex+"sr").html("(current)");
	$(".navbar-collapse").collapse('hide');

}

function convertHexToRGBA(hex) {
	conv = {'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'A':10,'B':11,'C':12,'D':13,'E':14,'F':15};
	second = hex.slice(3,5);
	third = hex.slice(5,7);
	first = conv[hex.slice(1,2)]*16+conv[hex.slice(2,3)];
	second = conv[hex.slice(3,4)]*16+conv[hex.slice(4,5)];
	third = conv[hex.slice(5,6)]*16+conv[hex.slice(6)];
	return "rgba("+first+","+second+","+third+",0.3)";

}

function shufflePop() {
	i = popColors.length;
  	while (i != 0) {
    	j = Math.floor(Math.random() * i);
    	i -= 1;
    	store = popColors[i];
    	popColors[i] = popColors[j];
    	popColors[j] = store;
  	}
  	i = grays.length;
  	while (i != 0) {
    	j = Math.floor(Math.random() * i);
    	i -= 1;
    	store = grays[i];
    	grays[i] = grays[j];
    	grays[j] = store;
    }
}

function shuffleCustom() {
	i = colors.length;
  	while (i != 0) {
    	j = Math.floor(Math.random() * i);
    	i -= 1;
    	store = colors[i];
    	colors[i] = colors[j];
    	colors[j] = store;
  	}
}

function shuffleColors() {
	if (mostPop) {
		shufflePop();
	} else {
		shuffleCustom();	
	}
}


function colorMap() {
	for (state of states) {
		maxTemp = Math.max.apply(null, customData[year][state]);
		winTemp = [];
		for (i=0; i<n; i++) {
			if (customData[year][state][i] == maxTemp) {
				winTemp.push(i);
			}
		};
		if (maxTemp == 0) {
			$("#"+state).css("fill", "#CCCCCC");
			$("#txt"+state).html("");
			if (statesWLines.includes(state)) {
				$("#path"+state).css("display", "none");
			}
		} else if (winTemp.length == 1) {
			$("#"+state).css("fill",colors[winTemp[0]]);
			$("#txt"+state).html(names[winTemp[0]]);
			if ($("#seeNames").prop("checked")==true) {
				if (statesWLines.includes(state)) {
					$("#path"+state).css("display", "block");
				} 
			} else {
				if (statesWLines.includes(state)) {
					$("#path"+state).css("display", "none");
				}
			}
		} else if (winTemp.length >= 2) {
			T = [colors[winTemp[0]]];
			for (i=1;i<winTemp.length;i++) {
				k=0;
				for (j=0;j<winners.length;j++) {
					if (winTemp[i] == winners[j][0]) {
						T.push(T[0]);
						T[0] = colors[winTemp[i]];
						k=1;
						break;
					}
				}
				if (k==0) {
					T.push(colors[winTemp[i]]);
				}
			}
			back_name = "#backgCol";
			fill_name = "url(#diagonalHatch";
			for (i=0;i<winTemp.length;i++) {
				back_name += winTemp[i];
				fill_name += winTemp[i];
			}
			fill_name += ")";
			$(back_name).css("fill",T[0]);
			for (i=0;i<winTemp.length - 1;i++) {
				stripe_name = "#stripeCol" + i;
				for (j=0;j<winTemp.length;j++) {
					stripe_name += winTemp[j];
				}
				$(stripe_name).css("stroke",T[i+1]);
			}
			$("#"+state).css("fill",fill_name);
			$("#txt"+state).html("");
			if (statesWLines.includes(state)) {
				$("#path"+state).css("display", "none");
			}
		}
	}
}

function whoWon() {
	maxTemp = -1;
	winners = [];
	colTemp = [];
	for (i=0; i<n; i++) {
		if (customData[year]['NAT'][i] > maxTemp) {
			winners = [names[i]];
			colTemp = [colors[i]];
			maxTemp = customData[year]['NAT'][i];
		} else if (customData[year]['NAT'][i] == maxTemp) {
			winners.push(names[i]);
			colTemp.push(colors[i]);
		}
	};
	$("#Yspan").html(year);
	$("#Wspan").html(winners[0])
	.css("fill", colTemp[0]);
	
}


function updateTotal() {
	if (mostPop) {
		L = mostPopN[sex][year].length;
		headline = "Most Popular<br>" + boyGirlBoth[sex] + " Names in " + year;
		words = "<h5>Top "+boyGirlBoth[sex]+" Names</h5><table class='table table-hover table-borderless table-sm'>";
		for (i=0; i<L; i++) {
			words = words + "<tr><td>" + mostPopN[sex][year][i][0] + "</td><td>" + mostPopN[sex][year][i][1] + "</td></tr>";
		}
		words += "</table>";
		$("#Yspan").html(year);
		$("#Wspan").html(mostPopN[sex][year][0][0])
		.css("fill", popColors[popNameColors[mostPopN[sex][year][0][0]]]);
	} else {
		headline = "Relative popularity of<br>";
		for (name of names) {
			headline = headline + name + ", ";
		}
		headline = headline.substr(0,headline.length-2);
		headline = headline + "<br>in " + year;
		words = "<table class='table table-hover table-borderless table-sm'>";
		T = [];
		for (i=0; i<n; i++) {
			if (customData[year]['NAT'][i] == 0) {
				res = "<5";
			} else {
				res = customData[year]['NAT'][i];
			}
			T.push(['<tr style="background-color:'+convertHexToRGBA(colors[i])+';" onMouseOver="this.style.backgroundColor=&quot;'+colors[i]+'&quot;" onMouseOut="this.style.backgroundColor=&quot;'+convertHexToRGBA(colors[i])+'&quot;"><td>' + names[i] + '</td><td>' + res + '</td><tr>', customData[year]['NAT'][i], i, names[i]]);
		};
		T.sort(function(a, b){return b[1] - a[1]});
		for (i=0; i<n; i++) {
			words += T[i][0];
		}
		words += "</table>";
		winners = [[T[0][2], T[0][3], T[0][1],colors[T[0][2]]]];
		for (i=1;i<T.length;i++) {
			if (T[i][1] == T[0][1]) {
				winners.push([T[i][2],T[i][3],T[i][1],colors[T[i][2]]]);
			} else {
				break;
			}
		}
		$("#Yspan").html(year);
		if (winners.length == 1) {
			$("#Wspan").html(winners[0][1])
			.css("fill", winners[0][3]);
		} else {
			$("#Wspan").html("Tie")
			.css("fill", "#000000");
		}
		
	}
	$(".headline").html(headline);
	$("#results").html(words);
	
}


function updatePopular() {
	$("#Wspan").css("fill", popColors[popNameColors[mostPopN[sex][year][0][0]]])
	.html(mostPopN[sex][year][0][0]);
	$("#Yspan").html(year);
	for (state of states) {
		winner = mostPopS[sex][year][state][0][0];
		if (mostPopS[sex][year][state][0][1] == mostPopS[sex][year][state][1][1]) {
			winner = "";
		}
		$("#txt"+state).html(winner);
		if (winner == mostPopN[sex][year][0][0]) {
			$("#"+state).css("fill", popColors[popNameColors[winner]]);
		} else if (winner == "") {
			winTemp = [mostPopS[sex][year][state][0][0],mostPopS[sex][year][state][1][0]];
			for (i=2; i<5; i++) {
				if (mostPopS[sex][year][state][i][1] == mostPopS[sex][year][state][0][1]) {
					winTemp.push(mostPopS[sex][year][state][i][0]);
				}
			}
			if (winTemp.includes(mostPopN[sex][year][0][0])) {
				temp = "#000000";
				for (i=0;i<winTemp.length;i++) {
					if ((winTemp[i] != mostPopN[sex][year][0][0]) && (winTemp[i] in grayConnection[sex])) {
						temp = grays[grayConnection[sex][winTemp[i]]];
					}
				}
				$("#backgCol24").css("fill",popColors[popNameColors[mostPopN[sex][year][0][0]]]);
				$("#stripeCol024").css("stroke",temp);
				$("#"+state).css("fill","url(#diagonalHatch24)");
			} else {
				temp = "#000000";
				for (i=1;i<winTemp.length;i++) {
					if (winTemp[i] in grayConnection[sex]) {
						temp = grays[grayConnection[sex][winTemp[i]]];
					}
				}
				$("#backgCol34").css("fill",grays[grayConnection[sex][winTemp[0]]]);
				$("#stripeCol034").css("stroke",temp);
				$("#"+state).css("fill","url(#diagonalHatch34)");
			}
		} else {
			$("#"+state).css("fill",grays[grayConnection[sex][winner]]);
		}
	};
}

function makeBoth() {
	mostPopN['B'] = {};
	mostPopS['B'] = {};
	for (i=minYear; i<=maxYear; i++) {
		winTemp = mostPopN['F'][i].concat(mostPopN['M'][i]);
		winTemp.sort(function(a, b){return b[1] - a[1]});
		for (j=10;j<20;j++) {
			if (winTemp[j][1] != winTemp[9][1]) {
				winTemp = winTemp.slice(0,j);
				break;
			}
		}
		mostPopN['B'][i] = winTemp;
		mostPopS['B'][i] = {};
		for (state of states) {
			winTemp = mostPopS['F'][i][state].concat(mostPopS['M'][i][state]);
			winTemp.sort(function(a, b){return b[1] - a[1]});
			for (j=5;j<10;j++) {
				if (winTemp[j][1] != winTemp[4][1]) {
					winTemp = winTemp.slice(0,j);
					break;
				}
			}
			mostPopS['B'][i][state] = winTemp;
		}
	}
}

function getStatePop(state) {
	words = "<h6>" + state + " results " + year + "</h6><table class='table table-hover table-borderless table-sm'>";
	if (mostPop) {
		L = mostPopS[sex][year][state].length;
		for (i=0; i<L; i++) {
			words = words + "<tr><td>" + mostPopS[sex][year][state][i][0] + "</td><td>" + mostPopS[sex][year][state][i][1] + "</td></tr>";
		}
	} else {
		T = [];
		for (i=0; i<n; i++) {
			if (customData[year][state][i] == 0) {
				res = "<5";
			} else {
				res = customData[year][state][i];
			}
			T.push(["<tr style='color:"+colors[i]+";'><td>" + names[i] + "</td><td>" + res + "</td></tr>", customData[year][state][i]]);
		};
		T.sort(function(a, b){return b[1] - a[1]});
		for (i=0; i<n; i++) {
			words += T[i][0];
		};
		words += "</table>";
	}
	$("#popup").html(words);
}

function newCustom() {
	url = "getdata.php?name1=" + $("#name1").prop("value");
	j=2;
	for (i=2; i<6; i++) {
		name = $("#name" + i).prop("value");
		if (name != "") {
			url = url + "&name" + j + "="+name;
			j++;
		}
	};
	fetch(url, { credentials: 'include' })
    .then(function(response) {
      	response.json()
      	.then(function(json) {
      		if (json=="No names have been submitted") {
      			warning = "<p style='color:red'>"+json+"</p>";
      			$("#flash").append(warning);
      			$("#submitNames").prop("disabled",false)
				.html("Submit Names");
				return;
      		}
      		names = json['names'];
      		n = names.length;
      		rawData = json['data'];
      		manageIncoming(rawData);
			mostPop = false;
			update();
			$("#submitNames").prop("disabled",false)
			.html("Submit");
			$(".sexChoice").removeClass("active");
			$(".sr-only").html("");
			$("#menuCustom").addClass("active");
			$("#menuCustomsr").html("(current)");
			$("#dd").collapse("hide");
			$(".navbar-collapse").collapse('hide');
		});
	})
	.catch(function (){
		warning = "<p style='color:red;'>Something went wrong on the server. Sorry about that. Feel free to try again!</p>";
		$("#flash").append(warning);
	});
}

function update() {
	$("#flash").html("");
	$("#sldYear").prop("value", year);
	updateTotal();
	if (mostPop) {
		updatePopular();
	} else {
		colorMap();
	}
	nameSize();
	link = "?year=" + year;
	if (mostPop) {
		link = link + "&sex=" + sex;
	} else {
		for (i=1;i<n+1;i++) {
			link = link + "&name" + i + "=" + names[i-1];
		}
	}
	window.history.pushState('','',link);
}

function step() {
	if (year<maxYear) {
		year++;
	} else {
		year = minYear;
	}
	update();
}

function nameSize() {
	$("#Wspan").removeAttr("textLength");
	$("#Wspan").removeAttr("lengthAdjust");
	if (document.getElementById("Wspan").getComputedTextLength() > Number($("#Wspanrect").attr("width"))) {
		$("#Wspan").attr("textLength",Number($("#Wspanrect").attr("width")))
		.attr("lengthAdjust", "spacingAndGlyphs");
	}

	for (state of states) {
		$("#txt"+state).removeAttr("textLength");
		$("#txt"+state).removeAttr("lengthAdjust");
		$("#"+state+"txt").removeAttr("textLength");
		$("#"+state+"txt").removeAttr("lengthAdjust");
		if (document.getElementById(state+"txt").getComputedTextLength() > Number($("#"+state+"rect").attr("width"))) {
			$("#txt"+state).attr("textLength",Number($("#"+state+"rect").attr("width")))
			.attr("lengthAdjust", "spacingAndGlyphs");
			$("#"+state+"txt").attr("textLength",Number($("#"+state+"rect").attr("width")))
			.attr("lengthAdjust", "spacingAndGlyphs");
		}
	}
}






/* =====================================================
INITIALIZATION
================================================ */


$(document).ready(function () {

	if ($(window).width()<768) {
		$("#controls").addClass("container");
		$("#controls").addClass("px-1");
		$("#rangeDiv").addClass("px-3");
		$("#controls").addClass("fixed-bottom");
		$("#controls").addClass("phoneControls");
		$("#theLink").attr("size","20");
	}

	$('.nameTxtBox').keypress(function(e){
      if(e.keyCode==13) {
      	$('#submitNames').click();
      }
    });

for (state of states) {
	pathStuff = $("#"+state).attr("d");
	document.getElementById(state+'g').insertAdjacentHTML('beforeend','<path d="'+pathStuff+'" id="'+state+'b" class="state stateboundary" />'); 

	$("#"+state+"b").insertAfter("#"+state);

	$("#"+state).addClass("statefill");



	$("#"+state+"g").on("mouseover",function () {
		$("#"+this.id.slice(0,2)+"b").css("stroke","#0000ff")
		.css("stroke-width", "3");
		$(this).appendTo("#statesAndNames");
		getStatePop(this.id.slice(0,2));
		$("#popup").css("display", "block")
		.css("position", "absolute")
		.css("left", (event.pageX + 30) + "px")
		.css("top", event.pageY + "px")
		.css("border","5px solid #BBBBBB")
		.css("padding","10px")
		.css("background-color","rgba(255,255,255,1)");
		if (statesBottom.includes(this.id.slice(0,2))) {
			$("#popup").css("top", (event.pageY - 150) + "px");
		}
		if (statesRight.includes(this.id.slice(0,2))) {
			$("#popup").css("left", (event.pageX - 170) + "px");
		}
	});
	$("#"+state+"g").on("mouseout", function() {
			$("#"+this.id.slice(0,2)+"b").css("stroke","#000000")
			.css("stroke-width", "0.970631");
		})
}

$("#sldYear").attr("max", maxYear)
.attr("min", minYear)
.prop("value", year)
.on("input", function (){
	year = $(this).prop("value");
	update();
});

$("#next").click(function () {
	if (year<maxYear) {
		year++;
	}
	update();
});

$("#back").click(function () {
	if (year>minYear) {
		year--;
	}
	update();
});

$("#play").click(function () {
	if ($(this).attr("value")=="play") {
		$(this).attr("value","pause")
		.html("<i class='fa fa-pause'></i>");
		timer = setInterval(step, 1200);
	} else {
		$(this).attr("value","play")
		.html("<i class='fa fa-play'></i>");
		clearInterval(timer);
	}

});

$("#seeNames").click(function () {
	if ($(this).prop("checked")==true) {
		$(".labels").attr("visibility", "visible");
		for (ST of statesWLines) {
			if ($("#txt"+ST).html() != ""){
				$("#path"+ST).css("display", "block");
			}
		}
		
	} else {
		$(".labels").attr("visibility", "hidden");
		for (ST of statesWLines) {
			$("#path"+ST).css("display", "none");
		}
	}
});



$("#submitNames").click(function () {
	$("#flash").html("");
	checksOut = true;
	for (i=1;i<6;i++) {
		checkstr = $("#name"+i).prop("value");
		if (checkstr.match(/[^A-z\s]/g) != null) {
			checksOut = false;
			break;
		}		
	}
	if (checksOut) {
		$(this).prop("disabled","true")
		.html("<span class='spinner-border spinner-border-sm'></span> Loading..");
		newCustom();
	} else {
		warning = "<p style='color:red'>Please only enter names with letters.</p>";
      	$("#flash").append(warning);
	}
});

$("#statesAndNames").on("mouseleave", function() {
		$("#popup").css("display","none");
});

$("#clearFields").click(function(){
	$("#name1").prop("value","");
	$("#name2").prop("value","");
	$("#name3").prop("value","");
	$("#name4").prop("value","");
	$("#name5").prop("value","");
});

$(document).keydown(function(e){
    if (e.which == 37) {
    	if (year>minYear) {
    		year--;
		}
		update();
		return false;
    }
    if (e.which == 39) {
    	if (year<maxYear) {
    		year++;
		}
		update();
		return false;
    }
});



	x = Number($("#YWrect").attr("x"));
	y = Number($("#YWrect").attr("y"));
	w = Number($("#YWrect").attr("width"));
	h = Number($("#YWrect").attr("height"));
	new_y = y + 0.5*h;
	new_x = x;
	$("#YW").attr("x", ""+new_x)
	.attr("y", ""+new_y)
	.attr("dominant-baseline", "middle");
	$("#YWrect").attr("visibility", "hidden");

	x = Number($("#Wspanrect").attr("x"));
	y = Number($("#Wspanrect").attr("y"));
	w = Number($("#Wspanrect").attr("width"));
	h = Number($("#Wspanrect").attr("height"));
	new_y = y + 0.5*h;
	new_x = x;
	$("#Wspan").attr("x", ""+new_x)
	.attr("y", ""+new_y)
	.attr("dominant-baseline", "middle");
	$("#Wspanrect").attr("visibility", "hidden");

	for (state of states) {
		$("#"+state+"txt").css("font-size", 23);
		x = Number($("#"+state+"rect").attr("x"));
		y = Number($("#"+state+"rect").attr("y"));
		w = Number($("#"+state+"rect").attr("width"));
		h = Number($("#"+state+"rect").attr("height"));
		new_y = y + 0.5*h;
		if (statesNCentered.includes(state)) {
			new_x = x+132;
			$("#"+state+"txt").attr("x", ""+new_x)
			.attr("y", ""+new_y)
			.attr("dominant-baseline", "middle");
			$("#txt"+state).attr("x", ""+new_x)
			.attr("y", ""+new_y)
			.attr("dominant-baseline", "middle");
		} else {
			new_x = 132+x + 0.5*w;
			$("#"+state+"txt").attr("x", ""+new_x)
			.attr("y", ""+new_y)
			.attr("dominant-baseline", "middle")
			.attr("text-anchor", "middle");
			$("#txt"+state).attr("x", ""+new_x)
			.attr("y", ""+new_y)
			.attr("dominant-baseline", "middle")
			.attr("text-anchor", "middle");
		}
		$("#"+state+"rect").attr("visibility", "hidden");
	}
	makeBoth();
	shuffleCustom();
	shufflePop();
	if (!mostPop) {
		manageIncoming(rawData);
		$(".sexChoice").removeClass("active");
		$(".sr-only").html("");
		$("#menuCustom").addClass("active");
		$("#menuCustomsr").html("(current)");
	} else {
		$(".sexChoice").removeClass("active");
		$(".sr-only").html("");
		$("#menu"+sex).addClass("active");
		$("#menu"+sex+"sr").html("(current)");
	}
	update();
	$("#svg").attr("visibility","visible");
});