if __name__ == "__main__":
    asyncio.run(main())
  import ccxt, asyncio, random
from telethon import TelegramClient
from datetime import datetime
import pandas as pd

api_id = '29445588'
api_hash = '725d4da07b094c43bdfaaa7a443b81ef'
bot_token = '7930060470:AAGSsve-C3N6owooHiCijG9Tm_1Nz3iZ8Zc'
channel = '@LAAC97'

symbols = []
exchange = ccxt.binance()
markets = exchange.load_markets()
for s in markets:
    if '/USDT' in s and ':' not in s:
        symbols.append(s)
symbols = symbols[:60]

client = TelegramClient('bot', api_id, api_hash)

# ------------------ نماذج كلاسيكية ------------------ #
def detect_double_top(df):
    if len(df) < 10:
        return False
    highs = df['high']
    if highs[-3] < highs[-5] and abs(highs[-5] - highs[-1]) / highs[-5] < 0.01:
        return 'Double Top'
    return False

def detect_double_bottom(df):
    if len(df) < 10:
        return False
    lows = df['low']
    if lows[-3] > lows[-5] and abs(lows[-5] - lows[-1]) / lows[-5] < 0.01:
        return 'Double Bottom'
    return False

# المزيد من النماذج لاحقاً...

async def send_trade(symbol, direction, entry, sl, targets, pattern):
    message = f"""꧁༺ 𝓢𝓒𝓐𝓛𝓟𝓘𝓝𝓖 300 ༻꧂\n\n✬S◦C°A˚L°P◦I... {symbol} ...N◦G°3˚0°0◦0✬\n𝓓𝓲𝓻𝓮𝓬𝓽𝓲𝓸𝓷 : {direction}\nLeverage : Cross 25x\n★ Entry : {entry} ★\n\n🔥Stoploss : {sl}🔥\n\nPattern: {pattern}\n\nミ★ SCALPING ★彡\nTarget 1 - {targets[0]}\nTarget 2 - {targets[1]}\nTarget 3 - {targets[2]}\nTarget 4 - {targets[3]}\n"""
    await client.send_message(channel, message)

async def main():
    await client.start(bot_token=bot_token)
    for symbol in symbols:
        ohlcv = exchange.fetch_ohlcv(symbol, '1m', limit=50)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        pattern = detect_double_top(df) or detect_double_bottom(df)
        if pattern:
            entry = df['close'].iloc[-1]
            direction = 'SELL' if 'Top' in pattern else 'BUY'
            sl = round(entry * (0.97 if direction == 'BUY' else 1.03), 4)
            targets = [round(entry * (1 + 0.01 * i), 4) if direction == 'BUY' else round(entry * (1 - 0.01 * i), 4) for i in range(1, 5)]
            await send_trade(symbol, direction, entry, sl, targets, pattern)
        await asyncio.sleep(3)

asyncio.run(main())
