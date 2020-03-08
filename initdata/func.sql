CREATE OR REPLACE FUNCTION ceil_minute(TIMESTAMP WITH TIME ZONE, INTERVAL)
RETURNS TIMESTAMP WITH TIME ZONE AS $$
  SELECT date_trunc('hour', $1) + $2 * ceil(date_part('minute', $1) / (to_char($2, 'MI')::integer * 1.0))
$$ LANGUAGE SQL;

CREATE OR REPLACE FUNCTION floor_minute(TIMESTAMP WITH TIME ZONE, INTERVAL)
RETURNS TIMESTAMP WITH TIME ZONE AS $$
  SELECT date_trunc('hour', $1) + $2 * floor(date_part('minute', $1) / (to_char($2, 'MI')::integer * 1.0))
$$ LANGUAGE SQL;
