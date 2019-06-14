# -*- coding: UTF-8 -*-
from django.db import models

# Create your models here.
from py2neo import Graph

'''
python neomodel_install_labels apps/nosqlquery.py nosqlquery.models --db bolt://neo4j:123456@localhost:7687
python neomodel_remove_labels apps/nosqlquery.py nosqlquery.models --db bolt://neo4j:123456@localhost:7687
'''

from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
                      UniqueIdProperty, RelationshipTo, RelationshipFrom, db, Relationship, StructuredRel)

db.set_connection('bolt://neo4j:123@localhost:7687')


class Medicine(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
    description = StringProperty()
    cures = RelationshipTo("Illness", "治疗")
    ingredient = RelationshipTo('Ingredient', '包含')


class Illness(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
    description = StringProperty()
    symptoms = RelationshipTo("Symptom", "表现")


class Symptom(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
    description = StringProperty()


class Ingredient(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
    description = StringProperty()
    cures = RelationshipTo("Illness", "治疗")
    interact = Relationship("Interact", "相互作用")


class Interact(StructuredRel):
    rank = IntegerProperty()
    rankCN = StringProperty()


def test():
    aqms = Medicine(name='阿奇霉素')
    aqms.save()
    fy = Illness(name="肺炎")
    fy.save()
    print(list(map(lambda x: x.name, Medicine.nodes.all())))
    aqms.delete()
    fy.delete()
    print(Illness.nodes.all())
    pass


def manually_import_data():
    # delete_all()

    ill_medic = open('病症_多个药物.csv', 'r', encoding='utf-8').readlines()
    medicines = list(map(lambda x: x.name, Medicine.nodes.all()))
    ills = list(map(lambda x: x.name, Illness.nodes.all()))
    for l in ill_medic:
        l = l.replace(r'\ufeff', '')
        illness = l.split(',')[0]
        medics = l.split(',')[1:]

        if illness not in ills:
            a = Illness(name=illness)
            a.save()
            ills.append(a)

        for m in medics:
            if m not in medicines:
                b = Medicine(name=m.strip())
                b.save()
                medicines.append(m)

            db.cypher_query(
                'MATCH(a:Medicine{name:"' + m + '"}),(b:Illness{name:"' + illness + '"})' +
                'CREATE (a)-[ingredient:治疗]->(b)')
    pass

    med_ingr = open('药物成分_处理.csv', 'r', encoding='utf-8').readlines()
    medicines = list(map(lambda x: x.name, Medicine.nodes.all()))
    ingredients = []
    for l in med_ingr:
        l = l.replace(r'\ufeff', '')
        if len(l.split(',')) <= 1:
            continue
        medic = l.split(',')[0]
        ingr = l.split(',')[1].strip()
        if ingr not in ingredients:
            a = Ingredient(name=ingr)
            a.save()
            ingredients.append(ingr)
        if medic not in medicines:
            b = Medicine(name=medic)
            b.save()
            medicines.append(medic)
            b.ingredient.connect(a)
        else:
            db.cypher_query(
                'MATCH(a:Medicine{name:"' + medic + '"}),(b:Ingredient{name:"' + ingr + '"})' +
                'CREATE (a)-[ingredient:包含]->(b)')

            b = Medicine.nodes.first(name=medic)
        print(b, a)

    ill_symp = open('疾病_症状.csv', 'r', encoding='utf-8').readlines()
    illnesses = list(map(lambda x: x.name, Illness.nodes.all()))
    symptoms = []
    for l in ill_symp:
        l = l.replace(r'\ufeff', '')
        if len(l.split(',')) <= 1:
            continue
        illness = l.split(',')[0]
        symptom = l.split(',')[1].strip()

        if symptom not in symptoms:
            a = Symptom(name=symptom)
            a.save()
            symptoms.append(symptom)
        else:
            pass
        if illness not in illnesses:
            b = Illness(name=illness)
            b.save()
            illnesses.append(illness)
            b.symptoms.connect(a)
        else:
            db.cypher_query(
                'MATCH(a:Symptom{name:"' + symptom + '"}),(b:Illness{name:"' + illness + '"})' +
                'CREATE (b)-[Symptom:表现]->(a)')
            b = Illness.nodes.first(name=illness)
        print(b, a)

    medic_desc = open('治疗.csv', 'r', encoding='utf-8').readlines()
    medics = list(map(lambda x: x.name, Medicine.nodes.all()))
    for l in medic_desc:
        l = l.replace(r'\ufeff', '').strip()
        medic = l.split(',')[0]
        desc = l.split(',')[1]
        if medic not in medics:
            b = Medicine(name=medic, description=desc)
            medics.append(medic)
            b.save()
        else:
            b = Medicine.nodes.first(name=medic)
            # b.desc = desc # 无效，坑
            db.cypher_query(
                'MATCH(m:Medicine{name:"' + medic + '"}) SET m.description = "' + desc + '";'
            )
        print(b)

    interact = open('相互关系.csv', 'r', encoding='utf-8').readlines()
    ingredients = list(map(lambda x: x.name, Ingredient.nodes.all()))
    pairs = []
    for l in interact:
        ws = l.split(',')
        if len(ws) != 4:
            continue
        ingr1 = ws[0]
        rank = ws[2]
        rankCN = ws[3]
        for i2 in ws[1].split('、'):
            ingr2 = i2
            if (ingr1, ingr2) in pairs:
                continue
            pairs.append((ingr1, ingr2))
            pairs.append((ingr2, ingr1))
            if ingr1 not in ingredients:
                a = Ingredient(name=ingr1)
                a.save()
                ingredients.append(ingr1)
            else:
                a = Ingredient.nodes.first(name=ingr1)
            if ingr2 not in ingredients:
                b = Ingredient(name=ingr2)
                b.save()
                ingredients.append(ingr2)
            else:
                b = Ingredient.nodes.first(name=ingr2)
            db.cypher_query(
                'MATCH(a:Ingredient{name:"' + ingr1 + '"}),(b:Ingredient{name:"' + ingr2 + '"})' +
                'CREATE (a)-[:相互作用{rank:"' + rank + '",rankCN:"' + rankCN + '"}]->(b)' +
                'CREATE (b)-[:相互作用{rank:"' + rank + '",rankCN:"' + rankCN + '"}]->(a)'
            )
            print(a, b)
    print(pairs)

    med_ingr = open('药物_包含的抗生素.csv', 'r',
                    encoding='utf-8').readlines()
    medicines = list(map(lambda x: x.name, Medicine.nodes.all()))
    ingredients = list(map(lambda x: x.name, Ingredient.nodes.all()))
    for l in med_ingr:
        l = l.replace(r'\ufeff', '')
        if len(l.split(',')) <= 1:
            continue
        medic = l.split(',')[0]
        ingr = l.split(',')[1].strip()
        if ingr not in ingredients:
            a = Ingredient(name=ingr)
            a.save()
            ingredients.append(ingr)
        if medic not in medicines:
            b = Medicine(name=medic)
            b.save()
            medicines.append(medic)
            # b.ingredient.connect(a)
        db.cypher_query(
            'MATCH(a:Medicine{name:"' + medic + '"}),(b:Ingredient{name:"' + ingr + '"})' +
            'CREATE (a)-[ingredient:包含]->(b)')

    interact = open('抗生素相互关系.csv', 'r',
                    encoding='utf-8').readlines()
    ingredients = list(map(lambda x: x.name, Ingredient.nodes.all()))
    pairs = []
    for l in interact:
        l = l.replace(r'\ufeff', '')
        ws = l.split(',')
        if len(ws) != 4:
            continue
        ingr1 = ws[0]
        rank = ws[2]
        rankCN = ws[3]
        for i2 in ws[1].split('、'):
            ingr2 = i2
            if (ingr1, ingr2) in pairs:
                continue
            pairs.append((ingr1, ingr2))
            pairs.append((ingr2, ingr1))
            if ingr1 not in ingredients:
                a = Ingredient(name=ingr1)
                a.save()
                ingredients.append(ingr1)
            else:
                a = Ingredient.nodes.first(name=ingr1)
            if ingr2 not in ingredients:
                b = Ingredient(name=ingr2)
                b.save()
                ingredients.append(ingr2)
            else:
                b = Ingredient.nodes.first(name=ingr2)
            db.cypher_query(
                'MATCH(a:Ingredient{name:"' + ingr1 + '"}),(b:Ingredient{name:"' + ingr2 + '"})' +
                'CREATE (a)-[:相互作用{rank:"' + rank + '",rankCN:"' + rankCN + '"}]->(b)' +
                'CREATE (b)-[:相互作用{rank:"' + rank + '",rankCN:"' + rankCN + '"}]->(a)'
            )
            print(a, b)
    print(pairs)


def delete_all():
    db.cypher_query('MATCH (n) OPTIONAL MATCH (n)-[r]-() DELETE n,r')


if __name__ == '__main__':
    # test()
    manually_import_data()
    # ill_medic = open('../../resources/病症_多个药物.csv', 'r', encoding='utf-8').readlines()
    # for l in ill_medic:
    #     print(l.replace(r'\ufeff', ''))
    #     print(l)
    pass
