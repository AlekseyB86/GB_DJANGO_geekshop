window.onload = function () {
    $('.basket_list').on('change', 'input[type=number]', function () {
        var target_href = event.target;

        $.ajax({
            url: "/basket/edit/" + target_href.name + "/" + target_href.value + "/",

            success: function (data) {
                $('.basket_list').html(data.result);
            }
        });
        return false;
    });
};
