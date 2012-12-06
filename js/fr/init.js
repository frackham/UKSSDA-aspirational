	

			
function init_app(bDebugMode)  {
  if (bDebugMode) { alert("!!!init!!!"); };
  
  	
		    
		    
		  if (jQuery) {  
				if (bDebugMode) { alert('jQuery is loaded!');   };
			  var jsonstudents = [{"id":"1","name":"Bob","ncyear":"7"},{"id":"2","name":"Brian","ncyear":"9"},{"id":"3","name":"Betty","ncyear":"7"},{"id":"4","name":"Jane","ncyear":"8"},{"id":"5","name":"James","ncyear":"9"},{"id":"6","name":"Jim","ncyear":"10"},{"id":"7","name":"Chris","ncyear":"11"},{"id":"8","name":"Keiran","ncyear":"11"},{"id":"9","name":"Karen","ncyear":"10"},{"id":"10","name":"Jethro","ncyear":"9"}];	
				if (bDebugMode) { alert(jsonstudents); };
				//for stud in jsonstudents {
  			//  alert(stud);	
				//}
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
				var data1 = [["26/08/2009", 45], ["26/08/2010", 56], ["26/08/2011", 67], ["26/08/2012", 68]];
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
			} 
			else {
  			//Alternative rendering here.
				if (bDebugMode) { alert('JQPlot is not loaded!'); }; 
  			console.log("JQPlot not loaded.");
  			}
			
			if (typeof window.CanvasRenderingContext2D == 'undefined' && typeof G_vmlCanvasManager == 'undefined') {
         if (bDebugMode) { alert("ExCanvas not loaded!"); };
      } else {
        console.log("ExCanvas not loaded."); 
        if (bDebugMode) { alert("ExCanvas loaded!"); };  
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