import pytest

from hot_tub import read


def test_read_thermal_bath():
    path = "C:/Users/jarlathd/source/product_data/grr_data/I310001EN_GRR-A0_PDE-PG_10-units_V=0.xlsx"
    info, summary = read.read_thermal_bath(path)
    info.to_html('thermal_bath_info')
    summary.to_html('thermal_bath_summary')

    #equation_df = read.extract_dataframe(summary, 'Diode Equation Per Sourcing Current')
    #two_current = read.extract_dataframe(summary, '2-Currents')
    three_current = read.extract_dataframe(summary, '3-Currents')
    
    ideality = read.get_ncurrent_ideality(three_current, 'GPIO', 80)
    return ideality

output = test_read_thermal_bath()
print(output)
print(type(output))
