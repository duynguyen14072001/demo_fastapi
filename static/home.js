$(document).ready(function () {
    $('#btnAdd').click(function () {
        $('#overlay').show();
        $('#modalAdd').slideDown();
    })

    $('#btnClose').click(function () {
        $('#overlay').hide();
        $('#modalAdd').hide('slide');
    });
});

$(document).on('click', '.btn-delete', function (e) {
    e.preventDefault();
    const formAction = $(this).closest('form');
    Swal.fire({
        title: "Are you sure?",
        text: "You won't be able to revert this!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Yes, delete it!"
    }).then((result) => {
        if (result.isConfirmed) {
            $.ajax({
                url: formAction.attr('action'),
                method: 'DELETE',
                success: function (response) {
                    formAction.submit();
                    window.location.href = "/";
                },
            });
        }
    });
})