function create_pdf()
{
    $.get('create_pdf/', function (url) {
        window.open(url);
    })
}