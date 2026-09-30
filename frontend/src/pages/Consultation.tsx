import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getPatient, createVisit, createPrescription, createInvoice } from '../services/api';

interface Medicine {
  name: string;
  dosage: string;
  frequency: string;
  duration: string;
  instructions: string;
}

const Consultation: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [patient, setPatient] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState('');
  const [showPrescription, setShowPrescription] = useState(false);
  const [showBilling, setShowBilling] = useState(false);

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

  // Prescription data
  const [medicines, setMedicines] = useState<Medicine[]>([]);
  const [rxNotes, setRxNotes] = useState('');

  // Billing data
  const [billItems, setBillItems] = useState<any[]>([]);
  const [discount, setDiscount] = useState(0);

  useEffect(() => {
    const fetchPatient = async () => {
      try {
        const data = await getPatient(parseInt(id!));
        setPatient(data);
      } catch (error) {
        console.error('Error fetching patient:', error);
      } finally {
        setIsLoading(false);
      }
    };
    fetchPatient();
  }, [id]);

  const handleVisitChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setVisitData((prev) => ({ ...prev, [name]: value }));
  };

  const addMedicine = () => {
    setMedicines([
      ...medicines,
      { name: '', dosage: '', frequency: '1-0-1', duration: '5 days', instructions: 'After food' },
    ]);
  };

  const updateMedicine = (index: number, field: keyof Medicine, value: string) => {
    const updated = [...medicines];
    updated[index][field] = value;
    setMedicines(updated);
  };

  const removeMedicine = (index: number) => {
    setMedicines(medicines.filter((_, i) => i !== index));
  };

  const addBillItem = () => {
    setBillItems([...billItems, { description: '', quantity: 1, rate: 0, amount: 0 }]);
  };

  const updateBillItem = (index: number, field: string, value: any) => {
    const updated = [...billItems];
    updated[index] = { ...updated[index], [field]: value };
    if (field === 'quantity' || field === 'rate') {
      updated[index].amount = updated[index].quantity * updated[index].rate;
    }
    setBillItems(updated);
  };

  const removeBillItem = (index: number) => {
    setBillItems(billItems.filter((_, i) => i !== index));
  };

  const subtotal = billItems.reduce((sum, item) => sum + item.amount, 0);
  const total = subtotal - discount;

  const handleSave = async () => {
    setError('');
    
    // Validation
    if (!visitData.chief_complaint.trim()) {
      setError('Please enter the chief complaint');
      return;
    }
    
    setIsSaving(true);

    try {
      // 1. Create visit
      const visit = await createVisit({
        patient_id: parseInt(id!),
        ...visitData,
        follow_up_date: visitData.follow_up_date || null,
      });

      // 2. Create prescription if medicines added
      const validMedicines = medicines.filter((m) => m.name.trim());
      if (validMedicines.length > 0) {
        await createPrescription({
          visit_id: visit.id,
          patient_id: parseInt(id!),
          medicines: validMedicines,
          notes: rxNotes,
        });
      }

      // 3. Create invoice if items added
      const validItems = billItems.filter((item) => item.description.trim() && item.amount > 0);
      if (validItems.length > 0) {
        await createInvoice({
          patient_id: parseInt(id!),
          visit_id: visit.id,
          items: validItems,
          discount: discount,
          gst_percent: 0,
        });
      }

      navigate(`/patients/${id}`);
    } catch (err: any) {
      console.error('Save error:', err);
      setError(err.response?.data?.detail || err.message || 'Failed to save consultation');
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

  if (!patient) {
    return <div className="alert alert-danger">Patient not found</div>;
  }

  return (
    <div>
      {/* Patient Header */}
      <div className="card">
        <div className="card-body flex gap-20" style={{ alignItems: 'center' }}>
          <div className="avatar" style={{ width: '60px', height: '60px', fontSize: '20px' }}>
            {patient.full_name.split(' ').map((n: string) => n[0]).join('').slice(0, 2)}
          </div>
          <div style={{ flex: 1 }}>
            <h2>{patient.full_name}</h2>
            <div className="flex gap-20">
              <span>{patient.patient_id}</span>
              <span>{patient.gender}, {patient.age || '-'} yrs</span>
              {patient.blood_group && <span>🩸 {patient.blood_group}</span>}
            </div>
          </div>
        </div>
      </div>

      {/* Allergy Alert */}
      {patient.allergies && (
        <div className="alert alert-danger">
          <strong>⚠️ ALLERGIES:</strong> {patient.allergies}
        </div>
      )}

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

      {/* Prescription Section - Collapsible */}
      <div className="card">
        <div 
          className="card-header" 
          style={{ cursor: 'pointer', display: 'flex', justifyContent: 'space-between' }}
          onClick={() => setShowPrescription(!showPrescription)}
        >
          <span>💊 Prescription {medicines.length > 0 && `(${medicines.length} medicines)`}</span>
          <span>{showPrescription ? '▼' : '▶'}</span>
        </div>
        {showPrescription && (
          <div className="card-body">
            {medicines.length === 0 ? (
              <p className="text-muted text-center">No medicines added</p>
            ) : (
              <table className="table">
                <thead>
                  <tr>
                    <th>Medicine</th>
                    <th style={{ width: '80px' }}>Dosage</th>
                    <th style={{ width: '90px' }}>Frequency</th>
                    <th style={{ width: '80px' }}>Duration</th>
                    <th style={{ width: '100px' }}>Instructions</th>
                    <th style={{ width: '40px' }}></th>
                  </tr>
                </thead>
                <tbody>
                  {medicines.map((med, index) => (
                    <tr key={index}>
                      <td>
                        <input
                          type="text"
                          className="form-control"
                          placeholder="Medicine name"
                          value={med.name}
                          onChange={(e) => updateMedicine(index, 'name', e.target.value)}
                        />
                      </td>
                      <td>
                        <input
                          type="text"
                          className="form-control"
                          placeholder="500mg"
                          value={med.dosage}
                          onChange={(e) => updateMedicine(index, 'dosage', e.target.value)}
                        />
                      </td>
                      <td>
                        <select
                          className="form-control"
                          value={med.frequency}
                          onChange={(e) => updateMedicine(index, 'frequency', e.target.value)}
                        >
                          <option value="1-0-0">1-0-0</option>
                          <option value="0-0-1">0-0-1</option>
                          <option value="1-0-1">1-0-1</option>
                          <option value="1-1-1">1-1-1</option>
                          <option value="SOS">SOS</option>
                        </select>
                      </td>
                      <td>
                        <input
                          type="text"
                          className="form-control"
                          placeholder="5 days"
                          value={med.duration}
                          onChange={(e) => updateMedicine(index, 'duration', e.target.value)}
                        />
                      </td>
                      <td>
                        <select
                          className="form-control"
                          value={med.instructions}
                          onChange={(e) => updateMedicine(index, 'instructions', e.target.value)}
                        >
                          <option value="Before food">Before</option>
                          <option value="After food">After</option>
                          <option value="With food">With</option>
                        </select>
                      </td>
                      <td>
                        <button
                          type="button"
                          className="btn btn-sm btn-danger"
                          onClick={() => removeMedicine(index)}
                        >
                          ✕
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
            <button type="button" className="btn btn-outline btn-sm" onClick={addMedicine}>
              + Add Medicine
            </button>

            {medicines.length > 0 && (
              <div className="form-group" style={{ marginTop: '15px' }}>
                <label className="form-label">Additional Notes</label>
                <textarea
                  className="form-control"
                  placeholder="Additional instructions..."
                  value={rxNotes}
                  onChange={(e) => setRxNotes(e.target.value)}
                  rows={2}
                />
              </div>
            )}
          </div>
        )}
      </div>

      {/* Billing Section - Collapsible */}
      <div className="card">
        <div 
          className="card-header" 
          style={{ cursor: 'pointer', display: 'flex', justifyContent: 'space-between' }}
          onClick={() => setShowBilling(!showBilling)}
        >
          <span>💰 Billing {total > 0 && `(₹${total.toLocaleString()})`}</span>
          <span>{showBilling ? '▼' : '▶'}</span>
        </div>
        {showBilling && (
          <div className="card-body">
            {billItems.length === 0 ? (
              <p className="text-muted text-center">No billing items added</p>
            ) : (
              <table className="table">
                <thead>
                  <tr>
                    <th>Description</th>
                    <th style={{ width: '70px' }}>Qty</th>
                    <th style={{ width: '100px' }}>Rate</th>
                    <th style={{ width: '100px' }}>Amount</th>
                    <th style={{ width: '40px' }}></th>
                  </tr>
                </thead>
                <tbody>
                  {billItems.map((item, index) => (
                    <tr key={index}>
                      <td>
                        <input
                          type="text"
                          className="form-control"
                          placeholder="Service description"
                          value={item.description}
                          onChange={(e) => updateBillItem(index, 'description', e.target.value)}
                        />
                      </td>
                      <td>
                        <input
                          type="number"
                          className="form-control"
                          value={item.quantity}
                          onChange={(e) => updateBillItem(index, 'quantity', parseInt(e.target.value) || 0)}
                          min="1"
                        />
                      </td>
                      <td>
                        <input
                          type="number"
                          className="form-control"
                          value={item.rate}
                          onChange={(e) => updateBillItem(index, 'rate', parseFloat(e.target.value) || 0)}
                          min="0"
                        />
                      </td>
                      <td>₹{item.amount.toLocaleString()}</td>
                      <td>
                        <button
                          type="button"
                          className="btn btn-sm btn-danger"
                          onClick={() => removeBillItem(index)}
                        >
                          ✕
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
            <button type="button" className="btn btn-outline btn-sm" onClick={addBillItem}>
              + Add Item
            </button>

            {billItems.length > 0 && (
              <div style={{ marginTop: '15px', textAlign: 'right' }}>
                <div className="mb-10">
                  Subtotal: <strong>₹{subtotal.toLocaleString()}</strong>
                </div>
                <div className="mb-10 flex gap-10" style={{ justifyContent: 'flex-end', alignItems: 'center' }}>
                  <span>Discount: ₹</span>
                  <input
                    type="number"
                    className="form-control"
                    style={{ width: '80px' }}
                    value={discount}
                    onChange={(e) => setDiscount(parseFloat(e.target.value) || 0)}
                    min="0"
                  />
                </div>
                <div style={{ fontSize: '18px' }}>
                  Total: <strong>₹{total.toLocaleString()}</strong>
                </div>
              </div>
            )}
          </div>
        )}
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

      {/* Actions */}
      <div className="flex gap-10" style={{ marginTop: '20px' }}>
        <button
          type="button"
          className="btn btn-secondary"
          onClick={() => navigate(`/patients/${id}`)}
        >
          Cancel
        </button>
        <button
          type="button"
          className="btn btn-primary"
          onClick={handleSave}
          disabled={isSaving}
        >
          {isSaving ? 'Saving...' : 'Save Consultation'}
        </button>
      </div>
    </div>
  );
};

export default Consultation;
