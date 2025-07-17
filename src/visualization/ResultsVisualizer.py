import matplotlib.pyplot as plt
import numpy as np


class ResultsVisualizer:
    def __init__(self):
        self.plot_data = {}

    def add_data(self, plot_data):
        self.plot_data = plot_data

    def plot_actual_vs_predicted(self, filename):
        y_true = self.plot_data['actual_vs_predicted']['y_true']
        y_pred = self.plot_data['actual_vs_predicted']['y_pred']

        plt.figure(figsize=(8, 6))
        plt.scatter(y_true, y_pred, alpha=0.5)
        plt.plot([min(y_true), max(y_true)], [min(y_true), max(y_true)], 'r--')
        plt.xlabel('Истинные значения')
        plt.ylabel('Предсказания')
        plt.title('Фактические vs Предсказанные значения')
        plt.grid(True)

        plt.savefig(filename, bbox_inches='tight', dpi=300)
        plt.close()

    def plot_feature_importance(self, filename):
        importances = self.plot_data['feature_importance']['importances']
        feature_names = self.plot_data['feature_importance']['feature_names']

        plt.figure(figsize=(10, 6))
        indices = np.argsort(importances)[::-1]
        plt.bar(range(len(importances)), importances[indices])
        plt.xticks(range(len(importances)), [feature_names[i] for i in indices], rotation=90)
        plt.title('Важность признаков')
        plt.tight_layout()

        plt.savefig(filename, bbox_inches='tight', dpi=300)
        plt.close()

