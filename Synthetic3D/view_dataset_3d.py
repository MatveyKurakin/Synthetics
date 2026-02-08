import os

import cv2
import numpy as np
import vtk
from vtk.util import numpy_support

path_to_data = "D:/Projects/UnetClass/pytorch/segmentation/data/original data/training"

read_slices = 25

class_name_list = ["mitochondria", "PSD", "vesicles", "axon", "boundaries", "mitochondrial boundaries"]
#class_name_list = class_name_list[:-1]

actor_list = []
actor_enabled_list = []
intensity = 2.0

EdgeVisibility = True

def inner_filter(data):
    data_filter = data.copy()

    for z in range(1, data.shape[0]-1):
        for y in range(1, data.shape[1] - 1):
            for x in range(1, data.shape[2] - 1):
                if  data[z  , y, x] > 0 and\
                    data[z+1, y, x] > 0 and\
                    data[z-1, y, x] > 0 and\
                    data[z, y+1, x] > 0 and\
                    data[z, y-1, x] > 0 and\
                    data[z, y  , x+1] > 0 and\
                    data[z, y  , x-1] > 0:
                    data_filter[z, y, x] = 0
    print("data filtred !")
    return data_filter
def get_poly_data_from_numpy(data):
    # Предположим, что data — ваш numpy массив
    assert 2 < len(data.shape)

    if len(data.shape) == 3 or data.shape[3] == 1:
        X, Y, Z = data.shape
        C = 1
    else:
        X, Y, Z, C = data.shape

    # Создаем сетку координат
    x = np.arange(X)
    y = np.arange(Y)
    z = np.arange(Z)
    X_grid, Y_grid, Z_grid = np.meshgrid(x, y, z, indexing='ij')

    # Векторизуем и объединяем координаты
    coords = np.column_stack((X_grid.ravel(), Y_grid.ravel(), Z_grid.ravel()))
    values = data.ravel() if C == 1 else data.reshape(-1, C)  # для RGB

    # Фильтруем точки, у которых значение != 0
    mask = values != 0 if C == 1 else np.any(values != 0, axis=1)
    filtered_coords = coords[mask]
    filtered_values = values[mask]

    # Создаем vtkPoints для только выбранных точек
    points_vtk = vtk.vtkPoints()
    points_vtk.SetNumberOfPoints(filtered_coords.shape[0])
    points_vtk.SetData(numpy_support.numpy_to_vtk(filtered_coords, deep=True))

    if C == 1:
        # Создаем vtkScalars для выбранных точек
        colors_vtk = numpy_support.numpy_to_vtk(filtered_values, deep=True, array_type=vtk.VTK_FLOAT)
        colors_vtk.SetName("scalars")
    else:
        # Этот блок нужно добавить, чтобы преобразовать массив RGB в vtk-совместимый формат:
        colors_vtk = vtk.vtkUnsignedCharArray()
        colors_vtk.SetNumberOfComponents(3)
        colors_vtk.SetNumberOfTuples(filtered_coords.shape[0])
        for i, color in enumerate(filtered_values):
            assert color.shape == (3,)
            colors_vtk.SetTuple3(i, int(color[0]), int(color[1]), int(color[2]))

    # Создаем polyData и добавляем точки и скаляры
    polyData = vtk.vtkPolyData()
    polyData.SetPoints(points_vtk)
    polyData.GetPointData().SetScalars(colors_vtk)

    return polyData

def get_actor_poly_data(polyData, C=1, filtered_values=(1,255)):
    # Создаем источник куба для глифа
    cubeSource = vtk.vtkCubeSource()
    cubeSource.SetXLength(1)
    cubeSource.SetYLength(1)
    cubeSource.SetZLength(1)

    # Настраиваем маппер
    glyphMapper = vtk.vtkGlyph3DMapper()
    glyphMapper.SetInputData(polyData)
    glyphMapper.SetSourceConnection(cubeSource.GetOutputPort())

    glyphMapper.SetScalarRange(0, 255)

    if C == 1:
        # Создаем таблицу цветовой карты для оттенков серого
        lookupTable = vtk.vtkLookupTable()
        lookupTable.SetNumberOfTableValues(256)
        lookupTable.SetRange(np.min(filtered_values), np.max(filtered_values))
        for i in range(256):
            gray = i / 255.0  # градации от 0 до 1
            lookupTable.SetTableValue(i, gray, gray, gray, 1.0)
        lookupTable.Build()
        glyphMapper.SetScalarModeToUsePointData()
        glyphMapper.SetColorModeToMapScalars()
        glyphMapper.SetLookupTable(lookupTable)
    else:
        glyphMapper.SetColorModeToDirectScalars()

    # Создаем актер для глифов
    glyphActor = vtk.vtkActor()
    glyphActor.SetMapper(glyphMapper)
    glyphActor.GetProperty().EdgeVisibilityOn()

    return glyphActor

def view_vtk_3D_data_list(data_list, slice_data):
    # Создаем рендерер и добавляем актер
    renderer = vtk.vtkRenderer()

    global actor_list
    global actor_enabled_list
    for data in data_list:
        polyData = get_poly_data_from_numpy(data*slice_data)
        actor = get_actor_poly_data(polyData)
        actor_list.append(actor)
        actor_enabled_list.append(True)
        renderer.AddActor(actor)



    renderer.SetBackground(0.1, 0.2, 0.4)

    # Создаем окно рендера
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindow.SetSize(800, 600)

    # Создаем интерактор
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(renderWindow)

    def EdgeVisibilityChange(obj, event):
        global EdgeVisibility
        if EdgeVisibility:
            for actor in actor_list:
                actor.GetProperty().EdgeVisibilityOff()
            EdgeVisibility = False
        else:
            for actor in actor_list:
                actor.GetProperty().EdgeVisibilityOn()
            EdgeVisibility = True
        renderWindow.Render()

    def on_default_style(obj, event):
        style = vtk.vtkInteractorStyleTrackballCamera()
        interactor.SetInteractorStyle(style)
    #def on_user_style(obj, event):
    #    style = vtk.vtkInteractorStyleTrackballCamera()
    #    interactor.SetInteractorStyle(style)

    def toggle_actor_pip(index):
        def toggle_actor(obj, event):
            global actor_enabled_list
            global actor_list
            if actor_enabled_list[index]:
                actor_list[index].VisibilityOff()
                actor_enabled_list[index] = False
            else:
                actor_list[index].VisibilityOn()
                actor_enabled_list[index] = True
            renderWindow.Render()
        return toggle_actor

    # Создаем источник света
    light = vtk.vtkLight()
    light.SetLightTypeToCameraLight()  # Связь с камерой
    global intensity
    light.SetIntensity(intensity)  # Увеличиваем яркость
    renderer.AddLight(light)

    # Функция для изменения яркости
    def set_light_brightness(value):
        global intensity # — значение от 0 до 1
        if value == "up":
            intensity += 1
        else:
            intensity -= 1
        light.SetIntensity(intensity)
        renderWindow.Render()
    def keypress_callback(obj, event):
        key = obj.GetKeySym()
        if key == 'z':
            toggle_actor_pip(0)(obj, event)
        elif key == 'x':
            toggle_actor_pip(1)(obj, event)
        elif key == 'c':
            toggle_actor_pip(2)(obj, event)
        elif key == 'v':
            toggle_actor_pip(3)(obj, event)
        elif key == 'b':
            toggle_actor_pip(4)(obj, event)
        elif key == 'n':
            toggle_actor_pip(5)(obj, event)


        elif key == 'a':
            EdgeVisibilityChange(obj, event)
        elif key == 's':
            on_default_style(obj, event)

       # Например, изменить яркость при нажатии клавиши "+" или "-"
        elif key == 'plus' or key == 'KP_Add':
            print("plus")
            set_light_brightness("up")  # максимально ярко
        elif key == 'minus' or key == 'KP_Subtract':
            print("minus")
            set_light_brightness("down")  # тускло




    interactor.AddObserver("KeyPressEvent", keypress_callback)
    # Запуск рендера
    interactor.Initialize()
    renderWindow.Render()
    interactor.Start()



img_names = [name for name in os.listdir(os.path.join(path_to_data, "original"))][:read_slices]
print(img_names)

data_epfl = np.zeros((read_slices, 768, 1024), dtype=np.uint8)
masks_list = []

for i, name in enumerate(img_names):
    img = cv2.imread(os.path.join(path_to_data, "original", name), 0)
    data_epfl[i] = img

for classname in class_name_list:
    masks_list.append(np.zeros((read_slices, 768, 1024), dtype=np.uint8))
    for i, name in enumerate(img_names):
        img = cv2.imread(os.path.join(path_to_data, classname, name), 0)
        img[img<127] = 0
        img[img>0] = 255
        masks_list[-1][i] = img
        #cv2.imshow("img", data_epfl[i])
        #cv2.waitKey()

    masks_list[-1] = inner_filter(masks_list[-1])
    masks_list[-1][masks_list[-1] > 0] = 1

view_vtk_3D_data_list(masks_list, data_epfl)
