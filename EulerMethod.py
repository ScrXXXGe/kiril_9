import asyncio
from asyncio import Queue
from typing import Callable, List, Tuple


class EulerMethod:
    def __init__(self, x_start: float, y_start: float, x_end: float, step_size: float,
                 differential_equation: Callable[[float, float], float]):
        self._differential_equation = differential_equation
        self._step_size = step_size
        self._x_end = x_end
        self._x_start = x_start
        self._y_start = y_start
        self._state = Queue()
        self._running = True

        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.euler_full())

    @property
    def differential_equation(self):
        return self._differential_equation

    @differential_equation.setter
    def differential_equation(self, value):
        self._differential_equation = value
        self.loop.create_task(self.euler_full())

    @property
    def step_size(self):
        return self._step_size

    @step_size.setter
    def step_size(self, value):
        self._step_size = value
        self.loop.create_task(self.euler_full())

    @property
    def x_end(self):
        return self._x_end

    @x_end.setter
    def x_end(self, value):
        self._x_end = value
        self.loop.create_task(self.euler_full())

    @property
    def x_start(self):
        return self._x_start

    @x_start.setter
    def x_start(self, value):
        self._x_start = value
        self.loop.create_task(self.euler_full())

    @property
    def y_start(self):
        return self._y_start

    @y_start.setter
    def y_start(self, value):
        self._y_start = value
        self.loop.create_task(self.euler_full())

    async def euler_step(self, x_current: float, step_size: float, y_current: float,
                         differential_equation: Callable[[float, float], float]) -> float:
        if step_size <= 0:
            raise ValueError("stepSize should be greater than zero")
        return y_current + step_size * differential_equation(x_current, y_current)

    async def euler_full(self):
        if self._x_start >= self._x_end:
            raise ValueError("xEnd should be greater than xStart")
        if self._step_size <= 0:
            raise ValueError("stepSize should be greater than zero")

        points = []
        points.append((self._x_start, self._y_start))
        y_current = self._y_start
        x_current = self._x_start

        while x_current < self._x_end:
            y_current = await self.euler_step(x_current, self._step_size, y_current, self._differential_equation)
            x_current += self._step_size
            points.append((x_current, y_current))

        await self._state.put(points)

    async def get_state(self) -> List[Tuple[float, float]]:
        return await self._state.get()

    def close(self):
        self._running = False
        for task in asyncio.all_tasks(self.loop):
            task.cancel()


# Usage example
async def main():
    def diff_eq(x, y):
        return (math.sin(x) - y) * math.cos(x)

    euler = EulerMethod(0, 0, 11.0, 0.5, diff_eq)


    state = await euler.get_state()
    print(state)

    euler.close()


asyncio.run(main())
