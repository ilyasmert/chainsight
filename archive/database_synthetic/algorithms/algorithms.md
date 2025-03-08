### **Algorithm Selection Based on Objectives**

| **Objective** | **Algorithm** |
| --- | --- |
| **14-Week Forecasting** | ARIMA, SARIMA, Prophet, LSTM |
| **Critical Product Identification** | Logistic Regression, Decision Trees, Random Forest, Gradient Boosting (XGBoost, LightGBM) |
| **Transportation Recommendations** | Linear Programming, MILP, Genetic Algorithms, Greedy Algorithms |
| **Production Rescheduling Recommendations** | MILP, Simulated Annealing, Genetic Algorithms |
| **Anomaly Detection for Stock Levels** | Isolation Forest, Autoencoders |

---

### **Forecasting Algorithm Details** ###
#### 1. **ARIMA (AutoRegressive Integrated Moving Average)**
- Suitable for univariate time-series forecasting.
- Assumes data is stationary or can be made stationary by differencing.
- Captures trends and seasonality but works best for short- to medium-term forecasts.

#### 2. **SARIMA (Seasonal ARIMA)** ###
- Extends ARIMA by incorporating seasonality.
- Handles periodic patterns, making it ideal for weekly or monthly seasonal data.
- Suitable for datasets with strong cyclical trends.

#### 3. **Prophet** ###
- Developed by Facebook for automated forecasting.
- Handles seasonality, holidays, and missing data effectively.
- Suitable for business forecasts with trend shifts.

 #### 4. **LSTM (Long Short-Term Memory)** ###
- A type of recurrent neural network (RNN) used for deep learning.
- Handles long-term dependencies, making it powerful for complex patterns.
- Requires more data and computational resources than traditional models.

---

### **Critical Product Algorithm Details** ###

#### 1. Logistic Regression
- **Purpose**: Used for binary or multi-class classification problems.
- **Use Case**: Identify critical products (e.g., shortage risk or demand surges) based on feature values.
- **Key Features**: 
  - Interpretable coefficients for feature importance.
  - Fast and computationally efficient.
- **Limitations**:
  - Assumes **linear relationships** between features.
  - Sensitive to **outliers**.

#### 2. Decision Trees
- **Purpose**: Non-linear classification and regression using hierarchical decisions.
- **Use Case**: Segment products based on predefined rules to determine criticality.
- **Key Features**:
  - Easy to interpret.
  - Handles both **numerical** and **categorical** data.
- **Limitations**:
  - Prone to **overfitting**.
  - Does not generalize well with small datasets.

#### 3. Random Forest
- **Purpose**: Ensemble learning method that builds multiple decision trees and averages results.
- **Use Case**: Identify critical products by reducing overfitting seen in individual decision trees.
- **Key Features**:
  - Improves **accuracy** and reduces **variance**.
  - Provides **feature importance rankings**.
- **Limitations**:
  - Requires more **computational resources**.
  - May be slower with **large datasets**.

#### 4. Gradient Boosting (XGBoost, LightGBM)
- **Purpose**: Ensemble methods that use boosting techniques for better predictions.
- **Use Case**: Prioritize critical products based on patterns learned from data.
- **Key Features**:
  - **XGBoost**: Faster, scalable, and handles **missing data** efficiently.
  - **LightGBM**: Optimized for large datasets and supports **categorical data** natively.
  - Handles **imbalanced data** effectively.
- **Limitations**:
  - Sensitive to **hyperparameters**.
  - Can be prone to **overfitting** if not tuned properly.

---




### **Transportation Algorithm Details**

#### **1. Linear Programming (LP)**
- **Purpose**: Optimize a linear objective function subject to linear constraints.
- **Use Case**: Continuous decision variables like minimizing transportation costs or maximizing efficiency.
- **Limitations**: Cannot handle discrete choices or non-linear constraints.

#### **2. Mixed-Integer Linear Programming (MILP)**
- **Purpose**: Extends LP with integer decision variables to handle discrete optimization problems.
- **Use Case**: Binary decisions (e.g., truck or container) with capacity constraints.
- **Limitations**: Computationally expensive for large datasets.

#### **3. Genetic Algorithms (GA)**
- **Purpose**: Heuristic optimization inspired by natural selection.
- **Use Case**: Non-linear or complex constraints, dynamic and multi-objective optimization.
- **Limitations**: Computationally intensive, slower convergence, and no guarantee of optimality.

#### **4. Greedy Algorithms**
- **Purpose**: Makes locally optimal decisions at each step to approximate a globally optimal solution.
- **Use Case**: Quick prioritization of urgent deliveries or cost-effective transport.
- **Limitations**: May not yield globally optimal results due to lack of backtracking.

---

###  Production Rescheduling Recommendations

#### 1. Mixed-Integer Linear Programming (MILP)
- **Purpose**: Optimizes schedules by considering discrete and continuous decision variables.
- **Use Case**: Minimize delays and reschedule production tasks under capacity and time constraints.
- **Key Features**:
  - Handles **binary decisions** (e.g., produce or wait).
  - Ensures globally optimal solutions for **linear constraints**.
- **Limitations**:
  - Computationally expensive for **large datasets**.
  - Requires specialized solvers like **CPLEX** or **Gurobi**.

#### 2. Simulated Annealing
- **Purpose**: Probabilistic optimization inspired by the annealing process in metallurgy.
- **Use Case**: Suitable for non-linear scheduling problems with complex constraints.
- **Key Features**:
  - Avoids local optima by allowing **temporary worsening solutions**.
  - Flexible for highly constrained optimization.
- **Limitations**:
  - Requires fine-tuning of cooling schedules.
  - Slower convergence compared to **greedy algorithms**.

#### 3. Genetic Algorithms (GA)
- **Purpose**: Evolutionary optimization based on selection, crossover, and mutation.
- **Use Case**: Optimizes production sequences by simulating genetic evolution.
- **Key Features**:
  - Suitable for **non-linear and dynamic constraints**.
  - Handles multi-objective problems (e.g., minimize costs and delays).
- **Limitations**:
  - Computationally intensive.
  - May not guarantee global optima but finds **good approximations**.

---

### Anomaly Detection for Stock Levels

#### 1. Isolation Forest

- **Purpose**: Detect anomalies by isolating data points through recursive partitioning.
- **Use Case**: Identify unusual stock levels (e.g., sudden spikes or drops).
- **Key Features**:
  - Effective for **high-dimensional data**.
  - Requires minimal parameter tuning.
  - Handles **imbalanced datasets** effectively.
- **Limitations**:
  - May not perform well when anomalies are **densely clustered**.
  - Sensitive to **noise** in data.

#### 2. Autoencoders

- **Purpose**: Neural network-based approach for anomaly detection by learning data representations.
- **Use Case**: Detect anomalies by reconstructing stock levels and measuring reconstruction errors.
- **Key Features**:
  - Suitable for **non-linear and complex patterns**.
  - Learns **latent features** for improved anomaly detection.
  - Scalable for large datasets.
- **Limitations**:
  - Requires **large datasets** for training.
  - Sensitive to **hyperparameter tuning**.
  - Computationally expensive compared to traditional methods.

---


