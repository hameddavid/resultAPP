$(document).ready(function ($) {
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
        $("#btnSubmitRole").html('<i class="mdi mdi-loading mdi-spin"></i>');
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
});
