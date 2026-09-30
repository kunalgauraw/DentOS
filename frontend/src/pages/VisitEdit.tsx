import React, { useEffect, useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { getPatient, getVisit, updateVisit, getPrescriptions } from '../services/api';

interface Medicine {
  name: string;
  dosage: string;
  frequency: string;
  duration: string;
  instructions: string;
}

const VisitEdit: React.FC = () => {
  const { patientId, visitId } = useParams<{ patientId: string; visitId: string }>();
  const navigate = useNavigate();
  const [patient, setPatient] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState('');

  // Visit data
  const [visitData, setVisitData] = useState({
    bp: '',
    blood_sugar: '',
    pulse: '',
    chief_complaint: '',
    examination_findings: '',
    advice: '',
    follow_up_date: '',
    follow_up_reason: '',
  });

  // Check if visit is from today
  const isToday = (dateString: string) => {
    const visitDate = new Date(dateString);
    const today = new Date();
    return visitDate.toDateString() === today.toDateString();
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [patientData, visitDataRes] = await Promise.all([
          getPatient(parseInt(patientId!)),
          getVisit(parseInt(visitId!)),
        ]);
        
        setPatient(patientData);
        
        // Check if visit is from today
        if (!isToday(visitDataRes.visit_date)) {
          setError('Cannot edit visits from previous days');
          setIsLoading(false);
          return;
        }
        
        setVisitData({
          bp: visitDataRes.bp || '',
          blood_sugar: visitDataRes.blood_sugar || '',
          pulse: visitDataRes.pulse || '',
          chief_complaint: visitDataRes.chief_complaint || '',
          examination_findings: visitDataRes.examination_findings || '',
          advice: visitDataRes.advice || '',
          follow_up_date: visitDataRes.follow_up_date || '',
          follow_up_reason: visitDataRes.follow_up_reason || '',
        });
      } catch (error) {
        console.error('Error fetching data:', error);
        setError('Failed to load visit data');
      } finally {
        setIsLoading(false);
      }
    };
    fetchData();
  }, [patientId, visitId]);

  const handleVisitChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setVisitData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSave = async () => {
    setError('');
    
    if (!visitData.chief_complaint.trim()) {
      setError('Please enter the chief complaint');
      return;
    }
    
    setIsSaving(true);

    try {
      await updateVisit(parseInt(visitId!), {
        ...visitData,
        follow_up_date: visitData.follow_up_date || null,
      });

      navigate(`/patients/${patientId}/visits/${visitId}`);
    } catch (err: any) {
      console.error('Save error:', err);
      setError(err.response?.data?.detail || err.message || 'Failed to save changes');
    } finally {
      setIsSaving(false);
    }
  };

  if (isLoading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
      </div>
    );
  }

  if (error && !patient) {
    return <div className="alert alert-danger">{error}</div>;
  }

  if (!patient) {
    return <div className="alert alert-danger">Patient not found</div>;
  }

  return (
    <div>
      {/* Header */}
      <div className="page-header flex-between">
        <h1 className="page-title">Edit Consultation</h1>
        <Link to={`/patients/${patientId}/visits/${visitId}`} className="btn btn-outline">
          Cancel
        </Link>
      </div>

      {/* Patient Header */}
      <div className="card">
        <div className="card-body flex gap-20" style={{ alignItems: 'center' }}>
          <div className="avatar" style={{ width: '50px', height: '50px', fontSize: '18px' }}>
            {patient.full_name.split(' ').map((n: string) => n[0]).join('').slice(0, 2)}
          </div>
          <div>
            <strong>{patient.full_name}</strong>
            <div className="text-muted">
              {patient.patient_id} | {patient.gender}, {patient.age || '-'} yrs
            </div>
          </div>
        </div>
      </div>

      {error && <div className="alert alert-danger">{error}</div>}

      {/* Vitals Section */}
      <div className="card">
        <div className="card-header">Vitals</div>
        <div className="card-body">
          <div className="form-row">
            <div className="form-group">
              <label className="form-label">BP (mmHg)</label>
              <input
                type="text"
                name="bp"
                className="form-control"
                placeholder="e.g., 120/80"
                value={visitData.bp}
                onChange={handleVisitChange}
              />
            </div>
            <div className="form-group">
              <label className="form-label">Blood Sugar (mg/dL)</label>
              <input
                type="text"
                name="blood_sugar"
                className="form-control"
                placeholder="e.g., 110"
                value={visitData.blood_sugar}
                onChange={handleVisitChange}
              />
            </div>
            <div className="form-group">
              <label className="form-label">Pulse (bpm)</label>
              <input
                type="text"
                name="pulse"
                className="form-control"
                placeholder="e.g., 72"
                value={visitData.pulse}
                onChange={handleVisitChange}
              />
            </div>
          </div>
        </div>
      </div>

      {/* Clinical Notes Section */}
      <div className="card">
        <div className="card-header">Clinical Notes</div>
        <div className="card-body">
          <div className="form-group">
            <label className="form-label">
              Chief Complaint <span className="required">*</span>
            </label>
            <textarea
              name="chief_complaint"
              className="form-control"
              placeholder="What brings the patient today?"
              value={visitData.chief_complaint}
              onChange={handleVisitChange}
              rows={2}
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label">Examination & Findings</label>
            <textarea
              name="examination_findings"
              className="form-control"
              placeholder="Clinical examination findings, diagnosis..."
              value={visitData.examination_findings}
              onChange={handleVisitChange}
              rows={3}
            />
          </div>

          <div className="form-group">
            <label className="form-label">Advice</label>
            <textarea
              name="advice"
              className="form-control"
              placeholder="Treatment advice, instructions..."
              value={visitData.advice}
              onChange={handleVisitChange}
              rows={2}
            />
          </div>
        </div>
      </div>

      {/* Follow-up Section */}
      <div className="card">
        <div className="card-header">Follow-up (Optional)</div>
        <div className="card-body">
          <div className="form-row">
            <div className="form-group">
              <label className="form-label">Follow-up Date</label>
              <input
                type="date"
                name="follow_up_date"
                className="form-control"
                value={visitData.follow_up_date}
                onChange={handleVisitChange}
              />
            </div>
            <div className="form-group">
              <label className="form-label">Reason</label>
              <input
                type="text"
                name="follow_up_reason"
                className="form-control"
                placeholder="e.g., Review, Next session"
                value={visitData.follow_up_reason}
                onChange={handleVisitChange}
              />
            </div>
          </div>
        </div>
      </div>

      <p className="text-muted" style={{ fontSize: '12px', marginBottom: '10px' }}>
        Note: Prescription and billing cannot be edited after creation.
      </p>

      {/* Actions */}
      <div className="flex gap-10">
        <button
          type="button"
          className="btn btn-secondary"
          onClick={() => navigate(`/patients/${patientId}/visits/${visitId}`)}
        >
          Cancel
        </button>
        <button
          type="button"
          className="btn btn-primary"
          onClick={handleSave}
          disabled={isSaving}
        >
          {isSaving ? 'Saving...' : 'Save Changes'}
        </button>
      </div>
    </div>
  );
};

export default VisitEdit;
