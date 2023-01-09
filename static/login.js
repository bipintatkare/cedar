function login(event) {
  event.preventDefault();
  //
  var email = document.getElementById("email").value;
  var Password = document.getElementById("password").value;

  if (email == "" || email == " " || Password == " " || Password == "") {
    toastr.error("Enter all required fields.");
    return;
  }

  $.ajax({
    type: "POST",
    url: "/api/v1/login/",
    data: {
      email: email,
      password: Password,
    },
    success: function (data) {
      if (data.hasOwnProperty("error")) {
        toastr.clear();
        toastr.error(data["error"]);
      } else {
        toastr.clear();
        toastr.success("Successfully logged in. ");

        setTimeout(function () {
          window.location.replace("/dashboard");
        }, 2000);
      }
    },
    error: function (data) {
      console.log("Error!");
    },
  });
}
