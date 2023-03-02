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

$(document).ready(function () {
    $('#printDoc').click(function () {
        // Create a new element to contain the body content
        var printContent = document.createElement('div');
        printContent.innerHTML = document.body.innerHTML;

        // Remove the title and URL elements
        var buttons = printContent.querySelector('.btn');
        buttons.forEach(function (button) {
            button.style.display = 'none'; // hide each button
        });

        // Open a new window and print the contents
        var printWindow = window.open();
        printWindow.document.write(printContent.innerHTML);
        printWindow.document.close();
        printWindow.focus();
        printWindow.print();
        printWindow.close();
    })
});


$(document).ready(function () {
    $('#generatePDF').click(function () {
        var element = document.body; // choose the element that you want to convert to PDF
        var buttons = element.querySelectorAll('.btn'); // select all buttons on the page
        buttons.forEach(function (button) {
            button.style.display = 'none'; // hide each button
        });
        filename = document.getElementById('filename').getAttribute('data-filename');
        var opt = {
            margin: [0, 0, 0, 0],
            filename: `invoice_${filename}`,
            image: { type: 'jpeg', quality: 1 },
            html2canvas: { scale: 3, dpi: 300, letterRendering: true, useCORS: true },
            jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' }
        };
        html2pdf().set(opt).from(element).save();
        setInterval(function () {
            buttons.forEach(function (button) {
                button.style.display = ''; // show each button
            });
        }, 1000);
    });
});

function copyToClipboard() {
    link = document.getElementById('copyLink').getAttribute('data-share');
    navigator.clipboard.writeText(link);
}
if (window.location.pathname == '/') {
const tomorrow = new Date();
tomorrow.setDate(tomorrow.getDate() + 1);
const formattedDate = tomorrow.toISOString().slice(0, 10);
document.getElementById("invoice_due_date").setAttribute("min", formattedDate);
}