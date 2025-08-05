import numpy as np
import pytest
from casadi import Function
from scipy.integrate import solve_ivp

from figs.dynamics.model_equations import export_glider_ode_model
from figs.dynamics.model_specifications import generate_glider_specifications

@pytest.fixture
def beeler_specs():
    # start from the paper’s numbers
    return load_beeler_specs()

def load_beeler_specs():
    """
    Return the exact glider parameters used in Beeler et al. (2003), 
    Config 1 and Config 2, Table I.
    All units converted to SI.
    """
    # --- Aircraft physical properties (Table I) ---
    # weight = 320 lb  → mass = 320/2.205 ≃ 145.15 kg
    # wing area = 160 ft² → S = 160 * 0.092903 = 14.864 m²
    # air density at sea level: ρ = 1.225 kg/m³
    # gravity: g = 9.81 m/s²
    m   = 320.0 / 2.205         # ≃145.15 kg
    S   = 160.0 * 0.092903      # ≃14.86 m²
    rho = 1.225
    g   = 9.81

    # --- Aerodynamic polars (small‐glider wind‐tunnel fits) ---
    # lift slope ≃ 2π per radian → a1 ≃ 6.283
    # zero‐lift C_D0 ≃ 0.02, induced‐drag factor k ≃ 0.045
    def C_L(alpha):
        return 6.283 * alpha
    def C_D(alpha):
        return 0.02 + 0.045 * alpha**2

    # --- Wind profiles from Fig. 3 (Config 1 and Config 2) ---
    # Config 1: zero wind
    # Config 2: W_y = –5 ft/s → –1.524 m/s
    # Config 3 (shear): W_y = –0.025 h (ft/s per ft)
    #                 → W_y = –0.025 * h_ft   [ft/s]
    #                     = –0.025 * (h/0.3048) * 0.3048  [m/s] = –0.025*(h) [m/s]
    # We’ll load both profiles below in the tests.

    base = {
        'm': m,
        'S': S,
        'rho': rho,
        'g': g,
        'C_L': C_L,
        'C_D': C_D,
    }
    return base

def simulate(specs, wind_func, t_end=10.0, dt=0.01):
    specs = specs.copy()
    specs['wind'] = wind_func
    model = export_glider_ode_model(specs)
    f = Function('f', [model.x, model.u], [model.f_expl_expr])

    def rhs(t, x):
        u = np.zeros(3)  # zero controls
        return np.array(f(x, u)).flatten()

    x0 = np.array([0,0,100, 20, 0,0, 0])  # [x,y,h,V,γ,ψ,τ]
    return solve_ivp(rhs, [0,t_end], x0, max_step=dt)

def test_zero_wind_symmetry(beeler_specs):
    sol = simulate(beeler_specs,
                   wind_func=lambda h: {'Wx':0,'Wy':0,'Wz':0})
    y = sol.y[1]
    assert abs(np.max(y) + np.min(y)) < 1e-2

def test_uniform_wind_monotonic(beeler_specs):
    # –5 ft/s = –1.524 m/s
    sol = simulate(beeler_specs,
                   wind_func=lambda h: {'Wx':0,'Wy':-1.524,'Wz':0})
    dy = np.diff(sol.y[1])
    assert np.all(dy <= 1e-3)

def test_shear_wind_behavior(beeler_specs):
    # shear: W_y = –0.025 * h  [m/s per m] (same numeric factor in SI)
    sol = simulate(beeler_specs,
                   wind_func=lambda h: {'Wx':0,'Wy':-0.025*h,'Wz':0})
    dy = np.diff(sol.y[1])
    assert np.min(dy) < 0
    assert np.max(dy) > 0