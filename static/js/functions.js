$(document).ready(function ($) {
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
    var ajaxurl = "/hod-role-action";
    $.ajax({
      type: type,
      url: ajaxurl,
      data: { id: $(this).data("id"), type: $(this).data("type") },
      dataType: "json",
      beforeSend: function () {
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
    var ajaxurl = "/hod-role-action";
    $.ajax({
      type: type,
      url: ajaxurl,
      data: { id: $(this).data("id"), type: $(this).data("type") },
      dataType: "json",
      beforeSend: function () {
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
});
