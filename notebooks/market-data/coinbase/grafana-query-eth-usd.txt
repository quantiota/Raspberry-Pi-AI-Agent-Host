SELECT 
    timestamp,
    first(price) AS open,
    last(price) AS close,
    first(size) AS vopen,
    last(size) AS vclose,
    2*pi()*(last(size) - first(size))/first(size)  AS percentage_change,
    min(price),
    max(price),
    sum(size) AS volume,
    cos(sum(size)) AS cos_volume
FROM trades
WHERE symbol = 'ETH-USD' AND timestamp > dateadd('d', -1, now())
SAMPLE BY 1T ALIGN TO CALENDAR;  
