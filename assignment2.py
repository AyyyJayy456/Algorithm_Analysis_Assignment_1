import heapq
import sys

#to use follow format: python3 assignment2.py "path to input file" "path to desired location of output file"
#input file needs to be in format: Height, Left X Value, Right X Value
#output file is given in format: Height, Left X value

def loadFromImport(fileName):
    #takes inputs from text file
    file = open(fileName, "r")

    buildings = []

    for line in file:
        values = line.strip().split(",")

        if len(values) != 3:
            continue

        height = int(values[0])
        left = int(values[1])
        right = int(values[2])

        buildings.append([height, left, right])

    file.close()

    return buildings


def exportToOutputFile(fileName, skyline):
    #exports output to file
    file = open(fileName, "w")

    for height, x in skyline:
        file.write(f"{height}, {x}\n")

    file.close()

#=========================================================================
# pseudocode: sweep-line + max-heap skyline algorithm (O(n log n))
#
# function getSkyline(buildings):
#     sort buildings by left x-coordinate
#     lines = every left and right x-coordinate from all buildings, sorted
#     priorityQueue = empty max-heap of (height, right edge)
#
#     for each x in lines:
#         add every building whose left edge is <= x to the heap
#         remove every building whose right edge is <= x from the heap
#         currentHeight = height of tallest building still in heap, or 0
#         if currentHeight changed from the last point, record (currentHeight, x)
#
#     return skyline
#
# time complexity: O(n log n) - sorting is O(n log n), and each of the 2n
# edges causes at most one heap push/pop, each O(log n)
#=========================================================================

class Assignment2:
    def getSkyline(self, buildings):

        #sorts buildings by left coordinate
        buildings.sort(key=lambda building: building[1])

        skyline = []
        lines = []
        priorityQueue = []

        #append all edges
        for height, left, right in buildings:
            lines.append(left)
            lines.append(right)

        lines.sort()

        buildingIndex = 0
        numberOfBuildings = len(buildings)

        for line in lines:

            #add all buildings beginning before this coordinate
            #(sweep forward: activates any building that has started)
            while (buildingIndex < numberOfBuildings and
                   buildings[buildingIndex][1] <= line):
                
                height, left, right = buildings[buildingIndex]

                #negative height creates max heap
                heapq.heappush(priorityQueue, (-height, right))

                buildingIndex += 1

            #remove ended buildings
            #(building's right edge passed, so it can't affect the skyline anymore)
            while priorityQueue and priorityQueue[0][1] <= line:
                heapq.heappop(priorityQueue)

            currentHeight = 0
            if priorityQueue:
                currentHeight = -priorityQueue[0][0]

            # records changes in height
            # (skip if height is unchanged, so output has no duplicate points)
            if skyline and skyline[-1][0] == currentHeight:
                continue
            skyline.append((currentHeight, line))

        return skyline


def main():

    if len(sys.argv) != 3:
        print("Bad Entry, Try Again")
        return

    inputFile = sys.argv[1]
    outputFile = sys.argv[2]
    buildings = loadFromImport(inputFile)
    solution = Assignment2()
    skyline = solution.getSkyline(buildings)
    exportToOutputFile(outputFile, skyline)


if __name__ == "__main__":
    main()