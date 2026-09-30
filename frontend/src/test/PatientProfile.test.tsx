import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import PatientProfile from '../pages/PatientProfile';

vi.mock('../services/api', () => ({
  getPatient: vi.fn().mockResolvedValue({
    id: 1, patient_id: 'PAT-000001', full_name: 'Test Patient', mobile: '9876543210',
    gender: 'female', age: 30, blood_group: 'A+', address: null, allergies: null,
    medical_conditions: null, current_medications: null,
    emergency_contact_name: null, emergency_contact_relation: null, emergency_contact_phone: null,
  }),
  getVisits: vi.fn().mockResolvedValue([]),
  getInvoices: vi.fn().mockResolvedValue([]),
  deletePatient: vi.fn(),
}));

const mockAuth = { isAdmin: false };
vi.mock('../context/AuthContext', () => ({
  useAuth: () => mockAuth,
}));

const renderProfile = () =>
  render(
    <MemoryRouter initialEntries={['/patients/1']}>
      <Routes>
        <Route path="/patients/:id" element={<PatientProfile />} />
      </Routes>
    </MemoryRouter>
  );

describe('Patient Profile - role based actions', () => {
  beforeEach(() => { mockAuth.isAdmin = false; });

  it('hides Delete for non-admin users', async () => {
    renderProfile();
    expect(await screen.findByText('Test Patient')).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /delete/i })).not.toBeInTheDocument();
    expect(screen.getByRole('link', { name: /edit/i })).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /start consultation/i })).toBeInTheDocument();
  });

  it('shows Delete for admin users', async () => {
    mockAuth.isAdmin = true;
    renderProfile();
    expect(await screen.findByText('Test Patient')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /delete/i })).toBeInTheDocument();
  });
});
