$("document").ready(function () {
    $("#password_top_div").hide();

    $("#login-form").validate({
        rules: {
            username: {
            required: true,
            email: true,
          },
        },
        messages: {
          username: "please enter your email address",
        },
        submitHandler: submitForm,
      });
      
      function submitForm() {
        console.log("Script seen")
        var data = $("#login-form").serialize();
        email = $("#username").val();
        $.ajax({
          type: "POST",
          url: "is_staff",
          data: data,
          beforeSend: function () {
            $("#error2").fadeOut();
            $("#login_button").html(
              '<i class="fa fa-spinner fa-spin"></i> &nbsp; verifying ...'
            );
            $("#login_button").prop("disabled", true);
          },
          success: function (response) {
            console.log(JSON.stringify(response.data)); return;
            if (response.data == "IS_STAFF") {
              $("#login_button").html("Log In");
              $("#login_button").prop("disabled", false);
              $("#password_top_div").show();
              $("form#login-form").prop("id", "new_form");
              $("button#login_button").prop("id", "login_button2");
    
              $("#login_button2").click(function (e) {
                var password = $("#userpassword").val();
                if (password == "") {
                  alert("Enter Password!");
                  return false;
                }
                e.preventDefault();
                $.ajax({
                  type: "POST",
                  url: "logic/login.php?email=" + email + "&password=" + password,
                  data: { userpassword: password },
                  beforeSend: function () {
                    $("#error2").fadeOut();
                    $("#login_button2").html(
                      '<i class="fa fa-spinner fa-spin"></i> &nbsp; Authenticating user ...'
                    );
                    $("#login_button2").prop("disabled", true);
                  },
                  success: function (response) {
                    console.log(response);
                    if (response == "success") {
                      setTimeout(' window.location.href = "authOTP.php"; ', 4000);
                    } else if (response == "2") {
                      $("#error2").fadeIn(1000, function () {
                        $("#login_button2").prop("disabled", false);
                        $("#error2").html(
                          '<div class="alert alert-danger"> Internet is required for account activation! </div>'
                        );
                        $("#login_button2").html("Log In");
                      });
                    } else if (response == "1") {
                      alert("OTP sent to your email");
                      setTimeout(' window.location.href = "authOTP.php"; ', 4000);
                    } else if (response == "3") {
                      $("#error2").fadeIn(1000, function () {
                        $("#login_button2").prop("disabled", false);
                        $("#error2").html(
                          '<div class="alert alert-danger"> Unable to send OTP to your email! </div>'
                        );
                        $("#login_button2").html("Log In");
                      });
                    } else if (response == "log_me_in") {
                      setTimeout(' window.location.href = "dashboard.php"; ', 4000);
                    } else {
                      $("#error2").fadeIn(1000, function () {
                        $("#login_button2").prop("disabled", false);
                        $("#error2").html(
                          '<div class="alert alert-danger"> ' + response + " </div>"
                        );
                        $("#login_button2").html("Log In");
                      });
                    }
                  },
                });
              });
              return false;
            } else {
              $("#error2").fadeIn(1000, function () {
                $("#login_button").prop("disabled", false);
                $("#error2").html(
                  '<div class="alert alert-danger"> ' + response + " </div>"
                );
                $("#login_button").html("Log In");
              });
            }
          },
        });
        return false;
      }
});