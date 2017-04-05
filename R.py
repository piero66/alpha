from rqalpha import run

config = {
    "base": {
        "run_id": "0002",
        "strategy_file": "rsi.py",#"buy_and_hold.py", #"pair_trading.py",
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
    
#main.update_bundle()
run(config)
