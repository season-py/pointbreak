#!/usr/bin/env python
# coding=utf-8
from datetime import datetime
from settings import SETTINGS
from decimal import Decimal
from pony.orm import Database, Set, Required, Optional, PrimaryKey

db = Database()
db.bind('sqlite', SETTINGS['database'], create_db=True)

class Coin(db.Entity):
    symbol = Required(str, unique=True)
    full_name = Optional(str)
    description = Optional(str)
    rank = Optional(int, default=0)
    is_valid = Required(int, default=1)
    ico_at = Optional(datetime)
    created_at = Required(datetime, sql_default='CURRENT_TIMESTAMP')
    marketcap_shots = Set('CoinMarketCapShot')
    yunbi_shots = Set('CoinYunbiShot')

class CoinMarketCapShot(db.Entity):
    coin = Required(Coin)
    price = Optional(Decimal)
    volume = Optional(Decimal)
    market_cap = Optional(Decimal)
    shotted_at = Required(datetime, sql_default='CURRENT_TIMESTAMP')
    PrimaryKey(coin, shotted_at)

class CoinYunbiShot(db.Entity):
    coin = Required(Coin)
    price = Optional(Decimal)
    volume = Optional(Decimal)
    market_cap = Optional(Decimal)
    shotted_at = Required(datetime, sql_default='CURRENT_TIMESTAMP')
    PrimaryKey(coin, shotted_at)

db.generate_mapping(create_tables=True)
