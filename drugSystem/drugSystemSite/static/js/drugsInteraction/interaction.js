$(document).ready(function () {
    // addSidebar();
});

function addSidebar() {
    $.ajax({
        type: "get",
        url: "../static/pieceHtml/main_sider.html",
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
        url: "../../static/pieceHtml/interaction_search_bar.html",
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
        url: "../../static/pieceHtml/search_result.html",
        async: true,
        success: function (data) {
            $("#button-group").next().after(data)
        }
    });
}

function showInteraction() {

    $("#medic-search-area").next().remove();
    $("#medic-search-area").next().remove();

    post_data = [];
    inputs = $("input[name='medic-input']");
    console.log(inputs);
    for (let d = 0; d < inputs.length; d++) {
        post_data.push({'name': inputs.eq(d).val()});
    }
    console.log(JSON.stringify(post_data));

    // post_data = [
    //     {'name': '西咪替丁片'},
    //     {'name': '格列吡嗪缓释片'},
    //     {'name': '鼻炎康片'}
    // ];

    $.ajax({
        type: "get",
        url: "../../static/pieceHtml/interaction_plot.html",
        async: true,
        success: function (html) {
            var doc = $(html);
            $("#medic-search-area").after(doc);
        }
    });

    console.log(document.getElementById('interaction-plot'));

    $.ajax({
        type: 'POST',
        url: "../../query/medic_interact/",
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
                url: "../../static/pieceHtml/interaction_details.html",
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

                    if (response.length < 1) {
                        doc.find("#medic-interaction").append('\n<p>没有药物相互作用</p>');
                    }
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
                    // doc.find("#medic-interaction").append('<strong><i class="fa fa-file-text-o margin-r-5"></i>用药建议：</strong>');
                    // doc.find("#medic-interaction").append('<p>' + response[response.length - 1]['suggestion'] + '</p>');
                    $("#medic-search-area").after(doc);
                }
            });
        }
    });
}

function interaction_plot() {
    post_data = [];
    inputs = $("input[name='medic-input']");
    console.log(inputs);
    for (let d = 0; d < inputs.length; d++) {
        post_data.push({'name': inputs.eq(d).val()});
    }
    console.log(JSON.stringify(post_data));

    // post_data = [
    //     {'name': '西咪替丁片'},
    //     {'name': '格列吡嗪缓释片'},
    //     {'name': '鼻炎康片'}
    // ];
    $.ajax({
        type: 'POST',
        url: "../../query/medic_interact_gexf/",
        data: JSON.stringify(
            post_data
        ),
        dataType: 'xml',
        success: function (xml, status) {
            console.log(xml);

            var myChart = echarts.init(document.getElementById('interaction-plot'));

            myChart.showLoading();
            myChart.hideLoading();
            var graph = echarts.dataTool.gexf.parse(xml);
            var categories = [];
            categories[0] = {
                name: '药物'
            };
            categories[1] = {
                name: '成分'
            };

            graph.nodes.forEach(function (node) {
                node.itemStyle.color = node.color;
                node.symbolSize = 20;
                node.value = node.symbolSize;
                // node.symbolSize /= 1.5;
                //change 开始
                node.category = node.attributes.modularity_class;
                // Use random x, y
                node.x = node.y = null;
                node.draggable = true;
                //change 结束
                // node.label = {
                //     normal: {
                //         show: True
                //     }
                // };
                // node.category = node.attributes.modularity_class;
            });
            option = {
                title: {
                    text: '',
                    subtext: 'Default layout',
                    top: 'bottom',
                    left: 'right',
                },
                tooltip: {},
                color: ['#EEC900', '#5CACEE'],
                legend: [{
                    // selectedMode: 'single',
                    data: categories.map(function (a) {
                        return a.name;
                    })
                }],
                animationDurationUpdate: 1500,
                animationEasingUpdate: 'quinticInOut',
                series: [
                    {
                        name: '名称',
                        type: 'graph',
                        layout: 'force',
                        circular: {
                            rotateLabel: true
                        },
                        data: graph.nodes,
                        links: graph.links,
                        categories: categories,
                        roam: true,
                        label: {//图形上的文本标签，可用于说明图形的一些数据信息
                            normal: {
                                show: true,//显示
                                position: 'right',//相对于节点标签的位置，默认在节点中间
                                //回调函数，你期望节点标签上显示什么
                                formatter: function (params) {
                                    return params.data.label;
                                },
                            }
                        },
                        // edgeLabel: {//线条的边缘标签
                        //     normal: {
                        //         show: false,
                        //         //通过回调函数设置连线上的标签
                        //         formatter: function (x) {
                        //             return x.data.label;
                        //         },
                        //         // textStyle: {
                        //         //         fontSize: 20
                        //         //      }
                        //     }
                        // },
                        //change start
                        force: {
                            repulison: 100,
                            gravity: 0.03,
                            edgeLength: 80,
                            layoutAnimation: true,
                        },
                        //change end
                        lineStyle: {
                            normal: {
                                color: 'source',
                                lineWidth: 10,
                            }
                        }
                    }
                ]
            };
            myChart.setOption(option);
        }
    });
}