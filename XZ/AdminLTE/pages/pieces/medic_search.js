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

function showSearchResult() {

    // console.log($("#medic-search-button").parent().parent().next());
    $("#medic-search-button").parent().parent().next().next().remove();
    $("#medic-search-button").parent().parent().next().remove();
    $.ajax({
        type: "get",
        url: "../pieces/search_result.html",
        async: true,
        success: function (html) {
            var data = [
                {
                    'name':'阿奇霉素分散片',
                    'ingredients':'阿奇霉素',
                    'description':'白色 片状',
                    'cures':'感冒'
                },
                {
                    'name':'感冒清颗粒',
                    'ingredients':'枸杞',
                    'description':'褐色 颗粒状',
                    'cures':'感冒'
                }
            ];
            var doc = $(html);

            for (var d = 0; d < data.length; d++) {
                console.log(data[d].name);
                console.log(html);
                doc.find('#table-body').append('<tr><td>'+data[d].name+'</td><td>'+data[d].ingredients+'</td><td>'
                    +data[d].description+'</td><td>'+data[d].cures+'</td></tr>');
            }

            $("#medic-search-button").parent().parent().after(doc)
        }
    });

    // $.post({
    //     type: 'POST',
    //     url: '/query/',
    //     data: {
    //         'searchby': 'name',
    //         'keyword': 'medic1'
    //     },
    //     success: function (data) {
    //     }
    // });
}

$('tr').click(function () {
    showMedicDetails();
});

function showMedicDetails() {
    $("#medic-search-area").next().remove();
    $.ajax({
        type: "get",
        url: "../pieces/medic_details.html",
        async: true,
        success: function (html) {
            var doc = $(html);
            var data = {
                'illnesses': ['A', 'B', 'C'],
                'ingredients': ['1', '2', '3'],
                'labels': ['1', '2', '3'],
                'tips': "hhhhh"
            };
            for (var ingr in data['illnesses']) {
                doc.find("#illnesses").append("<span class='label label-default'\n> " + ingr + " </span> ");
            }
            for (var ingr in data['ingredients']) {
                doc.find("#ingredients").append("<span class='label label-default'\n> " + ingr + " </span> ");
            }
            doc.find("#tips").append(data['tips']);
            $("#medic-search-area").after(doc)
        }
    });
//                            $.ajax({
//                                type: "get",
//                                url: "../pieces/medic_details.html",
//                                async: true,
//                                success: function (data) {
//                                    $("#search-result").after(data)
//                                }
//                            });
//                            ==========
    //                            $.post("/app/",
//                                {
//                                    forwt:"medicDetails"
//                                },
//                                function(data,status){


//                                    根据data修改表单内容；提示信息如果status异常
//                                });
//                        }
}