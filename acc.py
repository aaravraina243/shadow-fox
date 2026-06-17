import math
import statistics

def strategy_performance():
    print("===== Professional Trading Strategy Analyzer v3.1 (Fixed) =====\n")

    try:
        total_trades = int(input("Total number of trades: "))
        if total_trades <= 0:
            print("Total trades must be > 0.c  ")
            return

        wins = int(input("Number of winning trades: "))
        if wins < 0 or wins > total_trades:
            print("Invalid win count.")
            return

        losses = total_trades - wins
        avg_win = float(input("Average profit per winning trade: "))
        avg_loss = float(input("Average loss per losing trade (positive): "))

        print("\nEnter P/L for EACH trade (comma separated):")
        trade_results = list(map(float, input().split(",")))
        if len(trade_results) != total_trades:
            print("Mismatch in trade count!")
            return

        # Basic Metrics
        win_rate = wins / total_trades
        loss_rate = 1 - win_rate
        profit_factor = (wins * avg_win) / (losses * avg_loss) if losses > 0 else float("inf")
        expectancy = (win_rate * avg_win) - (loss_rate * avg_loss)
        rr_ratio = avg_win / avg_loss if avg_loss != 0 else float("inf")
        kelly = max(0, win_rate - (loss_rate / rr_ratio))

        # Win Rate Confidence Interval
        ci_low = max(0, win_rate - 1.96 * math.sqrt(win_rate * loss_rate / total_trades))
        ci_high = min(1, win_rate + 1.96 * math.sqrt(win_rate * loss_rate / total_trades))

        # Advanced Statistics
        mean_ret = statistics.mean(trade_results)
        stdev = statistics.pstdev(trade_results) if total_trades > 1 else 0

        sharpe = mean_ret / stdev if stdev > 0 else float("inf")

        # Downside volatility for Sortino
        neg_returns = [r for r in trade_results if r < 0]
        downside_dev = statistics.pstdev(neg_returns) if len(neg_returns) > 1 else 0
        sortino = mean_ret / downside_dev if downside_dev > 0 else float("inf")

        # Skew & Kurtosis (Fat-tail risk)
        skew = (sum((r - mean_ret)**3 for r in trade_results) / total_trades) / (stdev**3) if stdev > 0 else 0
        kurt = (sum((r - mean_ret)**4 for r in trade_results) / total_trades) / (stdev**4) if stdev > 0 else 0

        # Drawdown Metrics
        eq_curve = []
        running = 0
        peak = 0
        max_dd = 0

        for r in trade_results:
            running += r
            eq_curve.append(running)
            peak = max(peak, running)
            max_dd = max(max_dd, peak - running)

        calmar = (mean_ret / max_dd) if max_dd > 0 else float("inf")

        # Omega Ratio (threshold=0 = breakeven)
        good = sum(r for r in trade_results if r > 0)
        bad = -sum(r for r in trade_results if r < 0)
        omega = good / bad if bad > 0 else float("inf")

        # FIXED: Z-Score #1 - Profitability Test
        # Tests if average profit is significantly different from zero (breakeven)
        std_error_profit = stdev / math.sqrt(total_trades) if total_trades > 0 else 1
        z_score_profit = mean_ret / std_error_profit if std_error_profit > 0 else 0

        # FIXED: Z-Score #2 - Win Rate Test
        # Tests if win rate is significantly better than 50% (random chance)
        expected_win_rate = 0.5
        std_error_winrate = math.sqrt(expected_win_rate * (1 - expected_win_rate) / total_trades)
        z_score_winrate = (win_rate - expected_win_rate) / std_error_winrate if std_error_winrate > 0 else 0

        # Z-Score #3 - Runs Test (Consistency)
        # Tests if wins/losses are randomly distributed (no unusual streaks)
        wins_list = [1 if r > 0 else 0 for r in trade_results]
        runs = 1
        for i in range(1, len(wins_list)):
            if wins_list[i] != wins_list[i-1]:
                runs += 1

        n1 = sum(wins_list)
        n2 = len(wins_list) - n1
        expected_runs = (2 * n1 * n2 / total_trades) + 1 if total_trades > 0 else 0
        variance_runs = (2 * n1 * n2 * (2 * n1 * n2 - total_trades)) / (total_trades**2 * (total_trades - 1)) if total_trades > 1 else 1
        std_dev_runs = math.sqrt(variance_runs) if variance_runs > 0 else 1
        z_score_runs = (runs - expected_runs) / std_dev_runs if std_dev_runs > 0 else 0

        # Gain/Loss Ratio
        gain_loss_ratio = (avg_win / avg_loss) if avg_loss != 0 else float("inf")

        print("\n===== RESULTS =====")
        print(f"Win Rate: {win_rate*100:.2f}%")
        print(f"Profit Factor: {profit_factor:.2f}")
        print(f"Expectancy: {expectancy:.4f}")
        print(f"Risk-Reward: {rr_ratio:.2f}")
        print(f"Kelly %: {kelly*100:.2f}%")
        print(f"Win-Rate 95% CI: [{ci_low*100:.2f}%, {ci_high*100:.2f}%]")

        print("\n--- Volatility & Risk ---")
        print(f"Sharpe Ratio: {sharpe:.2f}")
        print(f"Sortino Ratio: {sortino:.2f}")
        print(f"Skewness: {skew:.2f}")
        print(f"Kurtosis: {kurt:.2f}")
        print(f"Max Drawdown: {max_dd:.2f}")
        print(f"Calmar Ratio: {calmar:.2f}")
        print(f"Omega Ratio: {omega:.2f}")
        print(f"Gain/Loss Ratio: {gain_loss_ratio:.2f}")

        print("\n--- Statistical Significance (Z-Scores) ---")
        print(f"Profitability Z-Score: {z_score_profit:.4f}")
        print(f"Win Rate Z-Score: {z_score_winrate:.4f}")
        print(f"Consistency Z-Score (Runs Test): {z_score_runs:.4f}")

        print("\n===== INTERPRETATION =====")

        # Profitability
        if expectancy > 0:
            print("✔ Positive expectancy → profitable edge.")
        else:
            print("⚠ Negative expectancy → long-term losing system.")

        # Statistical Significance - Profitability
        print("\n--- Statistical Confidence ---")
        if z_score_profit > 2.58:
            print("🔥 Highly significant profitability (99%+ confidence, Z > 2.58)")
        elif z_score_profit > 1.96:
            print("✔ Statistically significant profitability (95% confidence, Z > 1.96)")
        elif z_score_profit > 1.64:
            print("✔ Likely profitable (90% confidence, Z > 1.64)")
        elif z_score_profit > 0:
            print(f"⚠ Profitability not yet proven (Z = {z_score_profit:.2f})")
            print(f"   Need ~{int((1.96 / z_score_profit)**2 * total_trades) - total_trades} more trades for 95% confidence")
        else:
            print("⚠ No evidence of profitability")

        # Win Rate Significance
        if z_score_winrate > 1.96:
            print(f"✔ Win rate ({win_rate*100:.1f}%) significantly > 50% (95% confidence)")
        elif z_score_winrate > 1.64:
            print(f"✔ Win rate ({win_rate*100:.1f}%) likely > 50% (90% confidence)")
        else:
            print(f"⚠ Win rate not statistically proven above 50%")

        # Consistency Check
        if abs(z_score_runs) < 1.96:
            print("✔ Win/loss distribution is random (no unusual streaking)")
        else:
            print("⚠ Unusual streaking pattern detected - check for time-varying edge")

        # Risk-adjusted rating
        print("\n--- Risk Assessment ---")
        if sharpe > 2: 
            print("🔥 Excellent risk-adjusted returns (Sharpe > 2)")
        elif sharpe > 1: 
            print("✔ Good risk-adjusted returns (Sharpe > 1)")
        elif sharpe > 0:
            print("⚠ Poor risk-adjusted performance (Sharpe < 1)")
        else:
            print("⚠ Negative risk-adjusted returns")

        # Tail risk
        if kurt > 3: 
            print("⚠ High kurtosis → risk of black-swan losses!")
        if skew < -0.5: 
            print("⚠ Negative skew → occasional large losses likely")
        elif skew > 0.5:
            print("✔ Positive skew → occasional large wins")

        # Drawdown control
        if max_dd > abs(mean_ret) * 5:
            print(f"⚠ Drawdown risk very high! (DD = {max_dd:.0f}, Avg = {mean_ret:.0f})")
        elif max_dd > abs(mean_ret) * 3:
            print(f"⚠ Drawdown risk elevated (DD = {max_dd:.0f}, Avg = {mean_ret:.0f})")

        # Position sizing warning
        if kelly > 0.15:
            print(f"⚠ Kelly % ({kelly*100:.1f}%) is high - use 1/4 Kelly = {kelly*25:.1f}% max")

        print("\n--- Summary ---")
        if z_score_profit > 1.96 and sharpe > 1:
            print("✅ Strong statistical edge with good risk management")
        elif z_score_profit > 1.64:
            print("✅ Promising edge - continue trading and collecting data")
        else:
            print("⚠ Edge not yet proven - reduce position size and gather more data")

        print("\nTip: Aim for Z > 1.96 (95% confidence) with 100+ trades for robust validation.\n")

    except Exception as e:
        print("Error:", e)


strategy_performance()