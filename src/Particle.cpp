// CSC Latin America 2026 - Particle class implementation
#include "Particle.hpp"
#include <cmath>
#include <limits>

namespace csc2026 {

Particle::Particle(double px, double py, double pz, double mass)
    : m_px(px), m_py(py), m_pz(pz), m_mass(mass) {}

double Particle::eta() const {
    double p_total = p();
    if (p_total == 0.0) return 0.0;
    return 0.5 * std::log((p_total + m_pz) / (p_total - m_pz));
}

Particle Particle::operator+(const Particle& other) const {
    double new_px = m_px + other.m_px;
    double new_py = m_py + other.m_py;
    double new_pz = m_pz + other.m_pz;
    double e1 = energy();
    double e2 = other.energy();
    double e_total = e1 + e2;
    double p_total_sq = new_px * new_px + new_py * new_py + new_pz * new_pz;
    double new_mass = std::sqrt(std::max(0.0, e_total * e_total - p_total_sq));
    return Particle(new_px, new_py, new_pz, new_mass);
}

double invariantMass(const Particle& p1, const Particle& p2) {
    Particle combined = p1 + p2;
    return combined.mass();
}

} // namespace csc2026
