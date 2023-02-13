$(document).ready(function ($) {
  $("#login_button").click(function () {
    $("#login-form").validate({
      submitHandler: submitLoginForm,
    });

    function submitLoginForm(e) {
      var formData = $("#login-form").serialize();
      var type = "POST";
      var ajaxurl = "login";

      $.ajax({
        type: type,
        url: ajaxurl,
        data: formData,
        dataType: "json",
        beforeSend: function () {
          $("#login_button").html('<i class="fa fa-spinner fa-spin"></i>');
          $("#login_button").prop("disabled", true);
        },
        success: function (response) {
          console.log(response);
          alert(response.message);
          if (response.status === "success") {
            if (response.url === "semester-activation") {
              setTimeout(function () {
                window.location.href = "semester-activation";
              }, 1500);
            } else if (response.url === "otp") {
              setTimeout(function () {
                window.location.href = "otp";
              }, 1500);
            } else {
              setTimeout(function () {
                window.location.href = "user/dashboard";
              }, 1500);
            }
          }
        },
        error: function (response) {
          console.log(response);
          $("#login_button").html("Login");
          $("#login_button").prop("disabled", false);
          alert(response.responseJSON.message);
        },
      });
    }
  });
});
