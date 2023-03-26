#!/bin/bash

# Retrieve the current date and time
current_date=$(date +%Y-%m-%d\ %T)

# Retrieve the CAC40 Value
CAC40_value=$(wget -qO- https://www.tradingsat.com/cac-40-FR0003500008/ | sed -n 's/.*<span class="price">\([^<]*\)<\/span>.*/\1/p' | sed 's/&nbsp;/ /g')

# Remove space character from CAC40 value
CAC40_value=$(echo $CAC40_value | tr -d ' ')

# Use bc command to convert string to float
CACfloat=$(echo "scale=2; $CAC40_value" | bc 2>/dev/null)

# Check if bc command returned an error
if [ $? -ne 0 ]; then
  echo "Error: Unable to convert CAC40 value to float"
  exit 1
fi

# Save the Date and Value to a file
echo "$current_date,$CACfloat" >> CAC_values.txt

