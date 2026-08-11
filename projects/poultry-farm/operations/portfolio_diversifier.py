"""
Portfolio Diversifier Module
Analyzes diversification benefits of adding new investments to a portfolio
"""


class PortfolioDiversifier:
    """
    Analyzes portfolio diversification and suggests optimal allocations
    """
    
    def __init__(self):
        self.portfolio = {}
        
    def add_asset(self, symbol: str, weight: float, expected_return: float, 
                  volatility: float, correlations: dict = None):
        """
        Add an asset to the portfolio
        
        Args:
            symbol: Asset symbol/ticker
            weight: Portfolio weight (0.0 to 1.0)
            expected_return: Expected annual return (%)
            volatility: Annual volatility (%)
            correlations: Dictionary of correlations with other assets
        """
        if correlations is None:
            correlations = {}
            
        self.portfolio[symbol] = {
            'weight': weight,
            'expected_return': expected_return,
            'volatility': volatility,
            'correlations': correlations
        }
    
    def calculate_portfolio_metrics(self) -> dict:
        """
        Calculate overall portfolio metrics including return, risk, and diversification
        
        Returns:
            Dictionary with portfolio metrics
        """
        if not self.portfolio:
            return {'return': 0, 'volatility': 0, 'sharpe_ratio': 0, 'diversification_ratio': 0}
        
        # Calculate portfolio return (weighted average)
        portfolio_return = 0
        for asset in self.portfolio.values():
            portfolio_return += asset['weight'] * asset['expected_return']
        
        # Calculate portfolio volatility (considering correlations)
        portfolio_variance = 0
        symbols = list(self.portfolio.keys())
        
        for i, sym1 in enumerate(symbols):
            for j, sym2 in enumerate(symbols):
                w1 = self.portfolio[sym1]['weight']
                w2 = self.portfolio[sym2]['weight']
                vol1 = self.portfolio[sym1]['volatility']
                vol2 = self.portfolio[sym2]['volatility']
                
                if sym1 == sym2:
                    correlation = 1.0
                elif sym2 in self.portfolio[sym1]['correlations']:
                    correlation = self.portfolio[sym1]['correlations'][sym2]
                elif sym1 in self.portfolio[sym2]['correlations']:
                    correlation = self.portfolio[sym2]['correlations'][sym1]
                else:
                    # Default to 0.5 if correlation not specified
                    correlation = 0.5
                
                portfolio_variance += w1 * w2 * vol1 * vol2 * correlation
        
        portfolio_volatility = portfolio_variance ** 0.5
        
        # Calculate Sharpe ratio (assuming risk-free rate of 2%)
        sharpe_ratio = (portfolio_return - 2.0) / portfolio_volatility if portfolio_volatility > 0 else 0
        
        # Calculate diversification ratio
        weighted_individual_volatilities = 0
        for asset in self.portfolio.values():
            weighted_individual_volatilities += asset['weight'] * asset['volatility']
        
        diversification_ratio = weighted_individual_volatilities / portfolio_volatility if portfolio_volatility > 0 else 1
        
        return {
            'return': portfolio_return,
            'volatility': portfolio_volatility,
            'sharpe_ratio': sharpe_ratio,
            'diversification_ratio': diversification_ratio,
            'total_weight': sum(asset['weight'] for asset in self.portfolio.values())
        }
    
    def calculate_diversification_benefit(self, new_asset_symbol: str, new_asset_weight: float,
                                       new_asset_return: float, new_asset_volatility: float,
                                       new_asset_correlations: dict) -> dict:
        """
        Calculate the diversification benefit of adding a new asset to the portfolio
        
        Args:
            new_asset_symbol: Symbol of the new asset
            new_asset_weight: Proposed weight for the new asset
            new_asset_return: Expected return of the new asset
            new_asset_volatility: Volatility of the new asset
            new_asset_correlations: Correlations with existing portfolio assets
            
        Returns:
            Dictionary with diversification metrics
        """
        # Save original portfolio
        original_metrics = self.calculate_portfolio_metrics()
        
        # Temporarily add the new asset (adjusting weights proportionally)
        original_weights = {sym: asset['weight'] for sym, asset in self.portfolio.items()}
        
        # Adjust existing weights to accommodate new asset
        for symbol in self.portfolio:
            self.portfolio[symbol]['weight'] *= (1 - new_asset_weight)
        
        # Add new asset
        self.add_asset(
            symbol=new_asset_symbol,
            weight=new_asset_weight,
            expected_return=new_asset_return,
            volatility=new_asset_volatility,
            correlations=new_asset_correlations
        )
        
        # Calculate new portfolio metrics
        new_metrics = self.calculate_portfolio_metrics()
        
        # Restore original portfolio
        self.portfolio.pop(new_asset_symbol)
        for symbol in self.portfolio:
            self.portfolio[symbol]['weight'] = original_weights[symbol]
        
        # Calculate diversification benefit
        return {
            'original_return': original_metrics['return'],
            'new_return': new_metrics['return'],
            'return_change': new_metrics['return'] - original_metrics['return'],
            'original_volatility': original_metrics['volatility'],
            'new_volatility': new_metrics['volatility'],
            'volatility_change': new_metrics['volatility'] - original_metrics['volatility'],
            'original_sharpe': original_metrics['sharpe_ratio'],
            'new_sharpe': new_metrics['sharpe_ratio'],
            'sharpe_change': new_metrics['sharpe_ratio'] - original_metrics['sharpe_ratio'],
            'original_diversification_ratio': original_metrics['diversification_ratio'],
            'new_diversification_ratio': new_metrics['diversification_ratio'],
            'diversification_improvement': new_metrics['diversification_ratio'] - original_metrics['diversification_ratio'],
            'is_diversifying': new_metrics['volatility'] < original_metrics['volatility'] or new_metrics['diversification_ratio'] > original_metrics['diversification_ratio']
        }
    
    def suggest_optimal_allocation(self, assets: list, target_risk: float = None) -> dict:
        """
        Suggest an optimal allocation for a set of assets
        
        Args:
            assets: List of dictionaries containing asset data
                   Each asset dict should have: symbol, expected_return, volatility, correlations
            target_risk: Optional target portfolio volatility
            
        Returns:
            Dictionary with suggested allocation
        """
        # This is a simplified equal-weighting algorithm
        # In practice, this would use more sophisticated optimization techniques
        num_assets = len(assets)
        equal_weight = 1.0 / num_assets
        
        suggested_allocation = {}
        for asset in assets:
            suggested_allocation[asset['symbol']] = {
                'weight': equal_weight,
                'expected_return': asset['expected_return'],
                'volatility': asset['volatility']
            }
        
        # If target risk is specified, adjust weights accordingly
        if target_risk:
            # This is a simplified approach - in reality, you'd use quadratic programming
            current_portfolio = {}
            for asset in assets:
                current_portfolio[asset['symbol']] = {
                    'weight': equal_weight,
                    'expected_return': asset['expected_return'],
                    'volatility': asset['volatility'],
                    'correlations': asset.get('correlations', {})
                }
            
            # Placeholder for more complex optimization logic
            pass
        
        return suggested_allocation
    
    def analyze_sector_diversification(self) -> dict:
        """
        Analyze sector diversification within the portfolio
        
        Returns:
            Dictionary with sector concentration metrics
        """
        # This would require sector information for each asset
        # For now, returning a placeholder
        sectors = {}
        
        # Placeholder implementation
        # In a real implementation, this would map assets to sectors and calculate concentration
        for symbol in self.portfolio:
            # Assuming each asset has a 'sector' field which is not currently implemented
            sector = self.portfolio[symbol].get('sector', 'Unknown')
            if sector not in sectors:
                sectors[sector] = 0
            sectors[sector] += self.portfolio[symbol]['weight']
        
        return {
            'sector_weights': sectors,
            'most_concentrated': max(sectors.items(), key=lambda x: x[1]) if sectors else ('None', 0),
            'num_sectors': len(sectors),
            'herfindahl_hirschman_index': sum(w**2 for w in sectors.values()) if sectors else 0
        }
    
    def get_concentration_risks(self) -> list:
        """
        Identify concentration risks in the portfolio
        
        Returns:
            List of concentration risk warnings
        """
        risks = []
        
        # Check for single asset concentration (>50% of portfolio)
        for symbol, asset in self.portfolio.items():
            if asset['weight'] > 0.5:
                risks.append(f"High concentration in {symbol}: {asset['weight']*100:.1f}% of portfolio")
        
        # Calculate HHI (Herfindahl-Hirschman Index) for portfolio concentration
        hhi = sum((asset['weight'])**2 for asset in self.portfolio.values())
        if hhi > 0.25:
            risks.append(f"Portfolio is highly concentrated (HHI: {hhi:.3f})")
        elif hhi > 0.18:
            risks.append(f"Portfolio has moderate concentration (HHI: {hhi:.3f})")
        
        return risks


def main():
    """
    Example usage of PortfolioDiversifier
    """
    diversifier = PortfolioDiversifier()
    
    # Add some example assets to the portfolio
    diversifier.add_asset(
        symbol='SPY',
        weight=0.6,
        expected_return=10.0,
        volatility=15.0,
        correlations={'TLT': -0.2, 'GLD': 0.05}
    )
    
    diversifier.add_asset(
        symbol='TLT',
        weight=0.3,
        expected_return=5.0,
        volatility=10.0,
        correlations={'SPY': -0.2, 'GLD': 0.1}
    )
    
    # Calculate current portfolio metrics
    metrics = diversifier.calculate_portfolio_metrics()
    print("Current Portfolio Metrics:")
    print(f"Expected Return: {metrics['return']:.2f}%")
    print(f"Volatility: {metrics['volatility']:.2f}%")
    print(f"Sharpe Ratio: {metrics['sharpe_ratio']:.2f}")
    print(f"Diversification Ratio: {metrics['diversification_ratio']:.2f}")
    print(f"Total Weight: {metrics['total_weight']:.2f}")
    
    print("\nConcentration Risks:")
    for risk in diversifier.get_concentration_risks():
        print(f"- {risk}")
    
    # Analyze benefit of adding gold
    gold_benefit = diversifier.calculate_diversification_benefit(
        new_asset_symbol='GLD',
        new_asset_weight=0.1,
        new_asset_return=3.0,
        new_asset_volatility=18.0,
        new_asset_correlations={'SPY': 0.05, 'TLT': 0.1}
    )
    
    print(f"\nAdding GLD (10% weight) would result in:")
    print(f"Return Change: {gold_benefit['return_change']:+.2f}%")
    print(f"Volatility Change: {gold_benefit['volatility_change']:+.2f}%")
    print(f"Sharpe Ratio Change: {gold_benefit['sharpe_change']:+.2f}")
    print(f"Diversification Improvement: {gold_benefit['diversification_improvement']:+.2f}")
    print(f"Is Diversifying: {gold_benefit['is_diversifying']}")


if __name__ == "__main__":
    main()