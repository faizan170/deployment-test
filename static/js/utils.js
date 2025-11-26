function loadImg(event){
    // Hide any previous error when selecting a new file
    $('#errorMsg').hide();
    // Show preview image for selected file before upload (if any)
    if (event && event.target && event.target.files && event.target.files[0]) {
        $('#imagePreview').attr('src', URL.createObjectURL(event.target.files[0]));
    } else {
        $('#imagePreview').attr('src', '');
    }
}

// Upload image using ajax
$('#upload').click(function(){
    // Hide previous error and guard for selected file
    $('#errorMsg').hide();

    if (!$('#fileInput')[0].files || $('#fileInput')[0].files.length === 0) {
        $('#errorMsg').text('Please select an image before processing.').show();
        return;
    }

    var $btn = $(this);
    // change button state to processing
    $btn.prop('disabled', true).text('Processing...');

    // Create form data
    var formData = new FormData();
    // add file to form data
    formData.append('image', $('#fileInput')[0].files[0]);

    $.ajax({
        url: '/process', // API Endpoint
        type: 'POST', // Request type
        data: formData, // Request data
        contentType: false,
        processData: false,
        success: function(data){
            // On request success, show image from server and hide errors
            $('#imagePreview').attr('src', data.output_image);
            $('#errorMsg').hide();
        },
        error: function(xhr){
            // show error message (try to use server-provided message)
            var msg = 'Failed to process image. Please try again.';
            try {
                if (xhr && xhr.responseJSON && xhr.responseJSON.error) {
                    msg = xhr.responseJSON.error;
                } else if (xhr && xhr.responseText) {
                    msg = xhr.responseText;
                }
            } catch(e) {}
            $('#errorMsg').text(msg).show();
        },
        complete: function(){
            // restore button state
            $btn.prop('disabled', false).text('Process Image');
        }
    });
});
