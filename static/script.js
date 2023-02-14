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
});

$('#invoice_type').change(function () {
    if ($(this).val() == 'paid') {
        $('#transaction').show();
    }
    else {
        $('#transaction').hide();
    }
});

$('#trans_select').change(function () {
    console.log($(this).val() === 'other');
    if ($(this).val() === 'other') {
        $('#paid_through_other').show();
    }
    else {
        $('#paid_through_other').hide();
    }
});