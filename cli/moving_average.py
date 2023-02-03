def moving_average(data, days):
  data['MA ' + str(days)] = data['adjclose'].rolling(days).mean()
  return data
