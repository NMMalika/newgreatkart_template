// some scripts
console.log("SCRIPT.JS LOADED");
// jquery ready start
$(document).ready(function() {
	// jQuery code


    /* ///////////////////////////////////////

    THESE FOLLOWING SCRIPTS ONLY FOR BASIC USAGE, 
    For sliders, interactions and other

    */ ///////////////////////////////////////
    

	//////////////////////// Prevent closing from click inside dropdown
    $(document).on('click', '.dropdown-menu', function (e) {
      e.stopPropagation();
    });


    $('.js-check :radio').change(function () {
        var check_attr_name = $(this).attr('name');
        if ($(this).is(':checked')) {
            $('input[name='+ check_attr_name +']').closest('.js-check').removeClass('active');
            $(this).closest('.js-check').addClass('active');
           // item.find('.radio').find('span').text('Add');

        } else {
            item.removeClass('active');
            // item.find('.radio').find('span').text('Unselect');
        }
    });


    $('.js-check :checkbox').change(function () {
        var check_attr_name = $(this).attr('name');
        if ($(this).is(':checked')) {
            $(this).closest('.js-check').addClass('active');
           // item.find('.radio').find('span').text('Add');
        } else {
            $(this).closest('.js-check').removeClass('active');
            // item.find('.radio').find('span').text('Unselect');
        }
    });



	//////////////////////// Bootstrap tooltip
	if($('[data-toggle="tooltip"]').length>0) {  // check if element exists
		$('[data-toggle="tooltip"]').tooltip()
	} // end if




    
}); 
// jquery end

$(document).ready(function () {
  console.log("JS READY");

  $(document).on("change", "#colorSelect", function () {
    console.log("Color change detected");

    const color = $(this).val();
    const productId = $(this).data("product-id");
    const sizeSelect = $("#sizeSelect");

    sizeSelect.prop("disabled", true);
    sizeSelect.html("<option>Loading...</option>");

    $.ajax({
      url: "/store/get-sizes/",
      type: "GET",
      data: {
        product_id: productId,
        color: color,
      },
      success: function (response) {
        console.log("AJAX SUCCESS:", response);

        sizeSelect.html(
          '<option value="" disabled selected>Select Size</option>'
        );

        response.sizes.forEach(function (size) {
          sizeSelect.append(`<option value="${size}">${size}</option>`);
        });

        sizeSelect.prop("disabled", false);
      },
      error: function (xhr) {
        console.error("AJAX ERROR:", xhr.responseText);
      },
    });
  });
});


$(document).ready(function () {
  // ... your existing code to load sizes ...

  $("#sizeSelect").change(function () {
    var productId = $("#colorSelect").data("product-id");
    var color = $("#colorSelect").val();
    var size = $(this).val();

    if (color && size) {
      $.ajax({
        url: "/cart/check_cart/", // Ensure this matches your URL path
        data: {
          product_id: productId,
          color: color,
          size: size,
        },
        // Inside your AJAX success function
        success: function (response) {
          var container = $("#cart-button-container");
          if (response.in_cart) {
            container.html(`
            <div class="d-flex mb-3">
                <a href="#" class="btn btn-success mr-2 flex-grow-1">
                    <span class="text">Already added in Cart</span>
                    <i class="fas fa-check"></i>
                </a>
                <a href="/cart/" class="btn btn-primary flex-grow-1">
                    <span class="text">View Cart</span>
                    <i class="fas fa-eye"></i>
                </a>
            </div>
            <a href="/store/" class="btn btn-warning btn-block">
                <span class="text">Continue Shopping</span>
                <i class="fas fa-shopping-bag"></i>
            </a>
        `);
          } else {
            container.html(`
            <button type="submit" class="btn btn-primary btn-block">
                <span class="text">Add to cart</span>
                <i class="fas fa-shopping-cart"></i>
            </button>
        `);
          }
        },
      });
    }
  });
});
