# ai_agent/monitoring/dashboard.py
from ai_agent.metrics.metrics_calculator import AIAgentMetrics
import json

class MonitoringDashboard:
    def __init__(self):
        self.metrics_calc = AIAgentMetrics()
    
    def display_metrics(self):
        """Display metrics in a formatted way"""
        metrics = self.metrics_calc.calculate_ai_agent_metrics()
        
        print("="*50)
        print("AI AGENT PERFORMANCE DASHBOARD")
        print("="*50)
        print(f"Success Rate: {metrics['success_rate']}%")
        print(f"Total Queries: {metrics['total_queries']}")
        print(f"Average Response Time: {metrics['avg_response_time']}s")
        print(f"Error Rate: {metrics['error_rate']}%")
        print("="*50)
        
        return metrics
    
    def export_metrics_json(self, filename="metrics_report.json"):
        """Export metrics to JSON file"""
        metrics = self.metrics_calc.calculate_ai_agent_metrics()
        with open(filename, 'w') as f:
            json.dump(metrics, f, indent=2)
        print(f"Metrics exported to {filename}")

if __name__ == "__main__":
    dashboard = MonitoringDashboard()
    dashboard.display_metrics()
    dashboard.export_metrics_json()
