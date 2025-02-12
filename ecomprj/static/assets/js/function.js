console.log('hello')
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