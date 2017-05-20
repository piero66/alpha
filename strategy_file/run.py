from rqalpha import run
import time
config = {
    "base": {
        "run_id": "0031",
        "strategy_file": "strategy_t.py",#"buy_and_hold.py", #"pair_trading.py",
        "strategy_type": "stock",
        "stock_starting_cash": 10000000,
        "run_type": "p",
        "frequency": "1m",
        "data_bundle_path": ".rqalpha/bundle/"
    },
    "extra": {
        "log_level": "verbose",
    },
    "mod": {
        "sys_stock_realtime": {
        "enabled": True,
        }
    },
}


while True:
    try:
        run(config)
        time.sleep(100)
    except Exception as e:
        print('something error')
