(function ($) {
    "use strict";

    // Ensure jQuery and Slick exist before running
    if (typeof $ === "undefined") {
        console.error("jQuery is not loaded!");
        return;
    }

    if (typeof $.fn.slick === "undefined") {
        console.error("Slick is not loaded!");
        return;
    }

    /* Product Details */
    var productDetails = function () {
        if ($(".product-image-slider").length) {
            $(".product-image-slider").slick({
                slidesToShow: 1,
                slidesToScroll: 1,
                arrows: false,
                fade: false,
                asNavFor: ".slider-nav-thumbnails",
            });
        }

        if ($(".slider-nav-thumbnails").length) {
            $(".slider-nav-thumbnails").slick({
                slidesToShow: 4,
                slidesToScroll: 1,
                asNavFor: ".product-image-slider",
                dots: false,
                focusOnSelect: true,
                prevArrow:
                    '<button type="button" class="slick-prev"><i class="fi-rs-arrow-small-left"></i></button>',
                nextArrow:
                    '<button type="button" class="slick-next"><i class="fi-rs-arrow-small-right"></i></button>',
            });
        }

        // On before slide change, match active thumbnail to current slide
        $(".product-image-slider").on("beforeChange", function (event, slick, currentSlide, nextSlide) {
            $(".slider-nav-thumbnails .slick-slide").removeClass("slick-active");
            $(".slider-nav-thumbnails .slick-slide").eq(nextSlide).addClass("slick-active");
        });

        //Elevate Zoom
        if ($(".product-image-slider").length) {
            if ($(window).width() > 768) {
                $(".product-image-slider .slick-active img").elevateZoom({
                    zoomType: "inner",
                    cursor: "crosshair",
                    zoomWindowFadeIn: 500,
                    zoomWindowFadeOut: 750,
                });
            }
        }
    };

    // Run functions after document is ready
    $(document).ready(function () {
        productDetails();
    });

})(jQuery);
document.addEventListener("DOMContentLoaded", function () {
    var triggerTabList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tab"]'));
    triggerTabList.forEach(function (tab) {
        tab.addEventListener("click", function (event) {
            event.preventDefault();
            var tabInstance = new bootstrap.Tab(this);
            tabInstance.show();
        });
    });
});

