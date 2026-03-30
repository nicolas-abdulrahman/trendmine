from pytrends.request import TrendReq
import pandas as pd

# hl: Language (Portuguese - Brazil)
# tz: Timezone offset (Brazil is generally 180 minutes or 3 hours behind UTC)
pytrends = TrendReq(hl='pt-BR', tz=180)

# Search term
kw_list = ["Carnaval"]

# geo='BR' targets the entire country of Brazil
pytrends.build_payload(kw_list, cat=0, timeframe='today 12-m', geo='BR')

# 1. Interest Over Time
data = pytrends.interest_over_time()
print("--- Interest Over Time in Brazil ---")
print(data.head())

# 2. Interest by Region (States of Brazil)
region_data = pytrends.interest_by_region(resolution='COUNTRY', inc_low_vol=True, inc_geo_code=True)
print("\n--- Interest by Brazilian State ---")
print(region_data.sort_values(by='Carnaval', ascending=False).head())