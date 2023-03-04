from math import pi
from matplotlib.gridspec import GridSpec
import matplotlib.pyplot as plt
from pandas import DataFrame, Series
from random import uniform


def generate_points_coords(
    number_of_points: int, bounds: tuple = (0.0, 1.0)
) -> DataFrame:
    return DataFrame(
        {
            "x": [uniform(*bounds) for _ in range(number_of_points)],
            "y": [uniform(*bounds) for _ in range(number_of_points)],
        }
    )


def circle_equation_value(x: Series, r: float = 1) -> float:
    return (r**2 - x**2) ** 0.5


def check_if_points_inside_circle(points: DataFrame, r: float = 1) -> DataFrame:
    points["is_inside"] = points["y"] <= circle_equation_value(points["x"], r)
    return points


def estimate_pi(number_of_points: int, points: DataFrame, r: float = 1) -> list:
    points = check_if_points_inside_circle(points, r)
    subsequent_pi_values = []
    for current_number_of_points in range(1, number_of_points + 1):
        subsequent_pi_values.append(
            4
            * sum(points.head(current_number_of_points)["is_inside"])
            / current_number_of_points
        )
    return subsequent_pi_values


NUMBER_OF_POINTS = [10, 100, 1000, 10000]
NUMBER_OF_ATTEMPTS = 10
MAX_NUMBER_OF_POINTS = NUMBER_OF_POINTS[-1]

pts = []
estimated_pi = []

for num in NUMBER_OF_POINTS:
    pts = generate_points_coords(num)
    estimated_pi = estimate_pi(num, pts)
    final_pi = estimated_pi[-1]
    print(final_pi)

fig = plt.figure(constrained_layout=True)

gs = GridSpec(2, 3, figure=fig)
ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1:])
ax3 = fig.add_subplot(gs[-1, 0])
ax4 = fig.add_subplot(gs[-1, 1])
ax5 = fig.add_subplot(gs[-1, -1])

fig.suptitle("Estimating the value of PI using Monte Carlo method", fontweight="bold")

ax1.scatter(pts["x"], pts["y"], alpha=0.6, s=1, c=pts["is_inside"])
ax1.set_aspect("equal", "box")
ax1.set_title("10 000 randomly generated points")
ax1.set_xlabel("X")
ax1.set_ylabel("Y")

ax2.axhline(y=pi, color="red", zorder=1)
ax2.scatter(
    list(range(1, MAX_NUMBER_OF_POINTS + 1)), estimated_pi, s=0.05, alpha=0.8, zorder=2
)
ax2.set_title(
    "Current value of PI as the number of generated points increases from 1 to 10 000"
)

plt.show()

# to do:
# more attempts
# try different seed and different random number generator
# boxplots for all of the attempts
