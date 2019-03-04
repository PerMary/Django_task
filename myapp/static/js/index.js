function create_pdf()
{
    $.get('documents/create_pdf/', function (url) {
        window.open(url);
    })
}