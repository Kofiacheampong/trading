"""
Scalable Investment Analysis Framework
Handles large-scale investment analysis across thousands of securities
"""

import asyncio
import pandas as pd
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Optional, Tuple
import yfinance as yf
import time
from datetime import datetime, timedelta
import logging
from dataclasses import dataclass
import sqlite3
from threading import Lock


@dataclass
class InvestmentData:
    """Container for investment data"""
    symbol: str
    name: str
    sector: str
    industry: str
    market_cap: float
    fundamentals: Dict
    technicals: Dict
    risk_factors: Dict
    timestamp: datetime


class DataProvider:
    """Handles fetching investment data from various sources"""
    
    def __init__(self):
        self.cache = {}
        self.cache_lock = Lock()
        
    def get_bulk_symbols(self) -> List[str]:
        """Get list of symbols to analyze (in production, this would come from a database or API)"""
        # For demonstration, using a small subset - in production this could be 1000+ symbols
        major_stocks = [
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA', 'TSLA', 'AMD', 'INTC', 'ORCL',
            'IBM', 'CSCO', 'ADBE', 'NFLX', 'PYPL', 'AVGO', 'TXN', 'QCOM', 'TMUS', 'CHTR',
            'SBUX', 'CMCSA', 'INTU', 'AMGN', 'HON', 'BKNG', 'MDLZ', 'TSM', 'ASML', 'LIN',
            'NEE', 'EL', 'ABBV', 'ABT', 'PFE', 'JNJ', 'UNH', 'MRK', 'DHR', 'TMO'
        ]
        
        precious_metals = ['GLD', 'SLV', 'IAU', 'PHYS', 'SIVR']
        bonds_etfs = ['TLT', 'IEF', 'SHY', 'BND', 'AGG']
        
        return major_stocks + precious_metals + bonds_etfs
    
    def fetch_single_symbol_data(self, symbol: str) -> Optional[InvestmentData]:
        """Fetch data for a single symbol"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # Get historical data for technical analysis
            hist = ticker.history(period="1y")
            if hist.empty:
                return None
                
            # Calculate technical indicators
            returns = hist['Close'].pct_change().dropna()
            
            # Calculate volatility
            volatility = returns.std() * np.sqrt(252) * 100  # Annualized volatility
            
            # Calculate beta against SPY (S&P 500)
            spy_hist = yf.download('SPY', period="1y")['Close'].pct_change().dropna()
            overlapping_returns = pd.concat([returns, spy_hist], axis=1).dropna()
            if len(overlapping_returns) > 2:
                stock_returns = overlapping_returns.iloc[:, 0]
                market_returns = overlapping_returns.iloc[:, 1]
                
                # Calculate beta
                covariance = np.cov(stock_returns, market_returns)[0][1]
                market_variance = np.var(market_returns)
                beta = covariance / market_variance if market_variance != 0 else 1.0
            else:
                beta = 1.0  # Default beta if insufficient data
                
            # Prepare fundamentals
            fundamentals = {
                'pe_ratio': info.get('trailingPE', 0),
                'pb_ratio': info.get('priceToBook', 0),
                'debt_to_equity': info.get('debtToEquity', 0),
                'revenue_growth': info.get('revenueGrowth', 0),
                'earnings_growth': info.get('earningsGrowth', 0),
                'roa': info.get('returnOnAssets', 0),
                'roe': info.get('returnOnEquity', 0),
                'dividend_yield': info.get('dividendYield', 0) * 100 if info.get('dividendYield') else 0,
                'market_cap': info.get('marketCap', 0),
                'current_ratio': info.get('currentRatio', 0),
                'quick_ratio': info.get('quickRatio', 0),
            }
            
            # Prepare technicals
            technicals = {
                'volatility': volatility,
                'beta': beta,
                'rsi': self._calculate_rsi(hist['Close']),
                'macd': self._calculate_macd(hist['Close']),
                'sma_20': hist['Close'].tail(20).mean(),
                'sma_50': hist['Close'].tail(50).mean(),
                'sma_200': hist['Close'].tail(200).mean(),
                'atr': self._calculate_atr(hist),
                'volume_avg': hist['Volume'].tail(30).mean()
            }
            
            # Prepare risk factors
            risk_factors = {
                'sector_volatility': 'medium',  # Would come from sector data
                'liquidity_risk': 'low' if fundamentals['market_cap'] > 1e9 else 'high',
                'leverage_risk': 'high' if fundamentals['debt_to_equity'] > 1.0 else 'low',
                'concentration_risk': 'low',
                'regulatory_risk': 'low'
            }
            
            return InvestmentData(
                symbol=symbol,
                name=info.get('longName', symbol),
                sector=info.get('sector', 'Unknown'),
                industry=info.get('industry', 'Unknown'),
                market_cap=fundamentals['market_cap'],
                fundamentals=fundamentals,
                technicals=technicals,
                risk_factors=risk_factors,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            logging.error(f"Error fetching data for {symbol}: {str(e)}")
            return None
    
    def _calculate_rsi(self, prices, window=14):
        """Calculate Relative Strength Index"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs.iloc[-1]))
        return rsi if not np.isnan(rsi) else 50.0
    
    def _calculate_macd(self, prices, fast=12, slow=26, signal=9):
        """Calculate MACD indicator"""
        exp1 = prices.ewm(span=fast).mean()
        exp2 = prices.ewm(span=slow).mean()
        macd_line = exp1 - exp2
        return macd_line.iloc[-1] if not macd_line.empty else 0.0
    
    def _calculate_atr(self, df, window=14):
        """Calculate Average True Range"""
        high_low = df['High'] - df['Low']
        high_close = np.abs(df['High'] - df['Close'].shift())
        low_close = np.abs(df['Low'] - df['Close'].shift())
        true_range = np.maximum(high_low, np.maximum(high_close, low_close))
        atr = true_range.rolling(window=window).mean().iloc[-1]
        return atr if not np.isnan(atr) else 0.0
    
    def fetch_all_data_parallel(self, symbols: List[str], max_workers: int = 10) -> List[InvestmentData]:
        """Fetch data for all symbols in parallel"""
        results = []
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks
            future_to_symbol = {
                executor.submit(self.fetch_single_symbol_data, symbol): symbol 
                for symbol in symbols
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_symbol):
                result = future.result()
                if result:
                    results.append(result)
                    
        return results


class ScalableAnalyzer:
    """Handles large-scale investment analysis"""
    
    def __init__(self):
        self.data_provider = DataProvider()
        self.db_connection = sqlite3.connect(':memory:', check_same_thread=False)  # In-memory DB for demo
        self._setup_database()
        
    def _setup_database(self):
        """Set up database tables for storing analysis results"""
        cursor = self.db_connection.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analysis_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT,
                analysis_date TIMESTAMP,
                overall_score REAL,
                risk_score REAL,
                return_potential REAL,
                alignment_score REAL,
                diversification_score REAL,
                recommendation TEXT,
                confidence TEXT,
                user_profile_hash TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS investment_data_cache (
                symbol TEXT PRIMARY KEY,
                name TEXT,
                sector TEXT,
                industry TEXT,
                market_cap REAL,
                fundamentals_json TEXT,
                technicals_json TEXT,
                risk_factors_json TEXT,
                last_updated TIMESTAMP
            )
        ''')
        
        self.db_connection.commit()
    
    def store_investment_data(self, data: List[InvestmentData]):
        """Store investment data in database"""
        cursor = self.db_connection.cursor()
        
        for item in data:
            cursor.execute('''
                INSERT OR REPLACE INTO investment_data_cache 
                (symbol, name, sector, industry, market_cap, fundamentals_json, technicals_json, risk_factors_json, last_updated)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                item.symbol, item.name, item.sector, item.industry, item.market_cap,
                str(item.fundamentals), str(item.technicals), str(item.risk_factors), item.timestamp
            ))
        
        self.db_connection.commit()
    
    def bulk_analyze(self, user_profile: Dict, symbols: List[str] = None) -> List[Dict]:
        """Perform bulk analysis on multiple symbols for a user profile"""
        if symbols is None:
            symbols = self.data_provider.get_bulk_symbols()
        
        print(f"Starting bulk analysis for {len(symbols)} symbols...")
        
        # Fetch all data in parallel
        investment_data = self.data_provider.fetch_all_data_parallel(symbols)
        print(f"Fetched data for {len(investment_data)} symbols")
        
        # Store data in cache
        self.store_investment_data(investment_data)
        
        # Perform analysis in parallel
        results = []
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = []
            
            for data_item in investment_data:
                future = executor.submit(
                    self._analyze_single_investment,
                    data_item,
                    user_profile
                )
                futures.append((future, data_item.symbol))
            
            for future, symbol in futures:
                result = future.result()
                if result:
                    results.append(result)
                    
                    # Store in database
                    self._store_analysis_result(result, user_profile)
        
        # Sort by overall score
        results.sort(key=lambda x: x['overall_score'], reverse=True)
        
        return results
    
    def _analyze_single_investment(self, data: InvestmentData, user_profile: Dict) -> Optional[Dict]:
        """Analyze a single investment based on user profile"""
        try:
            # Calculate risk score (0-100, higher = more risk)
            risk_score = self._calculate_risk_score(data)
            
            # Calculate return potential
            return_potential = self._calculate_return_potential(data)
            
            # Calculate alignment with user goals
            alignment_score = self._calculate_alignment_score(data, user_profile)
            
            # Calculate diversification impact (simplified for bulk analysis)
            diversification_score = self._calculate_diversification_score(data, user_profile)
            
            # Calculate overall weighted score
            weighted_score = (
                (100 - risk_score) * 0.25 +  # Lower risk is better (25% weight)
                return_potential * 0.30 +     # Higher return is better (30% weight)
                alignment_score * 0.25 +      # Better alignment is better (25% weight)
                diversification_score * 0.20  # Better diversification is better (20% weight)
            )
            
            # Determine recommendation
            if weighted_score >= 75:
                recommendation = "Strong Buy"
                confidence = "High"
            elif weighted_score >= 60:
                recommendation = "Buy"
                confidence = "Medium"
            elif weighted_score >= 40:
                recommendation = "Hold"
                confidence = "Medium"
            else:
                recommendation = "Sell/Avoid"
                confidence = "High"
            
            return {
                'symbol': data.symbol,
                'name': data.name,
                'sector': data.sector,
                'market_cap': data.market_cap,
                'risk_score': risk_score,
                'return_potential': return_potential,
                'alignment_score': alignment_score,
                'diversification_score': diversification_score,
                'overall_score': weighted_score,
                'recommendation': recommendation,
                'confidence': confidence,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logging.error(f"Error analyzing {data.symbol}: {str(e)}")
            return None
    
    def _calculate_risk_score(self, data: InvestmentData) -> float:
        """Calculate risk score for an investment (0-100 scale)"""
        # Combine various risk factors
        fundamental_risk = 0
        if data.fundamentals['pe_ratio'] > 50:
            fundamental_risk += 20
        elif data.fundamentals['pe_ratio'] > 30:
            fundamental_risk += 10
            
        if data.fundamentals['debt_to_equity'] > 1.0:
            fundamental_risk += 25
        elif data.fundamentals['debt_to_equity'] > 0.5:
            fundamental_risk += 15
            
        # Technical risk based on volatility and beta
        technical_risk = min(50, data.technicals['volatility'] * 1.5)
        technical_risk += min(25, (data.technicals['beta'] - 1) * 15 if data.technicals['beta'] > 1 else 0)
        
        # Size factor (smaller companies have higher risk)
        size_factor = 0
        if data.market_cap < 2e9:  # Less than $2B
            size_factor = 15
        elif data.market_cap < 10e9:  # Less than $10B
            size_factor = 5
            
        total_risk = min(100, fundamental_risk + technical_risk + size_factor)
        return total_risk
    
    def _calculate_return_potential(self, data: InvestmentData) -> float:
        """Calculate potential return for an investment"""
        # Weight different factors
        growth_component = data.fundamentals['revenue_growth'] * 0.3 + data.fundamentals['earnings_growth'] * 0.3
        value_component = 0
        
        # Value based on PE ratio (lower PE = higher value)
        if data.fundamentals['pe_ratio'] > 0:
            if data.fundamentals['pe_ratio'] < 15:
                value_component = 10
            elif data.fundamentals['pe_ratio'] < 25:
                value_component = 5
        
        # Momentum component
        momentum_component = 0
        if data.technicals['sma_20'] > data.technicals['sma_50']:
            momentum_component = 5
        if data.technicals['sma_50'] > data.technicals['sma_200']:
            momentum_component += 3
            
        # Dividend yield
        dividend_component = data.fundamentals['dividend_yield'] * 0.5
        
        total_return = growth_component + value_component + momentum_component + dividend_component
        return max(0, min(50, total_return))  # Cap at 50% to be realistic
    
    def _calculate_alignment_score(self, data: InvestmentData, user_profile: Dict) -> float:
        """Calculate how well investment aligns with user profile"""
        score = 50  # Base score
        
        # Adjust based on user's risk tolerance
        user_risk = user_profile.get('risk_tolerance', 'moderate')
        risk_score = self._calculate_risk_score(data)
        
        if user_risk == 'conservative' and risk_score > 50:
            score -= min(30, risk_score - 50)
        elif user_risk == 'aggressive' and risk_score < 30:
            score -= 10
        elif user_risk == 'moderate' and abs(risk_score - 50) > 20:
            score -= 10
            
        # Adjust based on investment timeline
        timeline = user_profile.get('investment_timeline', 5)
        if data.sector in ['Technology', 'Consumer Cyclical'] and timeline < 3:
            score -= 15  # Higher risk for short-term in volatile sectors
            
        # Adjust based on sector preference
        preferred_sectors = user_profile.get('preferred_sectors', [])
        if preferred_sectors and data.sector in preferred_sectors:
            score += 10
            
        return max(0, min(100, score))
    
    def _calculate_diversification_score(self, data: InvestmentData, user_profile: Dict) -> float:
        """Calculate diversification impact"""
        current_holdings = user_profile.get('current_portfolio', {})
        
        if not current_holdings:
            return 50  # Neutral diversification impact
            
        # Calculate diversification based on sector differences
        current_sectors = set(holding.get('sector', '') for holding in current_holdings.values())
        new_sector = data.sector
        
        if new_sector not in current_sectors:
            diversification_score = 80  # Adding new sector is good
        else:
            diversification_score = 30  # Same sector, less benefit
            
        return diversification_score
    
    def _store_analysis_result(self, result: Dict, user_profile: Dict):
        """Store analysis result in database"""
        cursor = self.db_connection.cursor()
        
        # Create a hash of the user profile for grouping
        profile_hash = hash(str(sorted(user_profile.items())))
        
        cursor.execute('''
            INSERT INTO analysis_results 
            (symbol, analysis_date, overall_score, risk_score, return_potential, 
             alignment_score, diversification_score, recommendation, confidence, user_profile_hash)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            result['symbol'], result['timestamp'], result['overall_score'], 
            result['risk_score'], result['return_potential'], result['alignment_score'],
            result['diversification_score'], result['recommendation'], 
            result['confidence'], str(profile_hash)
        ))
        
        self.db_connection.commit()
    
    def get_top_recommendations(self, user_profile: Dict, count: int = 10) -> List[Dict]:
        """Get top recommendations for a user profile"""
        # First run analysis if needed
        all_results = self.bulk_analyze(user_profile)
        
        # Return top recommendations
        return all_results[:count]
    
    def filter_by_criteria(self, results: List[Dict], filters: Dict) -> List[Dict]:
        """Filter results by various criteria"""
        filtered = []
        
        for result in results:
            include = True
            
            # Apply sector filter
            if 'sectors' in filters and result['sector'] not in filters['sectors']:
                include = False
                
            # Apply risk filter
            if 'max_risk' in filters and result['risk_score'] > filters['max_risk']:
                include = False
                
            # Apply minimum score filter
            if 'min_score' in filters and result['overall_score'] < filters['min_score']:
                include = False
                
            # Apply market cap filter
            if 'min_market_cap' in filters and result['market_cap'] < filters['min_market_cap']:
                include = False
                
            if include:
                filtered.append(result)
                
        return filtered


class AnalysisScheduler:
    """Handles scheduling and automation of analysis runs"""
    
    def __init__(self, analyzer: ScalableAnalyzer):
        self.analyzer = analyzer
        self.scheduled_runs = []
        
    async def run_scheduled_analysis(self, user_profiles: List[Dict], frequency_minutes: int = 60):
        """Run scheduled analysis for multiple user profiles"""
        while True:
            print(f"Running scheduled analysis for {len(user_profiles)} user profiles...")
            
            for i, profile in enumerate(user_profiles):
                print(f"Analyzing for user {i+1}/{len(user_profiles)}")
                try:
                    results = self.analyzer.bulk_analyze(profile)
                    print(f"Completed analysis for user {i+1}, found {len(results)} investments analyzed")
                except Exception as e:
                    print(f"Error analyzing for user {i+1}: {str(e)}")
            
            print(f"Waiting {frequency_minutes} minutes until next run...")
            await asyncio.sleep(frequency_minutes * 60)


def main():
    """Demonstrate scalable investment analysis"""
    print("Initializing Scalable Investment Analysis Framework...")
    
    # Initialize the analyzer
    analyzer = ScalableAnalyzer()
    
    # Define a sample user profile
    user_profile = {
        'risk_tolerance': 'moderate',
        'investment_timeline': 5,
        'financial_goals': 'Long-term wealth growth with moderate risk',
        'preferred_sectors': ['Technology', 'Healthcare'],
        'current_portfolio': {
            'SPY': {'weight': 0.6, 'sector': 'Technology'},
            'TLT': {'weight': 0.3, 'sector': 'Financial Services'}
        }
    }
    
    # Run bulk analysis
    print("\nRunning bulk analysis for sample universe of securities...")
    start_time = time.time()
    
    results = analyzer.bulk_analyze(user_profile)
    
    end_time = time.time()
    print(f"\nAnalysis completed in {end_time - start_time:.2f} seconds")
    print(f"Analyzed {len(results)} securities")
    
    # Display top recommendations
    print(f"\nTop 10 Recommendations:")
    print("-" * 100)
    
    for i, result in enumerate(results[:10], 1):
        print(f"{i:2d}. {result['symbol']:6s} - {result['recommendation']:10s} | "
              f"Score: {result['overall_score']:5.1f} | "
              f"Risk: {result['risk_score']:4.1f} | "
              f"Return: {result['return_potential']:5.2f}% | "
              f"Sector: {result['sector']}")
    
    # Demonstrate filtering capabilities
    print(f"\nFiltered results - Technology sector only:")
    tech_results = analyzer.filter_by_criteria(
        results, 
        {'sectors': ['Technology']}
    )[:5]
    
    for i, result in enumerate(tech_results, 1):
        print(f"{i}. {result['symbol']} - {result['recommendation']} (Score: {result['overall_score']:.1f})")
    
    # Show how to run for different user profiles
    print(f"\nDemonstrating analysis for different risk profiles:")
    
    risk_profiles = [
        {
            'risk_tolerance': 'conservative',
            'investment_timeline': 10,
            'financial_goals': 'Capital preservation with modest growth'
        },
        {
            'risk_tolerance': 'aggressive',
            'investment_timeline': 3,
            'financial_goals': 'High growth potential'
        }
    ]
    
    for i, profile in enumerate(risk_profiles, 1):
        print(f"\nProfile {i} ({profile['risk_tolerance']}):")
        profile_results = analyzer.bulk_analyze(profile)
        
        top_3 = profile_results[:3]
        for j, result in enumerate(top_3, 1):
            print(f"  {j}. {result['symbol']} - {result['recommendation']} (Score: {result['overall_score']:.1f})")


if __name__ == "__main__":
    main()