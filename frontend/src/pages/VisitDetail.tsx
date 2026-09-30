import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getVisit, getPatient, getPrescriptions, getInvoices } from '../services/api';

const VisitDetail: React.FC = () => {
  const { patientId, visitId } = useParams<{ patientId: string; visitId: string }>();
  const [visit, setVisit] = useState<any>(null);
  const [patient, setPatient] = useState<any>(null);
  const [prescription, setPrescription] = useState<any>(null);
  const [invoice, setInvoice] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Check if visit is from today (editable)
  const isToday = (dateString: string) => {
    const visitDate = new Date(dateString);
    const today = new Date();
    return visitDate.toDateString() === today.toDateString();
  };

  const canEdit = visit ? isToday(visit.visit_date) : false;

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [visitData, patientData] = await Promise.all([
          getVisit(parseInt(visitId!)),
          getPatient(parseInt(patientId!)),
        ]);
        setVisit(visitData);
        setPatient(patientData);

        // Fetch related prescription and invoice
        const [prescriptions, invoices] = await Promise.all([
          getPrescriptions(parseInt(patientId!), parseInt(visitId!)),
          getInvoices(parseInt(patientId!)),
        ]);
        
        if (prescriptions.length > 0) {
          setPrescription(prescriptions[0]);
        }
        
        const visitInvoice = invoices.find((inv: any) => inv.visit_id === parseInt(visitId!));
        if (visitInvoice) {
          setInvoice(visitInvoice);
        }
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setIsLoading(false);
      }
    };
    fetchData();
  }, [patientId, visitId]);

  if (isLoading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
      </div>
    );
  }

  if (!visit || !patient) {
    return <div className="alert alert-danger">Visit not found</div>;
  }

  const visitDate = new Date(visit.visit_date).toLocaleDateString('en-IN', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  });

  return (
    <div>
      {/* Header */}
      <div className="page-header flex-between">
        <div>
          <h1 className="page-title">Visit Details</h1>
          <p className="text-muted">{visitDate} - {visit.visit_id}</p>
        </div>
        <div className="flex gap-10">
          {canEdit && (
            <Link to={`/patients/${patientId}/visits/${visitId}/edit`} className="btn btn-primary">
              ✏️ Edit
            </Link>
          )}
          <Link to={`/patients/${patientId}`} className="btn btn-outline">
            ← Back to Patient
          </Link>
        </div>
      </div>

      {/* Patient Info */}
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

      {/* Vitals */}
      {(visit.bp || visit.blood_sugar || visit.pulse) && (
        <div className="card">
          <div className="card-header">Vitals</div>
          <div className="card-body">
            <div className="flex gap-20">
              {visit.bp && <span><strong>BP:</strong> {visit.bp}</span>}
              {visit.blood_sugar && <span><strong>Sugar:</strong> {visit.blood_sugar}</span>}
              {visit.pulse && <span><strong>Pulse:</strong> {visit.pulse}</span>}
            </div>
          </div>
        </div>
      )}

      {/* Clinical Notes */}
      <div className="card">
        <div className="card-header">Clinical Notes</div>
        <div className="card-body">
          {visit.chief_complaint && (
            <div className="mb-10">
              <strong>Chief Complaint:</strong>
              <p>{visit.chief_complaint}</p>
            </div>
          )}
          {visit.examination_findings && (
            <div className="mb-10">
              <strong>Examination & Findings:</strong>
              <p>{visit.examination_findings}</p>
            </div>
          )}
          {visit.advice && (
            <div className="mb-10">
              <strong>Advice:</strong>
              <p>{visit.advice}</p>
            </div>
          )}
          {visit.follow_up_date && (
            <div>
              <strong>Follow-up:</strong> {new Date(visit.follow_up_date).toLocaleDateString('en-IN')}
              {visit.follow_up_reason && ` - ${visit.follow_up_reason}`}
            </div>
          )}
        </div>
      </div>

      {/* Prescription */}
      {prescription && prescription.medicines && prescription.medicines.length > 0 && (
        <div className="card">
          <div className="card-header">💊 Prescription</div>
          <div className="card-body">
            <table className="table">
              <thead>
                <tr>
                  <th>Medicine</th>
                  <th>Dosage</th>
                  <th>Frequency</th>
                  <th>Duration</th>
                  <th>Instructions</th>
                </tr>
              </thead>
              <tbody>
                {prescription.medicines.map((med: any, index: number) => (
                  <tr key={index}>
                    <td>{med.name}</td>
                    <td>{med.dosage}</td>
                    <td>{med.frequency}</td>
                    <td>{med.duration}</td>
                    <td>{med.instructions}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            {prescription.notes && (
              <p className="text-muted" style={{ marginTop: '10px' }}>
                <strong>Notes:</strong> {prescription.notes}
              </p>
            )}
          </div>
        </div>
      )}

      {/* Invoice */}
      {invoice && (
        <div className="card">
          <div className="card-header flex-between">
            <span>💰 Invoice - {invoice.invoice_id}</span>
            <span className={`badge ${invoice.status === 'paid' ? 'badge-success' : 'badge-warning'}`}>
              {invoice.status.toUpperCase()}
            </span>
          </div>
          <div className="card-body">
            <table className="table">
              <thead>
                <tr>
                  <th>Description</th>
                  <th>Qty</th>
                  <th>Rate</th>
                  <th>Amount</th>
                </tr>
              </thead>
              <tbody>
                {invoice.items && invoice.items.map((item: any, index: number) => (
                  <tr key={index}>
                    <td>{item.description}</td>
                    <td>{item.quantity}</td>
                    <td>₹{item.rate}</td>
                    <td>₹{item.amount}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            <div style={{ textAlign: 'right', marginTop: '10px' }}>
              {invoice.discount > 0 && (
                <div>Discount: ₹{invoice.discount}</div>
              )}
              <div style={{ fontSize: '18px' }}>
                <strong>Total: ₹{invoice.total}</strong>
              </div>
              <div className="text-muted">
                Paid: ₹{invoice.paid} | Outstanding: ₹{invoice.total - invoice.paid}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default VisitDetail;
