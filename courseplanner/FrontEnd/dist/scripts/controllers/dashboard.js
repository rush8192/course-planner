'use strict';

angular.module('coursePlannerApp')
  .controller('DashboardCtrl', function ($scope, $modal, $log, $http) {
    $scope.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];

    $scope.chartObject = {};

    $scope.onions = [
        {v: "Onions"},
        {v: 100}
    ];

    $scope.chartObject.data = {"cols": [
        {id: "t", label: "Topping", type: "string"},
        {id: "s", label: "Progress (%)", type: "number"}
      ], "rows": [
        {c: [
            {v: "Foo"},
            {v: 3}
          ]},
        {c: $scope.onions},
        {c: [
            {v: "Olives"},
            {v: 10}
          ]},
        {c: [
            {v: "Zucchini"},
            {v: 1}
          ]},
        {c: [
            {v: "Pepperoni"},
            {v: 2}
          ]}
    ]};


    // $routeParams.chartType == BarChart or PieChart or ColumnChart...
    $scope.chartObject.type = "BarChart"
    $scope.chartObject.options = {
        'title': 'Course Progress',
        'legend': 'none',
        'hAxis': {
            maxValue: 100
        }
    }

        $scope.oneAtATime = false;
        $scope.groups = [
            {
                title: "Fall - 2010",
                courses: [
                    {
                        designation: 'CS 106A',
                        title: 'FOOBAR',
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

        $scope.removeCourse = function(courses, course) {
            var i = courses.indexOf(course);
            courses.splice(i,1);
        };

        $scope.open = function (coursesGroup, selectedCourse) {

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
                $scope.removeCourse(coursesGroup, selectedCourse);
            }, function () {
                $log.info('Modal dismissed at: ' + new Date());
            });
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
        $scope.getLocation = function(val) {
            return $http.get('http://maps.googleapis.com/maps/api/geocode/json', {
                params: {
                    address: val,
                    sensor: false
                }
            }).then(function(res){
                var addresses = [];
                angular.forEach(res.data.results, function(item){
                    addresses.push(item.formatted_address);
                });
                return addresses;
            });
        };

        $scope.$watch('asyncSelected', function() {
            $scope.asyncSelected = $scope.asyncSelected.toLowerCase().replace(/,+/g,'');
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
    });
