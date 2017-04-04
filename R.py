from rqalpha import run

config = {
    "base": {
        "run_id": "0002",
        "strategy_file": "rsi.py",#"buy_and_hold.py", #"pair_trading.py",
        "start_date": "2016-06-01",
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
        "sys_stock_realtime": {  # "simple_stock_realtime_trade":{
        "enabled": True,
        }
    },
}
    

'''
 "mod": {
     "rqalpha_mod_sys_stock_realtime": { #"simple_stock_realtime_trade":{
         "enabled": True,
     }

 },
 '''
#main.update_bundle()
run(config)
