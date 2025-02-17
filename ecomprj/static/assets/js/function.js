console.log("JS file is loaded!");

$('#commentForm').submit(function(e)
{
e.preventDefault()
const month = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
const dt = new Date();
console.log(dt)
const comment_date = dt.getUTCDate() + " "+month[dt.getUTCMonth()]+","+dt.getFullYear()

$.ajax({
    data: $(this).serialize(),
    method: $(this).attr('method'),
    url: $(this).attr('action'),
    datatype: 'json',
    success: function(response){
        console.log('comment saved in db')
        if (response.bool==true){
            $('#review-response').html('Review added successfully')
            $('.hide-review-form').hide()
            $('.hide-review-line').hide()

            let _html = '<div class="single-comment justify-content-between d-flex mb-30">'
                _html+=  '<div class="user justify-content-between d-flex">'
                _html+='<div class="thumb text-center">'
                _html+='<img src="https://pinnacle.works/wp-content/uploads/2022/06/dummy-image.jpg" alt="" />'
                _html+='<a href="#" class="font-heading text-brand">'+response.context.user+'</a>'
                _html+='</div>'

                _html+='<div class="desc">'
                _html+='<div class="d-flex justify-content-between mb-10">'
                _html+='<div class="d-flex align-items-center"></div>'
                _html+='<span class="font-xs text-muted">'+comment_date+ '</span>'
                _html+='</div>'
                _html+='<div class>'
                for(let i=1;i<=response.context.rating;i++){
                _html+='<i class="fas fa-star text-warning"></i>'
                }
                _html+='</div>'
                _html+='<p class="mb-10">' +response.context.review+ '</p>'
                _html+='</div>'
                _html+='</div>'
                _html+='</div>'

                $('.comment-list').prepend(_html)
    

        }
    }
        
    

    
})
});


$(document).ready(function (){
    $('.filter-checkbox, #filter-btn').on('click', function(){
        console.log('filter is clicked')
        filter_object={}
        $('.filter-checkbox').each(function(){
            let filter_val = $(this).val()
            let filter_key=$(this).data('filter')
            let min_price = $('#max_price').attr('min')
            let max_price = $('#max_price').val()
            filter_object.min_price = min_price
            filter_object.max_price = max_price
            filter_object[filter_key]=Array.from(document.querySelectorAll('input[data-filter='+filter_key+']:checked')).map(function(e){
                return e.value
            })
        })
        console.log('json check',filter_object)
        $.ajax({
            data: filter_object,
            url: '/filter-products',
            dataType: 'json',
            beforeSend: function(){
                console.log('searching..')
            },
            success: function(response){
                console.log('response_data->',response.data)
                $('#filtered-product').html(response.data)

            }
        })
    })
    $('#max_price').on('blur',function(){
        let min_price = $(this).attr('min')
        let max_price = $(this).attr('max')
        let current_price = $(this).val()



        if(current_price < parseInt(min_price) || current_price>parseInt(max_price)){
            // console.log('error')
            min_price = Math.round(min_price*100)/100
            max_price = Math.round(max_price*100)/100
            alert('Price should be between $'+min_price+' and $'+max_price)
            $(this).val(min_price)
            $('#range').val(min_price)
            $(this).focus()

            return false
        }

    })
    // $('.btn').on('click',function(e){
    //     e.preventDefault()
    //     console.log('button is clicked')
    // })
}
)

// add to cart funtionality
// $('#add-to-cart-btn').on('click', function(){
//     let product_qty = $('#product-quantity').val()
//     let product_title = $('.product-title').val()
//     let product_id = $('.product-id').val()
//     let product_price = $('#current-price').text()
//     let this_val = $(this)
//     console.log('qty',product_qty)
//     console.log('title',product_title)
//     console.log('id',product_id)
//     console.log('price',product_price)

//     $.ajax({
//         url: '/add-to-cart',
//         data: {
//             'id': product_id,
//             'quantity': product_qty,
//             'title': product_title,
//             'price': product_price
//         },
//         dataType: 'json',
//         beforeSend: function(){
            
//             console.log('adding product to cart')
//         },
//         success: function(response){
//             this_val.html('Item added to cart')
//             console.log('added to cart')
//             $('.cart-items-count').text(response.totalcartitems)
//         }
//     })
// })

$('.add-to-cart-btn').on('click', function(){
    let this_val = $(this)
    let index = this_val.data('index')
    let product_qty = $('.product-quantity-'+index).val()
    let product_title = $('.product-title-'+index).val()
    let product_id = $('.product-id-'+index).val()
    let product_price = $('.current-product-price-'+index).text()
    let product_pid = $('.product-pid-'+index).val()
    let product_image = $('.product-image-'+index).val()
    console.log('qty',product_qty)
    console.log('title',product_title)
    console.log('id',product_id)
    console.log('price',product_price)
    console.log('index',index)
    console.log('image',product_image)
    console.log('pid',product_pid)

    $.ajax({
        url: '/add-to-cart',
        data: {
            'id': product_id,
            'quantity': product_qty,
            'title': product_title,
            'price': product_price,
            'pid':product_pid,
            'image': product_image,
        },
        dataType: 'json',
        beforeSend: function(){
            
            console.log('adding product to cart')
        },
        success: function(response){
            // this_val.html('✔️')
            this_val.html('✔️')
            console.log('added to cart')
            $('.cart-items-count').text(response.totalcartitems)
        }
    })
})


// delete product from cart
$(document).on('click','.delete-product',function(){
    let this_val = $(this)
    let product_id = $(this).attr('data-product')
    console.log('produtc id',product_id)

    $.ajax({
        url: '/delete-from-cart',
        data: {
            'id':product_id
        },
        dataType: 'json',
        beforeSend: function(){
            this_val.hide()
        },
        success: function(response){
            this_val.show()
            $('.cart-items-count').text(response.totalcartitems)
            $('#cart-list').html(response.data)
        }
    })
})

// update the cart

$(document).on('click','.update-product',function(){
    let product_id = $(this).attr('data-product')
    let this_val = $(this)
    let product_quantity = $('.product-quantity-'+product_id).val()
    console.log('product id ->',product_id)

    $.ajax({
        url: '/update-cart',
        data: {
            'id':product_id,
            'quantity': product_quantity
        },
        dataType: 'json',
        beforeSend: function(){
            this_val.hide()
        },
        success: function(response){
            this_val.show()
            $('.cart-items-count').text(response.totalcartitems)
            $('#cart-list').html(response.data)
        }
    })
})


// address default field
$(document).on('click','.make-default-address',function(){
    let id = $(this).attr('data-address-id')
    let this_val=$(this)
    console.log('button id->',id)
    console.log('button details->',this_val)

    $.ajax({
        url: '/make-default-address',
        data:{
            'id':id
        },
        dataType: 'json',
        success: function(response){
            console.log('changing address')
            if (response.boolean == true){
                $('.action_btn').show()
                $('.check-marked').hide()
                $('.button-'+id).hide()
                $('.check'+id).show()

            }
        }

    })
})

// add to wishlist
$(document).on('click','.add-to-wishlist',function(){
    let product_id=$(this).attr('data-product-item')
    let this_val = $(this)
    console.log('btn Id->',product_id)
    $.ajax({
        url:'/add-to-wishlist',
        data:{
            'id':product_id
        },
        dataType:'json',
        success: function(response){
            this_val.html('✔️')
            console.log('wishlist is clicked')
            if(response.bool == true){
                console.log('added to WL')
            }
        }
    })

})

// remove from wishlist
$(document).on('click','.remove-btn',function(){
    let product_id=$(this).attr('data-product-id')
    let this_val=$(this)
    console.log('remove btn is clickable with product id->',product_id)

    $.ajax({
        url: '/remove-from-wishlist',
        data:{
            'id':product_id
        },
        dataType: 'json',
        beforeSend:function(){
            console.log('sending request to remove from WL')
        },
        success: function(response){
            if(response.bool == true){
                console.log('deleted from WL')
                console.log('the json will be strucured --->',response.object)
                $('.wishlist-test').html(response.data)
            }
        }
    })
})