import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getInvoice, getPatient, createPayment } from '../services/api';

const Payment: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [invoice, setInvoice] = useState<any>(null);
  const [patient, setPatient] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState('');

  const [paymentData, setPaymentData] = useState({
    amount: 0,
    payment_mode: 'cash',
    reference_no: '',
    notes: '',
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const invoiceData = await getInvoice(parseInt(id!));
        setInvoice(invoiceData);
        setPaymentData((prev) => ({ ...prev, amount: invoiceData.balance }));

        const patientData = await getPatient(invoiceData.patient_id);
        setPatient(patientData);
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, [id]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setPaymentData((prev) => ({
      ...prev,
      [name]: name === 'amount' ? parseFloat(value) || 0 : value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsSaving(true);

    try {
      await createPayment({
        invoice_id: parseInt(id!),
        patient_id: invoice.patient_id,
        ...paymentData,
      });
      navigate('/billing');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to process payment');
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

  if (!invoice) {
    return <div className="alert alert-danger">Invoice not found</div>;
  }

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Collect Payment</h1>
      </div>

      <div className="grid-2">
        {/* Payment Form */}
        <div>
          <form onSubmit={handleSubmit}>
            {error && <div className="alert alert-danger">{error}</div>}

            <div className="card">
              <div className="card-header">Payment Details</div>
              <div className="card-body">
                <div className="form-group">
                  <label className="form-label">
                    Amount <span className="required">*</span>
                  </label>
                  <input
                    type="number"
                    name="amount"
                    className="form-control"
                    value={paymentData.amount}
                    onChange={handleChange}
                    max={invoice.balance}
                    min={1}
                    required
                  />
                  <small className="text-muted">
                    Balance: ₹{invoice.balance?.toLocaleString()}
                  </small>
                </div>

                <div className="form-group">
                  <label className="form-label">
                    Payment Mode <span className="required">*</span>
                  </label>
                  <select
                    name="payment_mode"
                    className="form-control"
                    value={paymentData.payment_mode}
                    onChange={handleChange}
                    required
                  >
                    <option value="cash">Cash</option>
                    <option value="upi">UPI (PhonePe/GPay)</option>
                    <option value="card">Card</option>
                    <option value="bank_transfer">Bank Transfer</option>
                  </select>
                </div>

                {paymentData.payment_mode !== 'cash' && (
                  <div className="form-group">
                    <label className="form-label">Reference Number</label>
                    <input
                      type="text"
                      name="reference_no"
                      className="form-control"
                      placeholder="Transaction ID / Reference"
                      value={paymentData.reference_no}
                      onChange={handleChange}
                    />
                  </div>
                )}

                <div className="form-group">
                  <label className="form-label">Notes</label>
                  <textarea
                    name="notes"
                    className="form-control"
                    placeholder="Optional notes..."
                    value={paymentData.notes}
                    onChange={handleChange}
                    rows={2}
                  />
                </div>
              </div>
            </div>

            <div className="flex gap-10">
              <button
                type="button"
                className="btn btn-secondary"
                onClick={() => navigate('/billing')}
              >
                Cancel
              </button>
              <button type="submit" className="btn btn-primary" disabled={isSaving}>
                {isSaving ? 'Processing...' : `Collect ₹${paymentData.amount.toLocaleString()}`}
              </button>
            </div>
          </form>
        </div>

        {/* Invoice Summary */}
        <div>
          <div className="card">
            <div className="card-header">Invoice Summary</div>
            <div className="card-body">
              <div className="mb-10">
                <strong>Invoice:</strong> {invoice.invoice_id}
              </div>
              <div className="mb-10">
                <strong>Patient:</strong> {patient?.full_name}
              </div>
              <div className="mb-10">
                <strong>Date:</strong> {new Date(invoice.invoice_date).toLocaleDateString()}
              </div>

              <hr style={{ margin: '15px 0', border: 'none', borderTop: '1px solid var(--gray-200)' }} />

              <div className="flex-between mb-10">
                <span>Total Amount</span>
                <strong>₹{invoice.total?.toLocaleString()}</strong>
              </div>
              <div className="flex-between mb-10">
                <span>Already Paid</span>
                <strong className="text-success">₹{invoice.paid?.toLocaleString()}</strong>
              </div>
              <div className="flex-between">
                <span>Balance Due</span>
                <strong className="text-danger">₹{invoice.balance?.toLocaleString()}</strong>
              </div>
            </div>
          </div>

          {/* Items */}
          <div className="card">
            <div className="card-header">Invoice Items</div>
            <div className="card-body" style={{ padding: 0 }}>
              <table className="table">
                <thead>
                  <tr>
                    <th>Description</th>
                    <th style={{ textAlign: 'right' }}>Amount</th>
                  </tr>
                </thead>
                <tbody>
                  {invoice.items?.map((item: any, index: number) => (
                    <tr key={index}>
                      <td>{item.description}</td>
                      <td style={{ textAlign: 'right' }}>₹{item.amount?.toLocaleString()}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Payment;
