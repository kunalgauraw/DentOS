import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import PatientForm from '../pages/PatientForm';

// Mock the API
vi.mock('../services/api', () => ({
  createPatient: vi.fn(),
}));

const renderPatientForm = () => {
  return render(
    <BrowserRouter>
      <PatientForm />
    </BrowserRouter>
  );
};

describe('Patient Registration Form', () => {
  it('renders page title', () => {
    renderPatientForm();
    
    expect(screen.getByText(/new patient registration/i)).toBeInTheDocument();
  });

  it('renders required field labels', () => {
    renderPatientForm();
    
    expect(screen.getByText(/full name/i)).toBeInTheDocument();
    expect(screen.getByText(/mobile/i)).toBeInTheDocument();
    expect(screen.getByText(/gender/i)).toBeInTheDocument();
  });

  it('renders optional field labels', () => {
    renderPatientForm();
    
    expect(screen.getByText(/age/i)).toBeInTheDocument();
    expect(screen.getByText(/blood group/i)).toBeInTheDocument();
  });

  it('has a submit button', () => {
    renderPatientForm();
    
    expect(screen.getByRole('button', { name: /save/i })).toBeInTheDocument();
  });

  it('allows entering patient details', () => {
    renderPatientForm();
    
    const nameInput = screen.getByPlaceholderText(/full name/i);
    const mobileInput = screen.getByPlaceholderText(/mobile/i);
    
    fireEvent.change(nameInput, { target: { value: 'Rahul Kumar' } });
    fireEvent.change(mobileInput, { target: { value: '9876543210' } });
    
    expect(nameInput).toHaveValue('Rahul Kumar');
    expect(mobileInput).toHaveValue('9876543210');
  });
});
