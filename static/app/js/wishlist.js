// $(document).ready(function () {
   
//     $(".add-to-cart-btn").click(function () {
//         var product_Id = $(this).data("product_id");
//         var Id = $(this).data("id");
//         var url = "/shop/cart/add/?product_id="+product_Id;
//         var remove_url= '/shop/wishlist/remove/'+Id+'/';
//         $.ajax({
//             type: "GET",
//             url: url,
//             success: function (data) {
//                 $('#header_wishlist_count').html(data.wishlist_count)
//                 $('.header_cart_count').html(data.cart_count)
//                 Swal.fire({
//                     title: "<strong>Item Added to Cart</strong>",
//                     icon: "success",
//                     html: `
//                         <p>Your item has been added to the cart successfully!</p>
//                         <p>What would you like to do next?</p>
//                     `,
//                     showCloseButton: true,
//                     showCancelButton: true,
//                     focusConfirm: false,
//                     confirmButtonText: `
//                         View Cart
//                         <i class="fa fa-shopping-cart"></i>
//                     `,
//                     confirmButtonAriaLabel: "View Cart",
//                     cancelButtonText: `
//                         Checkout
//                         <i class="fa fa-credit-card"></i>
//                     `,
//                     cancelButtonAriaLabel: "Checkout",
//                     timer: 5000, 
//                     timerProgressBar: true
//                 }).then((result) => {
//                     if (result.isConfirmed) {
//                         // Redirect to the view cart page
//                         window.location.href = '/shop/cart/';
//                     } else if (result.dismiss === Swal.DismissReason.cancel) {
//                         // Redirect to the checkout page
//                         window.location.href = '/checkout/';
//                     }
//                 });
//             },
//             error: function (data) {
//                 if (data.status == '401') {
//                     window.location.href = '/accounts/login/';
//                 } else {
//                     // Display error message with SweetAlert
//                     Swal.fire({
//                         title: "Error",
//                         icon: "error",
//                         text: data.responseJSON.message || "An error occurred while adding the item to the cart."
//                     });
//                 }
                
//             }
//         });
//         // Send AJAX request to remove from wishlist
//         $.ajax({
//             url: remove_url,  // Replace with the actual URL for removing from wishlist
//             success: function (data) {
//                 Swal.fire("Item removed from wishlist!");
//                   window.location.reload();
//             },
//             error: function (error) {
//                 Swal.fire({
//                     title: "Error",
//                     icon: "error",
//                     text: data.responseJSON.message || "An error occurred while removing the item from the wishlist."
//                 });
//             }
//         });
//     });
//     $(".remove-btn").click(function () {
//         var product_Id = $(this).data("product_id");
//         var remove_url= '/shop/wishlist/remove/'+product_Id+'/';
//         $.ajax({
//             type: "GET",
//             url: remove_url,
            
//             success: function (data) {
                
//                   Swal.fire("Item removed from wishlist!");
//                   window.location.reload();
                
//             },
//             error: function (data) {
//                 // Display error message
//                 Swal.fire({
//                     title: "Error",
//                     icon: "error",
//                     text: data.responseJSON.message || "An error occurred while removing the item from the wishlist."
//                 });
//             }
//         });
//     });
//   });


$(document).ready(function () {
   
    $(".add-to-cart-btn").click(function () {
        var product_Id = $(this).data("product_id");
        var Id = $(this).data("id");
        var url = "/shop/cart/add/?product_id="+product_Id;
        var remove_url= '/shop/wishlist/remove/'+Id+'/';
        $.ajax({
            type: "GET",
            url: url,
            success: function (data) {
                $('#header_wishlist_count').html(data.wishlist_count)
                $('.header_cart_count').html(data.cart_count)
                Swal.fire({
                    title: "<strong>Item Added to Cart</strong>",
                    icon: "success",
                    html: 
                        `<p>Your item has been added to the cart successfully!</p>
                        <p>What would you like to do next?</p>`,
                    showCloseButton: true,
                    showCancelButton: true,
                    focusConfirm: false,
                    confirmButtonText: 
                        `View Cart
                        <i class="fa fa-shopping-cart"></i>`,
                    confirmButtonAriaLabel: "View Cart",
                    cancelButtonText: 
                        `Checkout
                        <i class="fa fa-credit-card"></i>`,
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
        // Send AJAX request to remove from wishlist
        $.ajax({
            url: remove_url,  
            success: function (data) {
                Swal.fire("Item removed from wishlist!");
                window.location.reload();
            },
            error: function (xhr) {
                Swal.fire({
                    title: "Error",
                    icon: "error",
                    text: xhr.responseJSON?.message || "An error occurred while removing the item from the wishlist."
                });
            }
        });
    });

    $(".remove-btn").click(function () {
        var product_Id = $(this).data("product_id");
        var remove_url= '/shop/wishlist/remove/'+product_Id+'/';
        $.ajax({
            type: "GET",
            url: remove_url,
            
            success: function (data) {
                Swal.fire("Item removed from wishlist!");
                window.location.reload();
            },
            error: function (xhr) {
                // Display error message
                Swal.fire({
                    title: "Error",
                    icon: "error",
                    text: xhr.responseJSON?.message || "An error occurred while removing the item from the wishlist."
                });
            }
        });
    });

    // Add to wishlist functionality
    console.log("Wishlist script loaded"); // Debug line
    console.log("Found wishlist buttons:", $(".btn-action-wishlist").length); // Debug line
    
    $(".btn-action-wishlist").click(function (e) {
        console.log("Wishlist button clicked!"); // Debug line
        e.preventDefault();
        var product_Id = $(this).data("product-id");
        var url = "/shop/wishlist/add/?product_id=" + product_Id;
        
        console.log("Product ID:", product_Id); // Debug line
        console.log("URL:", url); // Debug line
        
        $.ajax({
            type: "GET",
            url: url,
            beforeSend: function() {
                console.log("Sending AJAX request..."); // Debug line
            },
            success: function (data) {
                console.log("AJAX success:", data); // Debug line
                $('#header_wishlist_count').html(data.wishlist_count);
                Swal.fire({
                    title: "Success",
                    icon: "success",
                    text: data.message,
                    timer: 2000,
                    showConfirmButton: false
                });
            },
            error: function (xhr) {
                console.log("AJAX error:", xhr.status, xhr.responseText); // Debug line
                if (xhr.status == 401) {
                    window.location.href = '/accounts/login/';
                } else {
                    Swal.fire({
                        title: "Error",
                        icon: "error",
                        text: xhr.responseJSON?.message || "An error occurred while adding to wishlist."
                    });
                }
            }
        });
    });
});
