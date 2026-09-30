import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import PatientForm from '../pages/PatientForm';
import * as api from '../services/api';

vi.mock('../services/api', () => ({
  createPatient: vi.fn(),
  checkMobile: vi.fn().mockResolvedValue([]),
}));

const mockNavigate = vi.fn();
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual<typeof import('react-router-dom')>('react-router-dom');
  return { ...actual, useNavigate: () => mockNavigate };
});

const renderPatientForm = () =>
  render(
    <BrowserRouter>
      <PatientForm />
    </BrowserRouter>
  );

const fill = (placeholder: RegExp, value: string) =>
  fireEvent.change(screen.getByPlaceholderText(placeholder), { target: { value } });

describe('Patient Registration Form', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders required fields and submit button', () => {
    renderPatientForm();
    expect(screen.getByText(/new patient registration/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/full name/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/mobile/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /save/i })).toBeInTheDocument();
  });

  it('rejects a mobile number that is not 10 digits', async () => {
    renderPatientForm();
    fill(/full name/i, 'Rahul Kumar');
    fill(/mobile/i, '12345');
    fill(/age/i, '30');
    fireEvent.click(screen.getByRole('button', { name: /save/i }));

    expect(await screen.findByText(/exactly 10 digits/i)).toBeInTheDocument();
    expect(api.createPatient).not.toHaveBeenCalled();
  });

  it('requires age', async () => {
    renderPatientForm();
    fill(/full name/i, 'Rahul Kumar');
    fill(/mobile/i, '9876543210');
    // bypass the browser's own `required` check to exercise our validator
    fireEvent.submit(screen.getByRole('button', { name: /save/i }).closest('form')!);

    expect(await screen.findByText(/age is required/i)).toBeInTheDocument();
    expect(api.createPatient).not.toHaveBeenCalled();
  });

  it('submits normalised data and navigates to the new profile', async () => {
    vi.mocked(api.createPatient).mockResolvedValue({ id: 42 });
    renderPatientForm();
    fill(/full name/i, 'Rahul Kumar');
    fill(/mobile/i, '9876543210');
    fill(/age/i, '30');
    fireEvent.click(screen.getByRole('button', { name: /save/i }));

    await waitFor(() => expect(api.createPatient).toHaveBeenCalledTimes(1));
    const payload = vi.mocked(api.createPatient).mock.calls[0][0];
    expect(payload).toMatchObject({ full_name: 'Rahul Kumar', mobile: '9876543210', age: 30, gender: 'male' });
    expect(mockNavigate).toHaveBeenCalledWith('/patients/42');
  });

  it('warns (but does not block) when the mobile is already registered', async () => {
    vi.mocked(api.checkMobile).mockResolvedValue([{ id: 7, full_name: 'Sita Devi', patient_id: 'PAT-000007' }]);
    renderPatientForm();
    fill(/mobile/i, '9876543210');
    fireEvent.blur(screen.getByPlaceholderText(/mobile/i));

    expect(await screen.findByText(/already registered/i)).toBeInTheDocument();
    expect(screen.getByText(/Sita Devi/)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /save/i })).not.toBeDisabled();
  });

  it('shows the server validation message on 422', async () => {
    vi.mocked(api.createPatient).mockRejectedValue({
      response: { data: { detail: [{ msg: 'Value error, Either age or date of birth is required' }] } },
    });
    renderPatientForm();
    fill(/full name/i, 'Rahul Kumar');
    fill(/mobile/i, '9876543210');
    fill(/age/i, '30');
    fireEvent.click(screen.getByRole('button', { name: /save/i }));

    expect(await screen.findByText(/either age or date of birth is required/i)).toBeInTheDocument();
  });
});
