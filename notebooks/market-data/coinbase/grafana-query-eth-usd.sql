SELECT 
    timestamp,
    first(price) AS ETH
FROM trades
WHERE symbol = 'ETH-USD'  AND timestamp > dateadd('d', -1, now())
SAMPLE BY 1s ALIGN TO CALENDAR;  


SELECT 
    timestamp,
    first(price) AS BTC
FROM trades
WHERE symbol = 'BTC-USD'  AND timestamp > dateadd('d', -1, now())
SAMPLE BY 1s ALIGN TO CALENDAR;  


SELECT 
    timestamp,
    sum(size) AS VOLUME
FROM trades
WHERE symbol = 'ETH-USD'  AND timestamp > dateadd('d', -1, now())
SAMPLE BY 1s ALIGN TO CALENDAR;  