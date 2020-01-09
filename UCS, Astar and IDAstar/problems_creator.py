import csv
from ways import load_map_from_csv
import random


def create_p(roads):
    with open('db/problems.csv', 'w', newline='') as csvFile:
        writer = csv.writer(csvFile)
        for i in range(100):
            start = random.randint(0, 944799)
            while len(roads.junctions()[start].links) == 0:
                start = random.randint(0, 944799)
            end = start
            prev = start
            loop_number = random.randint(5, 16)
            for j in range(loop_number):
                prev2 = prev
                prev = end
                if_random = 0
                temp = end
                for k in range(len(roads.junctions()[end].links)):
                    if if_random == 0:
                        temp = roads.junctions()[temp].links[random.randint(0, len(roads.junctions()[temp].links)-1)].target
                    else:
                        temp = roads.junctions()[temp].links[k].target
                    if temp != prev2:
                        end = temp
                        break
                    else:
                        if if_random == 0:
                            if_random = 1
                        temp = end
                if len(roads.junctions()[end].links) == 0:
                    break
            if start == end:
                end = roads.junctions()[start].links[0].target
            row = [start, end]
            writer.writerow(row)
    csvFile.close()


if __name__ == '__main__':
    create_p(load_map_from_csv())
