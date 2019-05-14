$(document).ready(function () {
    // addSidebar();
});

function addSidebar() {
    $.ajax({
        type: "get",
        url: "../pieces/main_sider.html",
        async: true,
        success: function (data) {
//                                    console.log(data);
            $("header").after(data)
        }
    });
}

$(document).ready(function () {
    // addSearchbar();
    // addSearchbar();
});

function addSearchbar() {
    $.ajax({
        type: "get",
        url: "../pieces/interaction_search_bar.html",
        async: true,
        success: function (data) {
            $("#button-group").before(data)
        }
    });
}

function removeSearchBar() {
    $("#button-group").prev().remove();
}

function showSearchResult() {
    $.ajax({
        type: "get",
        url: "../pieces/search_result.html",
        async: true,
        success: function (data) {
            $("#button-group").next().after(data)
        }
    });
}

function showInteraction() {
    $("#medic-search-area").next().remove();

    post_data = [];
    inputs = $("input[name='medic-input']");
    console.log(inputs);
    for (let d = 0; d < inputs.length; d++) {
        post_data.push({'name': inputs.eq(d).val()});
    }
    console.log(JSON.stringify(post_data));
    $.ajax({
        type: 'POST',
        url: "http://127.0.0.1:8000/query/medic_interact/",
        data: JSON.stringify(
            post_data
            // {'name': '西咪替丁片'},
            // {'name': '格列吡嗪缓释片'}
            // {'name': '鼻炎康片'}
        ),
        dataType: 'json',
        success: function (response, status) {
            // console.log(response);

            $.ajax({
                type: "get",
                url: "../pieces/interaction_details.html",
                async: true,
                success: function (html) {
                    var doc = $(html);
                    // var data = [
                    //     {
                    //         'medic1': "药物1",
                    //         'medic2': "药物2",
                    //         'type': "冲突",
                    //         'rank': 33,
                    //         'rankCN': '轻微',
                    //         'details': "balabala"
                    //     }, {
                    //         'medic1': "药物1",
                    //         'medic2': "药物2",
                    //         'type': "冲突",
                    //         'rank': 67,
                    //         'rankCN': '轻微',
                    //         'details': "balabala"
                    //     }, {
                    //         'suggestion': 'balabala'
                    //     }
                    // ];


                    for (let d = 0; d < response.length; d++) {
                        // console.log(response[d]);
                        doc.find("#medic-interaction").append('\n<span class="label label-info">' + response[d]['medic1'] + '</span>');
                        doc.find("#medic-interaction").append('\n<span class="label label-info">' + response[d]['medic2'] + '</span>');
                        doc.find("#medic-interaction").append('<span class="text-red">&ensp;<strong>' + response[d]['type'] + '</strong></span><p></p>');
                        doc.find("#medic-interaction").append('<div class="progress" style="width: 20%"><div class="progress-bar progress-bar-red"' +
                            ' role="progressbar" style="width: ' + response[d]['rank'] + '%"></div></div>');
                        doc.find("#medic-interaction").append('<p><strong>作用等级：</strong>' + response[d]['rankCN'] + '</p></span>');
                        doc.find("#medic-interaction").append('<p><strong>说明：</strong>&ensp;' + response[d]['details'] + '</p><hr>');
                    }
                    doc.find("#medic-interaction").append('<strong><i class="fa fa-file-text-o margin-r-5"></i>用药建议：</strong>');
                    doc.find("#medic-interaction").append('<p>' + response[response.length - 1]['suggestion'] + '</p>');
                    $("#medic-search-area").after(doc);
                }
            });
        }
    });
}

function setText() {

}