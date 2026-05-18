# algorithms/greedy.py
import heapq

def heuristic(a, b):
    # مسافة مانهاتن (Manhattan Distance) بالخط المستقيم
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def greedy(maze_grid, start, target):
    start = (start[0], start[1])
    target = (target[0], target[1])

    if start == target:
        return [start]

    # الـ Priority Queue بنخزن فيه: (h_score, current_node, path)
    # لاحظوا إننا بنرتب بناءً على الـ Heuristic بس (الجشع)
    open_set = []
    heapq.heappush(open_set, (heuristic(start, target), start, [start]))
    
    visited = set()
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    while open_set:
        # بيجيب المربع الأقرب للاعب بالنظر المباشر فوراً
        _, current, path = heapq.heappop(open_set)

        if current == target:
            return path

        if current in visited:
            continue
        visited.add(current)

        for dx, dy in directions:
            neighbor = (current[0] + dx, current[1] + dy)

            # التأكد من الحدود وأن المربع مش حيطة
            if (0 <= neighbor[1] < len(maze_grid) and 
                0 <= neighbor[0] < len(maze_grid[0]) and 
                maze_grid[neighbor[1]][neighbor[0]] != 1 and 
                neighbor not in visited):
                
                h_score = heuristic(neighbor, target)
                heapq.heappush(open_set, (h_score, neighbor, path + [neighbor]))

    return []