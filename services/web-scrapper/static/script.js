$(function() {
    // Listen for form submission
    $('#scrape-form').on('submit', function(event) {
        event.preventDefault();

        // Hide existing error messages
        $('#error').addClass('hidden');

        // Show loading spinner
        $('#loading').removeClass('hidden');

        // Disable form inputs and submit button
        $('#scrape-form input, #scrape-form button').prop('disabled', true);

        // Clear previous results
        $('#results tbody').empty();

        // Fetch the sitemap URLs
        var sitemapUrl = $('#sitemap-url').val();
        var excludeIds = $('#exclude-ids').val().split(',').map(function(id) {
            return id.trim();
        }).filter(function(id) {
            return id !== '';
        });
        var excludeClasses = $('#exclude-classes').val().split(',').map(function(className) {
            return className.trim();
        }).filter(function(className) {
            return className !== '';
        });
        $.ajax({
            method: 'POST',
            url: '/scrape',
            data: JSON.stringify({
                sitemap_url: sitemapUrl,
                exclude_ids: excludeIds,
                exclude_classes: excludeClasses
            }),
            contentType: 'application/json'
        }).done(function(data) {
            // Hide loading spinner
            $('#loading').addClass('hidden');

            // Enable form inputs and submit button
            $('#scrape-form input, #scrape-form button').prop('disabled', false);

            // Display the results table
            $('#results').removeClass('hidden');

            // Add each row to the table
            var tbody = $('#results tbody');
            data.forEach(function(result) {
                var row = $('<tr>');
                row.append($('<td>').text(result.url));
                row.append($('<td>').text(result.meta_title || ''));
                row.append($('<td>').text(result.meta_description || ''));
                row.append($('<td>').text(result.body || ''));
                tbody.append(row);
            });

            // Set the download link href attribute to the JSON file URL
            var downloadLink = $('#download-button');
            downloadLink.attr('href', '/download?file=' + data.file_name);
            downloadLink.removeClass('hidden');
        }).fail(function(jqXHR, textStatus, errorThrown) {
            // Hide loading spinner
            $('#loading').addClass('hidden');

            // Enable form inputs and submit button
            $('#scrape-form input, #scrape-form button').prop('disabled', false);

            // Display the error message
            $('#error').removeClass('hidden');
        });
    });

    // Listen for download button click
    $('#download-button').on('click', function(event) {
        event.preventDefault();

        // Send a GET request to the download URL
        window.location.href = $(this).attr('href');
    });
});
