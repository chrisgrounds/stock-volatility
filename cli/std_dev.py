from average import average
import math 

def std_dev(vols):
  mean = average(vols)
  deviations = []

  for vol in vols:
    deviation = vol - mean
    deviations.append(deviation * deviation)

  sum_of_squares = sum(deviations)
  variance = sum_of_squares / len(vols)

  return round(math.sqrt(variance), 2)
