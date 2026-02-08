from Synthetic3D.src.hard.draw_element import setPixel2D, setVoxel3D

"""
setPixel(x,y) - функция закрашивает пиксель, с координатами x и y
"""
def draw_line_2D(img, x1=0, y1=0, x2=0, y2=0, color=255, thickness=1):
    if thickness<0:
        raise Exception("thickness не может быть меньше 0!")

    dx = x2 - x1
    dy = y2 - y1

    sign_x = 1 if dx>0 else -1 if dx<0 else 0
    sign_y = 1 if dy>0 else -1 if dy<0 else 0

    if dx < 0: dx = -dx
    if dy < 0: dy = -dy

    if dx > dy:
        pdx, pdy = sign_x, 0
        es, el = dy, dx
    else:
        pdx, pdy = 0, sign_y
        es, el = dx, dy

    x, y = x1, y1

    error, t = el/2, 0

    setPixel2D(img, x, y, color, thickness)

    while t < el:
        error -= es
        if error < 0:
            error += el
            x += sign_x
            y += sign_y
        else:
            x += pdx
            y += pdy
        t += 1
        setPixel2D(img, x, y, color, thickness)

    return img

def draw_circle_2D(img, x, y, r, color, thickness):
    disp_x = x
    disp_y = y
    x = 0
    y = r
    delta = (1-2*r)
    error = 0
    while y >= 0:
        setPixel2D(img, disp_x + x, disp_y + y, color, thickness)
        setPixel2D(img, disp_x + x, disp_y - y, color, thickness)
        setPixel2D(img, disp_x - x, disp_y + y, color, thickness)
        setPixel2D(img, disp_x - x, disp_y - y, color, thickness)

        error = 2 * (delta + y) - 1
        if ((delta < 0) and (error <=0)):
            x+=1
            delta = delta + (2*x+1)
            continue
        error = 2 * (delta - x) - 1
        if ((delta > 0) and (error > 0)):
            y -= 1
            delta = delta + (1 - 2 * y)
            continue
        x += 1
        delta = delta + (2 * (x - y))
        y -= 1

def draw_ellips_2D(img, x, y, r1, r2, color, thickness):
    disp_x = x
    disp_y = y
    x = 0
    y = r2

    a2 = r1**2
    b2 = r2**2

    delta = a2*(3 - 2 * r2)

    '''
    while y >= 0:
        setPixel2D(img, disp_x + x, disp_y + y, color, thickness)
        setPixel2D(img, disp_x + x, disp_y - y, color, thickness)
        setPixel2D(img, disp_x - x, disp_y + y, color, thickness)
        setPixel2D(img, disp_x - x, disp_y - y, color, thickness)

        error = 2 * (delta + y) - 1
        if ((delta < 0) and (error <= 0)):
            x += 1
            delta = delta + b2 * (2 * x + 1)
            continue
        error = 2 * (delta - x) - 1
        if ((delta > 0) and (error > 0)):
            y -= 1
            delta = delta - a2 * (2 * y)
            continue
        x += 1
        delta = delta + b2 * (2 * x) + a2 * (2 * y)
        y -= 1
    '''

    while y >= 0:
        setPixel2D(img, disp_x + x, disp_y + y, color, thickness)
        setPixel2D(img, disp_x + x, disp_y - y, color, thickness)
        setPixel2D(img, disp_x - x, disp_y + y, color, thickness)
        setPixel2D(img, disp_x - x, disp_y - y, color, thickness)

        error = 2 * (delta + y) - 1
        if ((delta < 0) and (error <= 0)):
            x += 1
            delta = delta + b2 * (2 * x)
            continue
        y -= 1
        error = 2 * (delta - x) - 1
        if ((delta > 0) and (error > 0)):
            delta = delta - a2 * (2 * y)
            continue
        x += 1
        delta = delta + b2 * (2 * x) + a2 * (2 * y)

def draw_line_3D(data, point1, point2, color, thickness):
    x1, y1, z1 = point1
    x2, y2, z2 = point2

    setVoxel3D(data, point1, color, thickness)
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    dz = abs(z2 - z1)

    xs = 1 if x1 < x2 else -1
    ys = 1 if y1 < y2 else -1
    zs = 1 if z1 < z2 else -1

    # Driving axis is X-axis"
    if (dx >= dy and dx >= dz):
        p1 = 2 * dy - dx
        p2 = 2 * dz - dx
        while (x1 != x2):
            x1 += xs
            if (p1 >= 0):
                y1 += ys
                p1 -= 2 * dx
            if (p2 >= 0):
                z1 += zs
                p2 -= 2 * dx
            p1 += 2 * dy
            p2 += 2 * dz
            setVoxel3D(data, (x1, y1, z1), color, thickness)

    # Driving axis is Y-axis"
    elif (dy >= dx and dy >= dz):
        p1 = 2 * dx - dy
        p2 = 2 * dz - dy
        while (y1 != y2):
            y1 += ys
            if (p1 >= 0):
                x1 += xs
                p1 -= 2 * dy
            if (p2 >= 0):
                z1 += zs
                p2 -= 2 * dy
            p1 += 2 * dx
            p2 += 2 * dz
            setVoxel3D(data, (x1, y1, z1), color, thickness)

    # Driving axis is Z-axis"
    else:
        p1 = 2 * dy - dz
        p2 = 2 * dx - dz
        while (z1 != z2):
            z1 += zs
            if (p1 >= 0):
                y1 += ys
                p1 -= 2 * dz
            if (p2 >= 0):
                x1 += xs
                p2 -= 2 * dz
            p1 += 2 * dy
            p2 += 2 * dx
            setVoxel3D(data, (x1, y1, z1), color, thickness)
    return data

def generate_poinst_by_line_3D(point1, point2):
    x1, y1, z1 = point1
    x2, y2, z2 = point2

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    dz = abs(z2 - z1)

    xs = 1 if x1 < x2 else -1
    ys = 1 if y1 < y2 else -1
    zs = 1 if z1 < z2 else -1

    # Driving axis is X-axis"
    if (dx >= dy and dx >= dz):
        p1 = 2 * dy - dx
        p2 = 2 * dz - dx
        while (x1 != x2):
            x1 += xs
            if (p1 >= 0):
                y1 += ys
                p1 -= 2 * dx
            if (p2 >= 0):
                z1 += zs
                p2 -= 2 * dx
            p1 += 2 * dy
            p2 += 2 * dz
            yield (x1, y1, z1)

    # Driving axis is Y-axis"
    elif (dy >= dx and dy >= dz):
        p1 = 2 * dx - dy
        p2 = 2 * dz - dy
        while (y1 != y2):
            y1 += ys
            if (p1 >= 0):
                x1 += xs
                p1 -= 2 * dy
            if (p2 >= 0):
                z1 += zs
                p2 -= 2 * dy
            p1 += 2 * dx
            p2 += 2 * dz
            yield (x1, y1, z1)

    # Driving axis is Z-axis"
    else:
        p1 = 2 * dy - dz
        p2 = 2 * dx - dz
        while (z1 != z2):
            z1 += zs
            if (p1 >= 0):
                y1 += ys
                p1 -= 2 * dz
            if (p2 >= 0):
                x1 += xs
                p2 -= 2 * dz
            p1 += 2 * dy
            p2 += 2 * dx
            yield (x1, y1, z1)
