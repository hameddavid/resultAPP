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
  });

  $("#btnAddCourse").click(function (e){
    e.preventDefault();
    var formData = $("#addCourseForm").serialize();
     if(formData === null || formData == "") return false
    console.log(formData);
    var type = "POST";
    var ajaxurl = "/show";
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
      },
      error: function (response) {
        console.log(response);
        $("#btnAddCourse").html("Submit");
        $("#btnAddCourse").prop("disabled", false);
        alert(response.responseJSON.message);
      },
    });
  })

  $("#btnScoreInput").click(function () {
    $("#inputScoreForm").validate({
      submitHandler: submitInputScoreForm,
    });

    function submitInputScoreForm(e) {
      var formData = $("#inputScoreForm").serialize();
      var type = "POST";
      var ajaxurl = "";

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
        },
        error: function (response) {
          console.log(response);
          $("#btnScoreInput").html("Login");
          $("#btnScoreInput").prop("disabled", false);
          alert(response.responseJSON.message);
        },
      });
    }
  });

   $(".scoreTable").on("focusout", ".score", function(){
    const score = $(this).val()
    const grade = getGrade(score)
    const tr = $(this).closest("tr")
    const current_row = tr.index() + 1
    $('#'+current_row).val(grade)
  })

  const getGrade = (score) => {
    if(score >= 70){
      return 'A'
    }
    else if(score < 70 && score > 59){
      return 'B'
    }
    else if(score < 60 && score > 49){
      return 'C'
    }
    else if(score < 50 && score > 39){
      return 'D'
    }
    else {
      return 'F'
    }
  }
});
