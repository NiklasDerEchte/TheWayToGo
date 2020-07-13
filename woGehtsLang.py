import csv
import math
import queue

###################################################### Hilfs funktionen
def get_length_between_two_points(a, b): # Länge des Distanzvektors ausrechnen
    c = float(b[0]) - float(a[0]), float(b[1]) - float(a[1])
    return math.sqrt(c[0]*c[0] + c[1]*c[1])

def get_key_with_min_value(dict, visited_nodes = []): # Sucht den Knoten mit der geringsten Distanz und noch nicht besucht wurde
    cur_key = -1
    cur_value = -1
    for key, value in dict.items():
        if value == 0.0 or key in visited_nodes:
            continue
        if cur_key == -1:
            cur_key = key
        if cur_value == -1:
            cur_value = value

        if value < cur_value:
            cur_key = key
            cur_value = value

    return cur_key

###################################################### CSV Einlesen
input = []
with open('msg_standorte_deutschland.csv', newline='') as file:
    csvFile = csv.reader(file, delimiter=',')
    next(csvFile) # Header Zeile überspringen
    for row in csvFile:
        input.append(row)

###################################################### Adjazenzmatrix erstellen
adjazenzmatrix = {}
for from_node in input:
    tmp_adjazenten = {}
    for to_node in input:
        if to_node[0] == from_node[0]:
            tmp_adjazenten[to_node[0]] = 0.0
            continue

        a = from_node[6], from_node[7]
        b = to_node[6], to_node[7]
        ab_len = get_length_between_two_points(a, b)
        tmp_adjazenten[to_node[0]] = ab_len

    adjazenzmatrix[from_node[0]] = tmp_adjazenten

###################################################### "Dijkstra"-Algorithmus
visited_nodes = []
prio_queue = queue.PriorityQueue()

start_node = '1'
next_node = get_key_with_min_value(adjazenzmatrix[start_node])
adjazenten = start_node, next_node
distance = adjazenzmatrix[start_node][next_node]
prio_queue.put((distance, adjazenten)) # Füge die erste Stadt mit seinem Adjazenten mit der Distanz der Queue hinzu
visited_nodes.append(start_node) # Erster Knoten wurde besucht

while not prio_queue.empty(): # Algorithmus sucht immer die nächste Stadt mit dem kleinsten Pfad
    entry = prio_queue.get() # Entry = (Distanz, (Start_Knoten, Ziel_Knoten))
    cur_node = entry[1][1] # Ziel_Knoten wird mein Aktueller Knoten
    if cur_node in visited_nodes:
        continue
    visited_nodes.append(cur_node)
    print(entry)
    if len(visited_nodes) == len(input): # Wurden alle Knoten besucht ?
        break
    cur_distance = entry[0]
    next_node = get_key_with_min_value(adjazenzmatrix[cur_node], visited_nodes)
    distance = adjazenzmatrix[cur_node][next_node] + cur_distance
    adjazenten = cur_node, next_node
    prio_queue.put((distance, adjazenten)) # Neuer Knoten wurde besucht und die Distanz erweitert