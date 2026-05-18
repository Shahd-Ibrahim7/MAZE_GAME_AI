# algorithms/bfs.py
from collections import deque

def bfs(maze_grid, start, target):
    """
    start: إحداثيات البداية للعدو (x, y)
    target: إحداثيات الهدف للاعب (x, y)
    maze_grid: مصفوفة المتاهة (0 ممر، 1 حيطة)
    """
    # تحويل الإحداثيات لـ Tuples للتأكيد
    start = (start[0], start[1])
    target = (target[0], target[1])

    # لو العدو واقف فوق اللاعب أصلاً، يرجع مكانه
    if start == target:
        return [start]

    # الطابور (Queue) وهنخزن فيه المربع الحالي، والمسار اللي مشيناه عشان نوصل له
    # الـ Queue بيبدأ بنقطة البداية ومسار فيه نقطة البداية بس
    queue = deque([(start, [start])])
    
    # مجموعة (Set) لتسجيل المربعات اللي زرتها قبل كده عشان ماندخلش في إنفنيت لوب
    visited = set()
    visited.add(start)

    # اتجاهات الحركة الأربعة (يمين، شمال، تحت، فوق) بالـ (dx, dy)
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    while queue:
        current, path = queue.popleft()

        # أول ما نوصل لإحداثيات اللاعب (الهدف)، ارجع بالمسار كامل علطول!
        if current == target:
            return path

        # فحص الجيران الأربعة للمربع الحالي
        for dx, dy in directions:
            neighbor = (current[0] + dx, current[1] + dy)
            
            # التأكد إن المربع الجديد جوه حدود المتاهة ومش حيطة (مش 1) وما اتزارش قبل كده
            if (0 <= neighbor[1] < len(maze_grid) and 
                0 <= neighbor[0] < len(maze_grid[0]) and 
                maze_grid[neighbor[1]][neighbor[0]] != 1 and 
                neighbor not in visited):
                
                visited.add(neighbor)
                # ضيف المربع الجديد للـ Queue وزود خطوته على الـ Path الحالي
                queue.append((neighbor, path + [neighbor]))

    # لو مفيش أي طريق يوصل للاعب (ممر مقفول تماماً)
    return []