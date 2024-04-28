
$(document).ready(function () {
    function filterCompany() {
        var searchValue = $('#searchClients').val().toLowerCase();

        $('.carousel-item.active .card-container .card').each(function () {
            var companyName = $(this).data('appname').toLowerCase();

            if (companyName.includes(searchValue)) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    }
    $('#searchClients').on('keyup', filterCompany);
});
