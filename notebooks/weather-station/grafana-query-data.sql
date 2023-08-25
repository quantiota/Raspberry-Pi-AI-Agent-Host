
-- Retrieve the timestamp and data values: temerature, humidity, pressure, iaq

SELECT
    timestamp,        -- Select the timestamp of the data
    data      -- Select the temperature value
FROM  
    weather_data      -- From the 'weather_data' table
WHERE 
    timestamp > dateadd('d', -1, now()); -- Only select data from the past 24 hours