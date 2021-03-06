(function ($) {
  'use strict';

  // Preloader
  $(window).on('load', function () {
    $('#preloader').fadeOut('slow', function () {
      $(this).remove();
    });
  });

  
  // Instagram Feed
  if (($('#instafeed').length) !== 0) {
    var accessToken = $('#instafeed').attr('data-accessToken');
    var userFeed = new Instafeed({
      get: 'user',
      resolution: 'low_resolution',
      accessToken: accessToken,
      template: '<a href="{{link}}"><img src="{{image}}" alt="instagram-image"></a>'
    });
    userFeed.run();
  }

  setTimeout(function () {
    $('.instagram-slider').slick({
      dots: false,
      speed: 300,
      // autoplay: true,
      arrows: false,
      slidesToShow: 6,
      slidesToScroll: 1,
      responsive: [{
          breakpoint: 1024,
          settings: {
            slidesToShow: 4
          }
        },
        {
          breakpoint: 600,
          settings: {
            slidesToShow: 3
          }
        },
        {
          breakpoint: 480,
          settings: {
            slidesToShow: 2
          }
        }
      ]
    });
  }, 1500);


  // e-commerce touchspin
  $('input[name=\'product-quantity\']').TouchSpin();


  // Video Lightbox
  $(document).on('click', '[data-toggle="lightbox"]', function (event) {
    event.preventDefault();
    $(this).ekkoLightbox();
  });


  // Count Down JS
  $('#simple-timer').syotimer({
    year: 2022,
    month: 5,
    day: 9,
    hour: 20,
    minute: 30
  });

  //Hero Slider
  $('.hero-slider').slick({
    // autoplay: true,
    infinite: true,
    arrows: true,
    prevArrow: '<button type=\'button\' class=\'heroSliderArrow prevArrow tf-ion-chevron-left\'></button>',
    nextArrow: '<button type=\'button\' class=\'heroSliderArrow nextArrow tf-ion-chevron-right\'></button>',
    dots: true,
    autoplaySpeed: 7000,
    pauseOnFocus: false,
    pauseOnHover: false
  });
  $('.hero-slider').slickAnimation();


})(jQuery);

function bindCaptchaBtnClick() {
    $("#captcha-btn").on("click", function (event) {
        var $this = $(this);
        var email = $("input[name='email']").val();
        if (!email) {
            alert("??????????????????")
            return;
        }
        // ??????js???????????????ajax Async Javascript And XML???json???
        $.ajax({
            url: window.location.href+"/captcha",
            method: "POST",
            data: {
                "email": email
            },
            success: function (res) {
                var code = res['code'];
                if (code == 200) {
                    // ??????????????????
                    $this.off("click")
                    // ???????????????
                    var countdown = 60;
                    var timer = setInterval(function(){
                        countdown -= 1;
                        if(countdown > 0)
                        {
                            $this.text(countdown+"???");
                        }
                        else
                        {
                            $this.text("???????????????");
                            //????????????????????????
                            bindCaptchaBtnClick();
                            //???????????????
                            clearInterval(timer);
                        }
                    }, 1000);
                    alert('?????????????????????!')
                } else {
                    alert(res['message']);
                }
            }
        })
    });
}
// //????????????????????????
// function addressBtnClick(){
//
// }

/*
ajax?????????url????????????
?????????????????????
{
    ???code??????[400(????????????),200],
    ???price????????????????????????
}
*/
//????????????????????????
function addressBtnClick(){
    $(document).on("click",".tf-ion-close",function (event) {
         var $this=$(this);
         //??????????????????????????????id
         var addressId=parseInt($this.parent().next().text());
         if(!addressId){
             return;
         }

         $.ajax({
             url:"/user/address_delete",
             method:"POST",
             data:{
                'addressId': addressId
             },
             success: function (res) {
                var code=res['code'];
                if(code==200){
                    // ??????????????????
                    $this.off("click");
                    //???????????????
                    $this.parents('tr').remove();
                }else{
                    alert(res['message']);
                }
             }
        })
    })
}

function addAddressBtnClick(){
    $(document).on("click",".tf-pencil2",function () {
         var $this=$(this);
         //??????????????????????????????id
         var addressId=parseInt($this.parent().next().next().text());

         var name=$this.parents('tr').children().eq(0).text();
         var updateAddress=$this.parents('tr').children().eq(1).text();
         var telephoneNumber=$this.parents('tr').children().eq(2).text();
         console.log(name);
         console.log(updateAddress);
         console.log(telephoneNumber);

         //$("#firstGroup").before("<div class=\"form-group\"><div style=\"display: none\">addressId</div></div>");
        $("#address_id").attr('value',addressId)
        $("#updataAddress").modal();
    })
}

// function subsimtGoods(){
//     $("#inputImage").fileinput({
//              language: 'zh',
//              uploadUrl: "#",
//              allowedFileTypes: ['jpg','jepg']
//     })
//
//     console.log($("#inputImage").fileinput());
// }

// ????????????????????????????????????????????????
$(function () {
    //??????????????????????????????????????????
    bindCaptchaBtnClick();
    // addressBtnClick();
    // addAddressBtnClick();
    // subsimtGoods();
});