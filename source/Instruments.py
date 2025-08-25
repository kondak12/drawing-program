# Добавьте в верхнюю часть файла (глобальные импорты)
from abc import ABC, abstractmethod

import numpy as np
from numba import njit
import pygame
from configs import main_settings

# ---------- ПРЕДАЛОКАЦИЯ ГЛОБАЛЬНЫХ СТЕКОВ ----------
# Один раз выделяем максимально возможный стек (w*h).
# Это уменьшит аллокации при каждом вызове заливки.
_CANVAS_W = main_settings.CANVAS_SIZE[0]
_CANVAS_H = main_settings.CANVAS_SIZE[1]
_MAX_STACK = int(_CANVAS_W * _CANVAS_H)
# двумерные стек-буферы (int32)
_GLOBAL_STACK_X = np.empty(_MAX_STACK, dtype=np.int32)
_GLOBAL_STACK_Y = np.empty(_MAX_STACK, dtype=np.int32)


class Instrument(ABC):

    def __init__(self, display, draw_color, mouse_pos, draw_radius):
        self.display = display
        self.draw_color = draw_color
        self.mouse_pos = mouse_pos
        self.draw_radius = draw_radius

    @abstractmethod
    def draw(self) -> None:
        pass

    def set_draw_color(self, new_color: pygame.color.Color) -> None:
        self.draw_color = new_color

    def set_mouse_pos(self, new_pos: (int, int)) -> None:
        self.mouse_pos = new_pos

    def set_draw_radius(self, new_radius: int) -> None:
        self.draw_radius = new_radius


class BrushTool(Instrument):

    def __init__(self, display, draw_color, mouse_pos, draw_radius):
        super().__init__(display, draw_color, mouse_pos, draw_radius)
        self.__last_pos = None

    def __draw_example(self, mouse_button_target: int) -> None:
        if pygame.mouse.get_pressed()[mouse_button_target]:
            if self.__last_pos:

                dist_x = self.mouse_pos[0] - self.__last_pos[0]
                dist_y = self.mouse_pos[1] - self.__last_pos[1]
                distance = max(1, int((dist_x ** 2 + dist_y ** 2) ** 0.5))

                for i in range(distance):
                    x = int(self.__last_pos[0] + dist_x * i / distance)
                    y = int(self.__last_pos[1] + dist_y * i / distance)
                    pygame.draw.circle(self.display, self.draw_color, (x, y), self.draw_radius // 2)
            self.__last_pos = self.mouse_pos

        else:
            self.__last_pos = None

    def draw(self) -> None:
        self.__draw_example(0)

    def wash_draw(self) -> None:
        self.__draw_example(2)


# ---------- NUMBA-FILL (использует внешние стек-буферы) ----------
# cache=True — кэширует скомпилированную версию на диск между запусками
@njit(cache=True)
def _numba_fill_with_stack(arr, start_x, start_y, target_uint32, new_uint32,
                           stack_x, stack_y, max_stack):
    """
    arr: 2D uint32 array shape (width, height) with indexing arr[x,y]
    stack_x, stack_y: preallocated int32 arrays of length max_stack
    """
    w = arr.shape[0]
    h = arr.shape[1]

    # ограничительные проверки
    if start_x < 0 or start_x >= w or start_y < 0 or start_y >= h:
        return

    if arr[start_x, start_y] != target_uint32:
        return

    sp = 0
    stack_x[sp] = start_x
    stack_y[sp] = start_y
    sp += 1

    while sp > 0:
        sp -= 1
        x = stack_x[sp]
        y = stack_y[sp]

        # если уже не цель — пропускаем
        if arr[x, y] != target_uint32:
            continue

        # найти левую границу
        xl = x
        while xl >= 0 and arr[xl, y] == target_uint32:
            xl -= 1
        xl += 1

        # найти правую границу
        xr = x
        while xr < w and arr[xr, y] == target_uint32:
            xr += 1
        xr -= 1

        # заполнить спан
        xi = xl
        while xi <= xr:
            arr[xi, y] = new_uint32
            xi += 1

        # проверить соседние строки (y-1, y+1)
        for d in (-1, 1):
            ny = y + d
            if ny < 0 or ny >= h:
                continue

            xi = xl
            while xi <= xr:
                # пропускаем пиксели не целевого цвета
                if arr[xi, ny] != target_uint32:
                    xi += 1
                    continue

                sx = xi
                while xi <= xr and arr[xi, ny] == target_uint32:
                    xi += 1

                # push representative
                if sp < max_stack:
                    stack_x[sp] = sx
                    stack_y[sp] = ny
                    sp += 1
                else:
                    # защита — если стек переполнен (крайний случай), просто прерываем
                    return
    # функция модифицирует arr in-place

# ---------- FillTool (ускорённая версия) ----------
class FillTool(Instrument):
    """
    Очень быстрый FillTool, использующий numba-функцию с предвыделенным стеком.
    Вставьте в ваш код вместо старой реализации FillTool.
    """

    # Класс-атрибуты: глобальные стек-буферы переиспользуются
    _stack_x = _GLOBAL_STACK_X
    _stack_y = _GLOBAL_STACK_Y
    _max_stack = _MAX_STACK

    def __init__(self, display, draw_color, mouse_pos, draw_radius):
        super().__init__(display, draw_color, mouse_pos, draw_radius)
        self.__bottom_layer = None

    def __in_canvas(self) -> bool:
        width = main_settings.CANVAS_SIZE[0]
        height = main_settings.CANVAS_SIZE[1]
        # корректная проверка: координаты должны быть в диапазоне [0, width-1], [0, height-1]
        return (0 <= self.mouse_pos[0] < width) and (0 <= self.mouse_pos[1] < height)

    def set_bottom_layer(self) -> None:
        # получаем цвет в точке (возвращает pygame.Color)
        self.__bottom_layer = pygame.Surface.get_at(self.display, self.mouse_pos)

    @classmethod
    def warmup(cls):
        """
        Вызовите это при старте приложения, чтобы заранее JIT-скомпилировать функцию
        и избежать паузы при первом использовании в UI.
        """
        try:
            # маленький тестовый массив
            tmp = np.zeros((8, 8), dtype=np.uint32)
            # сделаем небольшую заливку (не влияет ни на что)
            _numba_fill_with_stack(tmp, 1, 1, np.uint32(0), np.uint32(1),
                                   cls._stack_x[:64].astype(np.int32), cls._stack_y[:64].astype(np.int32), 64)
        except Exception:
            # если что-то не так с numba на машине — игнорируем (fallback есть)
            pass

    def draw(self) -> None:
        # быстрые проверки
        if not (self.__in_canvas() and pygame.mouse.get_pressed()[0] == 1):
            return

        self.set_bottom_layer()
        surface = self.display
        target_color = self.__bottom_layer
        new_color = self.draw_color

        # быстрый выход, если цвета одинаковы
        if target_color == new_color:
            return

        start_x, start_y = int(self.mouse_pos[0]), int(self.mouse_pos[1])
        w, h = main_settings.CANVAS_SIZE
        if not (0 <= start_x < w and 0 <= start_y < h):
            return

        # целочисленные представления цветов (uint32)
        mapped_target = np.uint32(surface.map_rgb(target_color))
        mapped_new = np.uint32(surface.map_rgb(new_color))

        # Попытка использования surfarray + numba (максимум скорости)
        try:
            arr_view = pygame.surfarray.pixels2d(surface)  # view, не копия
            try:
                # ensure dtype uint32
                if arr_view.dtype != np.uint32:
                    arr_dtype_ok = False
                else:
                    arr_dtype_ok = True

                # проверяем contiguity и dtype
                if arr_view.flags.c_contiguous and arr_dtype_ok:
                    # можно работать in-place напрямую
                    _numba_fill_with_stack(arr_view, start_x, start_y,
                                           mapped_target, mapped_new,
                                           self._stack_x, self._stack_y, self._max_stack)
                    # освободить view
                    del arr_view
                else:
                    # создаём C-contiguous uint32 копию (единственная копия)
                    arr_copy = np.ascontiguousarray(arr_view, dtype=np.uint32)
                    del arr_view  # разблокировать поверхность перед blit
                    _numba_fill_with_stack(arr_copy, start_x, start_y,
                                           mapped_target, mapped_new,
                                           self._stack_x, self._stack_y, self._max_stack)
                    # Очень быстрая запись обратно в поверхность
                    pygame.surfarray.blit_array(surface, arr_copy)
                    del arr_copy
            except Exception:
                # очистим view, если что-то пошло не так
                try:
                    del arr_view
                except Exception:
                    pass

            return  # всё сделано (быстрый путь)
        except Exception:
            # если surfarray/pixels2d/numba недоступны — переходим к fallback
            pass

        # ---------- Fallback: PixelArray (быстрее get_at/set_at) ----------
        try:
            px = pygame.PixelArray(surface)
            target = surface.map_rgb(target_color)
            new = surface.map_rgb(new_color)
            if px[start_x, start_y] != target:
                del px
                return

            stack = [(start_x, start_y)]
            pop = stack.pop
            append = stack.append

            while stack:
                x, y = pop()

                xl = x
                while xl >= 0 and px[xl, y] == target:
                    xl -= 1
                xl += 1

                xr = x
                while xr < w and px[xr, y] == target:
                    xr += 1
                xr -= 1

                for xi in range(xl, xr + 1):
                    px[xi, y] = new

                for ny in (y - 1, y + 1):
                    if ny < 0 or ny >= h:
                        continue
                    xi = xl
                    while xi <= xr:
                        if px[xi, ny] != target:
                            xi += 1
                            continue
                        sx = xi
                        while xi <= xr and px[xi, ny] == target:
                            xi += 1
                        append((sx, ny))
            del px
        except Exception:
            # если даже PixelArray не доступен, в крайнем случае используем get_at/set_at (очень медленно)
            try:
                target = surface.map_rgb(target_color)
                new = surface.map_rgb(new_color)
                if surface.get_at((start_x, start_y)) != target_color:
                    return
                # простая BFS (не рекомендую) — здесь оставлена как абсолютный конец пути
                stack = [(start_x, start_y)]
                visited = set()
                while stack:
                    x, y = stack.pop()
                    if (x, y) in visited:
                        continue
                    visited.add((x, y))
                    if x < 0 or x >= w or y < 0 or y >= h:
                        continue
                    if surface.map_rgb(surface.get_at((x, y))) != target:
                        continue
                    surface.set_at((x, y), new_color)
                    stack.append((x+1, y)); stack.append((x-1, y)); stack.append((x, y+1)); stack.append((x, y-1))
            except Exception:
                # ничего не делаем — защита от незапланированных ошибок
                return


class PatternTool(Instrument):

    def __init__(self, display, draw_color, mouse_pos, draw_radius):
        super().__init__(display, draw_color, mouse_pos, draw_radius)
        self._start_pos = None
        self._background = None
        self._new_surface = None

    @abstractmethod
    def _create_new_surface(self, width, height) -> pygame.Surface:
        pass

    def draw(self) -> None:
        if pygame.mouse.get_pressed()[0]:

            if self._start_pos is None:
                self._start_pos = self.mouse_pos

                self._background = self.display.copy()

            self.display.blit(self._background, main_settings.ZERO_COORDINATES)

            x0, y0 = self._start_pos
            x1, y1 = self.mouse_pos
            width  = x1 - x0
            height = y1 - y0

            if width >= 0 and height >= 0:
                dest = (x0, y0)

            elif width < 0 and height < 0:
                dest = (x1, y1)
                width, height = -width, -height

            elif width >= 0 and height < 0:
                dest = (x0, y1)
                height = -height

            else:
                dest = (x1, y0)
                width = -width

            self._new_surface = self._create_new_surface(width, height)
            self.display.blit(self._new_surface, dest)

        else:
            self._start_pos = None
            self._background = None
            self._new_surface = None


class RectPatternTool(PatternTool):

    def __init__(self, display, draw_color, mouse_pos, draw_radius):
        super().__init__(display, draw_color, mouse_pos, draw_radius)

    def _create_new_surface(self, width, height) -> pygame.Surface:
        surf = pygame.Surface((width, height), pygame.SRCALPHA)

        pygame.draw.rect(
            surf,
            self.draw_color,
            pygame.Rect(0, 0, width, height),
            self.draw_radius
        )

        return surf


class CirclePatternTool(PatternTool):

    def __init__(self, display, draw_color, mouse_pos, draw_radius):
        super().__init__(display, draw_color, mouse_pos, draw_radius)

    def _create_new_surface(self, width, height) -> pygame.Surface:
        surf = pygame.Surface((width, height), pygame.SRCALPHA)

        pygame.draw.ellipse(
            surf,
            self.draw_color,
            (0, 0, width, height),
            self.draw_radius
        )

        return surf
    