# RushHourAI #
AI coded in Python that implements the A* search algorithm on the sliding puzzle game of RushHour

# Blocking Heuristic
Measured by the amount of cars in front of our Red Car on the horizontal plane

# Custom Heuristic
Measured by the amount of cars in front of our Red Car on the horizontal plane, as well as factoring the distance of the red
car from the exit. This custom heuristic reduces the amount of states visited by selecting the better path in cases of tie breakers for our previous heuristic.
