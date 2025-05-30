def compute_roi(analysis_result):
    # Check if analysis_result contains an error
    if "error" in analysis_result:
        return {"error": "Cannot compute ROI: Analysis failed"}
    
    # Check if required key exists
    if "recommended_panels" not in analysis_result:
        return {"error": "Solar panel recommendation missing from analysis"}
    
    try:
        # Solar panel specifications
        panel_capacity_kw = 0.35  # 350W panels
        panels = analysis_result["recommended_panels"]
        
        # Validate panels is a reasonable number
        if not isinstance(panels, (int, float)) or panels <= 0:
            return {"error": "Invalid number of recommended panels"}
        
        system_size_kw = panels * panel_capacity_kw

        # Energy calculations (Indian conditions)
        daily_output_kwh = system_size_kw * 4.5  # 4.5 peak sun hours average for India
        annual_output_kwh = daily_output_kwh * 365

        # Cost calculations (Indian market rates)
        cost_per_kw = 45000  # INR per kW installed
        total_cost = system_size_kw * cost_per_kw

        # Government incentives (30% subsidy)
        incentive_rate = 0.3
        incentive_amount = total_cost * incentive_rate
        net_cost = total_cost - incentive_amount

        # Savings calculation
        average_electricity_price = 7  # INR per kWh
        annual_savings = annual_output_kwh * average_electricity_price
        
        # Avoid division by zero
        if annual_savings <= 0:
            payback_period = float('inf')
        else:
            payback_period = net_cost / annual_savings

        return {
            "system_size_kw": round(system_size_kw, 2),
            "annual_output_kwh": round(annual_output_kwh),
            "total_cost_inr": round(total_cost),
            "incentive_inr": round(incentive_amount),
            "net_cost_inr": round(net_cost),
            "annual_savings_inr": round(annual_savings),
            "payback_period": round(payback_period, 2) if payback_period != float('inf') else "N/A"
        }
    
    except Exception as e:
        return {"error": f"ROI calculation failed: {str(e)}"}