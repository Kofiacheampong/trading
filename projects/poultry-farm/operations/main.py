#!/usr/bin/env python3
"""
Investment Decision Tool
Main application that ties together all modules
"""

import json
from investment_analyzer import InvestmentAnalyzer
from risk_calculator import RiskCalculator
from portfolio_diversifier import PortfolioDiversifier


def main():
    """
    Main application entry point
    Demonstrates the investment decision tool with AMD vs GOLD comparison
    """
    print("Welcome to the Investment Decision Tool")
    print("=" * 50)
    
    # Initialize all components
    analyzer = InvestmentAnalyzer()
    risk_calc = RiskCalculator()
    diversifier = PortfolioDiversifier()
    
    # Get user input for their profile
    print("\nPlease enter your investment profile:")
    
    # For demo purposes, we'll use default values
    # In a real app, we'd get this from user input
    analyzer.set_user_profile(
        risk_tolerance='moderate',
        investment_timeline=5,
        financial_goals='Long-term wealth growth with moderate risk'
    )
    
    print(f"Profile set: {analyzer.user_profile['risk_tolerance']} risk tolerance, "
          f"{analyzer.user_profile['investment_timeline']}-year timeline")
    
    # Add AMD stock data
    print("\nAnalyzing AMD stock...")
    analyzer.add_investment_option(
        symbol='AMD',
        name='Advanced Micro Devices Inc.',
        category='stock',
        fundamentals={
            'pe_ratio': 120.5,
            'debt_to_equity': 0.45,
            'revenue_growth': 18.2,
            'expected_growth': 22.0,
            'dividend_yield': 0.0
        },
        technicals={
            'volatility': 0.35,
            'beta': 1.35,
            'momentum_score': 65.0
        },
        risk_factors={
            'sector_volatility': 'high',
            'concentration_risk': 'medium',
            'regulatory_risk': 'low'
        }
    )
    
    # Add GOLD (using GLD ETF as proxy)
    print("Analyzing GOLD (GLD ETF)...")
    analyzer.add_investment_option(
        symbol='GLD',
        name='SPDR Gold Shares ETF',
        category='commodity',
        fundamentals={
            'pe_ratio': 0,  # N/A for commodities
            'debt_to_equity': 0,
            'revenue_growth': 0,
            'expected_growth': 3.0,  # Historical average
            'dividend_yield': 0.0
        },
        technicals={
            'volatility': 0.20,
            'beta': 0.10,  # Low correlation to equities
            'momentum_score': 45.0
        },
        risk_factors={
            'sector_volatility': 'medium',
            'concentration_risk': 'low',
            'regulatory_risk': 'very_low'
        }
    )
    
    # Perform detailed risk analysis for both investments
    print("\nPerforming Risk Analysis...")
    
    # Example risk calculations
    # Note: In a real implementation, these would use actual historical data
    amd_returns_example = [0.05, -0.02, 0.03, 0.08, -0.01, 0.06, 0.04, -0.03, 0.07, 0.02]
    gld_returns_example = [0.01, 0.02, -0.01, 0.03, 0.02, 0.01, -0.01, 0.02, 0.01, 0.03]
    market_returns_example = [0.03, 0.01, 0.02, 0.05, 0.00, 0.04, 0.03, -0.01, 0.05, 0.02]
    
    amd_volatility = risk_calc.calculate_volatility([100, 105, 103, 106, 114, 113, 117, 120, 117, 119])
    gld_volatility = risk_calc.calculate_volatility([180, 182, 180, 185, 189, 191, 190, 192, 193, 195])
    
    amd_beta = risk_calc.calculate_beta(amd_returns_example, market_returns_example)
    gld_beta = risk_calc.calculate_beta(gld_returns_example, market_returns_example)
    
    amd_sharpe = risk_calc.calculate_sharpe_ratio(amd_returns_example)
    gld_sharpe = risk_calc.calculate_sharpe_ratio(gld_returns_example)
    
    print(f"AMD - Volatility: {amd_volatility:.2f}%, Beta: {amd_beta:.2f}, Sharpe: {amd_sharpe:.2f}")
    print(f"GLD - Volatility: {gld_volatility:.2f}%, Beta: {gld_beta:.2f}, Sharpe: {gld_sharpe:.2f}")
    
    # Compare the investments
    print("\nGenerating Investment Recommendations...")
    comparison = analyzer.compare_investments(['AMD', 'GLD'])
    
    print("\nInvestment Comparison Report")
    print("=" * 80)
    
    for i, result in enumerate(comparison, 1):
        print(f"\n{i}. {result['symbol']} - {result['recommendation']}")
        print(f"   Overall Score: {result['overall_score']:.1f}/100")
        print(f"   Risk Score: {result['risk_score']:.1f}/100 (lower is less risky)")
        print(f"   Return Potential: {result['return_potential']:.2f}% annually")
        print(f"   Goal Alignment: {result['alignment_score']:.1f}/100")
        print(f"   Diversification Impact: {result['diversification_score']:.1f}/100")
        print(f"   Confidence: {result['confidence']}")
        print(f"   Rationale: {result['rationale']}")
    
    # Demonstrate portfolio diversification analysis
    print("\nPortfolio Diversification Analysis")
    print("=" * 50)
    
    # Set up a sample portfolio with SPY and TLT
    diversifier.add_asset(
        symbol='SPY',
        weight=0.6,
        expected_return=10.0,
        volatility=15.0,
        correlations={'TLT': -0.2}
    )
    
    diversifier.add_asset(
        symbol='TLT',
        weight=0.3,
        expected_return=5.0,
        volatility=10.0,
        correlations={'SPY': -0.2}
    )
    
    # Calculate current portfolio metrics
    current_metrics = diversifier.calculate_portfolio_metrics()
    print(f"Current Portfolio Metrics:")
    print(f"  Expected Return: {current_metrics['return']:.2f}%")
    print(f"  Volatility: {current_metrics['volatility']:.2f}%")
    print(f"  Sharpe Ratio: {current_metrics['sharpe_ratio']:.2f}")
    print(f"  Diversification Ratio: {current_metrics['diversification_ratio']:.2f}")
    
    # Analyze adding AMD or GLD to the portfolio
    print(f"\nAnalyzing addition of AMD to portfolio:")
    amd_benefit = diversifier.calculate_diversification_benefit(
        new_asset_symbol='AMD',
        new_asset_weight=0.1,
        new_asset_return=22.0,
        new_asset_volatility=35.0,
        new_asset_correlations={'SPY': 0.6, 'TLT': -0.1}
    )
    
    print(f"  Return Change: {amd_benefit['return_change']:+.2f}%")
    print(f"  Volatility Change: {amd_benefit['volatility_change']:+.2f}%")
    print(f"  Sharpe Ratio Change: {amd_benefit['sharpe_change']:+.2f}")
    print(f"  Diversification Improvement: {amd_benefit['diversification_improvement']:+.2f}")
    
    print(f"\nAnalyzing addition of GLD to portfolio:")
    gld_benefit = diversifier.calculate_diversification_benefit(
        new_asset_symbol='GLD',
        new_asset_weight=0.1,
        new_asset_return=3.0,
        new_asset_volatility=20.0,
        new_asset_correlations={'SPY': 0.05, 'TLT': 0.1}
    )
    
    print(f"  Return Change: {gld_benefit['return_change']:+.2f}%")
    print(f"  Volatility Change: {gld_benefit['volatility_change']:+.2f}%")
    print(f"  Sharpe Ratio Change: {gld_benefit['sharpe_change']:+.2f}")
    print(f"  Diversification Improvement: {gld_benefit['diversification_improvement']:+.2f}")
    
    # Final recommendation summary
    print(f"\nFinal Recommendation Summary")
    print("=" * 50)
    
    amd_rec = next(r for r in comparison if r['symbol'] == 'AMD')
    gld_rec = next(r for r in comparison if r['symbol'] == 'GLD')
    
    print(f"AMD Overall Score: {amd_rec['overall_score']:.1f} ({amd_rec['recommendation']})")
    print(f"GLD Overall Score: {gld_rec['overall_score']:.1f} ({gld_rec['recommendation']})")
    
    if amd_rec['overall_score'] > gld_rec['overall_score']:
        print(f"\nBased on your profile, AMD appears to be the better choice with a higher overall score.")
        print(f"However, AMD has higher risk ({amd_rec['risk_score']:.1f}) compared to GLD ({gld_rec['risk_score']:.1f}).")
    else:
        print(f"\nBased on your profile, GLD appears to be the better choice with a higher overall score.")
        print(f"GLD offers lower risk ({gld_rec['risk_score']:.1f}) compared to AMD ({amd_rec['risk_score']:.1f}).")
    
    print(f"\nNote: This analysis is for educational purposes only and does not constitute investment advice.")
    print(f"Please consult with a qualified financial advisor before making investment decisions.")


if __name__ == "__main__":
    main()