import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getInvoices, getTodayCollection } from '../services/api';

const Billing: React.FC = () => {
  const [invoices, setInvoices] = useState<any[]>([]);
  const [todayCollection, setTodayCollection] = useState<any>(null);
  const [filter, setFilter] = useState<'all' | 'pending' | 'paid'>('all');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [invoicesData, collectionData] = await Promise.all([
          getInvoices(undefined, filter === 'all' ? undefined : filter),
          getTodayCollection(),
        ]);
        setInvoices(invoicesData);
        setTodayCollection(collectionData);
      } catch (error) {
        console.error('Error fetching billing data:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, [filter]);

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'paid':
        return <span className="badge badge-success">Paid</span>;
      case 'partial':
        return <span className="badge badge-warning">Partial</span>;
      default:
        return <span className="badge badge-danger">Pending</span>;
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
      <div className="page-header">
        <h1 className="page-title">Billing</h1>
      </div>

      {/* Today's Collection */}
      {todayCollection && (
        <div className="card">
          <div className="card-header">
            <span>💰 Today's Collection - {new Date().toLocaleDateString()}</span>
          </div>
          <div className="card-body">
            <div className="stats-grid">
              <div className="stat-card success">
                <div className="value">₹{todayCollection.total?.toLocaleString() || 0}</div>
                <div className="label">Total Collected</div>
              </div>
              <div className="stat-card primary">
                <div className="value">₹{todayCollection.by_mode?.cash?.toLocaleString() || 0}</div>
                <div className="label">Cash</div>
              </div>
              <div className="stat-card primary">
                <div className="value">₹{todayCollection.by_mode?.upi?.toLocaleString() || 0}</div>
                <div className="label">UPI</div>
              </div>
              <div className="stat-card primary">
                <div className="value">{todayCollection.count || 0}</div>
                <div className="label">Transactions</div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Filter Tabs */}
      <div className="flex gap-10 mb-20">
        <button
          className={`btn ${filter === 'all' ? 'btn-primary' : 'btn-outline'}`}
          onClick={() => setFilter('all')}
        >
          All Invoices
        </button>
        <button
          className={`btn ${filter === 'pending' ? 'btn-primary' : 'btn-outline'}`}
          onClick={() => setFilter('pending')}
        >
          Pending
        </button>
        <button
          className={`btn ${filter === 'paid' ? 'btn-primary' : 'btn-outline'}`}
          onClick={() => setFilter('paid')}
        >
          Paid
        </button>
      </div>

      {/* Invoice List */}
      <div className="card">
        <div className="card-body" style={{ padding: 0 }}>
          <table className="table">
            <thead>
              <tr>
                <th>Invoice #</th>
                <th>Patient</th>
                <th>Date</th>
                <th>Total</th>
                <th>Paid</th>
                <th>Balance</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {invoices.length === 0 ? (
                <tr>
                  <td colSpan={8} className="text-center text-muted" style={{ padding: '40px' }}>
                    No invoices found
                  </td>
                </tr>
              ) : (
                invoices.map((inv) => (
                  <tr key={inv.id}>
                    <td>{inv.invoice_id}</td>
                    <td>
                      <Link to={`/patients/${inv.patient_id}`}>
                        <strong>{inv.patient_name}</strong>
                      </Link>
                    </td>
                    <td>{new Date(inv.invoice_date).toLocaleDateString()}</td>
                    <td>₹{inv.total?.toLocaleString()}</td>
                    <td className="text-success">₹{inv.paid?.toLocaleString()}</td>
                    <td className={inv.balance > 0 ? 'text-danger' : ''}>
                      ₹{inv.balance?.toLocaleString()}
                    </td>
                    <td>{getStatusBadge(inv.status)}</td>
                    <td>
                      {inv.balance > 0 && (
                        <Link to={`/billing/${inv.id}/pay`} className="btn btn-sm btn-primary">
                          Collect
                        </Link>
                      )}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Billing;
