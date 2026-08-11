"""
Investment Decision Tool
A framework for analyzing investment options like AMD vs GOLD
"""

import json
from datetime import datetime
from typing import Dict, List, Optional


class InvestmentAnalyzer:
    """
    Main class for analyzing investment options based on user preferences and market data
    """
    
    def __init__(self):
        self.user_profile = {}
        self.investment_options = {}
        
    def set_user_profile(self, risk_tolerance: str, investment_timeline: int, 
                        financial_goals: str, current_portfolio: dict = None):
        """
        Set user's investment profile
        
        Args:
            risk_tolerance: 'conservative', 'moderate', or 'aggressive'
            investment_timeline: years until investment horizon
            financial_goals: description of user's goals
            current_portfolio: dictionary of current holdings
        """
        self.user_profile = {
            'risk_tolerance': risk_tolerance,
            'investment_timeline': investment_timeline,
            'financial_goals': financial_goals,
            'current_portfolio': current_portfolio or {},
            'assessment_date': datetime.now().isoformat()
        }
        
    def add_investment_option(self, symbol: str, name: str, category: str, 
                            fundamentals: dict, technicals: dict, 
                            risk_factors: dict, correlation_data: dict = None):
        """
        Add an investment option to analyze
        
        Args:
            symbol: ticker symbol (e.g., 'AMD', 'GLD')
            name: full name of the investment
            category: 'stock', 'commodity', 'bond', 'etf', etc.
            fundamentals: fundamental analysis data
            technicals: technical analysis data
            risk_factors: risk assessment data
            correlation_data: correlation with other holdings
        """
        self.investment_options[symbol] = {
            'symbol': symbol,
            'name': name,
            'category': category,
            'fundamentals': fundamentals,
            'technicals': technicals,
            'risk_factors': risk_factors,
            'correlation_data': correlation_data or {}
        }
        
    def calculate_risk_score(self, symbol: str) -> float:
        """
        Calculate a risk score for an investment option (0-100 scale)
        Higher score = higher risk
        """
        option = self.investment_options[symbol]
        risk_score = 0
        
        # Fundamental risk factors
        pe_ratio = option['fundamentals'].get('pe_ratio', 0)
        debt_equity = option['fundamentals'].get('debt_to_equity', 0)
        revenue_growth = option['fundamentals'].get('revenue_growth', 0)
        
        # Technical risk factors
        volatility = option['technicals'].get('volatility', 0)
        beta = option['technicals'].get('beta', 1.0)
        
        # Calculate risk components (simplified)
        fundamental_risk = (pe_ratio / 100) * 20 + (debt_equity * 15)
        technical_risk = volatility * 30 + (beta - 1) * 10
        overall_risk = (fundamental_risk + technical_risk) / 2
        
        # Normalize to 0-100 scale
        risk_score = min(100, max(0, overall_risk))
        return risk_score
    
    def calculate_return_potential(self, symbol: str) -> float:
        """
        Calculate potential return for an investment option (annualized %)
        """
        option = self.investment_options[symbol]
        
        # Calculate return potential based on fundamentals and technicals
        growth_potential = option['fundamentals'].get('expected_growth', 0)
        momentum_score = option['technicals'].get('momentum_score', 0)
        dividend_yield = option['fundamentals'].get('dividend_yield', 0)
        
        # Weighted calculation
        return_potential = (growth_potential * 0.5) + (momentum_score * 0.3) + (dividend_yield * 0.2)
        
        return return_potential
    
    def assess_alignment_with_goals(self, symbol: str) -> float:
        """
        Assess how well the investment aligns with user's goals (0-100 scale)
        """
        # This would be more sophisticated in a real implementation
        # For now, we'll use a simplified approach based on user profile and investment type
        option = self.investment_options[symbol]
        
        alignment_score = 50  # Base score
        
        # Adjust based on user's risk tolerance
        user_risk = self.user_profile.get('risk_tolerance', 'moderate')
        option_risk = self.calculate_risk_score(symbol)
        
        if user_risk == 'conservative' and option_risk > 50:
            alignment_score -= 20
        elif user_risk == 'aggressive' and option_risk < 30:
            alignment_score -= 10
        elif user_risk == 'moderate' and abs(option_risk - 50) > 20:
            alignment_score -= 10
            
        # Adjust based on investment timeline
        timeline = self.user_profile.get('investment_timeline', 5)
        if option['category'] == 'commodity' and timeline < 3:
            alignment_score -= 15  # Commodities better for longer term
            
        return max(0, min(100, alignment_score))
    
    def calculate_diversification_impact(self, symbol: str) -> float:
        """
        Calculate how this investment would impact portfolio diversification (0-100 scale)
        Higher score = better diversification
        """
        # Simplified diversification calculation
        option = self.investment_options[symbol]
        current_holdings = self.user_profile.get('current_portfolio', {})
        
        # If no current portfolio, diversification impact is neutral
        if not current_holdings:
            return 50
            
        # Calculate diversification benefit based on category differences
        current_categories = set(holding.get('category', '') for holding in current_holdings.values())
        new_category = option['category']
        
        if new_category not in current_categories:
            # Adding new asset class improves diversification
            diversification_score = 80
        else:
            # Same category, less diversification benefit
            diversification_score = 30
            
        return diversification_score
    
    def generate_recommendation(self, symbol: str) -> Dict:
        """
        Generate a complete recommendation for an investment option
        """
        risk_score = self.calculate_risk_score(symbol)
        return_potential = self.calculate_return_potential(symbol)
        alignment_score = self.assess_alignment_with_goals(symbol)
        diversification_score = self.calculate_diversification_impact(symbol)
        
        # Overall score calculation
        weighted_score = (
            (100 - risk_score) * 0.25 +  # Lower risk is better (25% weight)
            return_potential * 0.30 +     # Higher return is better (30% weight)
            alignment_score * 0.25 +      # Better alignment is better (25% weight)
            diversification_score * 0.20  # Better diversification is better (20% weight)
        )
        
        # Determine recommendation level
        if weighted_score >= 75:
            recommendation_level = "Strong Buy"
            confidence = "High"
        elif weighted_score >= 60:
            recommendation_level = "Buy"
            confidence = "Medium"
        elif weighted_score >= 40:
            recommendation_level = "Hold"
            confidence = "Medium"
        else:
            recommendation_level = "Sell/Avoid"
            confidence = "High"
            
        return {
            'symbol': symbol,
            'risk_score': risk_score,
            'return_potential': return_potential,
            'alignment_score': alignment_score,
            'diversification_score': diversification_score,
            'overall_score': weighted_score,
            'recommendation': recommendation_level,
            'confidence': confidence,
            'rationale': self._generate_rationale(symbol, risk_score, return_potential, 
                                                alignment_score, diversification_score)
        }
    
    def _generate_rationale(self, symbol: str, risk_score: float, return_potential: float,
                           alignment_score: float, diversification_score: float) -> str:
        """
        Generate a textual rationale for the recommendation
        """
        option = self.investment_options[symbol]
        rationale_parts = []
        
        # Risk rationale
        if risk_score > 70:
            rationale_parts.append(f"{symbol} has high risk ({risk_score:.1f}/100), which may not suit all investors.")
        elif risk_score < 30:
            rationale_parts.append(f"{symbol} has low risk ({risk_score:.1f}/100), suitable for conservative investors.")
        else:
            rationale_parts.append(f"{symbol} has moderate risk ({risk_score:.1f}/100), appropriate for balanced portfolios.")
        
        # Return rationale
        if return_potential > 15:
            rationale_parts.append(f"It has high potential return ({return_potential:.2f}% annually).")
        elif return_potential > 5:
            rationale_parts.append(f"It has moderate potential return ({return_potential:.2f}% annually).")
        else:
            rationale_parts.append(f"It has lower potential return ({return_potential:.2f}% annually).")
        
        # Alignment rationale
        if alignment_score > 70:
            rationale_parts.append("It aligns well with your stated investment goals.")
        elif alignment_score > 40:
            rationale_parts.append("It moderately aligns with your investment goals.")
        else:
            rationale_parts.append("It may not align well with your stated investment goals.")
        
        # Diversification rationale
        if diversification_score > 70:
            rationale_parts.append("It would improve portfolio diversification.")
        elif diversification_score > 40:
            rationale_parts.append("It would have a neutral effect on portfolio diversification.")
        else:
            rationale_parts.append("It may not improve portfolio diversification.")
        
        return " ".join(rationale_parts)
    
    def compare_investments(self, symbols: List[str]) -> List[Dict]:
        """
        Compare multiple investment options and rank them
        """
        results = []
        for symbol in symbols:
            if symbol in self.investment_options:
                results.append(self.generate_recommendation(symbol))
        
        # Sort by overall score (highest first)
        results.sort(key=lambda x: x['overall_score'], reverse=True)
        return results


def main():
    """
    Example usage of the InvestmentAnalyzer
    """
    analyzer = InvestmentAnalyzer()
    
    # Set user profile
    analyzer.set_user_profile(
        risk_tolerance='moderate',
        investment_timeline=5,
        financial_goals='Long-term wealth growth with moderate risk'
    )
    
    # Add AMD stock
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
    
    # Compare the two investments
    comparison = analyzer.compare_investments(['AMD', 'GLD'])
    
    print("Investment Comparison Report")
    print("=" * 50)
    
    for i, result in enumerate(comparison, 1):
        print(f"\n{i}. {result['symbol']} - {result['recommendation']}")
        print(f"   Overall Score: {result['overall_score']:.1f}/100")
        print(f"   Risk Score: {result['risk_score']:.1f}/100")
        print(f"   Return Potential: {result['return_potential']:.2f}% annually")
        print(f"   Goal Alignment: {result['alignment_score']:.1f}/100")
        print(f"   Diversification Impact: {result['diversification_score']:.1f}/100")
        print(f"   Confidence: {result['confidence']}")
        print(f"   Rationale: {result['rationale']}")


if __name__ == "__main__":
    main()