# -*- coding: UTF-8 -*-
from django.db import models

# Create your models here.
from py2neo import Graph

'''
python neomodel_install_labels apps/nosqlquery.py nosqlquery.models --db bolt://neo4j:123456@localhost:7687
python neomodel_remove_labels apps/nosqlquery.py nosqlquery.models --db bolt://neo4j:123456@localhost:7687
'''

from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
                      UniqueIdProperty, RelationshipTo, RelationshipFrom, db, Relationship)

db.set_connection('bolt://neo4j:123@localhost:7687')


class Medicine(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
    description = StringProperty()
    cures = Relationship("Illness", "治疗")
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
    cures = Relationship("Illness", "治疗")


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

    ill_medic = open('../../resources/病症_多个药物.csv', 'r', encoding='utf-8').readlines()
    for l in ill_medic:
        l = l.replace(r'\ufeff', '')
        illness = l.split(',')[0]
        medics = l.split(',')[1:]
        a = Illness(name=illness)
        a.save()
        for m in medics:
            b = Medicine(name=m.strip())
            b.save()
            b.cures.connect(a)
            print(a, b)
    pass

    med_ingr = open('../../resources/药物成分_处理.csv', 'r', encoding='utf-8').readlines()
    medicines = list(map(lambda x: x.name, Medicine.nodes.all()))
    for l in med_ingr:
        l = l.replace(r'\ufeff', '')
        if len(l.split(',')) <= 1:
            continue
        medic = l.split(',')[0]
        ingr = l.split(',')[1].strip()

        a = Ingredient(name=ingr)
        a.save()
        if medic not in medicines:
            b = Medicine(name=medic)
            b.save()
            b.ingredient.connect(a)
        else:
            db.cypher_query(
                'MATCH(a:Medicine{name:"' + medic + '"}),(b:Ingredient{name:"' + ingr + '"})' +
                'CREATE (a)-[ingredient:包含]->(b)')

            b = Medicine.nodes.first(name=medic)
        print(b, a)

    ill_symp = open('../../resources/疾病_症状.csv', 'r', encoding='utf-8').readlines()
    illnesses = list(map(lambda x: x.name, Illness.nodes.all()))
    for l in ill_symp:
        l = l.replace(r'\ufeff', '')
        if len(l.split(',')) <= 1:
            continue
        illness = l.split(',')[0]
        symptom = l.split(',')[1].strip()

        a = Symptom(name=symptom)
        a.save()
        if illness not in illnesses:
            b = Illness(name=illness)
            b.save()
            b.symptoms.connect(a)
        else:
            db.cypher_query(
                'MATCH(a:Symptom{name:"' + symptom + '"}),(b:Illness{name:"' + illness + '"})' +
                'CREATE (a)-[Symptom:表现]->(b)')
            b = Illness.nodes.first(name=illness)
        print(b, a)

    medic_desc = open('../../resources/治疗.csv', 'r', encoding='utf-8').readlines()
    medics = list(map(lambda x: x.name, Illness.nodes.all()))
    for l in medic_desc:
        l = l.replace(r'\ufeff', '').strip()
        medic = l.split(',')[0]
        desc = l.split(',')[1]
        if medic not in medics:
            b = Medicine(name=medic, description=desc)
            b.save()
        else:
            b = Medicine.nodes.first(name=medic)
            b.desc = desc


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
