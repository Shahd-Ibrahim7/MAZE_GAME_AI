# algorithms/astar.py
import heapq

def heuristic(a, b):
    # حساب مسافة مانهاتن (Manhattan Distance) بين نقطتين
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(maze_grid, start, target):
    start = (start[0], start[1])
    target = (target[0], target[1])

    if start == target:
        return [start]

    # الـ Priority Queue (طابور الأولويات) عشان يختار دايماً المربع اللي ليه أقل f_score
    # بنخزن فيه: (f_score, current_node, path)
    open_set = []
    heapq.heappush(open_set, (0 + heuristic(start, target), start, [start]))
    
    # مصفوفة لتخزين أقل g_score (الخطوات الفعلية) وصلنا لها لكل مربع
    g_score = {start: 0}
    
    visited = set()
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    while open_set:
        # pop بيجيب المربع صاحب أقل تكلفة كليّة فوراً
        _, current, path = heapq.heappop(open_set)

        if current == target:
            return path

        if current in visited:
            continue
        visited.add(current)

        for dx, dy in directions:
            neighbor = (current[0] + dx, current[1] + dy)

            # التأكد من حدود المتاهة وأن المربع مش حيطة
            if (0 <= neighbor[1] < len(maze_grid) and 
                0 <= neighbor[0] < len(maze_grid[0]) and 
                maze_grid[neighbor[1]][neighbor[0]] != 1):
                
                # التكلفة للوصول للجار هي تكلفة المربع الحالي + 1
                tentative_g_score = g_score[current] + 1

                # لو السكة دي للجار أول مرة نشوفها أو أثرى من السكة القديمة
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + heuristic(neighbor, target)
                    heapq.heappush(open_set, (f_score, neighbor, path + [neighbor]))

    return []