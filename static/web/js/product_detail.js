$(".cart-add-btn").click(function () {
    var product_Id = $(this).data("product-id");
    var quantity = $("input[name='quantity']").val()
    var quantity = parseInt(quantity)
    console.log(product_Id, quantity)
    var url = "/shop/cart/add/?product_id="+product_Id+"&quantity="+quantity; 
    $.ajax({
        type: "GET",
        url: url,
        
        success: function (data) {
          $('.header_cart_count').html(data.cart_count)
          Swal.fire({
            title: "<strong>Item Added to Cart</strong>",
            icon: "success",
            html: `
                <p>Your item has been added to the cart successfully!</p>
                <p>What would you like to do next?</p>
            `,
            showCloseButton: true,
            showCancelButton: true,
            focusConfirm: false,
            confirmButtonText: `
                View Cart
                <i class="fa fa-shopping-cart"></i>
            `,
            confirmButtonAriaLabel: "View Cart",
            cancelButtonText: `
                Checkout
                <i class="fa fa-credit-card"></i>
            `,
            cancelButtonAriaLabel: "Checkout",
            timer: 5000, 
            timerProgressBar: true
          }).then((result) => {
              if (result.isConfirmed) {
                  // Redirect to the view cart page
                  window.location.href = '/shop/cart/';
              } else if (result.dismiss === Swal.DismissReason.cancel) {
                  // Redirect to the checkout page
                  window.location.href = '/checkout/';
              }
          });
          
            
        },
        error: function (data) {
          if (data.status == '401') {
            window.location.href = '/accounts/login/';
        } else {
            // Display error message with SweetAlert
            Swal.fire({
                title: "Error",
                icon: "error",
                text: data.responseJSON.message || "An error occurred while adding the item to the cart."
            });
        }
      }
    });
});
// wishlist add
$(".add-wishlist-btn").click(function () {
var product = $(this).data("product-id");
var url = "/shop/wishlist/add/?product_id="+product;
$.ajax({
type: "GET",
url: url,
success: function (data) {
    // Display success message
    $('#header_wishlist_count').html(data.wishlist_count)
    // Redirect to the wishlist page
    Swal.fire({
      title: "Item added to wishlist",
      icon: "success",
      text: "Your item has been added to the wishlist.",
      showCloseButton: true,
      showCancelButton: true,
      focusConfirm: false,
      confirmButtonText: "View Wishlist",
      confirmButtonAriaLabel: "View Wishlist",
      cancelButtonText: "Continue Shopping",
      cancelButtonAriaLabel: "Continue Shopping",
      timer: 5000, 
      timerProgressBar: true
  }).then((result) => {
      if (result.isConfirmed) {
          // Confirm button (View Wishlist) was clicked
          window.location.href = "/shop/wishlist/";
      } else {
          // Cancel button (Continue Shopping) was clicked
          window.location.href = "/shop/";
      }
  });
  
},
error: function (data) {
  if (data.status == '401') {
      window.location.href = '/accounts/login/';
  } else {
      // Display error message with SweetAlert
      Swal.fire({
          title: "Error",
          icon: "error",
          text: data.responseJSON.message || "An error occurred while adding the item to the wishlist."
      });
  }
}
});
})