import React, { useEffect, useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { getPatient, getVisits, getInvoices, deletePatient } from '../services/api';
import { useAuth } from '../context/AuthContext';

interface Patient {
  id: number;
  patient_id: string;
  full_name: string;
  mobile: string;
  gender: string;
  age: number | null;
  blood_group: string | null;
  address: string | null;
  allergies: string | null;
  medical_conditions: string | null;
  current_medications: string | null;
  emergency_contact_name: string | null;
  emergency_contact_relation: string | null;
  emergency_contact_phone: string | null;
}

const PatientProfile: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { isAdmin } = useAuth();
  const [patient, setPatient] = useState<Patient | null>(null);
  const [visits, setVisits] = useState<any[]>([]);
  const [invoices, setInvoices] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this patient? This cannot be undone.')) {
      try {
        await deletePatient(parseInt(id!));
        navigate('/patients');
      } catch (error) {
        alert('Failed to delete patient. They may have visits or invoices.');
      }
    }
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [patientData, visitsData, invoicesData] = await Promise.all([
          getPatient(parseInt(id!)),
          getVisits(parseInt(id!)),
          getInvoices(parseInt(id!)),
        ]);
        setPatient(patientData);
        setVisits(visitsData);
        setInvoices(invoicesData);
      } catch (error) {
        console.error('Error fetching patient data:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, [id]);

  if (isLoading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
      </div>
    );
  }

  if (!patient) {
    return <div className="alert alert-danger">Patient not found</div>;
  }

  const totalBilled = invoices.reduce((sum, inv) => sum + inv.total, 0);
  const totalPaid = invoices.reduce((sum, inv) => sum + inv.paid, 0);
  const outstanding = totalBilled - totalPaid;

  return (
    <div>
      {/* Patient Header */}
      <div className="card">
        <div className="card-body flex gap-20" style={{ alignItems: 'center' }}>
          <div
            className="avatar"
            style={{ width: '80px', height: '80px', fontSize: '28px' }}
          >
            {patient.full_name.split(' ').map((n) => n[0]).join('').slice(0, 2)}
          </div>
          <div style={{ flex: 1 }}>
            <h2>{patient.full_name}</h2>
            <div className="text-muted">{patient.patient_id}</div>
            <div className="flex gap-20" style={{ marginTop: '10px' }}>
              <span>👤 {patient.gender}, {patient.age || '-'} years</span>
              <span>📱 {patient.mobile}</span>
              {patient.blood_group && <span>🩸 {patient.blood_group}</span>}
            </div>
          </div>
          <div className="flex gap-10">
            <Link to={`/patients/${id}/edit`} className="btn btn-outline">
              ✏️ Edit
            </Link>
            <Link to={`/patients/${id}/visit`} className="btn btn-primary">
              🩺 Start Consultation
            </Link>
            {isAdmin && (
              <button onClick={handleDelete} className="btn btn-danger">
                Delete
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Allergy Alert */}
      {patient.allergies && (
        <div className="alert alert-danger">
          <strong>⚠️ ALLERGIES:</strong> {patient.allergies}
        </div>
      )}

      <div className="grid-2">
        {/* Left Column */}
        <div>
          {/* Medical Info */}
          <div className="card">
            <div className="card-header">Medical Information</div>
            <div className="card-body">
              <div className="mb-10">
                <strong>Blood Group:</strong> {patient.blood_group || 'Not recorded'}
              </div>
              <div className="mb-10">
                <strong>Medical Conditions:</strong>
                <p className="text-muted">{patient.medical_conditions || 'None recorded'}</p>
              </div>
              <div>
                <strong>Current Medications:</strong>
                <p className="text-muted">{patient.current_medications || 'None recorded'}</p>
              </div>
            </div>
          </div>

          {/* Contact Info */}
          <div className="card">
            <div className="card-header">Contact Information</div>
            <div className="card-body">
              <div className="mb-10">
                <strong>Mobile:</strong> {patient.mobile}
              </div>
              <div className="mb-10">
                <strong>Address:</strong> {patient.address || 'Not recorded'}
              </div>
              {patient.emergency_contact_name && (
                <div>
                  <strong>Emergency Contact:</strong>
                  <p className="text-muted">
                    {patient.emergency_contact_name}
                    {patient.emergency_contact_relation && ` (${patient.emergency_contact_relation})`}
                    {patient.emergency_contact_phone && ` - ${patient.emergency_contact_phone}`}
                  </p>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Right Column */}
        <div>
          {/* Billing Summary */}
          <div className="card">
            <div className="card-header">Billing Summary</div>
            <div className="card-body">
              <div className="flex-between mb-10">
                <span>Total Billed</span>
                <strong>₹{totalBilled.toLocaleString()}</strong>
              </div>
              <div className="flex-between mb-10">
                <span>Total Paid</span>
                <strong className="text-success">₹{totalPaid.toLocaleString()}</strong>
              </div>
              <div className="flex-between">
                <span>Outstanding</span>
                <strong className={outstanding > 0 ? 'text-danger' : 'text-success'}>
                  ₹{outstanding.toLocaleString()}
                </strong>
              </div>
              {outstanding > 0 && (
                <Link
                  to={`/billing?patient_id=${id}`}
                  className="btn btn-primary btn-sm"
                  style={{ width: '100%', justifyContent: 'center', marginTop: '15px' }}
                >
                  Collect Payment
                </Link>
              )}
            </div>
          </div>

          {/* Recent Visits */}
          <div className="card">
            <div className="card-header">
              <span>Recent Visits</span>
              <span className="badge badge-primary">{visits.length}</span>
            </div>
            <div className="card-body" style={{ padding: 0 }}>
              {visits.length === 0 ? (
                <p className="text-center text-muted" style={{ padding: '20px' }}>
                  No visits yet
                </p>
              ) : (
                <table className="table">
                  <thead>
                    <tr>
                      <th>Date</th>
                      <th>Complaint</th>
                      <th></th>
                    </tr>
                  </thead>
                  <tbody>
                    {visits.slice(0, 5).map((visit) => (
                      <tr key={visit.id}>
                        <td>{new Date(visit.visit_date).toLocaleDateString()}</td>
                        <td>{visit.chief_complaint || '-'}</td>
                        <td>
                          <Link 
                            to={`/patients/${id}/visits/${visit.id}`} 
                            className="btn btn-sm btn-outline"
                          >
                            View
                          </Link>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PatientProfile;
