$(document).ready(function ($) {
  $.ajaxSetup({
    headers: {
      "X-CSRFToken": $('meta[name="csrf-token"]').attr("content"),
    },
  });
  $(document).ajaxStart($.blockUI).ajaxStop($.unblockUI);

  $(".dept").hide();

  $("#hod").change(function () {
    if (this.checked) {
      $(".dept").show();
      $(".prog").hide();
      $(".adviser").hide();
      $(".officer").hide();
    } else {
      $(".dept").hide();
      $(".prog").show();
      $(".adviser").show();
      $(".officer").show();
    }
  });

  $("#btnSubmitRole").click(function (e) {
    e.preventDefault();
    var formData = $("#formSubmitRole").serialize();
    console.log(formData);
    var type = "POST";
    var ajaxurl = "/user-api/role";
    $.ajax({
      type: type,
      url: ajaxurl,
      data: formData,
      dataType: "json",
      beforeSend: function () {
        $("#btnSubmitRole").html('<i class="fa fa-spinner fa-spin"></i>');
      },
      success: function (response) {
        console.log(response);
        alert(response.message);
        $("#btnSubmitRole").html("Update Role");
      },
      error: function (response) {
        console.log(response);
        $("#btnSubmitRole").html("Update Role");
        alert(response.responseJSON.message);
      },
    });
  });

  $(".approve").click(function (e) {
    e.preventDefault();
    var type = "POST";
    var ajaxurl = "/user-api/hod-role-action";
    $.ajax({
      type: type,
      url: ajaxurl,
      data: { id: $(this).data("id"), type: $(this).data("type") },
      dataType: "json",
      beforeSend: function () {
        if (confirm("Approve this User?") == false) return false;
        $(this).html('<i class="fa fa-spinner fa-spin"></i>');
      },
      success: function (response) {
        console.log(response);
        alert(response.message);
        location.reload();
      },
      error: function (response) {
        console.log(response);
        $(this).html("Approve");
        alert(response.responseJSON.message);
      },
    });
    e.stopImmediatePropagation();
  });

  $(".disapprove").click(function (e) {
    e.preventDefault();
    var type = "POST";
    var ajaxurl = "/user-api/hod-role-action";
    $.ajax({
      type: type,
      url: ajaxurl,
      data: { id: $(this).data("id"), type: $(this).data("type") },
      dataType: "json",
      beforeSend: function () {
        if (confirm("Disapprove this User?") == false) return false;
        $(this).html('<i class="fa fa-spinner fa-spin"></i>');
      },
      success: function (response) {
        console.log(response);
        alert(response.message);
        location.reload();
      },
      error: function (response) {
        console.log(response);
        $(this).html("Disapprove");
        alert(response.responseJSON.message);
      },
    });
    e.stopImmediatePropagation();
  });

  $("#btnAddCourse").click(function (e) {
    e.preventDefault();
    var formData = $("#addCourseForm").serialize();
    if (formData === null || formData == "") return false;
    console.log(formData);
    var type = "POST";
    var ajaxurl = "/ug/api/ug-course-list-curr-based";
    $.ajax({
      type: type,
      url: ajaxurl,
      data: formData,
      dataType: "json",
      beforeSend: function () {
        $("#btnAddCourse").html('<i class="fa fa-spinner fa-spin"></i>');
        $("#btnAddCourse").prop("disabled", true);
      },
      success: function (response) {
        console.log(response);
        alert(response.message);
        $("#btnAddCourse").html("Submit");
        $("#btnAddCourse").prop("disabled", false);
        location.reload();
      },
      error: function (response) {
        console.log(response);
        $("#btnAddCourse").html("Submit");
        $("#btnAddCourse").prop("disabled", false);
        alert(response.responseJSON.message);
      },
    });
  });

  $("#_btnScoreInput").click(function () {
    $("#inputScoreForm").validate({
      submitHandler: submitInputScoreForm,
    });

    function submitInputScoreForm(e) {
      var table = $("#inputScoreTable").DataTable();
      var formData = $("#inputScoreForm").serialize();
      console.log(formData);
      var type = "POST";
      var ajaxurl = "/ug/api/submit-student-reg-score";

      $.ajax({
        type: type,
        url: ajaxurl,
        data: formData,
        dataType: "json",
        beforeSend: function () {
          $("#btnScoreInput").html('<i class="fa fa-spinner fa-spin"></i>');
          $("#btnScoreInput").prop("disabled", true);
        },
        success: function (response) {
          console.log(response);
          alert(response.message);
          $("#btnScoreInput").html("Submit");
          $("#btnScoreInput").prop("disabled", false);
        },
        error: function (response) {
          console.log(response);
          $("#btnScoreInput").html("Submit");
          $("#btnScoreInput").prop("disabled", false);
          alert(response.responseJSON.message);
        },
      });
    }
  });

  $(".scoreTable").on("focusout", ".score", function () {
    const id = $(this).data("id");
    const score = $(this).val();
    const grade = getGrade(score);
    //const tr = $(this).closest("tr");
    //const current_row = tr.index() + 1;
    $("#" + id).val(grade);
  });

  const getGrade = (score) => {
    if (score >= 70) {
      return "A";
    } else if (score < 70 && score > 59) {
      return "B";
    } else if (score < 60 && score > 49) {
      return "C";
    } else if (score < 50 && score > 39) {
      return "D";
    } else {
      return "F";
    }
  };

  $(".view_course").click(function (e) {
    $("#viewCourse").modal("show");
    $(".show_courses").html("");
    const email = $(this).data("email");
    $("#lec_email").html(email);
    $("#email").val(email);
    $.ajax({
      url: "/ug/api/get-user-courses-in-semester-for-approval",
      method: "POST",
      async: false,
      data: { email: email },
      success: function (response) {
        console.log(response);
        $.map(response.data, function (obj) {
          $(".show_courses").append(
            `<input name="courses[]" value= "${obj.id}" type="checkbox" required/> ` +
              obj.course_code +
              "<br />"
          );
        });
      },
    });
    e.stopImmediatePropagation();
  });

  $("#btnApproveCourse").click(function (e) {
    e.preventDefault();
    var formData = $("#formApproveCourse").serialize();
    console.log(formData);
    var type = "POST";
    var ajaxurl = "/ug/api/approve-disapprove-user-courses-in-semester";
    $.ajax({
      type: type,
      url: ajaxurl,
      data: formData,
      async: false,
      dataType: "json",
      beforeSend: function () {
        $("#btnApproveCourse").html('<i class="fa fa-spinner fa-spin"></i>');
        $("#btnApproveCourse").prop("disabled", true);
      },
      success: function (response) {
        console.log(response);
        alert(response.message);
        location.reload();
      },
      error: function (response) {
        console.log(response);
        alert(response.responseJSON.message);
        $("#btnApproveCourse").prop("disabled", false);
        $("#btnApproveCourse").html("Approve");
      },
    });
    e.stopImmediatePropagation();
  });

  $("#inputScoreForm").on("submit", function (e) {
    var table = $("#myProjectTable").DataTable();
    var form = this;
    var params = table.$("input").serializeArray();
    e.preventDefault();

    $.each(params, function () {
      if (!$.contains(document, form[this.name])) {
        $(form).append(
          $("<input>")
            .attr("type", "hidden")
            .attr("name", this.name)
            .val(this.value)
        );
      }
    });
    //$("#example-console-form").text($(form).serialize());
    var mydata = $(form).serialize();
    console.log(mydata);
    //$('input[type="hidden"]', form).remove();
    var type = "POST";
    var ajaxurl = "/ug/api/submit-student-reg-score";
    $.ajax({
      type: type,
      url: ajaxurl,
      data: mydata,
      dataType: "json",
      beforeSend: function () {
        $("#btnScoreInput").html('<i class="fa fa-spinner fa-spin"></i>');
        $("#btnScoreInput").prop("disabled", true);
      },
      success: function (response) {
        console.log(response);
        alert(response.message);
        $("#btnScoreInput").html("Submit");
        $("#btnScoreInput").prop("disabled", false);
      },
      error: function (response) {
        console.log(response);
        $("#btnScoreInput").html("Submit");
        $("#btnScoreInput").prop("disabled", false);
        alert(response.responseJSON.message);
      },
    });
  });

  $("#massUploadForm").on("submit", function (e) {
    e.preventDefault();
    const course = $("input[name=course_code]").val();
    const formData = new FormData(this);
    formData.append("course_code", course);
    $.ajax({
      type: "POST",
      url: "/ug/api/mass-submit-student-reg-score",
      data: formData,
      dataType: "json",
      contentType: false,
      cache: false,
      processData: false,
      beforeSend: function () {
        $("#btnMassUpload").html('<i class="fa fa-spinner fa-spin"></i>');
      },
      success: function (response) {
        console.log(response);
        $("#btnMassUpload").html("Upload");
        alert(response.message);
      },
      error: function (response) {
        console.log(response);
        alert(response.responseJSON.message);
        $("#btnMassUpload").html("Upload");
      },
    });
  });
});
