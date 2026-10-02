import numpy as np
from aircraft.Wing import Wing

def test_get_lift_coe_interpolation():#testing practice(useless)
    wing = Wing(
        10, 
        "NACA2412", 
        [30.0, 0.0], 
        0
        )
    
    AoA = 15.25
    
    lift_coe = wing.get_lift_coe(AoA)
    
    expected = 1.36875

    
    np.testing.assert_allclose(lift_coe, expected)