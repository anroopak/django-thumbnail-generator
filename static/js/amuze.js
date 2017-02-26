const DEFAULT_THUMBNAIL = "static/img/default-thumbnail.jpg";
const GET_URL = 'v1/media/';
const SUPPORT_FILE_FORMATS = [
    // For .mp4
    'video/mp4',
    // For .mov
    'video/quicktime',
    // For .avi
    'video/msvideo',
    'video/x-msvideo',
    'video/avi'
];

var files;
var pagination = {
    offset: 0,
    limit: 12,
    ordering: "-media_id"
};
var deleteMediaId = -1;

$(document).ready(function() {

    loadList({});

    $('#deleteModal').on('show.bs.modal', function(event) {
        var button = $(event.relatedTarget);
        var mediaId = button.data('media-id');
        var mediaName = button.data('media-name');
        var modal = $(this);
        modal.find('.modal-body .deleteText').text(mediaName);
        deleteMediaId = mediaId;
    })

    $("#deleteMediaBtn").on('click', deleteMedia);

    $('input[type=file]').on('change', prepareUpload);

    $('#uploadBtn').on('click', uploadFiles);

    $('#refreshBtn').on('click', loadList);


});

function loadList() {

    var searchText = $("#searchBox").val();
    console.log("searchText : " + searchText);
    var params = pagination;
    if (searchText) { params.search = searchText; } else { delete params.search; }

    var paramArr = [];
    for (p in params) {
        paramArr.push(p + "=" + encodeURIComponent(params[p]));
    }
    var paramStr = paramArr.join("&");


    $("#list-boxes").fadeOut(function() {
        $("#loading-block").fadeIn();

        var xhr = new XMLHttpRequest();
        xhr.open('GET', GET_URL + '?' + paramStr, true);
        xhr.send();
        xhr.onload = function() {
            var listBoxHtml = "";
            if (xhr.status >= 200 && xhr.status < 300) {
                var response = JSON.parse(xhr.responseText);
                if (response.count === 0) {
                    listBoxHtml = '<div class="alert alert-info alert-dismissible" role="alert"> \
                  <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button> \
                  <strong>Empty!</strong> No videos found. Lets upload.\
                </div>';
                } else {
                    for (var i = 0; i < response.results.length; i++) {
                        var thisMedia = response.results[i];
                        var mediaThumbnailUrl = thisMedia.thumbnail_url || DEFAULT_THUMBNAIL;
                        var mediaName = thisMedia.name;
                        var mediaId = thisMedia.media_id;
                        var mediaUrl = thisMedia.media_url;
                        listBoxHtml += '<div class="col-md-3 col-xs-12 col-sm-6"> \
                        <div class="amuze-thumbnail"> \
                            <img src="' + mediaThumbnailUrl + '" class="img-responsive"> \
                            <p> \
                            <button type="button" class="btn btn-danger btn-xs" data-toggle="modal" data-target="#deleteModal" data-media-id=' + mediaId + ' data-media-name="' + mediaName + '"> \
                                <span class="glyphicon glyphicon-trash"></span> \
                            </button> \
                            <a href="' + mediaUrl + '" target="_blank" class="btn btn-primary btn-xs">Play <span class="glyphicon glyphicon-play-circle"></span></a>\
                            ' + mediaName + ' \
                            </p> \
                        </div> \
                    </div>';
                    }
                }
            } else {
                listBoxHtml = '<div class="alert alert-danger alert-dismissible" role="alert"> \
                  <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button> \
                  <strong>Failed!</strong> Error in Loading.\
                </div>';
            }
            $("#list-boxes .row").html(listBoxHtml);
            $("#loading-block").fadeOut(function() {
                $("#list-boxes").fadeIn();
            });
        };
    });
}

function prepareUpload(event) {
    files = event.target.files;
}

function deleteMedia() {
    var xhr = new XMLHttpRequest();
    xhr.open('DELETE', 'v1/media/' + deleteMediaId + '/', true);
    xhr.send();
    xhr.onload = function() {
        if (xhr.status >= 200 && xhr.status < 300) {
            $("#deleteMessage").html('<div class="alert alert-success alert-dismissible" role="alert"> \
              <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button> \
              <strong>Done!</strong> File deleted successfully.\
            </div>');
            loadList({});
        } else {
            $("#deleteMessage").html('<div class="alert alert-danger alert-dismissible" role="alert"> \
              <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button> \
              <strong>Failed!</strong> Error in deleting.\
            </div>');
        }
    };
}

// Catch the form submit and upload the files
function uploadFiles(event) {
    $("#uploadBtn").attr("disabled", true);
    listBoxHtml = '<div class="alert alert-info alert-dismissible" role="alert"> \
                  <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button> \
                  <strong>Uploading!</strong> Please wait while upload is happening.\
                </div>';
    $("#list-boxes .row").html(listBoxHtml).fadeIn();
    // files = event.target.files;
    // Loader
    var data = new FormData();
    var error = 0;
    for (var i = files.length - 1; i >= 0; i--) {
        var file = files[i];
        if (!file.type.match('video.*') || (SUPPORT_FILE_FORMATS.indexOf(file.type) === -1)) {
            $("#uploadMessage").html('<div class="alert alert-warning alert-dismissible" role="alert"> \
              <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button> \
              <strong>Invalid Content Type!</strong> Support file formats - .mp4, .avi, .mov .\
            </div>');
            error = 1;
        } else if (file.size > 15 * 1024 * 1024) {
            $("#uploadMessage").html('<div class="alert alert-warning alert-dismissible" role="alert"> \
              <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button> \
              <strong>File too large!</strong> Supported file size is 15 MB.\
            </div>');
            error = 1;
        } else {
            data.append('media', file, file.name);
            data.append('name', $("#mediaName").val());
        }
    }
    if (!error) {
        var xhr = new XMLHttpRequest();
        xhr.open('POST', 'v1/media/', true);
        xhr.send(data);
        xhr.onload = function() {
            if (xhr.status >= 200 && xhr.status < 300) {
                $("#uploadMessage").html('<div class="alert alert-success alert-dismissible" role="alert"> \
              <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button> \
              <strong>Done!</strong> File uploaded successfully.\
            </div>');
                loadList({});
            } else {
                $("#uploadMessage").html('<div class="alert alert-danger alert-dismissible" role="alert"> \
              <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button> \
              <strong>Failed!</strong> Error in Upload.\
            </div>');
            }
        };
    }
    $("#uploadBtn").attr("disabled", false);
}
