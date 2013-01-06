	

			
function init_app(bDebugMode)  {
  if (bDebugMode) { alert("!!!init!!!"); };
  
			if (typeof window.CanvasRenderingContext2D === 'undefined' && typeof G_vmlCanvasManager === 'undefined') {
         if (bDebugMode) { alert("ExCanvas not loaded!"); };
      } else {
        console.log("ExCanvas not loaded."); 
        if (bDebugMode) { alert("ExCanvas loaded!"); };  
      }
  	
		    
		    
		  if (jQuery) {  
				if (bDebugMode) { alert('jQuery is loaded!');   };
			  var jsonstudents = [{"id":"1","name":"Bob","ncyear":"7"},{"id":"2","name":"Brian","ncyear":"9"},{"id":"3","name":"Betty","ncyear":"7"},{"id":"4","name":"Jane","ncyear":"8"},{"id":"5","name":"James","ncyear":"9"},{"id":"6","name":"Jim","ncyear":"10"},{"id":"7","name":"Chris","ncyear":"11"},{"id":"8","name":"Keiran","ncyear":"11"},{"id":"9","name":"Karen","ncyear":"10"},{"id":"10","name":"Jethro","ncyear":"9"}];	
				if (bDebugMode) { alert(jsonstudents); };
				//for stud in jsonstudents {
  			//  alert(stud);	
				//}
				//var paper = new Raphael(x, y, width, height); //option (a)   
        //var paper = new Raphael($( "#chart1" ), 320, 240); //option (b)   

				//var r = Raphael(10, 50, 640, 480);
				var r = Raphael(document.getElementById('chart1'), 640, 480);//document.getElementById('canvas_container'), ; // $("#chart1")
        // Creates pie chart at with center at 320, 200,
        // radius 100 and data: [55, 20, 13, 32, 5, 1, 2]
        r.piechart(320, 240, 100, [55, 20, 13, 32, 5, 1, 2]);	
				$("#chart1").css({zIndex: 0});
				
			}  else {
  		  console.log("jQuery not loaded.");	
  		  if (bDebugMode) { alert('jQuery not loaded!'); }; 
			}
			
			

			
			if (jQuery.ui) {   
				// UI loaded 
				if (bDebugMode) { alert('jQueryUI is loaded!');   };
				$( "#nav-primary ul" ).menu();
				
			  //$( "#testarea" ).accordion();
				//alert($("#nav-primary").height());
				$("#nav-primary").height($("#maincontent.main.wrapper.clearfix").height());
				//alert($("#nav-primary").height());
				if (bDebugMode) { alert('!'); };  
				
				
				//Fix for position issues with menu here...:
				$( ".primarynav" ).position({
          collision: "none"
        });
				
			} else {
  		  console.log("jQueryUI not loaded.");	
  		  if (bDebugMode) { alert('jQueryUI not loaded!'); }; 
			}


			if (jQuery.jqplot) {
  			//console.log("JQPlot loaded");
  			//Use http://docs.roxen.com/pike/7.0/tutorial/strings/sprintf.xml for working out sprintf notation.
				
  			
  			//TODO: From here, this should instead be loaded into the jinja template from the python request.
  			if (bDebugMode) { alert('JQPlot is loaded!'); }; 
  			
  			
        //var plot1 = $.jqplot('chart1', [[3,7,9,1,4,6,8,2,5]]);
  			//var plot1 = $.jqplot('chart1', [[1,2]],{title: '% attaining 5A*-C including English and Maths'  }); 
  			
  			/*
  			date1 = "26/08/2009"// "26/08/2009"
  			date2 = "26/08/2010"// "26/08/2010"
  			date3 = "26/08/2011"// "26/08/2011"
  			date4 = "26/08/2012"// "26/08/2012"
  			if (bDebugMode) { alert('Dates converted for jqplot and bootstrap issues.!'); }; 
  			//See https://groups.google.com/forum/?fromgroups=#!searchin/jqplot-users/bootstrap/jqplot-users/3d7B6np3Ruk/AgVlW2VZZRcJ on how to handle dates with both jqplot and bootstrap.
				var data1 = [[date1, 45], [date2, 56], [date3, 67], [date4, 68]];
  		  var plot1 = $.jqplot ('chart1', [data1], {
  		      //axesDefaults: { labelRenderer: $.jqplot.CanvasAxisLabelRenderer      },
  		      title: '% attaining 5A*-C including English and Maths',
            seriesDefaults:{
              pointLabels: { show: false },
              location: 's'
            },
  		      
            axes: { 
    		      xaxis: { 
      		      label: "Year", 
      		      pad: 1.2, 
      		      renderer: $.jqplot.DateAxisRenderer,
      		      labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
                tickRenderer: $.jqplot.CanvasAxisTickRenderer,
                tickOptions: {
                    // labelPosition: 'middle',
                    angle: 90
                    //formatString: '%b %#y'
                  }
      		      },
    		      yaxis: { label: "%5AC+EM", 
    		               min: 0, 
    		               max: 100,
    		               tickInterval: 10,
                       tickOptions:{
                        formatString:'%.0f'
                          } 
                },
  		      }, 
  		      highlighter: {        
    		      show: true,        
    		      sizeAdjust: 7.5,     
    		      },      
    		    cursor: {        
      		    show: false      
      		    }
		      }
  		  );
  		  */
			} 
			else {
  			//Alternative rendering here.
				if (bDebugMode) { alert('JQPlot is not loaded!'); }; 
  			console.log("JQPlot not loaded.");
  			}
			
			//THESE # .click functions NEED GENERALISING INTO A CLASS THAT TAKES A PARAMETER!
			
			$('.primarynav').click(function (e) {
				if (bDebugMode) { alert("Primary Nav object clicked."); };
  			
				e.stopPropagation(); //Prevents double call after function from bubbling to li after a.
  			var bIsObjectReturn = false
  			
  			currentItem = $(this).attr("id"); //Note MUST be $(this) for jQuery, and not simply 'this'.
				currentItemClasses = $(this).attr("class");
				
				if ($(this).hasClass("objectReturn")){bIsObjectReturn = true }; //Probably best to build in type of object at this point?
				
				//Temp:
				//alert('clicked on ' + currentItem);
				currentSection = currentItem.split("-")[0];
				currentSpecific = currentItem.split("-")[1];
				currentGetURI = '/' + currentSection + '/' + currentSpecific; //Where '/developer/schoollist' --> split of currentItem.
				if (bDebugMode) { alert("" + currentGetURI); };
				
				//TODO: [d] Add Google Analytics *virtual pageview* here.
				
				if (bIsObjectReturn === false) {
  				$.get(currentGetURI, function(data) {
    				$('#maincontent').html(data); //Google Analytics event tracking should be within the item itself.
    				
  				});
  				$('#loader').hide();
        } else {
         //Return the object.
         //TODO: [e] This is just by redirecting?
          if (bDebugMode) { alert("Redirecting to object.."); };
          window.location.href = currentGetURI;
        };				
			});
			
		    
		    $('#dev-crudtest').click(function (e) {    
			    e.stopPropagation(); //Prevents double call after function from bubbling to li after a.
				  $.get('/developer/crudtest', function(data) {
				  $('#maincontent').html(data);
				 });
		    });	
  
		    
};

function formButtonClick_Browse(e) {
  // #TODO: [e] Rename into something create dataset specific, or make more general. [refactor]
  //alert('clicked');
  alert(e);
  
  //Will return something like: datasource-browsebutton-attendance
  //From this, get the span for (a) path display and (b) validation
  arr = e.split("-");
  //alert(arr[1]);
  a = e.replace(arr[1], "pathvalue");
  b = e.replace(arr[1], "validationvalue");
  alert(a);
  alert(b);
  $('#'+a).text("Path to file here");
  $('#'+b).text("Whether matched validation.");
  
};

/*
function jqplotDateConversion(datestring){
  //Assumes "26/08/2009" format of string.
  arr = datestring.split("/");
  alert(''+arr[0]);
  alert(''+arr[1]);
  alert(''+arr[2]);
  newdate = Date(arr[2], arr[1], arr[0]).getTime());
  return newdate;
};*/