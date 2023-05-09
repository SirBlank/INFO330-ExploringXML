import sqlite3
import sys
import xml.etree.ElementTree as ET

# Incoming Pokemon MUST be in this format
#
# <pokemon pokedex="" classification="" generation="">
#     <name>...</name>
#     <hp>...</name>
#     <type>...</type>
#     <type>...</type>
#     <attack>...</attack>
#     <defense>...</defense>
#     <speed>...</speed>
#     <sp_attack>...</sp_attack>
#     <sp_defense>...</sp_defense>
#     <height><m>...</m></height>
#     <weight><kg>...</kg></weight>
#     <abilities>
#         <ability />
#     </abilities>
# </pokemon>



# Read pokemon XML file name from command-line
# (Currently this code does nothing; your job is to fix that!)
if len(sys.argv) < 2:
    print("You must pass at least one XML file name containing Pokemon to insert")

for i, arg in enumerate(sys.argv):
    connection = sqlite3.connect("pokemon.sqlite")
    try:
        cursor = connection.cursor()
        if i == 0:
            continue

        tree = ET.parse(arg)
        root = tree.getroot()


        name = root.find('name').text
        cursor.execute('SELECT count(*) FROM pokemon WHERE name=?', (name,))
        if cursor.fetchone()[0] > 0:
            print(f"{name} already exists in the database")
            continue

        pokedex = root.attrib['pokedex']
        classification = root.attrib['classification']
        generation = root.attrib['generation']
        hp = root.find('hp').text
        attack = root.find('attack').text
        defense = root.find('defense').text
        speed = root.find('speed').text
        sp_attack = root.find('sp_attack').text
        sp_defense = root.find('sp_defense').text
        height = root.find('height/m').text
        weight = root.find('weight/kg').text

        cursor.execute('INSERT INTO pokemon (pokedex, name, classification, generation, hp, attack, defense, speed, sp_attack, sp_defense, height, weight) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (pokedex, name, classification, generation, hp, attack, defense, speed, sp_attack, sp_defense, height, weight))
        connection.commit()

    finally:
        connection.close()
