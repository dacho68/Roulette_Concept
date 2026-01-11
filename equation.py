"""
Fit mathematical functions to roulette streak probability data.
Finds the best equation to model the relationship between number of spins
and probability of getting at least one streak.
"""

import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import linregress
import matplotlib.pyplot as plt


# Data from the table
spins = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
prob_1streak = np.array([1, 4.9, 7.9, 11.9, 14.3, 17.4, 19.7, 22.2, 25.4, 27.3]) #  7 consecutive reds
#prob_1streak = np.array([4.1,10.3,16.2,22.6,28,32.7,38.1,42.4,45.4,49])  #  6 consecutive reds

# Define various candidate functions
def linear(x, a, b):
    """Linear: y = ax + b"""
    return a * x + b


def logarithmic(x, a, b):
    """Logarithmic: y = a*ln(x) + b"""
    return a * np.log(x) + b


def power(x, a, b):
    """Power: y = a*x^b"""
    return a * np.power(x, b)


def square_root(x, a, b):
    """Square root: y = a*sqrt(x) + b"""
    return a * np.sqrt(x) + b


def exponential_saturation(x, a, b, c):
    """Exponential saturation: y = a*(1 - e^(-bx)) + c"""
    return a * (1 - np.exp(-b * x)) + c


def logarithmic_saturation(x, a, b):
    """Logarithmic saturation: y = a*ln(x + b)"""
    return a * np.log(x + b)


def fit_and_evaluate(func, x_data, y_data, func_name, param_names):
    """Fit function and calculate R-squared."""
    try:
        # Fit the function
        if func == exponential_saturation:
            # Better initial guess for exponential
            popt, pcov = curve_fit(func, x_data, y_data, maxfev=10000, p0=[30, 0.02, 0])
        else:
            popt, pcov = curve_fit(func, x_data, y_data, maxfev=10000)
        
        # Calculate predictions
        y_pred = func(x_data, *popt)
        
        # Calculate R-squared
        ss_res = np.sum((y_data - y_pred) ** 2)
        ss_tot = np.sum((y_data - np.mean(y_data)) ** 2)
        r_squared = 1 - (ss_res / ss_tot)
        
        # Calculate RMSE (Root Mean Square Error)
        rmse = np.sqrt(np.mean((y_data - y_pred) ** 2))
        
        return {
            'name': func_name,
            'params': popt,
            'param_names': param_names,
            'r_squared': r_squared,
            'rmse': rmse,
            'function': func
        }
    except Exception as e:
        return None


def format_equation(result):
    """Format the equation as a readable string."""
    name = result['name']
    params = result['params']
    
    if name == "Linear":
        return f"y = {params[0]:.4f}*x + {params[1]:.4f}"
    elif name == "Logarithmic":
        return f"y = {params[0]:.4f}*ln(x) + {params[1]:.4f}"
    elif name == "Power":
        return f"y = {params[0]:.4f}*x^{params[1]:.4f}"
    elif name == "Square Root":
        return f"y = {params[0]:.4f}*sqrt(x) + {params[1]:.4f}"
    elif name == "Exponential Saturation":
        return f"y = {params[0]:.4f}*(1 - e^(-{params[1]:.6f}*x)) + {params[2]:.4f}"
    elif name == "Logarithmic Saturation":
        return f"y = {params[0]:.4f}*ln(x + {params[1]:.4f})"
    else:
        return "Unknown"


def main():
    """Fit various functions and display results."""
    print("=" * 80)
    print("CURVE FITTING: Spins vs Probability of At Least 1 Streak")
    print("=" * 80)
    print("\nData:")
    print(f"{'Spins':<10} {'Probability (%)':<20}")
    print("-" * 30)
    for s, p in zip(spins, prob_1streak):
        print(f"{s:<10} {p:<20.1f}")
    
    # Fit all functions
    results = []
    
    functions = [
        (linear, "Linear", ['a', 'b']),
        (logarithmic, "Logarithmic", ['a', 'b']),
        (power, "Power", ['a', 'b']),
        (square_root, "Square Root", ['a', 'b']),
        (exponential_saturation, "Exponential Saturation", ['a', 'b', 'c']),
        (logarithmic_saturation, "Logarithmic Saturation", ['a', 'b']),
    ]
    
    for func, name, param_names in functions:
        result = fit_and_evaluate(func, spins, prob_1streak, name, param_names)
        if result:
            results.append(result)
    
    # Sort by R-squared (best fit first)
    results.sort(key=lambda x: x['r_squared'], reverse=True)
    
    print("\n" + "=" * 80)
    print("FITTED FUNCTIONS (Ranked by R²):")
    print("=" * 80)
    
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['name']}")
        print(f"   Equation: {format_equation(result)}")
        print(f"   R² = {result['r_squared']:.6f}")
        print(f"   RMSE = {result['rmse']:.4f}")
    
    # Best fit
    best = results[0]
    print("\n" + "=" * 80)
    print("BEST FIT MODEL:")
    print("=" * 80)
    print(f"\n{best['name']}")
    print(f"Equation: {format_equation(best)}")
    print(f"R² = {best['r_squared']:.6f}")
    print(f"RMSE = {best['rmse']:.4f}")
    
    # Predictions for additional values
    print("\n" + "=" * 80)
    print("PREDICTIONS USING BEST FIT:")
    print("=" * 80)
    test_spins = np.array([15, 25, 35, 45, 55, 75, 85, 95, 110, 120, 150, 200])
    predictions = best['function'](test_spins, *best['params'])
    
    print(f"{'Spins':<10} {'Predicted Probability (%)':<30}")
    print("-" * 40)
    for s, p in zip(test_spins, predictions):
        print(f"{s:<10} {p:<30.2f}")
    
    # Plot the results
    plot_results(spins, prob_1streak, results[:3])  # Plot top 3 fits


def plot_results(x_data, y_data, results):
    """Plot the data and fitted curves."""
    plt.figure(figsize=(12, 8))
    
    # Plot original data
    plt.scatter(x_data, y_data, color=BetType.RED, s=100, zorder=5, label='Actual Data', marker='o')
    
    # Generate smooth curve for plotting
    x_smooth = np.linspace(x_data.min(), x_data.max(), 300)
    
    # Plot each fitted curve
    colors = ['blue', 'green', 'orange', 'purple', 'brown']
    for i, result in enumerate(results):
        y_smooth = result['function'](x_smooth, *result['params'])
        label = f"{result['name']} (R²={result['r_squared']:.4f})"
        plt.plot(x_smooth, y_smooth, color=colors[i], linewidth=2, label=label, alpha=0.7)
    
    plt.xlabel('Number of Spins', fontsize=12, fontweight='bold')
    plt.ylabel('Probability of At Least 1 Streak (%)', fontsize=12, fontweight='bold')
    plt.title('Curve Fitting: Spins vs Streak Probability', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Save the plot
    plt.savefig('streak_probability_fit.png', dpi=300, bbox_inches='tight')
    print("\n" + "=" * 80)
    print(f"Plot saved as 'streak_probability_fit.png'")
    print("=" * 80)
    
    plt.show()


if __name__ == "__main__":
    main()
