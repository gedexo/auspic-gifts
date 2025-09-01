$(".cart-add-btn-quick").click(function () {
    var product_Id = $(this).data("product-id");
    var quantity = $("input[name='quantity']").val()
    var quantity = parseInt(quantity)
    console.log(product_Id, quantity)
    var url = "/shop/cart/add/?product_id="+product_Id+"&quantity="+quantity; 
    $.ajax({
        type: "GET",
        url: url,
        
        success: function (data) {
          window.location.href = "/shop/cart/";
          showAlert(data.message, "alert-success");
            
        },
        error: function (data) {
          if (data.status == '401') {window.location.href = '/accounts/login/';
          }else{showAlert(data.responseJSON.message, "alert-danger");}
      }
    });
});
// wishlist add
$(".btn-action-wishlist-quick").click(function () {
var product = $(this).data("product-id");
var url = "/shop/wishlist/add/?product_id="+product;
$.ajax({
type: "GET",
url: url,
success: function (data) {
    // Display success message
    $('#header_wishlist_count').html(data.wishlist_count)
    // Redirect to the wishlist page
    window.location.href = "/shop/wishlist/";
},
error: function (data) {
  if (data.status == '401') {window.location.href = '/accounts/login/';
  }else{showAlert(data.responseJSON.message, "alert-danger");}
}
})
})
function showAlert(message, alertClass) {
    var alertContainer = $("#alert-container");
    var alertDiv = $("<div>").addClass("alert " + alertClass).text(message);
    alertContainer.append(alertDiv);

    // Automatically hide the alert after 5 seconds
    setTimeout(function () {
        alertDiv.remove();
    }, 800);
}