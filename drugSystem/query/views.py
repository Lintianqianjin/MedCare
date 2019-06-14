# -*- coding: UTF-8 -*-
import json
# import simplejson
from django.http import HttpResponse
from django.shortcuts import render

import sys, pprint
from .pygexf import Gexf
import json
from lxml import etree
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from neomodel import db, Q

from nosqlquery.models import Medicine
from query.models import User


@csrf_exempt
def medic_interact_gexf(request):
    if (request.method == 'POST'):
        print("POST/interact")
        # print(request.POST)
        json_post = json.loads(request.body.decode())
        print(json_post)
        # json_post = [
        #     {'name': '西咪替丁片'},
        #     {'name': '格列吡嗪缓释片'}
        # ]
        response_data = []
        medic_ingrs = {}
        for medic in json_post:
            name = medic['name']
            ingrs = db.cypher_query('MATCH (m:Medicine{name:"' + name + '"})-[r:包含]->(i:Ingredient)RETURN i.name;')
            print(ingrs)
            medic_ingrs[name] = []
            for i in ingrs[0]:
                medic_ingrs[name].append(i[0])

        checked = []
        rankCN = {
            '1': '严重',
            '2': '谨慎',
            '3': '注意',
            '4': '一般'
        }
        for d1 in json_post:
            for d2 in json_post:
                name1 = d1['name']
                checked.append(name1)
                name2 = d2['name']
                if name2 not in checked:
                    a_data = {}
                    print(name1, name2)
                    ingrs1 = medic_ingrs[name1]
                    ingrs2 = medic_ingrs[name2]
                    a_data['medic1'] = name1
                    a_data['medic2'] = name2
                    a_data['medic1_ingrs'] = ingrs1
                    a_data['medic2_ingrs'] = ingrs2
                    a_data['type'] = '冲突'
                    a_data['details'] = ''
                    a_data['rank'] = 0
                    a_data['interact_details'] = []
                    for i1 in ingrs1:
                        for i2 in ingrs2:
                            print(i1, i2)
                            interact = db.cypher_query(
                                'MATCH (i1:Ingredient{name:"' + i1 + '"})-[r:相互作用]->(i2:Ingredient{name:"' + i2 + '"}) RETURN r.rank;')
                            print(interact)
                            if len(interact[0]) > 0:
                                rank = interact[0][0][0]
                                a_data['interact_details'].append({'ingr1': i1, 'ingr2': i2, 'rank': rank})
                                a_data['details'] += (name1 + '的药物成分' + i1 + '与' +
                                                      name2 + '的药物成分' + i2 + '之间存在' + rankCN[
                                                          str(rank)] + '等级的冲突；')
                                if int(rank) > a_data['rank']:
                                    a_data['rank'] = 125- int(rank) * 25
                                    a_data['rankCN'] = rankCN[rank]
                    print(a_data)
                    if (a_data['rank'] != 0):
                        response_data.append(a_data)
        response_data.append(medic_ingrs)
        print(response_data)
        xml = convertJsonToGexf(response_data)
        print(xml)
    return HttpResponse(xml, content_type='text/plain')


def convertJsonToGexf(data):
    drugsColor = ('255', '215', '0')
    ingreColor = ('92', '172', '238')
    # 建gexf
    gexf = Gexf("MedCare", "curIneraction")
    graph = gexf.addGraph("undirected", "static", "curIneraction")

    # 记录节点和边的数量#
    num_edges = 0
    num_nodes = 0
    # 记录节点和节点序号的字典
    nodesDict = dict()
    edgesDict = dict()
    ### add drugNodes and 'contains' Edges 开始###
    for drug in data[-1]:
        # 先添加当前药物
        nodesDict[drug] = str(num_nodes)
        graph.addNode(str(num_nodes), drug, r=drugsColor[0], g=drugsColor[1], b=drugsColor[2])
        num_nodes += 1
        # 添加当前药物包含的成分
        for containingre in data[-1][drug]:
            # 有可能其它药也包含这个成分，所以先判断是否需要加入新节点。不存在则加入
            if containingre not in nodesDict:
                nodesDict[containingre] = str(num_nodes)
                graph.addNode(str(num_nodes), containingre, r=ingreColor[0], g=ingreColor[1], b=ingreColor[2])
                num_nodes += 1
            # 不管是不是未出现过的成分，需要添加当前药包含当前成分的边，所以在if外
            # if (nodesDict[drug], nodesDict[containingre]) not in edgesDict:
            edgesDict[(nodesDict[drug], nodesDict[containingre])] = str(num_edges)
            graph.addEdge(str(num_edges), nodesDict[drug], nodesDict[containingre], label='含有')
            num_edges += 1
    ### add drugNodes and 'contains' Edges 结束###

    ### add ingre interaction 开始###
    for interactionDict in data[:-1]:
        for ingreInteractionDetail in interactionDict['interact_details']:
            # 此时应当所有节点都已添加，如果key error 则数据有问题
            id1 = nodesDict[ingreInteractionDetail['ingr1']]
            id2 = nodesDict[ingreInteractionDetail['ingr2']]
            # 避免不同的药之间是同样的成分相互作用，所以加判断，必须未出现过，才添加这个相互作用的边
            if (id1, id2) not in edgesDict and (id2, id1) not in edgesDict:
                graph.addEdge(str(num_edges), id1, id2, weight=ingreInteractionDetail['rank'],
                              label=interactionDict['rankCN'])
                num_edges += 1
    ### add ingre interaction 结束###

    output_file = open("data.gexf", "wb")
    gexf.write(output_file)

    return etree.tostring(gexf.getXML()).decode('utf-8')


@csrf_exempt
def interact(request):
    '''
    data:
    [
        {'name':'ingr1'}.
        {'name':'ingr2'}
    ]
    '''
    if (request.method == 'POST'):
        print("POST/interact")
        # print(request.POST)
        json_post = json.loads(request.body.decode())
        print(json_post)
        # json_post = [
        #     {'name': '西咪替丁片'},
        #     {'name': '格列吡嗪缓释片'}
        # ]
        response_data = []
        medic_ingrs = {}
        for medic in json_post:
            name = medic['name']
            ingrs = db.cypher_query('MATCH (m:Medicine{name:"' + name + '"})-[r:包含]->(i:Ingredient)RETURN i.name;')
            print(ingrs)
            medic_ingrs[name] = []
            for i in ingrs[0]:
                medic_ingrs[name].append(i[0])

        checked = []
        rankCN = {
            '1': '严重',
            '2': '谨慎',
            '3': '注意',
            '4': '一般'
        }
        for d1 in json_post:
            for d2 in json_post:
                name1 = d1['name']
                checked.append(name1)
                name2 = d2['name']
                if name2 not in checked:
                    a_data = {}
                    print(name1, name2)
                    ingrs1 = medic_ingrs[name1]
                    ingrs2 = medic_ingrs[name2]
                    a_data['medic1'] = name1
                    a_data['medic2'] = name2
                    a_data['medic1_ingrs'] = ingrs1
                    a_data['medic2_ingrs'] = ingrs2
                    a_data['type'] = '冲突'
                    a_data['details'] = ''
                    a_data['rank'] = 0
                    a_data['interact_details'] = []
                    for i1 in ingrs1:
                        for i2 in ingrs2:
                            print(i1, i2)
                            interact = db.cypher_query(
                                'MATCH (i1:Ingredient{name:"' + i1 + '"})-[r:相互作用]->(i2:Ingredient{name:"' + i2 + '"}) RETURN r.rank;')
                            print(interact)
                            if len(interact[0]) > 0:
                                rank = interact[0][0][0]
                                a_data['interact_details'].append({'ingr1': i1, 'ingr2': i2, 'rank': rank})
                                a_data['details'] += (name1 + '的药物成分' + i1 + '与' +
                                                      name2 + '的药物成分' + i2 + '之间存在' + rankCN[
                                                          str(rank)] + '等级的冲突；')
                                if int(rank) > a_data['rank']:
                                    a_data['rank'] = int(rank) * 25
                                    a_data['rankCN'] = rankCN[rank]
                    print(a_data)
                    if (a_data['rank'] != 0):
                        response_data.append(a_data)
        # response_data.append(medic_ingrs)
        print(response_data)
    return HttpResponse(json.dumps(response_data, ensure_ascii=False), content_type='application/json, charset=utf-8')


@csrf_exempt
def medic_details(request):
    if (request.method == 'POST'):
        print("POST/medic_details")
        print(request.POST)
        json_post = json.loads(request.body.decode())
        # json_post = {
        #     'name': '氯美扎酮'
        # }
        name = json_post['name']
        response_data = {}
        print(name)
        response_data['name'] = name
        ingrs = db.cypher_query('MATCH (m:Medicine{name:"' + name + '"})-[r:包含]->(i:Ingredient)RETURN i.name;')
        response_data['ingredients'] = []
        print(ingrs)
        if len(ingrs[0]) == 0:
            response_data['ingredients'].append('无')
        else:
            for i in ingrs[0]:
                response_data['ingredients'].append(i[0])
        cures = db.cypher_query('MATCH (m:Medicine{name:"' + name + '"})-[r:治疗]->(i:Illness)RETURN i.name;')
        print(cures)
        response_data['cures'] = []
        if len(cures[0]) == 0:
            response_data['cures'].append('无')
        else:
            for i in cures[0]:
                response_data['cures'].append(i[0])
        description = db.cypher_query('MATCH (m:Medicine{name:"' + name + '"})RETURN m.description;')[0][0][0]
        print(description)
        if description is None:
            response_data['description'] = '无'
        else:
            response_data['description'] = description
        print(response_data)
    return HttpResponse(json.dumps(response_data, ensure_ascii=False), content_type='application/json, charset=utf-8')


@csrf_exempt
def medic_search(request):
    '''
    data:
    {
        'searchBy':'name'/'ingredient',
        'keyword':''
    }
    '''
    if (request.method == 'POST'):
        print("POST/medic_details")
        print(request.POST)
        json_post = json.loads(request.body.decode())
        print(json_post)
        if json_post['keyword'] == '':
            msg = {'warning': 'query keyword should not be ""'}
            return HttpResponse(json.dumps(msg, ensure_ascii=False), content_type='application/json, charset=utf-8')
        # json_post = {
        #     # 'searchBy':'ingredient',
        #     # 'keyword': '郁金'
        #     'searchBy': 'name',
        #     'keyword': '氯美扎酮'
        # }
        if json_post['searchBy'] == 'name':
            query = 'MATCH (m:Medicine)WHERE m.name =~ ".*' + json_post['keyword'] + '.*" RETURN m.name;'
            # medicines = Medicine.nodes.filter(Q(name__contains=json_post['keyword']))
            medicines = db.cypher_query(query)
        elif json_post['searchBy'] == 'ingredient':
            query = 'MATCH (m:Medicine)-[r:包含]->(i:Ingredient{name:"' + json_post['keyword'] + '"})RETURN m.name;'
            medicines = db.cypher_query(query)
        print(json_post)
        print(medicines)
        response_data = []
        for medic in medicines[0]:
            a_data = {}
            print(medic[0])
            a_data['name'] = medic[0]
            ingrs = db.cypher_query('MATCH (m:Medicine{name:"' + medic[0] + '"})-[r:包含]->(i:Ingredient)RETURN i.name;')
            a_data['ingredients'] = []
            print(ingrs)
            for i in ingrs[0]:
                a_data['ingredients'].append(i[0])
            # 这里只是显示在表格上，所以取前5个成分
            a_data['ingredients'] = a_data['ingredients'][0:5]
            cures = db.cypher_query('MATCH (m:Medicine{name:"' + medic[0] + '"})-[r:治疗]->(i:Illness)RETURN i.name;')
            print(cures)
            a_data['cures'] = []
            for i in cures[0]:
                a_data['cures'].append(i[0])
            description = db.cypher_query('MATCH (m:Medicine{name:"' + medic[0] + '"})RETURN m.description;')[0][0]
            print(description)
            a_data['description'] = description
            print(a_data)
            response_data.append(a_data)
        print(response_data)
    return HttpResponse(json.dumps(response_data, ensure_ascii=False), content_type='application/json, charset=utf-8')
