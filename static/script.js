$(document).ready(function () {
    var i = 1;
    $("#add_row").click(function () {
        b = i - 1;
        $('#addr' + i).html($('#addr' + b).html());
        $('#item_nos').val(i + 1);
        $('#tab_logic').append('<tr id="addr' + (i + 1) + '"></tr>');
        i++;
    });
    $("#delete_row").click(function () {
        if (i > 1) {
            $("#addr" + (i - 1)).html('');
            i--;
        }
        calc();
    });
    
    $('#tab_logic tbody').on('keyup change', function () {
        calc();
    });
    $('#advance_amount').on('keyup change', function () {
        calc_total();
    });


});

function calc() {
    $('#tab_logic tbody tr').each(function (i, element) {
        var html = $(this).html();
        if (html != '') {
            calc_total();
        }
    });
}

function calc_total() {
    total = 0;
    $('.total').each(function () {
        total += parseInt($(this).val());
    });
    $('#sub_total').val(total.toFixed(2));
    $('#total_amount').val((total - $('#advance_amount').val()).toFixed(2));
}