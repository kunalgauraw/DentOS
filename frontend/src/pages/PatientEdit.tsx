import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { getPatient, updatePatient } from '../services/api';
import { apiErrorMessage } from './PatientForm';

const PatientEdit: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState('');

  const [formData, setFormData] = useState({
    full_name: '',
    mobile: '',
    gender: 'male',
    age: '',
    blood_group: '',
    address: '',
    allergies: '',
    medical_conditions: '',
    current_medications: '',
    emergency_contact_name: '',
    emergency_contact_relation: '',
    emergency_contact_phone: '',
  });

  useEffect(() => {
    const fetchPatient = async () => {
      try {
        const patient = await getPatient(parseInt(id!));
        setFormData({
          full_name: patient.full_name || '',
          mobile: patient.mobile || '',
          gender: patient.gender || 'male',
          age: patient.age?.toString() || '',
          blood_group: patient.blood_group || '',
          address: patient.address || '',
          allergies: patient.allergies || '',
          medical_conditions: patient.medical_conditions || '',
          current_medications: patient.current_medications || '',
          emergency_contact_name: patient.emergency_contact_name || '',
          emergency_contact_relation: patient.emergency_contact_relation || '',
          emergency_contact_phone: patient.emergency_contact_phone || '',
        });
      } catch (err) {
        setError('Failed to load patient');
      } finally {
        setIsLoading(false);
      }
    };
    fetchPatient();
  }, [id]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const validateForm = (): string | null => {
    if (!formData.full_name.trim() || formData.full_name.trim().length < 2) {
      return 'Full name must be at least 2 characters';
    }
    const mobileDigits = formData.mobile.replace(/\D/g, '');
    if (mobileDigits.length !== 10) {
      return 'Mobile number must be exactly 10 digits';
    }
    if (!formData.age) {
      return 'Age is required';
    }
    return null;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    const validationError = validateForm();
    if (validationError) {
      setError(validationError);
      return;
    }

    setIsSaving(true);

    try {
      await updatePatient(parseInt(id!), {
        ...formData,
        mobile: formData.mobile.replace(/\D/g, ''),
        age: parseInt(formData.age),
      });
      navigate(`/patients/${id}`);
    } catch (err: any) {
      setError(apiErrorMessage(err, 'Failed to update patient'));
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

  return (
    <div>
      <div className="page-header flex-between">
        <h1 className="page-title">Edit Patient</h1>
        <Link to={`/patients/${id}`} className="btn btn-outline">
          Cancel
        </Link>
      </div>

      <form onSubmit={handleSubmit}>
        {error && <div className="alert alert-danger">{error}</div>}

        <div className="card">
          <div className="card-header">Basic Information</div>
          <div className="card-body">
            <div className="form-row">
              <div className="form-group">
                <label className="form-label">
                  Full Name <span className="required">*</span>
                </label>
                <input
                  type="text"
                  name="full_name"
                  className="form-control"
                  value={formData.full_name}
                  onChange={handleChange}
                  required
                />
              </div>
              <div className="form-group">
                <label className="form-label">
                  Mobile Number <span className="required">*</span>
                </label>
                <input
                  type="tel"
                  name="mobile"
                  className="form-control"
                  value={formData.mobile}
                  onChange={handleChange}
                  required
                />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label className="form-label">
                  Gender <span className="required">*</span>
                </label>
                <select
                  name="gender"
                  className="form-control"
                  value={formData.gender}
                  onChange={handleChange}
                  required
                >
                  <option value="male">Male</option>
                  <option value="female">Female</option>
                  <option value="other">Other</option>
                </select>
              </div>
              <div className="form-group">
                <label className="form-label">
                  Age <span className="required">*</span>
                </label>
                <input
                  type="number"
                  name="age"
                  className="form-control"
                  value={formData.age}
                  onChange={handleChange}
                  min="0"
                  max="120"
                  required
                />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label className="form-label">Blood Group</label>
                <select
                  name="blood_group"
                  className="form-control"
                  value={formData.blood_group}
                  onChange={handleChange}
                >
                  <option value="">Select...</option>
                  <option value="A+">A+</option>
                  <option value="A-">A-</option>
                  <option value="B+">B+</option>
                  <option value="B-">B-</option>
                  <option value="AB+">AB+</option>
                  <option value="AB-">AB-</option>
                  <option value="O+">O+</option>
                  <option value="O-">O-</option>
                </select>
              </div>
              <div className="form-group">
                <label className="form-label">Address</label>
                <input
                  type="text"
                  name="address"
                  className="form-control"
                  value={formData.address}
                  onChange={handleChange}
                />
              </div>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="card-header">Medical Information</div>
          <div className="card-body">
            <div className="form-group">
              <label className="form-label">Allergies</label>
              <textarea
                name="allergies"
                className="form-control"
                placeholder="List any known allergies"
                value={formData.allergies}
                onChange={handleChange}
                rows={2}
              />
            </div>
            <div className="form-group">
              <label className="form-label">Medical Conditions</label>
              <textarea
                name="medical_conditions"
                className="form-control"
                placeholder="List any medical conditions"
                value={formData.medical_conditions}
                onChange={handleChange}
                rows={2}
              />
            </div>
            <div className="form-group">
              <label className="form-label">Current Medications</label>
              <textarea
                name="current_medications"
                className="form-control"
                placeholder="List current medications"
                value={formData.current_medications}
                onChange={handleChange}
                rows={2}
              />
            </div>
          </div>
        </div>

        <div className="card">
          <div className="card-header">Emergency Contact</div>
          <div className="card-body">
            <div className="form-row">
              <div className="form-group">
                <label className="form-label">Contact Name</label>
                <input
                  type="text"
                  name="emergency_contact_name"
                  className="form-control"
                  value={formData.emergency_contact_name}
                  onChange={handleChange}
                />
              </div>
              <div className="form-group">
                <label className="form-label">Relation</label>
                <select
                  name="emergency_contact_relation"
                  className="form-control"
                  value={formData.emergency_contact_relation}
                  onChange={handleChange}
                >
                  <option value="">Select...</option>
                  <option value="Spouse">Spouse</option>
                  <option value="Parent">Parent</option>
                  <option value="Child">Child</option>
                  <option value="Sibling">Sibling</option>
                  <option value="Other">Other</option>
                </select>
              </div>
            </div>
            <div className="form-group">
              <label className="form-label">Contact Phone</label>
              <input
                type="tel"
                name="emergency_contact_phone"
                className="form-control"
                value={formData.emergency_contact_phone}
                onChange={handleChange}
              />
            </div>
          </div>
        </div>

        <div className="flex gap-10">
          <button
            type="button"
            className="btn btn-secondary"
            onClick={() => navigate(`/patients/${id}`)}
          >
            Cancel
          </button>
          <button type="submit" className="btn btn-primary" disabled={isSaving}>
            {isSaving ? 'Saving...' : 'Save Changes'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default PatientEdit;
