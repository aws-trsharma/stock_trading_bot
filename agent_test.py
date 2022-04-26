import datetime

from polygon import RESTClient

def ts_to_datetime(ts) -> str:
    return datetime.datetime.fromtimestamp(ts / 1000.0).strftime('%Y-%m-%d %H:%M')

def main():
    key = "rydZhCt3V32JH6CH3zkO856yVvr1HZoz" #Polygon key Free
    with RESTClient(key) as client:
        from_ = "2022-04-01"
        to = "2022-04-18"

        resp = client.stocks_equities_daily_open_close("AAPL", "2022-04-16")
        print(f"On: {resp.from_} Apple opened at {resp.open} and closed at {resp.close}")

        #resp = client.stocks_equities_daily_open_close("AAPL", 1, "day", from_, to, unadjusted=False)


        #print(f"Minute aggregates for {resp.ticker} between {from_} and {to}.")

        #for result in resp.results:
            #dt = ts_to_datetime(result["t"])
            #print(f"{dt}\n\tO: {result['o']}\n\tH: {result['h']}\n\tL: {result['l']}\n\tC: {result['c']} ")

if __name__ == '__main__':
    main()


