-- Retrieve the timestamp and data values: latitude, longitude

SELECT
    timestamp,        -- Select the timestamp of the data
    data              -- Select the data value
FROM  
    gps_data      -- From the 'gps_data' table
WHERE 
    timestamp > dateadd('d', -1, now()); -- Only select data from the past 24 hours
