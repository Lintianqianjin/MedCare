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

function changeSearchBy() {
    var t1 = $("#search-by-1").text();
    var t2 = $("#search-by-2").text();
    $("#search-by-1").text(t2);
    $("#search-by-1").append('<span class="fa fa-caret-down"></span>');
    $("#search-by-2").text(t1);
}

function showSearchResult() {
    // console.log($("#medic-search-button").parent().parent().next());
    $("#medic-search-button").parent().parent().next().next().remove();
    $("#medic-search-button").parent().parent().next().remove();
    $("#medic-search-button").parent().parent().parent().parent().next().remove();

    post_data = {};
    console.log("'" + $("#search-by-1").text() + "'");
    if ($("#search-by-1").text().indexOf('名称') != -1) {
        post_data['searchBy'] = 'name';
        post_data['keyword'] = $("input#search-input").val();
    } else {
        post_data['searchBy'] = 'ingredient';
        post_data['keyword'] = $("input#search-input").val();
    }
    console.log(post_data);

    $.ajax({
        type: 'POST',
        url: "../../query/medic_search/",
        data: JSON.stringify(
            post_data
        ),
        dataType: 'json',
        success: function (response, status) {
            console.log(response)
            $.ajax({
                type: "get",
                url: "../../static/pieceHtml/search_result.html",
                async: true,
                success: function (html) {
                    var doc = $(html);

                    for (var d = 0; d < response.length; d++) {
                        // console.log(data[d].name);
                        // console.log(html);
                        doc.find('#table-body').append('<tr onclick="showMedicDetails(this)"><td>' + response[d].name + '</td><td>' + response[d].ingredients + '</td><td>'
                            + response[d].description + '</td><td>' + response[d].cures + '</td></tr>');
                    }

                    $("#medic-search-button").parent().parent().after(doc)
                }
            });
        }
    });
}


function showMedicDetails(obj) {
    $("#medic-search-area").next().remove();
    name1 = $(obj).find("td").eq(0).text();

    console.log('"' + name1 + '"');
    post_data = {
        'name': name1
    };

    $.ajax({
        type: 'POST',
        url: "../../query/medic_details/",
        data: JSON.stringify(
            post_data
        ),
        dataType: 'json',
        success: function (response, status) {
            $.ajax({
                type: "get",
                url: "../../static/pieceHtml/medic_details.html",
                async: true,
                success: function (html) {
                    var doc = $(html);
                    // var data = {
                    //     'illnesses': ['A', 'B', 'C'],
                    //     'ingredients': ['1', '2', '3'],
                    //     'labels': ['1', '2', '3'],
                    //     'description': "hhhhh"
                    // };

                    doc.find("#medic-name").append(post_data['name']);
                    for (let d = 0; d < response['cures'].length; d++) {
                        doc.find("#illnesses").append("<span class='label label-warning'>" + response['cures'][d] + "</span>\n");
                    }
                    for (let d = 0; d < response['ingredients'].length; d++) {
                        doc.find("#ingredients").append("<span class='label label-info'>" + response['ingredients'][d] + "</span>\n");
                    }
                    doc.find("#description").append(response['description']);
                    $("#medic-search-area").after(doc)
                }
            });
        }
    });

}