from fastapi import FastAPI
import requests

app = FastAPI()

USD_CNY_URL = "https://fx.cmbchina.com/api/v1/fx/rate"
GOLD_URL = "https://data-asg.goldprice.org/dbXRates/USD"

def get_usd_to_cny():
    url = "https://fx.cmbchina.com/api/v1/fx/rate"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
    }
    resp = requests.get(url, headers=headers)
    print(resp.text)  # 🔹 先打印看看返回了什么
    data = resp.json()
    body = data.get("body", [])
    for item in body:
        if item.get("ccyNbr") == "美元":
            # ⚠️ 转成 float
            return float(item.get("rtbBid")) / 100
    raise RuntimeError("未找到美元汇率")

def convert_ny_to_beijing(ny_str):
    from datetime import datetime
    import pytz
    # 去掉th/NY
    clean_str = ny_str.replace("th", "").replace(" NY", "")
    dt = datetime.strptime(clean_str, "%b %d %Y, %I:%M:%S %p")
    ny_tz = pytz.timezone("America/New_York")
    bj_tz = pytz.timezone("Asia/Shanghai")
    dt_ny = ny_tz.localize(dt)
    dt_bj = dt_ny.astimezone(bj_tz)
    return dt_bj.strftime("%Y-%m-%d %H:%M:%S")

@app.get("/rPrice")
def gold_price():
    usd_to_cny = get_usd_to_cny()
    resp = requests.get(GOLD_URL)
    data = resp.json()
    item = data["items"][0]
    xau_usd = item["xauPrice"]
    cny_per_gram = xau_usd * usd_to_cny / 31.1034768
    beijing = convert_ny_to_beijing(data["date"])
    return {
        "usdPerOunce": xau_usd,
        "cnyPerGram": round(cny_per_gram, 4),
        "beijingTime": beijing
    }