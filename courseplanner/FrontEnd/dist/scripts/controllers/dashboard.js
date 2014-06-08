'use strict';

angular.module('coursePlannerApp')
  .controller('DashboardCtrl', function ($scope, $modal, $log, $http, Courses, RefreshService, MM) {
    $scope.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];

    $scope.chartObject = {};

    $scope.onions = [
        {v: 'Onions'},
        {v: 100}
    ];

    $scope.chartObject.data = {'cols': [
        {id: 't', label: 'Topping', type: 'string'},
        {id: 's', label: 'Progress (%)', type: 'number'}
      ], 'rows': [
        {c: [
            {v: 'Foo'},
            {v: 3}
          ]},
          {c: $scope.onions},
          {c: [
            {v: 'Olives'},
            {v: 10}
          ]},
        {c: [
            {v: 'Zucchini'},
            {v: 1}
          ]},
        {c: [
            {v: 'Pepperoni'},
            {v: 2}
          ]}
    ]};

    $scope.addMM = function () {
        var getAll = $scope.getAllCourses;
        var modalInstance = $modal.open({
            templateUrl: 'addMMModal.html',
            controller: AddMMModalInstanceCtrl,
            resolve: {
            }
        });
    };

    var AddMMModalInstanceCtrl = function ($scope, $modalInstance) {
        //$scope.selectedMM = [{designation:"FOO"},{designation:"BAR"}];
        $scope.selectedMM = [];
        $scope.addToSelected = function($item,$model,$label) {
            $scope.selectedMM.push($item);
        }
        $scope.ok = function () {
            $modalInstance.close();
            for (var i in $scope.selectedMM) {
                MM.add({ps_key:$scope.selectedMM[i].ps_key});
            }
        };

        $scope.cancel = function () {
            $modalInstance.dismiss('cancel');
        };

        $scope.searchForMM = function(val) {
            return MM.query({prefix:val})
            .$promise.then(function(res){
                var mm = [];
                angular.forEach(res, function(item){
                    for (var key in item) {
                        if (key.indexOf("$") !== 0) {
                            item.designation = key;
                            item.ps_key = item[key];
                            delete item[key];
                        }
                    }
                    mm.push(item);
                });
                return mm;
            });
        };
    };

    $scope.getAllCourses = function () {
        var courses = [];
        var groups = $scope.groups;
        var total = 0;
        for (var i = 0; i < groups.length; i++) {
            var group = groups[i];
            var group_courses = group.courses;
            for (var j = 0; j < group_courses.length; j++) {
                if (total % 4 == 0) courses.push([])
                courses[courses.length-1].push({course_num: group_courses[j].course_num});
                total++;
            }
        }
        return courses;
    };

    $scope.seeAllCourses = function () {
        var getAll = $scope.getAllCourses;
        var modalInstance = $modal.open({
            templateUrl: 'allCoursesModalContent.html',
            controller: AllCoursesModalInstanceCtrl,
            resolve: {
                courses: function() {
                    return $scope.getAllCourses()
                }
            }
        });
    };
    
    var AllCoursesModalInstanceCtrl = function ($scope, $modalInstance, courses) {
        $scope.courses = courses;
        $scope.ok = function () {
            $modalInstance.close();
        };
        $scope.cancel = function () {
            $modalInstance.dismiss('cancel');
        };
    };

    $scope.transcriptModal = function () {
        var modalInstance = $modal.open({
            templateUrl: 'uploadTranscriptModal.html',
            controller: UploadInstanceCtrl
        });
    };

    $scope.oneAtATime = false;
    $scope.groups = Courses.query();
    $scope.groups.refresh = function() {
        $scope.groups = Courses.query();
    };
    RefreshService.register($scope.groups);
    $scope.foobar = [
        {
            title: "Fall - 2010",
            courses: [
                {
                    designation: 'CS 106A',
                    title: 'FOOBAR',
                    key: 123,
                    description: 'Introduction to the engineering of computer applications emphasizing modern software engineering principles: object-oriented design, decomposition, encapsulation, abstraction, and testing. Uses the Java programming language. Emphasis is on good programming style and the built-in facilities of the Java language. No prior programming experience required. Summer quarter enrollment is limited; application required.'
                },
                {
                    designation: 'IHUM',
                    title: 'Worst Class Ever',
                    key: 456,
                    description: 'How is a living, thinking human being like, or not like, a machine? This might seem like a new question for the Information Age, yet it has been a preoccupation of our civilization for centuries. From the culmination of the Scientific Revolution in the seventeenth century, philosophers, physiologists, engineers, authors, political actors and artists of every kind have taken humanity¿s measure by comparing humans with machines. Our course follows this tradition.nTogether, we ask a number of questions about what it means to think of the human mind, body, and society as types of machines. How has the machine served as a metaphor for the cosmos and culture? How do we interact with machines, and how have machines influenced literature, performance, and the arts? What separates us from our machines, and are we really as separate as we think we are?nWe explore the shifting boundary lines between the mechanical and the human by considering how humanity has created or imagined machines and our interconnections with them. What do the concepts of ¿machine,¿ ¿human,¿ ¿alive,¿ ¿intelligent¿ and ¿self-aware¿ mean in different times and places, including our own? We will consider how humans may be conceived and designed as well as manipulated as machines, and how our artificial creations may in turn reflect and reflect upon their human creators.nThe philosophical, scientific and ethical questions regarding the relationship of humans to machines are not just the preoccupations of our current moment. These questions have generated long, rich traditions of responses. We must draw upon these if we are to confront our current concerns, not as isolated actors, but as members of an ever-evolving culture.'
                },
                {
                    designation: 'CME 100',
                    title: 'Vector Calculus',
                    description: 'Computation and visualization using MATLAB. Differential vector calculus: analytic geometry in space, functions of several variables, partial derivatives, gradient, unconstrained maxima and minima, Lagrange multipliers. Integral vector calculus: multiple integrals in Cartesian, cylindrical, and spherical coordinates, line integrals, scalar potential, surface integrals, Greens, divergence, and Stokes theorems. Examples and applications drawn from various engineering fields. Prerequisites: MATH 41 and 42, or 10 units AP credit.'
                }
            ]
        },
        {
            title: "Winter - 2011",
            courses: [
                {
                    designation: 'CS 106A',
                    title: 'Introduction to Computer Programming',
                    description: 'Introduction to the engineering of computer applications emphasizing modern software engineering principles: object-oriented design, decomposition, encapsulation, abstraction, and testing. Uses the Java programming language. Emphasis is on good programming style and the built-in facilities of the Java language. No prior programming experience required. Summer quarter enrollment is limited; application required.'
                },
                {
                    designation: 'IHUM',
                    title: 'Worst Class Ever',
                    description: 'How is a living, thinking human being like, or not like, a machine? This might seem like a new question for the Information Age, yet it has been a preoccupation of our civilization for centuries. From the culmination of the Scientific Revolution in the seventeenth century, philosophers, physiologists, engineers, authors, political actors and artists of every kind have taken humanity¿s measure by comparing humans with machines. Our course follows this tradition.nTogether, we ask a number of questions about what it means to think of the human mind, body, and society as types of machines. How has the machine served as a metaphor for the cosmos and culture? How do we interact with machines, and how have machines influenced literature, performance, and the arts? What separates us from our machines, and are we really as separate as we think we are?nWe explore the shifting boundary lines between the mechanical and the human by considering how humanity has created or imagined machines and our interconnections with them. What do the concepts of ¿machine,¿ ¿human,¿ ¿alive,¿ ¿intelligent¿ and ¿self-aware¿ mean in different times and places, including our own? We will consider how humans may be conceived and designed as well as manipulated as machines, and how our artificial creations may in turn reflect and reflect upon their human creators.nThe philosophical, scientific and ethical questions regarding the relationship of humans to machines are not just the preoccupations of our current moment. These questions have generated long, rich traditions of responses. We must draw upon these if we are to confront our current concerns, not as isolated actors, but as members of an ever-evolving culture.'
                },
                {
                    designation: 'CME 100',
                    title: 'Vector Calculus',
                    description: 'Computation and visualization using MATLAB. Differential vector calculus: analytic geometry in space, functions of several variables, partial derivatives, gradient, unconstrained maxima and minima, Lagrange multipliers. Integral vector calculus: multiple integrals in Cartesian, cylindrical, and spherical coordinates, line integrals, scalar potential, surface integrals, Greens, divergence, and Stokes theorems. Examples and applications drawn from various engineering fields. Prerequisites: MATH 41 and 42, or 10 units AP credit.'
                }
            ]
        },
        {
            title: "Spring - 2011",
            courses: [
                {
                    designation: 'CS 106A',
                    title: 'Introduction to Computer Programming',
                    description: 'Introduction to the engineering of computer applications emphasizing modern software engineering principles: object-oriented design, decomposition, encapsulation, abstraction, and testing. Uses the Java programming language. Emphasis is on good programming style and the built-in facilities of the Java language. No prior programming experience required. Summer quarter enrollment is limited; application required.'
                },
                {
                    designation: 'IHUM',
                    title: 'Worst Class Ever',
                    description: 'How is a living, thinking human being like, or not like, a machine? This might seem like a new question for the Information Age, yet it has been a preoccupation of our civilization for centuries. From the culmination of the Scientific Revolution in the seventeenth century, philosophers, physiologists, engineers, authors, political actors and artists of every kind have taken humanity¿s measure by comparing humans with machines. Our course follows this tradition.nTogether, we ask a number of questions about what it means to think of the human mind, body, and society as types of machines. How has the machine served as a metaphor for the cosmos and culture? How do we interact with machines, and how have machines influenced literature, performance, and the arts? What separates us from our machines, and are we really as separate as we think we are?nWe explore the shifting boundary lines between the mechanical and the human by considering how humanity has created or imagined machines and our interconnections with them. What do the concepts of ¿machine,¿ ¿human,¿ ¿alive,¿ ¿intelligent¿ and ¿self-aware¿ mean in different times and places, including our own? We will consider how humans may be conceived and designed as well as manipulated as machines, and how our artificial creations may in turn reflect and reflect upon their human creators.nThe philosophical, scientific and ethical questions regarding the relationship of humans to machines are not just the preoccupations of our current moment. These questions have generated long, rich traditions of responses. We must draw upon these if we are to confront our current concerns, not as isolated actors, but as members of an ever-evolving culture.'
                },
                {
                    designation: 'CME 100',
                    title: 'Vector Calculus',
                    description: 'Computation and visualization using MATLAB. Differential vector calculus: analytic geometry in space, functions of several variables, partial derivatives, gradient, unconstrained maxima and minima, Lagrange multipliers. Integral vector calculus: multiple integrals in Cartesian, cylindrical, and spherical coordinates, line integrals, scalar potential, surface integrals, Greens, divergence, and Stokes theorems. Examples and applications drawn from various engineering fields. Prerequisites: MATH 41 and 42, or 10 units AP credit.'
                }
            ]
        },
        {
            title: "Fall - 2011",
            courses: [
                {
                    designation: 'CS 106A',
                    title: 'Introduction to Computer Programming',
                    description: 'Introduction to the engineering of computer applications emphasizing modern software engineering principles: object-oriented design, decomposition, encapsulation, abstraction, and testing. Uses the Java programming language. Emphasis is on good programming style and the built-in facilities of the Java language. No prior programming experience required. Summer quarter enrollment is limited; application required.'
                },
                {
                    designation: 'IHUM',
                    title: 'Worst Class Ever',
                    description: 'How is a living, thinking human being like, or not like, a machine? This might seem like a new question for the Information Age, yet it has been a preoccupation of our civilization for centuries. From the culmination of the Scientific Revolution in the seventeenth century, philosophers, physiologists, engineers, authors, political actors and artists of every kind have taken humanity¿s measure by comparing humans with machines. Our course follows this tradition.nTogether, we ask a number of questions about what it means to think of the human mind, body, and society as types of machines. How has the machine served as a metaphor for the cosmos and culture? How do we interact with machines, and how have machines influenced literature, performance, and the arts? What separates us from our machines, and are we really as separate as we think we are?nWe explore the shifting boundary lines between the mechanical and the human by considering how humanity has created or imagined machines and our interconnections with them. What do the concepts of ¿machine,¿ ¿human,¿ ¿alive,¿ ¿intelligent¿ and ¿self-aware¿ mean in different times and places, including our own? We will consider how humans may be conceived and designed as well as manipulated as machines, and how our artificial creations may in turn reflect and reflect upon their human creators.nThe philosophical, scientific and ethical questions regarding the relationship of humans to machines are not just the preoccupations of our current moment. These questions have generated long, rich traditions of responses. We must draw upon these if we are to confront our current concerns, not as isolated actors, but as members of an ever-evolving culture.'
                },
                {
                    designation: 'CME 100',
                    title: 'Vector Calculus',
                    description: 'Computation and visualization using MATLAB. Differential vector calculus: analytic geometry in space, functions of several variables, partial derivatives, gradient, unconstrained maxima and minima, Lagrange multipliers. Integral vector calculus: multiple integrals in Cartesian, cylindrical, and spherical coordinates, line integrals, scalar potential, surface integrals, Greens, divergence, and Stokes theorems. Examples and applications drawn from various engineering fields. Prerequisites: MATH 41 and 42, or 10 units AP credit.'
                }
            ]
        },
        {
            title: "Winter - 2012",
            courses: [
                {
                    designation: 'CS 106A',
                    title: 'Introduction to Computer Programming',
                    description: 'Introduction to the engineering of computer applications emphasizing modern software engineering principles: object-oriented design, decomposition, encapsulation, abstraction, and testing. Uses the Java programming language. Emphasis is on good programming style and the built-in facilities of the Java language. No prior programming experience required. Summer quarter enrollment is limited; application required.'
                },
                {
                    designation: 'IHUM',
                    title: 'Worst Class Ever',
                    description: 'How is a living, thinking human being like, or not like, a machine? This might seem like a new question for the Information Age, yet it has been a preoccupation of our civilization for centuries. From the culmination of the Scientific Revolution in the seventeenth century, philosophers, physiologists, engineers, authors, political actors and artists of every kind have taken humanity¿s measure by comparing humans with machines. Our course follows this tradition.nTogether, we ask a number of questions about what it means to think of the human mind, body, and society as types of machines. How has the machine served as a metaphor for the cosmos and culture? How do we interact with machines, and how have machines influenced literature, performance, and the arts? What separates us from our machines, and are we really as separate as we think we are?nWe explore the shifting boundary lines between the mechanical and the human by considering how humanity has created or imagined machines and our interconnections with them. What do the concepts of ¿machine,¿ ¿human,¿ ¿alive,¿ ¿intelligent¿ and ¿self-aware¿ mean in different times and places, including our own? We will consider how humans may be conceived and designed as well as manipulated as machines, and how our artificial creations may in turn reflect and reflect upon their human creators.nThe philosophical, scientific and ethical questions regarding the relationship of humans to machines are not just the preoccupations of our current moment. These questions have generated long, rich traditions of responses. We must draw upon these if we are to confront our current concerns, not as isolated actors, but as members of an ever-evolving culture.'
                },
                {
                    designation: 'CME 100',
                    title: 'Vector Calculus',
                    description: 'Computation and visualization using MATLAB. Differential vector calculus: analytic geometry in space, functions of several variables, partial derivatives, gradient, unconstrained maxima and minima, Lagrange multipliers. Integral vector calculus: multiple integrals in Cartesian, cylindrical, and spherical coordinates, line integrals, scalar potential, surface integrals, Greens, divergence, and Stokes theorems. Examples and applications drawn from various engineering fields. Prerequisites: MATH 41 and 42, or 10 units AP credit.'
                }
            ]
        },
        {
            title: "Spring - 2012",
            courses: [
                {
                    designation: 'CS 106A',
                    title: 'Introduction to Computer Programming',
                    description: 'Introduction to the engineering of computer applications emphasizing modern software engineering principles: object-oriented design, decomposition, encapsulation, abstraction, and testing. Uses the Java programming language. Emphasis is on good programming style and the built-in facilities of the Java language. No prior programming experience required. Summer quarter enrollment is limited; application required.'
                },
                {
                    designation: 'IHUM',
                    title: 'Worst Class Ever',
                    description: 'How is a living, thinking human being like, or not like, a machine? This might seem like a new question for the Information Age, yet it has been a preoccupation of our civilization for centuries. From the culmination of the Scientific Revolution in the seventeenth century, philosophers, physiologists, engineers, authors, political actors and artists of every kind have taken humanity¿s measure by comparing humans with machines. Our course follows this tradition.nTogether, we ask a number of questions about what it means to think of the human mind, body, and society as types of machines. How has the machine served as a metaphor for the cosmos and culture? How do we interact with machines, and how have machines influenced literature, performance, and the arts? What separates us from our machines, and are we really as separate as we think we are?nWe explore the shifting boundary lines between the mechanical and the human by considering how humanity has created or imagined machines and our interconnections with them. What do the concepts of ¿machine,¿ ¿human,¿ ¿alive,¿ ¿intelligent¿ and ¿self-aware¿ mean in different times and places, including our own? We will consider how humans may be conceived and designed as well as manipulated as machines, and how our artificial creations may in turn reflect and reflect upon their human creators.nThe philosophical, scientific and ethical questions regarding the relationship of humans to machines are not just the preoccupations of our current moment. These questions have generated long, rich traditions of responses. We must draw upon these if we are to confront our current concerns, not as isolated actors, but as members of an ever-evolving culture.'
                },
                {
                    designation: 'CME 100',
                    title: 'Vector Calculus',
                    description: 'Computation and visualization using MATLAB. Differential vector calculus: analytic geometry in space, functions of several variables, partial derivatives, gradient, unconstrained maxima and minima, Lagrange multipliers. Integral vector calculus: multiple integrals in Cartesian, cylindrical, and spherical coordinates, line integrals, scalar potential, surface integrals, Greens, divergence, and Stokes theorems. Examples and applications drawn from various engineering fields. Prerequisites: MATH 41 and 42, or 10 units AP credit.'
                }
            ]
        },
        {
            title: "Fall - 2012",
            courses: [
                {
                    designation: 'CS 106A',
                    title: 'Introduction to Computer Programming',
                    description: 'Introduction to the engineering of computer applications emphasizing modern software engineering principles: object-oriented design, decomposition, encapsulation, abstraction, and testing. Uses the Java programming language. Emphasis is on good programming style and the built-in facilities of the Java language. No prior programming experience required. Summer quarter enrollment is limited; application required.'
                },
                {
                    designation: 'IHUM',
                    title: 'Worst Class Ever',
                    description: 'How is a living, thinking human being like, or not like, a machine? This might seem like a new question for the Information Age, yet it has been a preoccupation of our civilization for centuries. From the culmination of the Scientific Revolution in the seventeenth century, philosophers, physiologists, engineers, authors, political actors and artists of every kind have taken humanity¿s measure by comparing humans with machines. Our course follows this tradition.nTogether, we ask a number of questions about what it means to think of the human mind, body, and society as types of machines. How has the machine served as a metaphor for the cosmos and culture? How do we interact with machines, and how have machines influenced literature, performance, and the arts? What separates us from our machines, and are we really as separate as we think we are?nWe explore the shifting boundary lines between the mechanical and the human by considering how humanity has created or imagined machines and our interconnections with them. What do the concepts of ¿machine,¿ ¿human,¿ ¿alive,¿ ¿intelligent¿ and ¿self-aware¿ mean in different times and places, including our own? We will consider how humans may be conceived and designed as well as manipulated as machines, and how our artificial creations may in turn reflect and reflect upon their human creators.nThe philosophical, scientific and ethical questions regarding the relationship of humans to machines are not just the preoccupations of our current moment. These questions have generated long, rich traditions of responses. We must draw upon these if we are to confront our current concerns, not as isolated actors, but as members of an ever-evolving culture.'
                },
                {
                    designation: 'CME 100',
                    title: 'Vector Calculus',
                    description: 'Computation and visualization using MATLAB. Differential vector calculus: analytic geometry in space, functions of several variables, partial derivatives, gradient, unconstrained maxima and minima, Lagrange multipliers. Integral vector calculus: multiple integrals in Cartesian, cylindrical, and spherical coordinates, line integrals, scalar potential, surface integrals, Greens, divergence, and Stokes theorems. Examples and applications drawn from various engineering fields. Prerequisites: MATH 41 and 42, or 10 units AP credit.'
                }
            ]
        }
    ];

    $scope.refresh = function() {
        $log.info("Refreshed course list");
        $scope.groups = Courses.query();
    }

    $scope.removeCourse = function(courses, course) {
        var i = courses.indexOf(course);
        courses.splice(i,1);
    };

    $scope.openCourse = function (coursesGroup, selectedCourse) {

        var modalInstance = $modal.open({
            templateUrl: 'courseDetailsModalContent.html',
            controller: ModalInstanceCtrl,
            resolve: {
                course: function () {
                    return selectedCourse;
                }
            }
        });

        modalInstance.result.then(function () {
            //call delete on the server
            Courses.remove({cand_course_key:selectedCourse.key}).$promise.then(function() {
                $scope.removeCourse(coursesGroup, selectedCourse);   
            });
        }, function () {
            $log.info('Modal dismissed at: ' + new Date());
        });
    };

    var UploadInstanceCtrl = function ($scope, $modalInstance) {
        $scope.ok = function () {
            $modalInstance.close();
        };
        $scope.cancel = function () {
            $modalInstance.dismiss('cancel');
        };
    };

    var ModalInstanceCtrl = function ($scope, $modalInstance, course) {
        $scope.course = course;
        $scope.ok = function () {
            $modalInstance.close();
        };

        $scope.cancel = function () {
            $modalInstance.dismiss('cancel');
        };
    };

    $scope.list1 = {title: 'AngularJS - Drag Me'};
    $scope.foo = true;
  
    // Any function returning a promise object can be used to load values asynchronously
    $scope.searchForCourses = function(val) {
        return Courses.search({prefix:val})
        .$promise.then(function(res){
            var courses = [];
            angular.forEach(res, function(item){
                for (var key in item) {
                    if (key.indexOf("$") !== 0) {
                        item.designation = key;
                        item.course_key = item[key];
                        delete item[key];
                    }
                }
                courses.push(item);
            });
            return courses;
        });
    };

    $scope.displayCourseInfo = function ($item, $model, $label) {
        $scope.tryAddCourse($item);
    };

    $scope.tryAddCourse = function (selectedCourse) {

        var modalInstance = $modal.open({
            templateUrl: 'tryAddCourseModalContent.html',
            controller: TryAddCourseCtrl,
            resolve: {
                course: function () {
                    return selectedCourse.$describe();
                },
                groups: function () {
                    return $scope.groups;
                }
            }
        });

        modalInstance.result.then(function () {
            $log.info('Course Added');
        }, function () {
            $log.info('Modal dismissed at: ' + new Date());
        });
    };

    var TryAddCourseCtrl = function ($scope, $modalInstance, course, groups) {
        $scope.course = course;
        $scope.terms = [
                        {name:"Autumn",value:"autumn"},
                        {name:"Winter",value:"winter"},
                        {name:"Spring",value:"spring"},
                        {name:"Summer",value:"summer"}
                       ];
        $scope.term = $scope.terms[0];
        $scope.years = [
                        {name:"2010",value:"2010"},
                        {name:"2011",value:"2011"},
                        {name:"2012",value:"2012"},
                        {name:"2013",value:"2013"},
                        {name:"2014",value:"2014"}
                       ];
        $scope.year = $scope.years[0];
        $scope.grades = [
                        {name:"A+",value:"4.3"},
                        {name:"A",value:"4.0"},
                        {name:"A-",value:"3.7"},
                        {name:"B+",value:"3.3"},
                        {name:"B",value:"3.0"},
                        {name:"B-",value:"2.7"},
                        {name:"C+",value:"2.3"},
                        {name:"C",value:"2.0"},
                        {name:"C-",value:"1.7"},
                        {name:"D+",value:"1.3"},
                        {name:"D",value:"1.0"},
                        {name:"D-",value:"0.7"},
                        {name:"F",value:"0.0"},
                        {name:"N/A",value:"-1"}
                       ];
        $scope.grade = $scope.grades[0];
        $scope.unit_opts = [
                        {name:"1",value:"1"},
                        {name:"2",value:"2"},
                        {name:"3",value:"3"},
                        {name:"4",value:"4"},
                        {name:"5",value:"5"},
                        {name:"6",value:"6"},
                        {name:"7",value:"7"},
                        {name:"8",value:"8"},
                        {name:"9",value:"9"},
                        {name:"10",value:"10"}
                       ];
        $scope.units = $scope.unit_opts[3];

        $scope.ok = function (term, year, grade, units) {
            var data = $.param({term: term, year: year, grade: grade, units: units, course_key: course.key});
            Courses.add(data).$promise.then(RefreshService.refresh);
            //groups = Courses.query();
            $modalInstance.close();
        };

        $scope.cancel = function () {
            //$log.log(groups);
            //var gots = Courses.query();
            $modalInstance.dismiss('cancel');
        };
    };

    $scope.$watch('asyncSelected', function() {
        //$scope.asyncSelected = $scope.asyncSelected.toLowerCase().replace(/,+/g,'');
    });

    $scope.mm = [
        {
            name: "Computer Science",
            requirement_groups: [
                {
                    name: "Mathematics",
                    requirements: [
                        {
                            name: "MATH 41",
                            fulfilling: null
                        },
                        {
                            name: "MATH 42",
                            fulfilling: null
                        },
                        {
                            name: "CS 103",
                            fulfilling: null
                        },
                        {
                            name: "CS 109",
                            fulfilling: null
                        },
                        {
                            name: "Elective",
                            fulfilling: null
                        },
                        {
                            name: "Elective",
                            fulfilling: null
                        }
                    ]
                },
                {
                    name: "Science",
                    requirements: [
                        {
                            name: "PHYS 41",
                            fulfilling: null
                        },
                        {
                            name: "PHYS 43",
                            fulfilling: null
                        },
                        {
                            name: "Elective",
                            fulfilling: null
                        }
                    ]
                },
                {
                    name: "Technology in Society",
                    requirements: [
                        {
                            name: "TIS",
                            fulfilling: null
                        }
                    ]
                },
                {
                    name: "Depth",
                    requirements: [
                        {
                            name: "MATH 41",
                            fulfilling: null
                        },
                        {
                            name: "MATH 42",
                            fulfilling: null
                        },
                        {
                            name: "CS 103",
                            fulfilling: null
                        },
                        {
                            name: "CS 109",
                            fulfilling: null
                        },
                        {
                            name: "Elective",
                            fulfilling: null
                        },
                        {
                            name: "Elective",
                            fulfilling: null
                        }
                    ]
                },
                {
                    name: "Core",
                    requirements: [
                        {
                            name: "PHYS 41",
                            fulfilling: null
                        },
                        {
                            name: "PHYS 43",
                            fulfilling: null
                        },
                        {
                            name: "Elective",
                            fulfilling: null
                        }
                    ]
                },
                {
                    name: "WIM",
                    requirements: [
                        {
                            name: "TIS",
                            fulfilling: null
                        }
                    ]
                }
            ]
        },
        {
            name: "Physics",
            requirement_groups: [
                {
                    name: "Mathematics",
                    requirements: [
                        {
                            name: "MATH 41",
                            fulfilling: null
                        },
                        {
                            name: "MATH 42",
                            fulfilling: null
                        },
                        {
                            name: "Elective",
                            fulfilling: null
                        },
                        {
                            name: "Elective",
                            fulfilling: null
                        }
                    ]
                },
                {
                    name: "Science",
                    requirements: [
                        {
                            name: "PHYS 41",
                            fulfilling: null
                        },
                        {
                            name: "PHYS 43",
                            fulfilling: null
                        },
                        {
                            name: "Elective",
                            fulfilling: null
                        }
                    ]
                },
                {
                    name: "Technology in Society",
                    requirements: [
                        {
                            name: "TIS",
                            fulfilling: null
                        }
                    ]
                }
            ]
        }
    ];
})
.controller('TransUploadCtrl', function ($scope, $http, $timeout, $upload, RefreshService) {
    $scope.add = function() {
      var f = document.getElementById('transFile').files[0];
      var status = document.getElementById('statusSpan');
      var button = document.getElementById('uploadTransButton');

      button.disabled = true;

      status.innerHTML = "Starting Upload";

      var xhr = new XMLHttpRequest();
      xhr.open('POST', "/api/trans/upload", true);
      xhr.onreadystatechange = function(e) {
            if (4 == this.readyState ) {
                if ( 200 == this.status) {
                    status.innerHTML = "Upload Success!";
                } else {
                    status.innerHTML = "Upload Failed! status is " + this.status;
                }
                button.disabled = false;
                RefreshService.refresh();
            }
      };
      xhr.send(f);  
      status.innerHTML = "Uploading. . .";
    }
})
.directive('disableDrop', function () {
    return {
        restrict: 'A',
        scope: {
            disableDrop: "="
        },
        link: function(scope, elm, attrs) {
            scope.$watch('disableDrop', function(newValue, oldValue) {
                if (newValue != null) {
                    elm.droppable("option","disabled",true);
                } else {
                    elm.droppable("option","disabled",false);
                }
            });
        }
    }
})
.factory('Courses', function ($resource) {
    var foo = $resource('/api/student/course/ ', { // only GET and POST are defined
        course_key:'@course_key',
        prefix:'@prefix',
        cand_course_key:'@cand_course_key'
    }, {
        describe: {method:'GET',url:'/api/course/:course_key'}, // show general description info for a course
        search: {method:'GET',url:'/api/course/search/:prefix',isArray:true}, // search for a course
        add: {method:'POST',headers:{'Content-Type': 'application/x-www-form-urlencoded'}}, // add a course
        remove: {method:'DELETE',url:'/api/student/course/:cand_course_key'} // delete a course 
    });
    return foo;
})
.factory('MM', function ($resource) {
    return $resource('/api/programsheet/search/:prefix', {
        prefix:'@prefix',
        ps_key:'@ps_key'
    }, {
        add: {method:'POST',url:'/api/sps/:ps_key'}
    });
})
.service('RefreshService', function() {
    var toRefresh = [];
    this.register = function(item) {
        toRefresh.push(item);
    };
    this.refresh = function() {
        for (var i in toRefresh) {
            toRefresh[i].refresh();
        }
    };
});
