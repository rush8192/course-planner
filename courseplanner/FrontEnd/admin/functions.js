var course_keys = {}
var ps_keys = {}

var modifyCourseViewModal = function() {
  var course_num = document.getElementById('course-search-box').value;
  document.getElementById("viewCourseModalLabel").innerHTML = course_num;
  var xhr = new XMLHttpRequest();
  course_key = course_keys[course_num];
  xhr.onreadystatechange = function() {
    if (xhr.readyState == 4) {
      var json_str = "Program Sheet does not exist!";
      if (xhr.status === 200) {
        json_str = xhr.responseText;
      }
      $("textarea#viewCourseTextAreaID").val(json_str);
    }
  }
  xhr.open("GET", "/api/course/" + course_key, true);
  xhr.send();
}

var modifyCourseCreateModal = function() {
  var ps_name = document.getElementById('course-search-box').value;
  document.getElementById("createCourseModalLabel").innerHTML = ps_name;
  var json_str = '{\n' +
                 '\"course_num\":' + '\"' + ps_name + '\",\n' +
                 '\"other_things\":[]\n' +
                 '}';
  $("textarea#createCourseTextAreaID").val(json_str);
}

var modifyCourseDeleteModal = function() {
  var ps_name = document.getElementById('course-search-box').value;
  document.getElementById("deleteCourseModalLabel").innerHTML = ps_name;
}

var modifyViewModal = function() {
  var ps_name = document.getElementById('program-sheet-search-box').value;
  ps_key = ps_keys[ps_name];
  document.getElementById("viewModalLabel").innerHTML = ps_name;
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function() {
    if (xhr.readyState == 4) {
      var json_str = "Program Sheet does not exist!";
      if (xhr.status === 200) {
        json_str = xhr.responseText;
      }
      $("textarea#viewTextAreaID").val(json_str);
    }
  }
  xhr.open("GET", "/api/programsheet?ps_key=" + ps_key, true);
  xhr.send();
}

var modifyCreateModal = function() {
  var ps_name = document.getElementById('program-sheet-search-box').value;
  document.getElementById("createModalLabel").innerHTML = ps_name;
  var json_str = '{\n' +
                 '\"ps_name\":' + '\"' + ps_name + '\",\n' +
                 '\"req_boxes\":[]\n' +
                 '}';
  $("textarea#createTextAreaID").val(json_str);
}

var modifyDeleteModal = function() {
  var ps_name = document.getElementById('program-sheet-search-box').value;
  document.getElementById("deleteModalLabel").innerHTML = ps_name;
}

var isValidJson = function(json) {
    try {
        JSON.parse(json);
        return true;
    } catch (e) {
        return false;
    }
}

var createProgramSheet = function() {
  ps_name = document.getElementById("createModalLabel").innerHTML;
  var ps_json_str = document.getElementById('createTextAreaID').value;
  if (!isValidJson(ps_json_str)) {
    window.alert("Invalid JSON");
    return;
  }
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function() {
    if (xhr.readyState == 4) {
      var json_str = xhr.responseText;
      json = JSON.parse(json_str);
      ps_exists = json.exists;
      if (ps_exists) {
        window.alert("Program Sheet already exists!");
        return;
      }
      var send_xhr = new XMLHttpRequest();
      send_xhr.onreadystatechange = function() {
        if (send_xhr.readyState === 4) {
          if (send_xhr.status === 200) {
            window.alert("Success!");
            return;
          }
          else {
            window.alert("Failed to Add Program Sheet :(");
          }
        }
      }
      send_xhr.open("POST", "/api/programsheet", true);
      var params = "ps_json=" + ps_json_str;
      send_xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
      send_xhr.send(params)
    }
  }
  xhr.open("PUT", "/api/programsheet", true);
  var params = "ps_name=" + ps_name;
  //Send the proper header information along with the request
  xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhr.send(params);
}

var deleteProgramSheet = function() {
  ps_name = document.getElementById("deleteModalLabel").innerHTML;
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function() {
    if (xhr.readyState == 4) {
      if (xhr.status === 200) {
        window.alert("Successfully deleted!");
        return;
      }
      else {
        window.alert("Program sheet does not exist");
      }
    }
  }
  xhr.open("DELETE", "/api/programsheet?ps_name=" + ps_name, true);
  xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhr.send() 
}