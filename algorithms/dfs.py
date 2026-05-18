# algorithms/dfs.py

def dfs(maze_grid, start, target):
    """
    start: إحداثيات البداية للعدو (x, y)
    target: إحداثيات الهدف للاعب (x, y)
    maze_grid: مصفوفة المتاهة
    """
    start = (start[0], start[1])
    target = (target[0], target[1])

    if start == target:
        return [start]

    # استخدام الـ Stack (قائمة عادية في بايثون وبنعمل لها append و pop)
    # بنخزن (المربع الحالي، والـ path اللي وصلنا له)
    stack = [(start, [start])]
    visited = set()

    # اتجاهات الحركة الأربعة
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    while stack:
        # pop() بتجيب آخر عنصر دخل الـ Stack (تأصيل الـ LIFO العميق)
        current, path = stack.pop()

        if current == target:
            return path

        if current not in visited:
            visited.add(current)

            for dx, dy in directions:
                neighbor = (current[0] + dx, current[1] + dy)
                
                # التأكد من الحدود ومن إنها مش حيطة وما زرتهاش
                if (0 <= neighbor[1] < len(maze_grid) and 
                    0 <= neighbor[0] < len(maze_grid[0]) and 
                    maze_grid[neighbor[1]][neighbor[0]] != 1 and 
                    neighbor not in visited):
                    
                    stack.append((neighbor, path + [neighbor]))

    return []