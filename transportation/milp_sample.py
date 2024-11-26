# created by Kıvanç Filizci on 26 Nov 2024
# SPRINT-2 : ITEM-1 : Literature Review on Optimization Algorithms for Transportation

import pulp

# Define the problem
prob = pulp.LpProblem("Transportation_Optimization", pulp.LpMinimize)

# Parameters
C_t = 100  # Cost per unit for truck transport
C_c = 50   # Cost per unit for container transport
Q_t = 500  # Quota for truck transport
Q_c = 1000 # Quota for container transport
D = 1200   # Total demand

# Decision variables
x_t = pulp.LpVariable('x_t', lowBound=0, upBound=Q_t, cat='Integer')
x_c = pulp.LpVariable('x_c', lowBound=0, upBound=Q_c, cat='Integer')

# Objective function
prob += C_t * x_t + C_c * x_c, "Total_Transportation_Cost"

# Constraints
prob += x_t + x_c >= D, "Demand_Fulfillment"

# Solve the problem
prob.solve()

# Output the results
status = f"Status: {pulp.LpStatus[prob.status]}"
units_truck = f"Units transported by truck: {x_t.varValue}"
units_container = f"Units transported by container: {x_c.varValue}"
total_cost = f"Total Cost: ${pulp.value(prob.objective)}"

# Print the results
print(status)
print(units_truck)
print(units_container)
print(total_cost)

# Write the results to a text file
with open('transportation_results.txt', 'w') as file:
    file.write(status + '\n')
    file.write(units_truck + '\n')
    file.write(units_container + '\n')
    file.write(total_cost + '\n')