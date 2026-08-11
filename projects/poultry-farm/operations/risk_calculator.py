"""
Risk Calculator Module
Calculates various risk metrics for investment analysis
"""


class RiskCalculator:
    """
    Calculates different types of risk metrics for investments
    """
    
    @staticmethod
    def calculate_volatility(prices: list) -> float:
        """
        Calculate price volatility (standard deviation of returns)
        
        Args:
            prices: List of historical prices
            
        Returns:
            Float representing volatility as a percentage
        """
        if len(prices) < 2:
            return 0.0
            
        # Calculate returns
        returns = []
        for i in range(1, len(prices)):
            ret = (prices[i] - prices[i-1]) / prices[i-1]
            returns.append(ret)
            
        # Calculate mean return
        mean_return = sum(returns) / len(returns)
        
        # Calculate variance
        squared_diffs = [(r - mean_return) ** 2 for r in returns]
        variance = sum(squared_diffs) / len(squared_diffs)
        
        # Calculate standard deviation (volatility)
        volatility = variance ** 0.5
        
        # Convert to percentage
        return volatility * 100
    
    @staticmethod
    def calculate_beta(stock_returns: list, market_returns: list) -> float:
        """
        Calculate beta coefficient (measure of systematic risk)
        
        Args:
            stock_returns: List of stock returns
            market_returns: List of market returns (e.g., S&P 500)
            
        Returns:
            Beta coefficient
        """
        if len(stock_returns) != len(market_returns) or len(stock_returns) < 2:
            return 1.0  # Default beta
            
        n = len(stock_returns)
        
        # Calculate means
        avg_stock = sum(stock_returns) / n
        avg_market = sum(market_returns) / n
        
        # Calculate covariance and variance
        covariance = 0
        market_variance = 0
        
        for i in range(n):
            stock_dev = stock_returns[i] - avg_stock
            market_dev = market_returns[i] - avg_market
            
            covariance += stock_dev * market_dev
            market_variance += market_dev * market_dev
        
        if market_variance == 0:
            return 1.0
            
        beta = covariance / market_variance
        return beta
    
    @staticmethod
    def calculate_sharpe_ratio(returns: list, risk_free_rate: float = 0.02) -> float:
        """
        Calculate Sharpe ratio (risk-adjusted return)
        
        Args:
            returns: List of investment returns
            risk_free_rate: Risk-free rate of return (default 2%)
            
        Returns:
            Sharpe ratio
        """
        if len(returns) < 2:
            return 0.0
            
        # Calculate average return
        avg_return = sum(returns) / len(returns)
        
        # Calculate excess return
        excess_return = avg_return - risk_free_rate
        
        # Calculate standard deviation of returns
        mean_return = sum(returns) / len(returns)
        squared_diffs = [(r - mean_return) ** 2 for r in returns]
        variance = sum(squared_diffs) / len(squared_diffs)
        std_dev = variance ** 0.5
        
        if std_dev == 0:
            return 0.0
            
        # Calculate Sharpe ratio
        sharpe_ratio = excess_return / std_dev
        return sharpe_ratio
    
    @staticmethod
    def calculate_value_at_risk(returns: list, confidence_level: float = 0.05) -> float:
        """
        Calculate Value at Risk (VaR) at a given confidence level
        
        Args:
            returns: List of historical returns
            confidence_level: Confidence level (e.g., 0.05 for 95% confidence)
            
        Returns:
            Value at Risk as a percentage
        """
        if len(returns) == 0:
            return 0.0
            
        # Sort returns in ascending order
        sorted_returns = sorted(returns)
        
        # Calculate index corresponding to confidence level
        index = int(confidence_level * len(sorted_returns))
        
        # VaR is the return at the calculated index (as a negative value)
        var = abs(sorted_returns[index]) if index < len(sorted_returns) else 0.0
        
        return var * 100  # Convert to percentage
    
    @staticmethod
    def calculate_correlation(series1: list, series2: list) -> float:
        """
        Calculate Pearson correlation coefficient between two series
        
        Args:
            series1: First data series
            series2: Second data series
            
        Returns:
            Correlation coefficient (-1 to 1)
        """
        if len(series1) != len(series2) or len(series1) < 2:
            return 0.0
            
        n = len(series1)
        
        # Calculate means
        mean1 = sum(series1) / n
        mean2 = sum(series2) / n
        
        # Calculate numerator and denominators for correlation formula
        numerator = 0
        sum_sq_diff1 = 0
        sum_sq_diff2 = 0
        
        for i in range(n):
            diff1 = series1[i] - mean1
            diff2 = series2[i] - mean2
            
            numerator += diff1 * diff2
            sum_sq_diff1 += diff1 * diff1
            sum_sq_diff2 += diff2 * diff2
        
        denominator = (sum_sq_diff1 * sum_sq_diff2) ** 0.5
        
        if denominator == 0:
            return 0.0
            
        correlation = numerator / denominator
        return correlation
    
    @staticmethod
    def calculate_max_drawdown(price_series: list) -> float:
        """
        Calculate maximum drawdown (peak-to-trough decline)
        
        Args:
            price_series: List of historical prices
            
        Returns:
            Maximum drawdown as a percentage
        """
        if len(price_series) < 2:
            return 0.0
            
        max_price = price_series[0]
        max_dd = 0.0
        
        for price in price_series:
            if price > max_price:
                max_price = price
            elif price < max_price:
                dd = (max_price - price) / max_price * 100
                if dd > max_dd:
                    max_dd = dd
        
        return max_dd


def main():
    """
    Example usage of RiskCalculator
    """
    calc = RiskCalculator()
    
    # Example price data
    amd_prices = [120, 125, 118, 122, 127, 130, 128, 132, 135, 140]
    market_prices = [4000, 4050, 4020, 4080, 4100, 4150, 4120, 4180, 4200, 4250]
    
    # Calculate various risk metrics
    volatility = calc.calculate_volatility(amd_prices)
    print(f"Volatility: {volatility:.2f}%")
    
    # Calculate returns for beta calculation
    amd_returns = [(amd_prices[i] - amd_prices[i-1]) / amd_prices[i-1] for i in range(1, len(amd_prices))]
    market_returns = [(market_prices[i] - market_prices[i-1]) / market_prices[i-1] for i in range(1, len(market_prices))]
    
    beta = calc.calculate_beta(amd_returns, market_returns)
    print(f"Beta: {beta:.2f}")
    
    sharpe = calc.calculate_sharpe_ratio(amd_returns)
    print(f"Sharpe Ratio: {sharpe:.2f}")
    
    var = calc.calculate_value_at_risk(amd_returns)
    print(f"Value at Risk (95%): {var:.2f}%")
    
    correlation = calc.calculate_correlation(amd_returns, market_returns)
    print(f"Correlation with market: {correlation:.2f}")
    
    max_dd = calc.calculate_max_drawdown(amd_prices)
    print(f"Max Drawdown: {max_dd:.2f}%")


if __name__ == "__main__":
    main()