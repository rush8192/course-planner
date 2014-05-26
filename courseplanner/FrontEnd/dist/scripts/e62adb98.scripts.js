"use strict";angular.module("coursePlannerApp",["ngCookies","ngResource","ngSanitize","ngRoute","googlechart","ui.bootstrap","ngDragDrop"]).config(["$routeProvider",function(a){a.when("/",{templateUrl:"views/dashboard.html",controller:"DashboardCtrl"}).otherwise({redirectTo:"/"})}]),angular.module("coursePlannerApp").controller("DashboardCtrl",["$scope","$modal","$log","$http",function(a,b,c,d){a.awesomeThings=["HTML5 Boilerplate","AngularJS","Karma"],a.chartObject={},a.onions=[{v:"Onions"},{v:100}],a.chartObject.data={cols:[{id:"t",label:"Topping",type:"string"},{id:"s",label:"Progress (%)",type:"number"}],rows:[{c:[{v:"Foo"},{v:3}]},{c:a.onions},{c:[{v:"Olives"},{v:10}]},{c:[{v:"Zucchini"},{v:1}]},{c:[{v:"Pepperoni"},{v:2}]}]},a.chartObject.type="BarChart",a.chartObject.options={title:"Course Progress",legend:"none",hAxis:{maxValue:100}},a.oneAtATime=!1,a.groups=[{title:"Fall - 2010",courses:[{designation:"CS 106A",title:"FOOBAR",description:"Introduction to the engineering of computer applications emphasizing modern software engineering principles: object-oriented design, decomposition, encapsulation, abstraction, and testing. Uses the Java programming language. Emphasis is on good programming style and the built-in facilities of the Java language. No prior programming experience required. Summer quarter enrollment is limited; application required."},{designation:"IHUM",title:"Worst Class Ever",description:"How is a living, thinking human being like, or not like, a machine? This might seem like a new question for the Information Age, yet it has been a preoccupation of our civilization for centuries. From the culmination of the Scientific Revolution in the seventeenth century, philosophers, physiologists, engineers, authors, political actors and artists of every kind have taken humanity¿s measure by comparing humans with machines. Our course follows this tradition.nTogether, we ask a number of questions about what it means to think of the human mind, body, and society as types of machines. How has the machine served as a metaphor for the cosmos and culture? How do we interact with machines, and how have machines influenced literature, performance, and the arts? What separates us from our machines, and are we really as separate as we think we are?nWe explore the shifting boundary lines between the mechanical and the human by considering how humanity has created or imagined machines and our interconnections with them. What do the concepts of ¿machine,¿ ¿human,¿ ¿alive,¿ ¿intelligent¿ and ¿self-aware¿ mean in different times and places, including our own? We will consider how humans may be conceived and designed as well as manipulated as machines, and how our artificial creations may in turn reflect and reflect upon their human creators.nThe philosophical, scientific and ethical questions regarding the relationship of humans to machines are not just the preoccupations of our current moment. These questions have generated long, rich traditions of responses. We must draw upon these if we are to confront our current concerns, not as isolated actors, but as members of an ever-evolving culture."},{designation:"CME 100",title:"Vector Calculus",description:"Computation and visualization using MATLAB. Differential vector calculus: analytic geometry in space, functions of several variables, partial derivatives, gradient, unconstrained maxima and minima, Lagrange multipliers. Integral vector calculus: multiple integrals in Cartesian, cylindrical, and spherical coordinates, line integrals, scalar potential, surface integrals, Greens, divergence, and Stokes theorems. Examples and applications drawn from various engineering fields. Prerequisites: MATH 41 and 42, or 10 units AP credit."}]},{title:"Winter - 2011",courses:[{designation:"CS 106A",title:"Introduction to Computer Programming",description:"Introduction to the engineering of computer applications emphasizing modern software engineering principles: object-oriented design, decomposition, encapsulation, abstraction, and testing. Uses the Java programming language. Emphasis is on good programming style and the built-in facilities of the Java language. No prior programming experience required. Summer quarter enrollment is limited; application required."},{designation:"IHUM",title:"Worst Class Ever",description:"How is a living, thinking human being like, or not like, a machine? This might seem like a new question for the Information Age, yet it has been a preoccupation of our civilization for centuries. From the culmination of the Scientific Revolution in the seventeenth century, philosophers, physiologists, engineers, authors, political actors and artists of every kind have taken humanity¿s measure by comparing humans with machines. Our course follows this tradition.nTogether, we ask a number of questions about what it means to think of the human mind, body, and society as types of machines. How has the machine served as a metaphor for the cosmos and culture? How do we interact with machines, and how have machines influenced literature, performance, and the arts? What separates us from our machines, and are we really as separate as we think we are?nWe explore the shifting boundary lines between the mechanical and the human by considering how humanity has created or imagined machines and our interconnections with them. What do the concepts of ¿machine,¿ ¿human,¿ ¿alive,¿ ¿intelligent¿ and ¿self-aware¿ mean in different times and places, including our own? We will consider how humans may be conceived and designed as well as manipulated as machines, and how our artificial creations may in turn reflect and reflect upon their human creators.nThe philosophical, scientific and ethical questions regarding the relationship of humans to machines are not just the preoccupations of our current moment. These questions have generated long, rich traditions of responses. We must draw upon these if we are to confront our current concerns, not as isolated actors, but as members of an ever-evolving culture."},{designation:"CME 100",title:"Vector Calculus",description:"Computation and visualization using MATLAB. Differential vector calculus: analytic geometry in space, functions of several variables, partial derivatives, gradient, unconstrained maxima and minima, Lagrange multipliers. Integral vector calculus: multiple integrals in Cartesian, cylindrical, and spherical coordinates, line integrals, scalar potential, surface integrals, Greens, divergence, and Stokes theorems. Examples and applications drawn from various engineering fields. Prerequisites: MATH 41 and 42, or 10 units AP credit."}]},{title:"Spring - 2011",courses:[{designation:"CS 106A",title:"Introduction to Computer Programming",description:"Introduction to the engineering of computer applications emphasizing modern software engineering principles: object-oriented design, decomposition, encapsulation, abstraction, and testing. Uses the Java programming language. Emphasis is on good programming style and the built-in facilities of the Java language. No prior programming experience required. Summer quarter enrollment is limited; application required."},{designation:"IHUM",title:"Worst Class Ever",description:"How is a living, thinking human being like, or not like, a machine? This might seem like a new question for the Information Age, yet it has been a preoccupation of our civilization for centuries. From the culmination of the Scientific Revolution in the seventeenth century, philosophers, physiologists, engineers, authors, political actors and artists of every kind have taken humanity¿s measure by comparing humans with machines. Our course follows this tradition.nTogether, we ask a number of questions about what it means to think of the human mind, body, and society as types of machines. How has the machine served as a metaphor for the cosmos and culture? How do we interact with machines, and how have machines influenced literature, performance, and the arts? What separates us from our machines, and are we really as separate as we think we are?nWe explore the shifting boundary lines between the mechanical and the human by considering how humanity has created or imagined machines and our interconnections with them. What do the concepts of ¿machine,¿ ¿human,¿ ¿alive,¿ ¿intelligent¿ and ¿self-aware¿ mean in different times and places, including our own? We will consider how humans may be conceived and designed as well as manipulated as machines, and how our artificial creations may in turn reflect and reflect upon their human creators.nThe philosophical, scientific and ethical questions regarding the relationship of humans to machines are not just the preoccupations of our current moment. These questions have generated long, rich traditions of responses. We must draw upon these if we are to confront our current concerns, not as isolated actors, but as members of an ever-evolving culture."},{designation:"CME 100",title:"Vector Calculus",description:"Computation and visualization using MATLAB. Differential vector calculus: analytic geometry in space, functions of several variables, partial derivatives, gradient, unconstrained maxima and minima, Lagrange multipliers. Integral vector calculus: multiple integrals in Cartesian, cylindrical, and spherical coordinates, line integrals, scalar potential, surface integrals, Greens, divergence, and Stokes theorems. Examples and applications drawn from various engineering fields. Prerequisites: MATH 41 and 42, or 10 units AP credit."}]},{title:"Fall - 2011",courses:[{designation:"CS 106A",title:"Introduction to Computer Programming",description:"Introduction to the engineering of computer applications emphasizing modern software engineering principles: object-oriented design, decomposition, encapsulation, abstraction, and testing. Uses the Java programming language. Emphasis is on good programming style and the built-in facilities of the Java language. No prior programming experience required. Summer quarter enrollment is limited; application required."},{designation:"IHUM",title:"Worst Class Ever",description:"How is a living, thinking human being like, or not like, a machine? This might seem like a new question for the Information Age, yet it has been a preoccupation of our civilization for centuries. From the culmination of the Scientific Revolution in the seventeenth century, philosophers, physiologists, engineers, authors, political actors and artists of every kind have taken humanity¿s measure by comparing humans with machines. Our course follows this tradition.nTogether, we ask a number of questions about what it means to think of the human mind, body, and society as types of machines. How has the machine served as a metaphor for the cosmos and culture? How do we interact with machines, and how have machines influenced literature, performance, and the arts? What separates us from our machines, and are we really as separate as we think we are?nWe explore the shifting boundary lines between the mechanical and the human by considering how humanity has created or imagined machines and our interconnections with them. What do the concepts of ¿machine,¿ ¿human,¿ ¿alive,¿ ¿intelligent¿ and ¿self-aware¿ mean in different times and places, including our own? We will consider how humans may be conceived and designed as well as manipulated as machines, and how our artificial creations may in turn reflect and reflect upon their human creators.nThe philosophical, scientific and ethical questions regarding the relationship of humans to machines are not just the preoccupations of our current moment. These questions have generated long, rich traditions of responses. We must draw upon these if we are to confront our current concerns, not as isolated actors, but as members of an ever-evolving culture."},{designation:"CME 100",title:"Vector Calculus",description:"Computation and visualization using MATLAB. Differential vector calculus: analytic geometry in space, functions of several variables, partial derivatives, gradient, unconstrained maxima and minima, Lagrange multipliers. Integral vector calculus: multiple integrals in Cartesian, cylindrical, and spherical coordinates, line integrals, scalar potential, surface integrals, Greens, divergence, and Stokes theorems. Examples and applications drawn from various engineering fields. Prerequisites: MATH 41 and 42, or 10 units AP credit."}]},{title:"Winter - 2012",courses:[{designation:"CS 106A",title:"Introduction to Computer Programming",description:"Introduction to the engineering of computer applications emphasizing modern software engineering principles: object-oriented design, decomposition, encapsulation, abstraction, and testing. Uses the Java programming language. Emphasis is on good programming style and the built-in facilities of the Java language. No prior programming experience required. Summer quarter enrollment is limited; application required."},{designation:"IHUM",title:"Worst Class Ever",description:"How is a living, thinking human being like, or not like, a machine? This might seem like a new question for the Information Age, yet it has been a preoccupation of our civilization for centuries. From the culmination of the Scientific Revolution in the seventeenth century, philosophers, physiologists, engineers, authors, political actors and artists of every kind have taken humanity¿s measure by comparing humans with machines. Our course follows this tradition.nTogether, we ask a number of questions about what it means to think of the human mind, body, and society as types of machines. How has the machine served as a metaphor for the cosmos and culture? How do we interact with machines, and how have machines influenced literature, performance, and the arts? What separates us from our machines, and are we really as separate as we think we are?nWe explore the shifting boundary lines between the mechanical and the human by considering how humanity has created or imagined machines and our interconnections with them. What do the concepts of ¿machine,¿ ¿human,¿ ¿alive,¿ ¿intelligent¿ and ¿self-aware¿ mean in different times and places, including our own? We will consider how humans may be conceived and designed as well as manipulated as machines, and how our artificial creations may in turn reflect and reflect upon their human creators.nThe philosophical, scientific and ethical questions regarding the relationship of humans to machines are not just the preoccupations of our current moment. These questions have generated long, rich traditions of responses. We must draw upon these if we are to confront our current concerns, not as isolated actors, but as members of an ever-evolving culture."},{designation:"CME 100",title:"Vector Calculus",description:"Computation and visualization using MATLAB. Differential vector calculus: analytic geometry in space, functions of several variables, partial derivatives, gradient, unconstrained maxima and minima, Lagrange multipliers. Integral vector calculus: multiple integrals in Cartesian, cylindrical, and spherical coordinates, line integrals, scalar potential, surface integrals, Greens, divergence, and Stokes theorems. Examples and applications drawn from various engineering fields. Prerequisites: MATH 41 and 42, or 10 units AP credit."}]},{title:"Spring - 2012",courses:[{designation:"CS 106A",title:"Introduction to Computer Programming",description:"Introduction to the engineering of computer applications emphasizing modern software engineering principles: object-oriented design, decomposition, encapsulation, abstraction, and testing. Uses the Java programming language. Emphasis is on good programming style and the built-in facilities of the Java language. No prior programming experience required. Summer quarter enrollment is limited; application required."},{designation:"IHUM",title:"Worst Class Ever",description:"How is a living, thinking human being like, or not like, a machine? This might seem like a new question for the Information Age, yet it has been a preoccupation of our civilization for centuries. From the culmination of the Scientific Revolution in the seventeenth century, philosophers, physiologists, engineers, authors, political actors and artists of every kind have taken humanity¿s measure by comparing humans with machines. Our course follows this tradition.nTogether, we ask a number of questions about what it means to think of the human mind, body, and society as types of machines. How has the machine served as a metaphor for the cosmos and culture? How do we interact with machines, and how have machines influenced literature, performance, and the arts? What separates us from our machines, and are we really as separate as we think we are?nWe explore the shifting boundary lines between the mechanical and the human by considering how humanity has created or imagined machines and our interconnections with them. What do the concepts of ¿machine,¿ ¿human,¿ ¿alive,¿ ¿intelligent¿ and ¿self-aware¿ mean in different times and places, including our own? We will consider how humans may be conceived and designed as well as manipulated as machines, and how our artificial creations may in turn reflect and reflect upon their human creators.nThe philosophical, scientific and ethical questions regarding the relationship of humans to machines are not just the preoccupations of our current moment. These questions have generated long, rich traditions of responses. We must draw upon these if we are to confront our current concerns, not as isolated actors, but as members of an ever-evolving culture."},{designation:"CME 100",title:"Vector Calculus",description:"Computation and visualization using MATLAB. Differential vector calculus: analytic geometry in space, functions of several variables, partial derivatives, gradient, unconstrained maxima and minima, Lagrange multipliers. Integral vector calculus: multiple integrals in Cartesian, cylindrical, and spherical coordinates, line integrals, scalar potential, surface integrals, Greens, divergence, and Stokes theorems. Examples and applications drawn from various engineering fields. Prerequisites: MATH 41 and 42, or 10 units AP credit."}]},{title:"Fall - 2012",courses:[{designation:"CS 106A",title:"Introduction to Computer Programming",description:"Introduction to the engineering of computer applications emphasizing modern software engineering principles: object-oriented design, decomposition, encapsulation, abstraction, and testing. Uses the Java programming language. Emphasis is on good programming style and the built-in facilities of the Java language. No prior programming experience required. Summer quarter enrollment is limited; application required."},{designation:"IHUM",title:"Worst Class Ever",description:"How is a living, thinking human being like, or not like, a machine? This might seem like a new question for the Information Age, yet it has been a preoccupation of our civilization for centuries. From the culmination of the Scientific Revolution in the seventeenth century, philosophers, physiologists, engineers, authors, political actors and artists of every kind have taken humanity¿s measure by comparing humans with machines. Our course follows this tradition.nTogether, we ask a number of questions about what it means to think of the human mind, body, and society as types of machines. How has the machine served as a metaphor for the cosmos and culture? How do we interact with machines, and how have machines influenced literature, performance, and the arts? What separates us from our machines, and are we really as separate as we think we are?nWe explore the shifting boundary lines between the mechanical and the human by considering how humanity has created or imagined machines and our interconnections with them. What do the concepts of ¿machine,¿ ¿human,¿ ¿alive,¿ ¿intelligent¿ and ¿self-aware¿ mean in different times and places, including our own? We will consider how humans may be conceived and designed as well as manipulated as machines, and how our artificial creations may in turn reflect and reflect upon their human creators.nThe philosophical, scientific and ethical questions regarding the relationship of humans to machines are not just the preoccupations of our current moment. These questions have generated long, rich traditions of responses. We must draw upon these if we are to confront our current concerns, not as isolated actors, but as members of an ever-evolving culture."},{designation:"CME 100",title:"Vector Calculus",description:"Computation and visualization using MATLAB. Differential vector calculus: analytic geometry in space, functions of several variables, partial derivatives, gradient, unconstrained maxima and minima, Lagrange multipliers. Integral vector calculus: multiple integrals in Cartesian, cylindrical, and spherical coordinates, line integrals, scalar potential, surface integrals, Greens, divergence, and Stokes theorems. Examples and applications drawn from various engineering fields. Prerequisites: MATH 41 and 42, or 10 units AP credit."}]}],a.removeCourse=function(a,b){var c=a.indexOf(b);a.splice(c,1)},a.open=function(d,f){var g=b.open({templateUrl:"courseDetailsModalContent.html",controller:e,resolve:{course:function(){return f}}});g.result.then(function(){a.removeCourse(d,f)},function(){c.info("Modal dismissed at: "+new Date)})};var e=function(a,b,c){a.course=c,a.ok=function(){b.close()},a.cancel=function(){b.dismiss("cancel")}};a.list1={title:"AngularJS - Drag Me"},a.foo=!0,a.getLocation=function(a){return d.get("http://maps.googleapis.com/maps/api/geocode/json",{params:{address:a,sensor:!1}}).then(function(a){var b=[];return angular.forEach(a.data.results,function(a){b.push(a.formatted_address)}),b})},a.$watch("asyncSelected",function(){a.asyncSelected=a.asyncSelected.toLowerCase().replace(/,+/g,"")}),a.mm=[{name:"Computer Science",requirement_groups:[{name:"Mathematics",requirements:[{name:"MATH 41",fulfilling:null},{name:"MATH 42",fulfilling:null},{name:"CS 103",fulfilling:null},{name:"CS 109",fulfilling:null},{name:"Elective",fulfilling:null},{name:"Elective",fulfilling:null}]},{name:"Science",requirements:[{name:"PHYS 41",fulfilling:null},{name:"PHYS 43",fulfilling:null},{name:"Elective",fulfilling:null}]},{name:"Technology in Society",requirements:[{name:"TIS",fulfilling:null}]},{name:"Depth",requirements:[{name:"MATH 41",fulfilling:null},{name:"MATH 42",fulfilling:null},{name:"CS 103",fulfilling:null},{name:"CS 109",fulfilling:null},{name:"Elective",fulfilling:null},{name:"Elective",fulfilling:null}]},{name:"Core",requirements:[{name:"PHYS 41",fulfilling:null},{name:"PHYS 43",fulfilling:null},{name:"Elective",fulfilling:null}]},{name:"WIM",requirements:[{name:"TIS",fulfilling:null}]}]},{name:"Physics",requirement_groups:[{name:"Mathematics",requirements:[{name:"MATH 41",fulfilling:null},{name:"MATH 42",fulfilling:null},{name:"Elective",fulfilling:null},{name:"Elective",fulfilling:null}]},{name:"Science",requirements:[{name:"PHYS 41",fulfilling:null},{name:"PHYS 43",fulfilling:null},{name:"Elective",fulfilling:null}]},{name:"Technology in Society",requirements:[{name:"TIS",fulfilling:null}]}]}]}]).directive("disableDrop",function(){return{restrict:"A",scope:{disableDrop:"="},link:function(a,b){a.$watch("disableDrop",function(a){null!=a?b.droppable("option","disabled",!0):b.droppable("option","disabled",!1)})}}}),function(a,b){angular.module("googlechart",[]).constant("googleChartApiConfig",{version:"1",optionalSettings:{packages:["corechart"]}}).provider("googleJsapiUrl",function(){var a="https:",b="//www.google.com/jsapi";this.setProtocol=function(b){a=b},this.setUrl=function(a){b=a},this.$get=function(){return(a?a:"")+b}}).factory("googleChartApiPromise",["$rootScope","$q","googleChartApiConfig","googleJsapiUrl",function(c,d,e,f){var g=d.defer(),h=function(){var a={callback:function(){var a=e.optionalSettings.callback;c.$apply(function(){g.resolve()}),angular.isFunction(a)&&a.call(this)}};a=angular.extend({},e.optionalSettings,a),b.google.load("visualization",e.version,a)},i=a.getElementsByTagName("head")[0],j=a.createElement("script");return j.setAttribute("type","text/javascript"),j.src=f,j.addEventListener?j.addEventListener("load",h,!1):j.onreadystatechange=function(){("loaded"===j.readyState||"complete"===j.readyState)&&(j.onreadystatechange=null,h())},i.appendChild(j),g.promise}]).directive("googleChart",["$timeout","$window","$rootScope","googleChartApiPromise",function(a,b,c,d){return{restrict:"A",scope:{chart:"=chart",onReady:"&",select:"&"},link:function(b,e){function f(a,c,d){if("undefined"!=typeof b.chart.formatters[a]){if(null==b.formatters[a])if(b.formatters[a]=new Array,"color"===a)for(var e=0;e<b.chart.formatters[a].length;e++){for(var f=new c,g=0;g<b.chart.formatters[a][e].formats.length;g++){var h=b.chart.formatters[a][e].formats[g];"undefined"!=typeof h.fromBgColor&&"undefined"!=typeof h.toBgColor?f.addGradientRange(h.from,h.to,h.color,h.fromBgColor,h.toBgColor):f.addRange(h.from,h.to,h.color,h.bgcolor)}b.formatters[a].push(f)}else for(var g=0;g<b.chart.formatters[a].length;g++)b.formatters[a].push(new c(b.chart.formatters[a][g]));for(var g=0;g<b.formatters[a].length;g++)b.chart.formatters[a][g].columnNum<d.getNumberOfColumns()&&b.formatters[a][g].format(d,b.chart.formatters[a][g].columnNum);("arrow"===a||"bar"===a||"color"===a)&&(b.chart.options.allowHtml=!0)}}function g(){g.triggered||void 0==b.chart||(g.triggered=!0,a(function(){g.triggered=!1,"undefined"==typeof b.formatters&&(b.formatters={});var c;c=b.chart.data instanceof google.visualization.DataTable?b.chart.data:Array.isArray(b.chart.data)?google.visualization.arrayToDataTable(b.chart.data):new google.visualization.DataTable(b.chart.data,.5),"undefined"!=typeof b.chart.formatters&&(f("number",google.visualization.NumberFormat,c),f("arrow",google.visualization.ArrowFormat,c),f("date",google.visualization.DateFormat,c),f("bar",google.visualization.BarFormat,c),f("color",google.visualization.ColorFormat,c));var d=b.chart.customFormatters;if("undefined"!=typeof d)for(name in d)f(name,d[name],c);var h={chartType:b.chart.type,dataTable:c,view:b.chart.view,options:b.chart.options,containerId:e[0]};b.chartWrapper=new google.visualization.ChartWrapper(h),google.visualization.events.addListener(b.chartWrapper,"ready",function(){b.chart.displayed=!0,b.$apply(function(a){a.onReady({chartWrapper:a.chartWrapper})})}),google.visualization.events.addListener(b.chartWrapper,"error",function(a){console.log("Chart not displayed due to error: "+a.message+". Full error object follows."),console.log(a)}),google.visualization.events.addListener(b.chartWrapper,"select",function(){var a=b.chartWrapper.getChart().getSelection()[0];a&&b.$apply(function(){b.select({selectedItem:a})})}),a(function(){e.empty(),b.chartWrapper.draw()})},0,!0))}function h(){d.then(function(){g()})}b.$watch("chart",function(){h()},!0),c.$on("resizeMsg",function(){a(function(){b.chartWrapper&&h()})})}}}]).run(["$rootScope","$window",function(a,b){angular.element(b).bind("resize",function(){a.$emit("resizeMsg")})}])}(document,window);