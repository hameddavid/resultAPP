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
        },
        success: function (response) {
          console.log(response);
          alert(response.message);

          setTimeout(function () {
            window.location.href = "user/dashboard";
          }, 1800);
        },
        error: function (response) {
          console.log(response);
          $("#login_button").html("Login");
          alert("hey");
          alert(response.responseJSON.message);
        },
      });
    }
  });
});
