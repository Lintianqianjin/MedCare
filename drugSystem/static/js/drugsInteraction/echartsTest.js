var myChart = echarts.init(document.getElementById('main'));

myChart.showLoading();
$.get('../static/les-miserables.gexf', function (xml) {
    myChart.hideLoading();
    var graph = echarts.dataTool.gexf.parse(xml);
    var categories = [];
    for (var i = 0; i < 9; i++) {
        categories[i] = {
            name: '类目' + i
        };
    }
    graph.nodes.forEach(function (node) {
        node.itemStyle = null;
        node.symbolSize = 10;
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
        //         show: node.symbolSize > 30
        //     }
        // };
        // node.category = node.attributes.modularity_class;
    });
    option = {
        title: {
            text: '',
            subtext: 'Default layout',
            top: 'bottom',
            left: 'right'
        },
        tooltip: {},
        legend: [{
            // selectedMode: 'single',
            data: categories.map(function (a) {
                return a.name;
            })
        }],
        animationDurationUpdate: 1500,
        animationEasingUpdate: 'quinticInOut',
        series : [
            {
                name: 'Les Miserables',
                type: 'graph',
                layout: 'force',
                circular: {
                    rotateLabel: true
                },
                data: graph.nodes,
                links: graph.links,
                categories: categories,
                roam: true,
                label: {
                    normal: {
                        position: 'right',
                        // formatter: '{b}'
                    }
                },
                //change start
                force: {
                    repulison:100
                },
                //change end
                lineStyle: {
                    normal: {
                        color: 'source',
                    }
                }
            }
        ]
    };
    myChart.setOption(option);
}, 'xml');
